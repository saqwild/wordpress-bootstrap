"""Step 2 - Narration.

Synthesises each shot's narration with Kokoro (offline neural TTS) and writes
build/timeline.json. Speech length drives every shot's duration, so the
animation is always timed to the voice, never the other way round.

Run with the TTS environment:  ttsvenv/bin/python tts.py --models <dir>
"""
import argparse
import json
import pathlib

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = pathlib.Path(__file__).parent
SR = 24000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True, help="dir with kokoro-v1.0.onnx and voices-v1.0.bin")
    ap.add_argument("--build", default=str(HERE / "build"))
    args = ap.parse_args()

    script = json.loads((HERE / "script.json").read_text())
    build = pathlib.Path(args.build)
    (build / "audio").mkdir(parents=True, exist_ok=True)

    models = pathlib.Path(args.models)
    tts = Kokoro(str(models / "kokoro-v1.0.onnx"), str(models / "voices-v1.0.bin"))
    voice = script["voice"]
    lang = "en-gb" if voice.startswith("b") else "en-us"

    t = 0.0
    shots = []
    for i, shot in enumerate(script["shots"]):
        audio, sr = tts.create(shot["narration"], voice=voice, speed=script["voice_speed"], lang=lang)
        assert sr == SR
        path = build / "audio" / f"{i:02d}_{shot['id']}.wav"
        sf.write(path, audio, sr)
        speech = len(audio) / sr
        pad = shot.get("pad", script["default_pad"])
        dur = max(script["lead_in"] + speech + pad, shot.get("min_duration", 0))
        shots.append({"id": shot["id"], "start": round(t, 3), "duration": round(dur, 3),
                      "speech_start": round(t + script["lead_in"], 3), "speech": round(speech, 3),
                      "audio": str(path.relative_to(build))})
        print(f"{shot['id']:10s} speech {speech:5.1f}s  shot {dur:5.1f}s")
        t += dur

    timeline = {"fps": script["fps"], "total": round(t, 3),
                "frames": int(round(t * script["fps"])), "shots": shots}
    (build / "timeline.json").write_text(json.dumps(timeline, indent=2))
    print(f"TOTAL {t:.1f}s = {t / 60:.2f} min, {timeline['frames']} frames")


if __name__ == "__main__":
    main()
