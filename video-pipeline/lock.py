"""Step 3 - Build, animate and render the combination lock in Blender.

Everything here is code: the model is generated procedurally (no downloaded
assets, no licence questions), the wheel motion comes from a small physics
simulation of the drive pin / fly pick-up, and the camera, ghosting, labels
and highlights are driven by script.json + build/timeline.json.

  venv/bin/python lock.py --build <dir> --frames 0 6915          # render PNGs
  venv/bin/python lock.py --build <dir> --stills 120 900 2400    # preview stills
  venv/bin/python lock.py --build <dir> --check                  # sim report only

Engine: Workbench (fast on CPU). On a GPU box set ENGINE = "BLENDER_EEVEE".
"""
import argparse
import json
import math
import pathlib
import sys
import time

import bpy  # noqa: I001  (bpy must be imported before bmesh when run as a module)
import bmesh
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

HERE = pathlib.Path(__file__).parent
TAU = 2 * math.pi
STEP = TAU / 40          # one dial number
ENGINE = "BLENDER_WORKBENCH"

# ---------------------------------------------------------------- dimensions
R = 0.85                 # disc radius (cam and both wheels)
T = 0.13                 # disc thickness
GATE_DEPTH = 0.16
GATE_HALF = 0.118        # half gate width, radians
PIN_R = 0.55             # radius of pins / flys
PIN_W = 0.18             # angular width of pin + fly (contact separation)
Y_NORMAL = {"cam": -0.30, "a": -0.08, "b": 0.14}
Y_EXPLODED = {"cam": -0.62, "a": -0.12, "b": 0.38}
FENCE_REST = 0.87        # fence bottom height (rim top is R = 0.85)
LATCH_DROP = 0.16
SHACKLE_OPEN = 0.75

COL = {
    "body": (0.70, 0.72, 0.76), "index": (0.95, 0.25, 0.20), "dial": (0.07, 0.07, 0.08),
    "print": (0.95, 0.95, 0.95), "cap": (0.62, 0.63, 0.66), "shackle": (0.86, 0.87, 0.89),
    "spindle": (0.55, 0.57, 0.60), "cam": (0.96, 0.76, 0.16), "a": (0.95, 0.45, 0.15),
    "b": (0.20, 0.50, 0.95), "pin": (0.97, 0.97, 0.97), "latch": (0.86, 0.22, 0.22),
    "gate": (1.0, 0.86, 0.12),
}
HIGHLIGHT = (1.0, 0.97, 0.55, 1.0)


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


# ================================================================ timeline
class Channel:
    """Piecewise eased value over frames; segments appended in time order."""

    def __init__(self, v0):
        self.v0 = v0
        self.segs = []          # (f0, f1, v0, v1, shape)

    def at(self, f):
        v = self.v0
        for f0, f1, a, b, shape in self.segs:
            if f < f0:
                break
            u = 1.0 if f1 <= f0 else (f - f0) / (f1 - f0)
            if u >= 1.0:
                v = b if shape != "pulse2" else a
                continue
            if shape == "ease":
                v = lerp(a, b, smooth(u))
            elif shape == "linear":
                v = lerp(a, b, u)
            elif shape == "pulse2":           # two out-and-back bumps
                v = a + (b - a) * math.sin(math.pi * ((u * 2) % 1.0)) ** 2
            elif shape == "flash":            # rise, hold, fall
                v = a + (b - a) * min(1.0, u / 0.15, (1 - u) / 0.25)
            return v
        return v

    def add(self, f0, f1, target, shape="ease"):
        start = self.at(f0)
        self.segs.append((f0, f1, start, target, shape))


def build_timeline(script, timeline):
    fps = timeline["fps"]
    ch = {}

    def channel(name, v0):
        if name not in ch:
            ch[name] = Channel(v0)
        return ch[name]

    for name in ("body", "dial", "shackle", "latch"):
        channel("alpha_" + name, 1.0)
    for name in ("gate_cam", "gate_a", "gate_b", "fence"):
        channel("hl_" + name, 0.0)
    channel("explode", 0.0)
    channel("latch_dz", 0.0)
    channel("shackle_dz", 0.0)
    dial = channel("dial", 0.0)

    shots = []
    for spec, t in zip(script["shots"], timeline["shots"]):
        f0 = int(round(t["start"] * fps))
        n = int(round(t["duration"] * fps))
        shots.append({"spec": spec, "f0": f0, "n": n})

    hl_colors = {}
    for s in shots:
        spec, f0, n = s["spec"], s["f0"], s["n"]
        fr = lambda u: f0 + u * n  # noqa: E731
        for ev in sorted(spec.get("events", []), key=lambda e: e["t"][0]):
            a, b = fr(ev["t"][0]), fr(ev["t"][1])
            kind = ev["type"]
            if kind == "alpha":
                for tgt in ev["targets"]:
                    ch["alpha_" + tgt].add(a, b, ev["to"])
            elif kind == "explode":
                ch["explode"].add(a, b, ev["to"])
            elif kind == "highlight":
                for tgt in ev["targets"]:
                    ch["hl_" + tgt].add(a, b, 1.0, "flash")
                    if "color" in ev:
                        hl_colors.setdefault(tgt, []).append((a, b, tuple(ev["color"])))
            elif kind in ("dial", "dial_turn"):
                cur = dial.at(a)
                if kind == "dial_turn":
                    sign = 1 if ev["dir"] == "R" else -1
                    target = cur + sign * ev["turns"] * TAU
                else:
                    want = ev["to"] * STEP
                    if ev["dir"] == "R":   # clockwise from the front: numbers count up
                        d = (want - cur) % TAU
                        target = cur + d + ev["full_turns"] * TAU
                    else:
                        d = (cur - want) % TAU
                        target = cur - d - ev["full_turns"] * TAU
                dial.add(a, b, target)
            elif kind == "pull_blocked":
                ch["shackle_dz"].add(a, b, 0.035, "pulse2")
                ch["latch_dz"].add(a, b, -(FENCE_REST - R), "pulse2")
            elif kind == "open":
                mid = lerp(a, b, 0.45)
                ch["latch_dz"].add(a, mid, -LATCH_DROP)
                ch["shackle_dz"].add(a, mid, LATCH_DROP)
                ch["shackle_dz"].add(mid, b, SHACKLE_OPEN)
            elif kind == "close":
                mid = lerp(a, b, 0.7)
                ch["shackle_dz"].add(a, mid, 0.0)
                ch["latch_dz"].add(mid, b, 0.0)
            else:
                raise ValueError(f"unknown event {kind}")
    return shots, ch, hl_colors


# ================================================================ physics
def simulate(dial_angles, theta_a0, theta_b0):
    """Drive pin -> fly pick-up with free play. Returns per-frame angles and pick-up frames.

    Angles are clockwise from the top, seen from the front. The cam is fixed to the dial.
    Cam pin and both wheel tabs sit at local angle 0, so the relative angle between a driver
    and its follower must stay within [PIN_W/2, TAU - PIN_W/2] (the free play); outside it,
    the driver drags the follower.
    """
    lo, hi = PIN_W / 2, TAU - PIN_W / 2
    ta, tb = theta_a0, theta_b0
    out, pickups = [], []
    touching = {"a": False, "b": False}
    for f, tc in enumerate(dial_angles):
        contact = {}
        rel = tc - ta
        if rel > hi:
            ta = tc - hi
        elif rel < lo:
            ta = tc - lo
        contact["a"] = min(abs(tc - ta - hi), abs(tc - ta - lo)) < 1e-6
        rel = ta - tb
        if rel > hi:
            tb = ta - hi
        elif rel < lo:
            tb = ta - lo
        contact["b"] = min(abs(ta - tb - hi), abs(ta - tb - lo)) < 1e-6
        for key in ("a", "b"):
            if contact[key] and not touching[key]:
                pickups.append((f, key))
            touching[key] = contact[key]
        out.append((tc, ta, tb))
    return out, pickups


def wrap(x):
    return (x + math.pi) % TAU - math.pi


# ================================================================ geometry
def new_obj(name, mesh, color, parent=None):
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.color = (*color, 1.0)
    if parent:
        obj.parent = parent
    return obj


def finish(bm, name, smooth_angle=35):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    me.set_sharp_from_angle(angle=math.radians(smooth_angle))
    return me


def ring_points(radius_fn, angles):
    return [(radius_fn(a) * math.sin(a), radius_fn(a) * math.cos(a)) for a in angles]


def prism(name, pts_xz, y0, y1, fan=False):
    """Extrude a closed XZ polygon from y0 to y1.

    fan=True triangulates each cap as a fan around (0, 0); use it for star-shaped outlines
    such as a notched disc, where an n-gon cap shades with visible seams.
    """
    bm = bmesh.new()
    if not fan:
        vs = [bm.verts.new((x, y0, z)) for x, z in pts_xz]
        face = bm.faces.new(vs)
        ext = bmesh.ops.extrude_face_region(bm, geom=[face])
        moved = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=moved, vec=(0, y1 - y0, 0))
        return finish(bm, name)
    n = len(pts_xz)
    front = [bm.verts.new((x, y0, z)) for x, z in pts_xz]
    back = [bm.verts.new((x, y1, z)) for x, z in pts_xz]
    cf, cb = bm.verts.new((0, y0, 0)), bm.verts.new((0, y1, 0))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((cf, front[j], front[i]))
        bm.faces.new((cb, back[i], back[j]))
        bm.faces.new((front[i], front[j], back[j], back[i]))
    return finish(bm, name)


def disc_mesh(name, radius, thick, gate=None, segs=192):
    angles = [i * TAU / segs for i in range(segs)]
    if gate is not None:
        g0, g1 = gate - GATE_HALF, gate + GATE_HALF
        inside = lambda a: abs(wrap(a - gate)) < GATE_HALF  # noqa: E731
        angles = [a for a in angles if not inside(a)]
        angles += [g0, g0 + 1e-4, g1 - 1e-4, g1]
        angles.sort(key=lambda a: a % TAU)

        def rfn(a, g0=g0 % TAU, g1=g1 % TAU):
            a = a % TAU
            if abs(a - g0) < 1e-9 or abs(a - g1) < 1e-9:
                return radius
            return radius - GATE_DEPTH if abs(wrap(a - gate)) < GATE_HALF else radius
        pts = ring_points(rfn, angles)
    else:
        pts = ring_points(lambda a: radius, angles)
    return prism(name, pts, -thick / 2, thick / 2, fan=True)


def cylinder_y(name, radius, length, segs=32, forward=True):
    """Cylinder along +Y (or -Y) starting at the origin."""
    angles = [i * TAU / segs for i in range(segs)]
    pts = ring_points(lambda a: radius, angles)
    return prism(name, pts, 0, length if forward else -length)


def box(name, x0, x1, y0, y1, z0, z1):
    return prism(name, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y0, y1)


class Lock:
    def __init__(self, gates):
        sc = bpy.context.scene
        self.parts = {}
        P = self.parts

        # body + index mark
        P["body"] = new_obj("body", cylinder_y("body", 1.45, 1.35, 96), COL["body"])
        P["body"].location.y = -0.80
        bezel = disc_mesh("bezel", 1.32, 0.04, None, 96)
        P["bezel"] = new_obj("bezel", bezel, (0.60, 0.62, 0.66), P["body"])
        P["bezel"].location = (0, -0.02, 0)
        P["index"] = new_obj("index", prism("index", [(-0.09, 1.40), (0.09, 1.40), (0, 1.24)], -0.88, -0.84), COL["index"])

        # dial (rotates about Y), printed numbers, ticks, grip ridges, cap
        P["dial"] = new_obj("dial", disc_mesh("dial", 1.12, 0.14, None, 128), COL["dial"])
        P["dial"].location.y = -0.90
        self.dial_parts = [P["dial"]]
        ticks = bmesh.new()
        for n in range(40):
            a = -n * STEP
            r0 = 0.93 if n % 5 == 0 else 0.99
            w = 0.012 if n % 5 == 0 else 0.008
            c, s = math.cos(a), math.sin(a)
            corners = [(-w, r0), (w, r0), (w, 1.08), (-w, 1.08)]
            vs = [ticks.verts.new((cx * c + cz * s, -0.075, -cx * s + cz * c)) for cx, cz in corners]
            f = ticks.faces.new(vs)
            ext = bmesh.ops.extrude_face_region(ticks, geom=[f])
            bmesh.ops.translate(ticks, verts=[e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)], vec=(0, -0.006, 0))
        self.dial_parts.append(new_obj("ticks", finish(ticks, "ticks"), COL["print"], P["dial"]))
        for n in range(0, 40, 5):
            cu = bpy.data.curves.new(f"num{n}", "FONT")
            cu.body = str(n)
            cu.align_x = "CENTER"
            cu.align_y = "CENTER"
            cu.size = 0.2
            cu.extrude = 0.004
            ob = new_obj(f"num{n}", cu, COL["print"], P["dial"])
            a = -n * STEP
            ob.matrix_basis = (Matrix.Translation((0.80 * math.sin(a), -0.08, 0.80 * math.cos(a)))
                               @ Matrix.Rotation(a, 4, "Y") @ Matrix.Rotation(math.pi / 2, 4, "X"))
            self.dial_parts.append(ob)
        ridges = bmesh.new()
        for i in range(90):
            a = i * TAU / 90
            c, s = math.cos(a), math.sin(a)
            corners = [(-0.012, 1.11), (0.012, 1.11), (0.012, 1.135), (-0.012, 1.135)]
            vs = [ridges.verts.new((cx * c + cz * s, -0.065, -cx * s + cz * c)) for cx, cz in corners]
            f = ridges.faces.new(vs)
            ext = bmesh.ops.extrude_face_region(ridges, geom=[f])
            bmesh.ops.translate(ridges, verts=[e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)], vec=(0, 0.13, 0))
        self.dial_parts.append(new_obj("ridges", finish(ridges, "ridges"), (0.12, 0.12, 0.13), P["dial"]))
        cap = new_obj("cap", cylinder_y("cap", 0.16, 0.05, 48, forward=False), COL["cap"], P["dial"])
        cap.location.y = -0.07
        self.dial_parts.append(cap)

        # spindle
        P["spindle"] = new_obj("spindle", cylinder_y("spindle", 0.07, 1.2, 32), COL["spindle"])
        P["spindle"].location.y = -0.95

        # cam + wheels with gates, gate fills, pins and flys
        self.discs = {}
        for key, color in (("cam", COL["cam"]), ("a", COL["a"]), ("b", COL["b"])):
            g = gates[key]
            disc = new_obj(key, disc_mesh(key, R, T, g), color)
            fill_pts = ring_points(lambda a: R, [g - GATE_HALF + i * 2 * GATE_HALF / 12 for i in range(13)])
            rr = R - GATE_DEPTH
            fill_pts += ring_points(lambda a: rr, [g + GATE_HALF - i * 2 * GATE_HALF / 12 for i in range(13)])
            fill = new_obj("gate_" + key, prism("gate_" + key, fill_pts, -T / 2 - 0.003, T / 2 + 0.003), COL["gate"], disc)
            fill.color = (*COL["gate"], 0.35)
            self.discs[key] = disc
            P["gate_" + key] = fill
        self.pins = {}
        pin_specs = [("cam_pin", "cam", True), ("fly_a", "a", False), ("pin_a", "a", True), ("fly_b", "b", False)]
        for name, parent, back in pin_specs:
            ob = new_obj(name, cylinder_y(name, 0.045, 1.0, 20, forward=back), COL["pin"], self.discs[parent])
            ob.location = (0, (T / 2) if back else (-T / 2), PIN_R)
            self.pins[name] = ob

        # latch with fence
        P["latch"] = new_obj("latch", box("latch", -0.35, 0.72, -0.40, 0.24, 0.95, 1.08), COL["latch"])
        P["fence"] = new_obj("fence", box("fence", -0.06, 0.06, -0.39, 0.23, FENCE_REST, 0.95), COL["latch"], P["latch"])

        # shackle (curve with round bevel)
        cu = bpy.data.curves.new("shackle", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = 0.15
        cu.bevel_resolution = 6
        cu.use_fill_caps = True
        sp = cu.splines.new("POLY")
        pts = [(-0.62, 0, 1.0), (-0.62, 0, 2.3)]
        pts += [(-0.62 * math.cos(i * math.pi / 24), 0, 2.3 + 0.62 * math.sin(i * math.pi / 24)) for i in range(1, 24)]
        pts += [(0.62, 0, 2.3), (0.62, 0, 1.0)]
        sp.points.add(len(pts) - 1)
        for p, co in zip(sp.points, pts):
            p.co = (*co, 1)
        P["shackle"] = new_obj("shackle", cu, COL["shackle"])

        self.groups = {
            "body": [P["body"], P["bezel"], P["index"]],
            "dial": self.dial_parts,
            "shackle": [P["shackle"]],
            "latch": [P["latch"], P["fence"]],
        }
        self.base_alpha = {o.name: o.color[3] for o in sc.objects}

    # ------------------------------------------------------------ per-frame state
    def apply(self, st):
        P = self.parts
        tc, ta, tb = st["angles"]
        ex = st["explode"]
        ys = {k: lerp(Y_NORMAL[k], Y_EXPLODED[k], ex) for k in Y_NORMAL}
        for key, ang in (("cam", tc), ("a", ta), ("b", tb)):
            d = self.discs[key]
            d.location = (0, ys[key], 0)
            d.rotation_euler = (0, ang, 0)
        P["dial"].rotation_euler = (0, tc, 0)
        gap1 = (ys["a"] - T / 2) - (ys["cam"] + T / 2)
        gap2 = (ys["b"] - T / 2) - (ys["a"] + T / 2)
        for name, gap in (("cam_pin", gap1), ("fly_a", gap1), ("pin_a", gap2), ("fly_b", gap2)):
            self.pins[name].scale = (1, 0.68 * gap, 1)
        P["latch"].location.z = st["latch_dz"]
        P["shackle"].location.z = st["shackle_dz"]

        for group, objs in self.groups.items():
            a = st["alpha_" + group]
            for o in objs:
                c = o.color
                o.color = (c[0], c[1], c[2], a)
                o.hide_render = a < 0.01
        for key in ("cam", "a", "b"):
            h = st["hl_gate_" + key]
            g = P["gate_" + key]
            base = COL["gate"]
            g.color = (lerp(base[0], HIGHLIGHT[0], h), lerp(base[1], HIGHLIGHT[1], h), lerp(base[2], HIGHLIGHT[2], h), lerp(0.35, 0.95, h))
            dc = COL[key]
            self.discs[key].color = (lerp(dc[0], 1.0, 0.25 * h), lerp(dc[1], 1.0, 0.25 * h), lerp(dc[2], 0.6, 0.25 * h), 1)
        h = st["hl_fence"]
        hc = st.get("hl_fence_color", HIGHLIGHT)
        lc = COL["latch"]
        a = st["alpha_latch"]
        P["fence"].color = (lerp(lc[0], hc[0], h), lerp(lc[1], hc[1], h), lerp(lc[2], hc[2], h), a)
        for name, ob in self.pins.items():
            k = st["pin_flash"].get(name, 0.0)
            ob.color = (1.0, lerp(0.97, 0.35, k), lerp(0.97, 0.1, k), 1)

    def anchors(self, st):
        tc, ta, tb = st["angles"]
        ex = st["explode"]
        ys = {k: lerp(Y_NORMAL[k], Y_EXPLODED[k], ex) for k in Y_NORMAL}
        ang = {"cam": tc, "a": ta, "b": tb}
        gates = self.gates_local

        def on_disc(key, radius, local, dy=0.0):
            w = local + ang[key]
            return Vector((radius * math.sin(w), ys[key] + dy, radius * math.cos(w)))

        rg = R - GATE_DEPTH / 2
        return {
            "shackle_top": Vector((0, 0, 2.97 + st["shackle_dz"])),
            "body_side": Vector((-1.36, -0.45, -0.50)),
            "dial_edge": Vector((-0.80, -0.98, -0.62)),
            "index": Vector((0, -0.88, 1.32)),
            "cam_rim": Vector((-0.55, ys["cam"], 0.62)),
            "spindle": Vector((0, -0.62, 0.0)),
            "wheel_a_rim": Vector((0.84, ys["a"], 0.10)),
            "wheel_b_rim": Vector((0.70, ys["b"], -0.46)),
            "latch": Vector((0.35, -0.05, 1.08 + st["latch_dz"])),
            "fence": Vector((0.0, -0.08, FENCE_REST + 0.02 + st["latch_dz"])),
            "gate_cam": on_disc("cam", rg, gates["cam"]),
            "gate_a": on_disc("a", rg, gates["a"]),
            "gate_b": on_disc("b", rg, gates["b"]),
            "cam_pin": on_disc("cam", PIN_R, 0.0, T / 2 + 0.3 * (ys["a"] - ys["cam"] - T)),
            "fly_a": on_disc("a", PIN_R, 0.0, -T / 2 - 0.3 * (ys["a"] - ys["cam"] - T)),
            "pin_a": on_disc("a", PIN_R, 0.0, T / 2 + 0.3 * (ys["b"] - ys["a"] - T)),
            "fly_b": on_disc("b", PIN_R, 0.0, -T / 2 - 0.3 * (ys["b"] - ys["a"] - T)),
        }


# ================================================================ scene setup
def setup_scene(script):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = ENGINE
    sc.render.resolution_x, sc.render.resolution_y = script["resolution"]
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.display.render_aa = "8"
    sc.display.shadow_shift = 0.1
    sc.display.light_direction = (0.45, -0.55, 0.70)
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "OBJECT"
    sh.show_shadows = True
    sh.shadow_intensity = 0.35
    sh.show_cavity = True
    sh.cavity_type = "BOTH"
    sh.cavity_ridge_factor = 1.0
    sh.cavity_valley_factor = 1.2
    sh.show_object_outline = True
    sh.object_outline_color = (0.05, 0.05, 0.07)
    sh.show_specular_highlight = True
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = 35
    cam_data.clip_start = 0.05
    cam = bpy.data.objects.new("cam", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    return sc, cam


def camera_pose(spec, u):
    c = spec["camera"]
    a, b = c["from"], c["to"]
    k = smooth(u)
    az = math.radians(lerp(a["az"], b["az"], k))
    el = math.radians(lerp(a["el"], b["el"], k))
    dist = lerp(a["dist"], b["dist"], k)
    tgt = Vector(c["target"])
    loc = tgt + dist * Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    return loc, tgt


def look_at(cam, loc, tgt):
    cam.location = loc
    cam.rotation_euler = (tgt - loc).to_track_quat("-Z", "Y").to_euler()


# ================================================================ main
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--frames", nargs=2, type=int)
    ap.add_argument("--stills", nargs="*", type=int)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    build = pathlib.Path(args.build)
    script = json.loads((HERE / "script.json").read_text())
    timeline = json.loads((build / "timeline.json").read_text())
    nframes = timeline["frames"]
    shots, ch, hl_colors = build_timeline(script, timeline)

    dial = [ch["dial"].at(f) for f in range(nframes)]
    # Each driver/follower pair starts in the middle of its free play, so nothing is picked up
    # until the first "turn right" gathers the wheels. Each disc's gate is then cut where the
    # simulation leaves that disc once the full combination has been dialled: the gates are a
    # consequence of the mechanism, not hand-placed.
    final_frame = next(s["f0"] + s["n"] - 1 for s in shots if s["spec"]["id"] == "third")
    states, pickups = simulate(dial, -math.pi, -2 * math.pi)
    tc_f, ta_f, tb_f = states[final_frame]
    gates = {"cam": wrap(-tc_f), "a": wrap(-ta_f), "b": wrap(-tb_f)}

    report = {"gates_local_deg": {k: round(math.degrees(v), 1) for k, v in gates.items()},
              "pickups": [(round(f / timeline["fps"], 2), k) for f, k in pickups]}
    for s in shots:
        if s["spec"]["id"] in ("gates", "fence", "third", "open", "recap3"):
            f = s["f0"] + s["n"] - 1 if s["spec"]["id"] not in ("gates", "fence") else s["f0"] + s["n"] // 2
            tc, ta, tb = states[f]
            report[s["spec"]["id"]] = {k: round(math.degrees(wrap(gates[k] + v)), 1) for k, v in (("cam", tc), ("a", ta), ("b", tb))}
    print("SIM", json.dumps(report))
    (build / "sim_report.json").write_text(json.dumps(report, indent=2))
    if args.check:
        return

    sc, cam = setup_scene(script)
    lock = Lock(gates)
    lock.gates_local = gates

    # pin flash when a pick-up happens
    flash_len = int(1.2 * timeline["fps"])
    pin_of = {"a": ["cam_pin", "fly_a"], "b": ["pin_a", "fly_b"]}

    def state(f):
        st = {name: c.at(f) for name, c in ch.items() if name != "dial"}
        st["angles"] = states[f]
        for tgt, spans in hl_colors.items():
            for a, b, col in spans:
                if a <= f <= b:
                    st[f"hl_{tgt}_color"] = col
        flashes = {}
        for pf, key in pickups:
            if 0 <= f - pf < flash_len:
                k = 1 - (f - pf) / flash_len
                for name in pin_of[key]:
                    flashes[name] = max(flashes.get(name, 0), k)
        st["pin_flash"] = flashes
        return st

    shot_of = []
    for i, s in enumerate(shots):
        shot_of += [i] * s["n"]
    shot_of += [len(shots) - 1] * (nframes - len(shot_of))

    def place_camera(f):
        s = shots[shot_of[f]]
        u = (f - s["f0"]) / max(1, s["n"] - 1)
        loc, tgt = camera_pose(s["spec"], u)
        look_at(cam, loc, tgt)

    frames = []
    if args.stills:
        frames = args.stills
        outdir = build / "stills"
    else:
        frames = range(args.frames[0], min(args.frames[1], nframes))
        outdir = build / "frames"
    outdir.mkdir(parents=True, exist_ok=True)
    W, H = script["resolution"]

    anchors_out = {}
    t0 = time.time()
    for i, f in enumerate(frames):
        st = state(f)
        lock.apply(st)
        place_camera(f)
        bpy.context.view_layer.update()
        proj = {}
        for name, co in lock.anchors(st).items():
            v = world_to_camera_view(sc, cam, co)
            proj[name] = [round(v.x * W, 1), round((1 - v.y) * H, 1), round(v.z, 3)]
        anchors_out[f] = {"anchors": proj, "dial": st["angles"][0]}
        sc.render.filepath = str(outdir / f"{f:05d}.png")
        bpy.ops.render.render(write_still=True)
        if i % 24 == 0:
            el = time.time() - t0
            print(f"frame {f}  {el / (i + 1):.2f}s/frame", flush=True)
    tag = "stills" if args.stills else f"{frames.start:05d}_{frames.stop:05d}"
    (build / f"anchors_{tag}.json").write_text(json.dumps(anchors_out))
    print("DONE", tag, f"{(time.time() - t0) / max(1, len(frames)):.2f}s/frame")


if __name__ == "__main__":
    main()
