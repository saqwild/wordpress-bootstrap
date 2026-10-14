# Explained From Within: automated Blender explainer pipeline

A working, end-to-end pipeline that turns a reviewed script into a finished,
narrated 3D explainer video. The first episode is **"How does a Combination
Lock work?"** (about 4:48, 1280×720, 24 fps).

Everything is generated from code: no stock footage, no downloaded models, no
AI imagery. That means no licence questions and nothing that can drift between
shots.

## Process flow

```
 ┌────────────────────┐   HUMAN GATE 1: fact-check script + shot list
 │ 1. script.json     │   (narration, chapters, camera moves, events, labels)
 └─────────┬──────────┘
           ▼
 ┌────────────────────┐   Kokoro neural TTS (offline). Speech length sets
 │ 2. tts.py          │   every shot's duration → build/timeline.json
 └─────────┬──────────┘
           ▼
 ┌────────────────────┐   procedural model + pin/fly physics simulation
 │ 3. lock.py --check │   → build/sim_report.json (gates must read 0.0°
 └─────────┬──────────┘     at the end of "third" and "recap3")
           ▼
 ┌────────────────────┐   HUMAN GATE 2: look at ~15 preview stills
 │    lock.py --stills│   (framing, ghosting, labels)
 └─────────┬──────────┘
           ▼
 ┌────────────────────┐   all frames, parallel + resumable chunks
 │ 4. render_all.py   │   (Workbench on CPU ≈ 1–1.5 s/frame)
 └─────────┬──────────┘
           ▼
 ┌────────────────────┐   gradient, labels, step captions, dial readout,
 │ 5. post.py         │   end card, music bed + ducking, MP4, SRT,
 └─────────┬──────────┘   thumbnail, description with chapters
           ▼
     HUMAN GATE 3: watch the final cut, then upload
```

## What is automated and what isn't

| Step | Automated? | Notes |
|---|---|---|
| Script & shot list | Drafted by an LLM, **reviewed by a human** | The mechanism research is the risky part: see "Accuracy" below |
| Voice | ✅ | Kokoro TTS, `am_michael`. Swap `voice` in script.json |
| Timing | ✅ | Shots stretch to the narration; event times are fractions of a shot |
| Model | ✅ | Built in code: discs, gates, pins, flys, latch, fence, dial with numbers |
| Motion | ✅ | `simulate()` drags each wheel only when a pin actually touches its fly; gates are cut where the simulation leaves each disc |
| Camera, ghosting, explode, highlights | ✅ | Declarative events in script.json |
| Labels | ✅ | 3D anchors are projected to the screen every frame and drawn in post |
| Music | ✅ | Generated pad (royalty-free), ducked under the voice |
| Final review | **Human** | Watch it before publishing |

## Accuracy (read before publishing)

* The model is a **generic dial padlock: two wheels plus a drive cam with its
  own gate**. That is the layout in which the standard "right 3 turns, left past
  the first number once, right directly to the third" sequence is physically
  consistent. The simulation shows that a cam + three-wheel pack would need a
  longer sequence, like safe locks use. Brands and models differ, so the
  description says "simplified, generic".
* The fence/latch/ramp behaviour is described as "in many padlocks". That is
  how the narration words it on purpose.
* "Numbers one or two away often work" reflects commonly reported
  manufacturing tolerance. It is hedged in the narration.

## Running it

```bash
# environments (bpy needs Python 3.11 and numpy<2; Kokoro needs numpy 2 → keep them separate)
uv venv -p 3.11 venv    && uv pip install -p venv/bin/python bpy "numpy<2" pillow
uv venv -p 3.11 ttsvenv && uv pip install -p ttsvenv/bin/python kokoro-onnx soundfile phonemizer-fork
# models: kokoro-v1.0.onnx + voices-v1.0.bin from github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
# headless Linux without a GPU also needs software GL: apt install libegl1 libegl-mesa0 libgl1-mesa-dri

ttsvenv/bin/python tts.py   --models <model dir> --build build
venv/bin/python    lock.py  --build build --check
venv/bin/python    lock.py  --build build --stills 400 1700 3000 4800
python3            render_all.py --python venv/bin/python --build build --jobs 3
venv/bin/python    post.py  --build build          # → build/final.mp4 (+ captions.srt, thumbnail.jpg, description.md)
```

On a rented GPU, set `ENGINE = "BLENDER_EEVEE"` in lock.py for soft shadows and
nicer materials. That's about 10 s/frame on this CPU, but fast on a GPU.

## Making the next episode

Most of the pipeline is reusable: `tts.py`, `post.py`, `render_all.py`, the
timeline/event system and the camera/label code. What changes per topic is the
model and its motion (`Lock` and `simulate()` in lock.py). Topics whose parts
follow simple geometric rules (gears, locks, cams, pumps, escalator steps) can
be fully code-generated like this one. Others need CAD/model imports (see the
sourcing notes in chat).
