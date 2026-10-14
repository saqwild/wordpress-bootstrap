"""Step 4 - Composite, mix and encode.

Takes the transparent Blender frames and adds everything 2D: background gradient,
part labels with leader lines, step captions, live dial readout, watermark and end
card. Mixes narration with a generated (royalty-free) ambient bed that ducks under
the voice, encodes the MP4, and writes subtitles, a thumbnail and the YouTube
description with chapters.

  venv/bin/python post.py --build <dir> [--frames 0 480] [--out name.mp4]
"""
import argparse
import json
import math
import pathlib
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).parent
FONT_DIR = pathlib.Path("/usr/share/fonts/opentype/inter")
CHANNEL = "Explained From Within"
TAGLINE = "Hidden processes, made visible."
SR = 24000
TAU = 2 * math.pi


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_LABEL = font("Inter-SemiBold.otf", 26)
F_STEP = font("Inter-SemiBold.otf", 27)
F_SMALL = font("Inter-Medium.otf", 18)
F_READ = font("InterDisplay-Bold.otf", 64)
F_WM = font("Inter-SemiBold.otf", 18)
F_END1 = font("InterDisplay-Bold.otf", 70)
F_END2 = font("Inter-Medium.otf", 32)


def fade(t, t0, t1, ramp=0.35):
    if t < t0 or t > t1:
        return 0.0
    return max(0.0, min(1.0, (t - t0) / ramp, (t1 - t) / ramp))


def gradient(w, h):
    t = np.linspace(0, 1, h)[:, None]
    g = np.zeros((h, w, 4), np.uint8)
    g[..., 0] = 112 - 44 * t
    g[..., 1] = 122 - 46 * t
    g[..., 2] = 138 - 48 * t
    # soft vignette
    yy, xx = np.mgrid[0:h, 0:w]
    v = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2
    shade = 1 - 0.18 * np.clip(v - 0.3, 0, 1)
    g[..., :3] = (g[..., :3] * shade[..., None]).astype(np.uint8)
    g[..., 3] = 255
    return Image.fromarray(g, "RGBA")


def draw_label(layer, text, anchor, a, W, H, placed):
    if a <= 0 or anchor is None or anchor[2] <= 0:
        return
    d = ImageDraw.Draw(layer)
    ax, ay = anchor[0], anchor[1]
    tw = d.textlength(text, font=F_LABEL)
    bw, bh = tw + 28, 44
    right = ax > W * 0.5
    bx = ax + 70 if right else ax - 70 - bw
    by = ay - 90
    bx = min(max(bx, 24), W - bw - 24)
    by = min(max(by, 24), H - bh - 24)
    # keep label boxes from overlapping: nudge down, then up, until clear
    for k in range(12):
        if not any(bx < x1 + 12 and bx + bw > x0 - 12 and by < y1 + 8 and by + bh > y0 - 8 for x0, y0, x1, y1 in placed):
            break
        by = min(max(ay - 90 + (k // 2 + 1) * (bh + 10) * (1 if k % 2 == 0 else -1), 24), H - bh - 24)
    placed.append((bx, by, bx + bw, by + bh))
    alpha = int(255 * a)
    edge_x = bx if right else bx + bw
    d.line([(ax, ay), (edge_x, by + bh / 2)], fill=(255, 255, 255, int(220 * a)), width=3)
    d.ellipse([ax - 6, ay - 6, ax + 6, ay + 6], fill=(255, 255, 255, alpha), outline=(20, 22, 28, alpha), width=2)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(18, 20, 26, int(215 * a)))
    d.text((bx + 14, by + bh / 2), text, font=F_LABEL, fill=(255, 255, 255, alpha), anchor="lm")


def draw_step(layer, text, a):
    if a <= 0:
        return
    d = ImageDraw.Draw(layer)
    parts = text.split("   ", 1)
    x, y = 36, 32
    if len(parts) == 2:
        head, body = parts
        hw = d.textlength(head, font=F_STEP)
        bw = d.textlength(body, font=F_STEP)
        d.rounded_rectangle([x, y, x + hw + bw + 64, y + 52], radius=12, fill=(18, 20, 26, int(215 * a)))
        d.rounded_rectangle([x + 6, y + 6, x + hw + 30, y + 46], radius=9, fill=(255, 205, 40, int(255 * a)))
        d.text((x + 18, y + 26), head, font=F_STEP, fill=(18, 20, 26, int(255 * a)), anchor="lm")
        d.text((x + hw + 46, y + 26), body, font=F_STEP, fill=(255, 255, 255, int(255 * a)), anchor="lm")
    else:
        w = d.textlength(text, font=F_STEP)
        d.rounded_rectangle([x, y, x + w + 36, y + 52], radius=12, fill=(18, 20, 26, int(215 * a)))
        d.text((x + 18, y + 26), text, font=F_STEP, fill=(255, 255, 255, int(255 * a)), anchor="lm")


def draw_readout(layer, angle, moving, a, W):
    if a <= 0:
        return
    d = ImageDraw.Draw(layer)
    num = int(round(angle / (TAU / 40))) % 40
    x1, y0 = W - 36, 32
    x0 = x1 - 190
    d.rounded_rectangle([x0, y0, x1, y0 + 128], radius=14, fill=(18, 20, 26, int(215 * a)))
    d.text((x0 + 18, y0 + 22), "DIAL", font=F_SMALL, fill=(170, 176, 190, int(255 * a)), anchor="lm")
    if moving:
        d.text((x1 - 18, y0 + 22), "RIGHT" if moving > 0 else "LEFT", font=F_SMALL,
               fill=(255, 205, 40, int(255 * a)), anchor="rm")
    d.text(((x0 + x1) / 2, y0 + 80), f"{num:02d}", font=F_READ, fill=(255, 255, 255, int(255 * a)), anchor="mm")


def draw_watermark(layer, W, H):
    d = ImageDraw.Draw(layer)
    d.text((W - 28, H - 24), CHANNEL, font=F_WM, fill=(255, 255, 255, 120), anchor="rs")


def draw_end_card(layer, a, W, H):
    if a <= 0:
        return
    d = ImageDraw.Draw(layer)
    d.rectangle([0, 0, W, H], fill=(14, 16, 22, int(200 * a)))
    d.text((W / 2, H / 2 - 30), CHANNEL, font=F_END1, fill=(255, 255, 255, int(255 * a)), anchor="mm")
    d.text((W / 2, H / 2 + 45), TAGLINE, font=F_END2, fill=(255, 205, 40, int(255 * a)), anchor="mm")


# ---------------------------------------------------------------- audio
def read_wav(path):
    with wave.open(str(path)) as w:
        assert w.getframerate() == SR
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2" if w.getsampwidth() == 2 else "<i4")
        if w.getsampwidth() == 4:
            return data.astype(np.float32) / 2**31
        return data.astype(np.float32) / 2**15


def ambient_bed(n, seed=7):
    """Slow four-chord pad (sines with detune), generated here so it is royalty-free."""
    t = np.arange(n) / SR
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (MIDI)
    seg = 8.0
    out = np.zeros(n, np.float32)
    rng = np.random.default_rng(seed)
    for k in range(int(n / SR / seg) + 2):
        notes = chords[k % 4]
        s0 = int(k * seg * SR)
        s1 = min(n, int((k + 1.5) * seg * SR))
        if s0 >= n:
            break
        tt = t[s0:s1] - k * seg
        env = np.clip(tt / 2.5, 0, 1) * np.clip((seg * 1.5 - tt) / 3.0, 0, 1)
        for m in notes + [notes[0] - 12]:
            f = 440 * 2 ** ((m - 69) / 12)
            for det in (-0.12, 0.12):
                ph = rng.uniform(0, TAU)
                out[s0:s1] += (np.sin(TAU * (f + det) * tt + ph) + 0.25 * np.sin(TAU * 2 * (f + det) * tt + ph)) * env
    # gentle low-pass (moving average)
    k = 24
    y = np.convolve(out, np.ones(k, np.float32) / k, mode="same")
    return y / (np.abs(y).max() + 1e-9)


def mix_audio(script, timeline, build, total_samples):
    voice = np.zeros(total_samples, np.float32)
    for s in timeline["shots"]:
        clip = read_wav(build / s["audio"])
        i0 = int(s["speech_start"] * SR)
        i1 = min(total_samples, i0 + len(clip))
        voice[i0:i1] += clip[: i1 - i0]
    voice *= 0.89 / (np.abs(voice).max() + 1e-9)
    bed = ambient_bed(total_samples)
    # duck the bed while the voice is speaking
    env = np.convolve(np.abs(voice), np.ones(SR // 5) / (SR // 5), mode="same")
    duck = 1.0 - 0.55 * np.clip(env / 0.05, 0, 1)
    duck = np.convolve(duck, np.ones(SR // 2) / (SR // 2), mode="same")
    fade_n = int(SR * 3)
    edge = np.ones(total_samples, np.float32)
    edge[:fade_n] = np.linspace(0, 1, fade_n)
    edge[-fade_n:] = np.linspace(1, 0, fade_n)
    mix = voice + bed * 0.075 * duck * edge
    mix = np.clip(mix, -1, 1)
    path = build / "mix.wav"
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
    return path


# ---------------------------------------------------------------- text outputs
def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(script, timeline, build):
    import re
    cues = []
    for spec, s in zip(script["shots"], timeline["shots"]):
        parts = [p.strip() for p in re.split(r"(?<=[.?!:])\s+", spec["narration"]) if p.strip()]
        split = []
        for p in parts:
            if len(p) > 90 and ", " in p:
                mid = len(p) // 2
                cut = min((i for i in range(len(p)) if p.startswith(", ", i)), key=lambda i: abs(i - mid))
                split += [p[:cut + 1], p[cut + 2:]]
            else:
                split.append(p)
        total = sum(len(p) for p in split)
        t = s["speech_start"]
        for p in split:
            d = s["speech"] * len(p) / total
            cues.append((t, t + d, p))
            t += d
    lines = []
    for i, (a, b, text) in enumerate(cues, 1):
        lines += [str(i), f"{srt_time(a)} --> {srt_time(b)}", text, ""]
    (build / "captions.srt").write_text("\n".join(lines))


def write_description(script, timeline, build):
    chapters = []
    for spec, s in zip(script["shots"], timeline["shots"]):
        if spec.get("chapter"):
            t = int(s["start"])
            chapters.append(f"{t // 60}:{t % 60:02d} {spec['chapter']}")
    combo = "-".join(str(n) for n in script["combination"])
    text = f"""{script['title']}

Turn right, turn left, turn right... but what is actually happening inside the lock? We make the body transparent and follow a dial padlock from the inside: the drive cam, two wheels, the drive pins and flys that pick them up one by one, and the fence that drops into three lined-up gates.

CHAPTERS
{chr(10).join(chapters)}

ABOUT THIS ANIMATION
This is a simplified, generic dial padlock (two wheels plus a drive cam, combination {combo}), not a specific brand or model. Real locks differ in wheel count, latch design and tolerances. Every movement of the wheels is computed from the pin-and-fly pick-up, so the turning sequence shown is the one this mechanism actually needs. Scale, colours and the transparent body are for clarity.

Animation: procedurally modelled and rendered in Blender. Narration: synthetic voice (Kokoro TTS). Music: generated for this video.

FURTHER READING
- Rotary combination lock (Wikipedia): https://en.wikipedia.org/wiki/Rotary_combination_lock
- How Combination Locks Work (HowStuffWorks): https://home.howstuffworks.com/home-improvement/home-diy/combination-lock.htm

#howitworks #combinationlock #engineering #3danimation #explainedfromwithin
"""
    (build / "description.md").write_text(text)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--frames", nargs=2, type=int)
    ap.add_argument("--out", default="final.mp4")
    args = ap.parse_args()

    build = pathlib.Path(args.build)
    script = json.loads((HERE / "script.json").read_text())
    timeline = json.loads((build / "timeline.json").read_text())
    W, H = script["resolution"]
    fps = timeline["fps"]
    nframes = timeline["frames"]
    f_start, f_end = (args.frames if args.frames else (0, nframes))
    f_end = min(f_end, nframes)

    anchors = {}
    for p in sorted(build.glob("anchors_*_*.json")):
        anchors.update({int(k): v for k, v in json.loads(p.read_text()).items()})

    shot_ranges = []
    for spec, s in zip(script["shots"], timeline["shots"]):
        shot_ranges.append((s["start"], s["start"] + s["duration"], spec, s))

    total_samples = int(timeline["total"] * SR) + SR
    mix = mix_audio(script, timeline, build, total_samples)
    write_srt(script, timeline, build)
    write_description(script, timeline, build)

    bg = gradient(W, H)
    out = build / args.out
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-ss", f"{f_start / fps:.3f}", "-i", str(mix), "-c:v", "libx264", "-preset", "medium",
           "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", "-shortest", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    prev_dial = None
    thumb_frame = None
    for f in range(f_start, f_end):
        t = f / fps
        spec, s = next(((sp, s) for a, b, sp, s in shot_ranges if a <= t < b), shot_ranges[-1][2:])
        st, en = s["start"], s["start"] + s["duration"]
        frame = bg.copy()
        png = build / "frames" / f"{f:05d}.png"
        if png.exists():
            frame.alpha_composite(Image.open(png).convert("RGBA"))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        info = anchors.get(f, {})
        anc = info.get("anchors", {})
        placed = []
        for lab in spec.get("labels", []):
            t0 = st + lab["t"][0] * s["duration"]
            t1 = st + lab["t"][1] * s["duration"]
            draw_label(layer, lab["text"], anc.get(lab["anchor"]), fade(t, t0, t1), W, H, placed)
        if spec.get("step"):
            draw_step(layer, spec["step"], fade(t, st, en - 0.05))
        dial = info.get("dial")
        if spec.get("readout") and dial is not None:
            moving = 0 if prev_dial is None or abs(dial - prev_dial) < 1e-4 else (1 if dial > prev_dial else -1)
            draw_readout(layer, dial, moving, fade(t, st, en, 0.3) if not spec.get("end_card") else 1.0, W)
        prev_dial = dial
        draw_watermark(layer, W, H)
        if spec.get("end_card"):
            draw_end_card(layer, fade(t, en - 4.2, en + 10, 0.8), W, H)
        frame.alpha_composite(layer)
        enc.stdin.write(frame.convert("RGB").tobytes())
        if spec["id"] == "third" and t >= en - 0.6 and thumb_frame is None:
            thumb_frame = frame.copy()
        if f % 240 == 0:
            print(f"post {f}/{f_end}", flush=True)
    enc.stdin.close()
    enc.wait()

    if thumb_frame is not None:
        th = thumb_frame.convert("RGBA")
        d = ImageDraw.Draw(th)
        big = font("InterDisplay-Bold.otf", 96)
        d.text((60, H - 210), "3 GATES.", font=big, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(18, 20, 26, 255))
        d.text((60, H - 110), "1 SLOT.", font=big, fill=(255, 205, 40, 255), stroke_width=6, stroke_fill=(18, 20, 26, 255))
        th.convert("RGB").save(build / "thumbnail.jpg", quality=92)
    print("WROTE", out)


if __name__ == "__main__":
    main()
