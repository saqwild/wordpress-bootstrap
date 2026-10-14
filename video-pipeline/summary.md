# Explained From Within: Project Bible

*Everything we discussed, tested, built and decided. Last updated 2026-10-14.*

---

## Contents
1. [Goal](#1-goal)
2. [The channel today](#2-the-channel-today)
3. [Competitor research](#3-competitor-research)
4. [Jared Owen deep-dive (benchmark)](#4-jared-owen-deep-dive-the-benchmark)
5. [Strategy recommendations](#5-strategy-recommendations)
6. [Automation: what can and can't be automated](#6-automation-what-can-and-cant-be-automated)
7. [3D model sourcing and licences](#7-3d-model-sourcing-and-licences)
8. [The pipeline we built](#8-the-pipeline-we-built)
9. [Test log: what we ran, numbers, problems and fixes](#9-test-log)
10. [What worked well](#10-what-worked-well)
11. [What failed or is weak](#11-what-failed-or-is-weak)
12. [GPU vs CPU](#12-gpu-vs-cpu)
13. [Where ComfyUI fits (and doesn't)](#13-where-comfyui-fits-and-doesnt)
14. [Rigging](#14-rigging)
15. [Story writing: voice and plan](#15-story-writing-voice-and-plan)
16. [Scaling to complex models](#16-scaling-to-complex-models)
17. [To-do / roadmap](#17-to-do--roadmap)
18. [Open questions and decisions](#18-open-questions-and-decisions)
19. [References](#19-references)

---

## 1. Goal

Grow **Explained From Within** (youtube.com/@explainedfromwithin) by:
1. Understanding competitors and what video style wins in this niche.
2. Building a **mostly automated, human-checked** production pipeline for accurate
   "how it works" 3D explainers in Jared Owen's style (Blender), alongside the existing
   AI-generated "micro-journey" style.

Ground rule: **automated, not unattended.** Every episode passes human checkpoints
(see §6).

---

## 2. The channel today

*Snapshot taken 2026-10-14 by reading the channel page directly.*

| Item | Value |
|---|---|
| Joined | 17 Sep 2026 |
| Videos | 5, all long-form (~9:56–10:37), no Shorts |
| Total views | ~41 |
| Style | AI-generated cinematic 3D "micro-journeys", with a fictional miniature Explorer + capsule as guide, sources linked |
| Pillars (from the channel description) | Inside Your Body · Inside Materials · Inside Manufacturing · Inside Technology |
| Tagline | "Hidden processes, made visible." |

| Video | Views at snapshot | Length |
|---|---|---|
| How Glass Bottles Are Made: Sand to Bottle, From the Inside | 28 | 10:37 |
| How Concrete Hardens—Not by Drying, From the Inside | 8 | 9:56 |
| How a Platelet Plug Forms Inside a Tiny Cut \| Explained From Within | 3 | 9:56 |
| What Sunburn Actually Does Inside Your Skin - Hour by Hour \| inside you body | 2 | 9:56 |
| The 24-Hour No Sleep Timeline: What Really Happens \| inside your body. | 0 | 9:56 |

**Problems found:**
- The topics are split across 4 pillars after only 5 videos, so YouTube can't tell who the audience is.
- Title typo: "inside **you** body" plus a double space in the sunburn title.
- Suffixes like "| Explained From Within" and "| inside your body." waste the title characters shown in search.
- "…From the Inside" is branding, not a reason to click. The concrete title's "Not by Drying" is the best hook so far.
- There's too little data to judge performance yet; don't change course because of 41 views.

---

## 3. Competitor research

*Numbers taken 2026-10-14. "Median" = median views of a channel's last ~30 uploads;
"×" = how many times the channel median a video got (outlier strength).*

### 3a. Inside Manufacturing / Materials

| Channel | Subs | Median | Best recent outliers | Takeaway |
|---|---|---|---|---|
| **Stories Behind Everything** ⭐ (@StoriesBehindEverything-j6g) | 49.1K (59 videos) | 10.5K | *How Is Gasoline Made? The Dangerous Process Behind Modern Fuel*: **2.2M (×209)**; Bacon 402K; Pringles 255K; Desalination 174K | **Best template for a new channel.** Formula: `How Is [famous product] Made? The [Dangerous/Incredible] Process Behind [big number]`. 8–11 min, chapters, uploads every ~3 days |
| History of Simple Things (@historyofsimplethings) | 1.04M (4.2K videos) | 9.7K | LED bulbs 84K; *How Steel Can Rust Inside Solid Concrete* 69K in 1 day; *What Actually Happens When Concrete Hardens?* 28K | Covers **your exact concrete topic**. "Why do…/How does…" everyday questions, ~8 min, very high volume |
| Made Vision (@MadeVision-TV) | 257K (42 videos) | 273K | Reese's 4M; Domino's 2.7M; Dunkin 2.1M | Famous food brands × factory |
| Inside the Secret Factory (@MadeInSecrecy) | 4.79K | 789 | *Inside the Factory Where Laptops Are Made (The SECRET FULL process)* 246K (×312) | One big hit on a tech product |
| Factorama (@Factorama_eng) | 10.2K | 3K | Fiber optic 114K; Copper 79K; **Glass bottles 49K** | Ranks on your glass-bottle topic |

### 3b. Inside Your Body

| Channel | Subs | Median | Best recent outliers | Takeaway |
|---|---|---|---|---|
| The Infographics Show | 15.5M | 500K | *What Lethal Radiation Does to Your Body (Hour by Hour)* 877K in 9 days | Real stakes + timeline + true story, 18–20 min |
| Life According to Science | 81.2K | 2.2K | *Autophagy Every Day for 30 Days* 110K (×50) | "What happens if… for 30 days" |
| The Walking Effect | **242 subs** | 358 | *What Happens Inside Your Body When You Walk 1 Hour Every Day* 18K (×50) | Tiny channels can break out |
| Fasted Fred | 49.3K | 2.1K | *The 7 Stages of a 36-Hour Fast* 21K | Stages/levels format |
| DoodleProof | 29.4K | 561 | *You're Walking Wrong for Fat Loss* 22K | Hand-drawn health |
| Body Explained, MEDIVAULT, Clinora_X | ~0 | 9–60 | Same "hour by hour" titles as yours | **Crowded with near-identical AI channels getting no traction** |
| Institute of Human Anatomy | 8.93M | 495K | Alcohol or THC 3.5M | Real cadaver lab, high authority |
| Kurzgesagt | 25.7M | 5.15M | n/a | The top of the market |

### 3c. Mechanisms (Inside Technology)
**Jared Owen**: see §4.

### 3d. Patterns that win
- **Manufacturing:** famous products, plus danger or scale in the title, about 8–11 min, step-by-step from raw material to shelf, chapters.
- **Body:** real stakes plus a timeline ("Hour by Hour", "Day by Day", "7 Stages"); big channels go 18–22 min and open with a real person's story.
- **Mechanisms:** plain search titles ("How does a ___ work?"), accurate 3D, slow pacing. These win over the long term through search.

---

## 4. Jared Owen deep-dive (the benchmark)

**Channel:** 4.44M subs, **121 videos in ~10 years** (about one a month), recent median **5.6M**.
Top videos: Titanic 22M · Escalator **19.8M** (6 years old) · Military Helicopter 17M ·
Enigma 14M · Statue of Liberty 14M · Elevator 7.7M · **Combination Lock 7.5M** (7 years old) ·
Spiral Escalator 1.19M (4 months, 11:57, the clip you uploaded).

**Tools:**
- **Blender: confirmed.** He learned it in college, sometimes starts from a bought base model
  (TurboSquid) and heavily modifies it (BlenderNation interviews).
- **Remotion: no.** His most-viewed videos predate Remotion (first released early 2021),
  and the 2D layer is just simple labels any editor can add.

**Style, measured from your uploaded Spiral Escalator clip** (frames every 20 s, cut detection):

| Element | What he does |
|---|---|
| Background | Plain grey-blue backdrop; the machine is the only subject |
| Colour coding | Yellow step edges, orange/blue key parts, cyan/magenta paths |
| Explaining tools | Exploded views, a part shown on its own, see-through housings, a green-grid "diagram mode" |
| Context | Earth globe, real location photos (mall atrium, Osaka), history (1896 patent and photo, then a 3D rebuild) |
| Labels | Small plain text boxes ("Wheels", "Friction Wheel", "Ball Joints") |
| **Pacing** | **4.4 cuts/min, typical shot ~6.4 s, longest single shot ~110 s.** Motion comes from slow camera moves, not cuts |
| Story order | Strange thing first → refresher on the basics → history → the hard problem → the solution |
| Sponsor | Brilliant segment around 5:00–5:40 |
| End | End screen at ~11:40 |

**His real advantage is geometry that stays the same in every shot**, which AI video can't reliably match.

---

## 5. Strategy recommendations

1. **Pick one main pillar for the next 10–15 videos.** The data favours **Manufacturing/Materials**
   for a new channel: Stories Behind Everything went from 0 to 49K subs in 59 videos, and the body
   niche is flooded with copycat AI channels plus higher accuracy risk. Body topics can be an
   occasional side series. *(Your decision.)*
2. **Titles:**
   - Use the competitor formula, e.g. *"How Are Glass Bottles Made? The 11-Second Process That Turns Sand Into a Bottle"*.
   - Keep hooks like *"Not by Drying"*.
   - Drop the channel-name suffixes and fix the typo.
3. **Topics:** big, famous products (gasoline, steel, Coca-Cola, chips, tyres, smartphones)
   before niche industrial ones.
4. **Keep** the Explorer and the sourced descriptions. They set you apart from AI-slop channels,
   which YouTube is cracking down on.
5. **Channel split:** machines in the **Blender pipeline**; body and materials in your **AI micro-journey** style.
6. **Cadence:** quality over volume. One strong video a week is a realistic target for the Blender pipeline.

---

## 6. Automation: what can and can't be automated

**Verdict:** about 70–80% of the *labour* automates. The critical 20% is accuracy (research and models)
and story quality, and that needs human checkpoints.

| Stage | Automated? | Tool |
|---|---|---|
| Research + script | Drafted by an LLM, **human fact-check** | Claude |
| Beat sheet / shot list | Yes, from a fixed set of shot types | JSON |
| Narration | Yes | Kokoro TTS (or your own voice) |
| 3D model | **Depends on the topic** (§7, §16) | Code / CAD import |
| Motion and rigging | Yes for machines (constraints, drivers, simulation) | Python in Blender |
| Camera, labels, ghosting, highlights | Yes | script.json events |
| Render | Fully | Blender run headless |
| Finishing (compositing, music, subtitles, metadata) | Yes | post.py, ffmpeg |
| Final review | **Human** | You |

**Human checkpoints:**
1. **Gate 1:** fact-check the script and beat sheet.
2. **Gate 2:** check the model, mechanism and preview stills (~5 min).
3. **Gate 3:** watch the final cut before uploading.

**Policy risk:** since **15 July 2025**, YouTube demonetizes "inauthentic" (mass-produced or
repetitive) content. AI is allowed if it adds original value. Fully templated, unattended
uploads are exactly the profile it targets, which is why the human checkpoints matter.

---

## 7. 3D model sourcing and licences

*Licence summaries come from help pages and forum quotes. Check each site's current terms
before your first monetized upload. This is not legal advice.*

| Source | Insides accurate | Parts separate | Motion included | OK for monetized YouTube? | Scriptable download |
|---|---|---|---|---|---|
| **Code-built models** (gears, cams, chains, springs, locks) | ✅ exact | ✅ | ✅ (you script it) | ✅ no licence risk | ✅ |
| **Onshape public documents** | ✅ real CAD | ✅ | mates only | ⚠️ Probably: terms reportedly give a royalty-free licence on free users' public docs created after Aug 2018. Verify | ✅ API |
| Printables / Thingiverse print-in-place mechanisms | ✅ built to work | ✅ | ❌ | ⚠️ Per model: use CC0/CC-BY, skip NC | Partly |
| Sketchfab | ⚠️ often shells | sometimes | ✅ often (glTF) | ⚠️ CC0/CC-BY yes, NC/ND no. Still running in 2026 but slowly shrinking after the move to Fab | ✅ API |
| CGTrader | ⚠️ varies | varies | sometimes | ✅ Royalty-free licence reportedly allows rendered video, commercial included; no resale of the model | ❌ |
| **GrabCAD** | ✅ best engineering library | ✅ | mates only | ❌ **Commercial use needs the designer's explicit written permission** | ❌ |
| NASA 3D Resources | ⚠️ mostly exteriors | some | ❌ | ✅ generally, but no implied endorsement or logo misuse | ❌ |
| Manufacturer catalogues (TraceParts, McMaster-Carr) | ✅ standard parts | ✅ | ❌ | ⚠️ licensed for design use; check before showing on screen | ❌ |

**Key points:**
- "Free to download" doesn't mean "free to use in a monetized video".
- CAD **mates don't carry over** into Blender. You get perfect parts and no motion; rebuilding motion with drivers is the easy, scriptable part.
- Image-to-3D (Hunyuan3D, TRELLIS) produces **one fused mesh**. Hunyuan's parts decomposition (via API) splits it into pieces but doesn't make a working mechanism. Fine for static props only.

**Priority order:** code-built → Onshape → CGTrader / CC0-CC-BY Sketchfab → GrabCAD with written permission.

**CAD → Blender:** there's no built-in STEP import.
- Free **STEP Importer** extension (Blender 5.1+); part names reportedly don't match the CAD tree.
- **CadQuery/OCP** script (pip-installable, runs headless) that reads the assembly and exports one named mesh per part. **Not yet tested.**

**Licence ledger:** log source URL, licence and required credit for each model, and credit them in the description.

---

## 8. The pipeline we built

**Location:** `video-pipeline/` on branch `claude/stoic-maxwell-bozzh6`
(commits `0b599b1`, `5278509`).

```
 script.json ──► tts.py ──► timeline.json ──► lock.py --check ──► lock.py --stills
 (Gate 1)        Kokoro      speech sets        physics report     (Gate 2)
                             shot lengths       gates must = 0°
      ──► render_all.py ──► frames/*.png ──► post.py ──► final.mp4 + captions.srt
          parallel,          transparent      labels, captions,    + thumbnail.jpg
          resumable          Workbench        readout, music        + description.md
                                                                     (Gate 3)
```

| File | Role |
|---|---|
| `script.json` | Episode definition: narration, chapters, camera from→to (azimuth/elevation/distance), events (alpha, explode, dial, highlight, pull_blocked, open, close), labels, step captions, dial readout |
| `tts.py` | Kokoro TTS per shot; speech length + padding = shot length → `timeline.json` |
| `lock.py` | Procedural lock model, **pin/fly pick-up physics simulation**, gates cut from where the simulation leaves each disc, per-frame state, label anchors projected to the screen, Workbench render |
| `render_all.py` | Parallel, resumable chunked rendering |
| `post.py` | Gradient background, labels with leader lines and anti-overlap, step pills, live dial readout (number + LEFT/RIGHT), watermark, end card, generated music bed with ducking, H.264/AAC encode, SRT, thumbnail, description with chapters |
| `README.md` | Process flow and run commands |

**Episode 1 output:** *How does a Combination Lock work?*
- 4:48 · 1280×720 · 24 fps · 6,913 frames · 20.8 MB.
- Combination **35-6-18**.
- Voice: Kokoro `am_michael` at 0.94× speed.
- 15 shots: hook, exterior, inside, gates, fence, pins, pick-up, second, third, open, re-lock, recap ×3, outro.

**Environment** (cloud container: 4 CPU, 15 GB RAM, no GPU):
- Blender 5.0.1 as a Python module (`pip install bpy`, needs **Python 3.11** and **numpy<2**).
- Kokoro TTS in a **separate** environment (it needs numpy 2).
- Mesa software OpenGL (`libegl1 libegl-mesa0 libgl1-mesa-dri`) so Workbench/Eevee can run headless.

---

## 9. Test log

### 9a. Network (cloud session)
| Host | Status | Impact |
|---|---|---|
| www.youtube.com | ✅ after you added it to the allow list | Channel and competitor data |
| i.ytimg.com | ❌ blocked | **Couldn't view thumbnails** |
| Social Blade, Invidious, Piped, Playboard | ❌ | No historical growth data |
| Wikipedia, GrabCAD, Sketchfab, Printables, CGTrader, RSM blog | ❌ | Couldn't verify the mechanism or search model libraries directly |
| pypi.org, GitHub release downloads, archive.ubuntu.com | ✅ | Installs, Kokoro model, Mesa |
| YouTube watch pages | ⚠️ rate-limited | Used the player API instead |

### 9b. Render engine benchmark (4 CPU cores, 1280×720)
| Engine | Time/frame | Verdict |
|---|---|---|
| **Workbench** | **~0.8 s** (simple test); **1.0–1.5 s** for the real scene | ✅ Used. Flat "technical illustration" look |
| Eevee | ~10 s (software OpenGL) | ❌ on CPU (~20 h for the video). **Use on a GPU** |
| Cycles (CPU, 12–16 samples) | ~12 s | ❌ on CPU |

**Full render:** 3 workers × 12 chunks, about 1.1 s/frame effective, roughly 2 h 10 min for 6,913 frames.
Post-processing and encode took a few minutes.

**Audio:** peak −1.2 dB, mean −25.6 dB, no dropouts. Voice quality not yet checked by ear.

### 9c. Problems hit and how they were fixed
| # | Problem | Fix |
|---|---|---|
| 1 | YouTube blocked | You added it to the network allow list |
| 2 | Watch pages redirected to Google's rate-limit page | Used YouTube's player API |
| 3 | Eevee/Workbench produced no image (`libEGL.so.1` missing) | Installed Mesa software OpenGL |
| 4 | `bpy` broke after Kokoro upgraded numpy to 2.x | Separate environments: `venv` (bpy, numpy<2) and `ttsvenv` (Kokoro) |
| 5 | Old kokoro-onnx 0.3.3 got installed and failed on the voices file | Pinned `kokoro-onnx>=0.4.9` |
| 6 | espeak-ng data path pointed at a hard-coded build folder | Symlinked that path to the packaged data (cloud workaround; may not be needed locally) |
| 7 | `import bmesh` failed | Import `bpy` before `bmesh` when Blender runs as a Python module |
| 8 | **Physics:** with a cam + 3 wheels, the standard R3 / L-past-once / R-direct sequence can't set all wheels; the pins can't reach the last wheel in time | Switched to **2 wheels + a drive cam with its own gate** (3 gates, 3 numbers); the simulation confirms the sequence works |
| 9 | Unwanted pick-ups during the hook; a gate hidden at the back | Wheels start in the middle of their free play; **combination searched** (35-6-18) so all gates start in view (81°/131°/35°) |
| 10 | False "contact" flash at shot boundaries | Track contact state instead of motion state |
| 11 | Dark seam across disc faces | Built the notched disc faces as triangle fans from the centre |
| 12 | Framing too tight (shackle cut off) | 35mm lens + distances ×0.85 |
| 13 | Labels overlapping | Collision-avoiding placement in post |
| 14 | Latch blocked the top-down gate views | Hide the latch during gate and recap shots |
| 15 | Shell quoting broke the render driver | Rewrote it as `render_all.py` |
| 16 | 2-hour background-task limit stopped the wait | Render was detached (nohup) and resumable; re-armed the wait |

---

## 10. What worked well
- **Physics-driven motion:** the video can't show anything mechanically impossible, and it caught the 3-wheel error.
- **Code-built model:** no licences, no drift, and the dial, ticks and numbers read clearly.
- **Voice-first timing:** shots stretch to fit the narration, so nothing is cut off.
- **Declarative script.json:** camera moves, ghosting, explode and highlights are data, not code.
- **2D layer:** labels with leader lines, step pills and the live dial readout look clean and Jared-like.
- **Resumable parallel rendering** survived the task time limit.
- **Complete deliverables:** MP4, SRT, thumbnail and a description with chapters, sources and AI-voice disclosure.

## 11. What failed or is weak
1. **The narration says things that aren't on screen.** The *spring*, *ramp* and *shackle notch* are
   mentioned but **not modelled**. You caught this. The root cause is that events are timed as a
   fraction of each shot, not to the spoken word, and nothing checks that what's said is shown.
2. **Flat visuals:** Workbench on CPU gives no soft shadows and no metal materials.
3. **Story wasn't planned:** written straight through, with no beat sheet and no voice guide (§15).
4. **Mechanism isn't verified against a real teardown:** the 2-wheel + cam design is physically
   consistent and hedged as "generic", but specific brands are unconfirmed.
5. **Thumbnail is a quick automatic one;** needs real design.
6. **Kokoro voice:** fine for testing, not a brand voice.
7. **Per-topic model and simulation code is the real cost** of each episode.
8. Thumbnails of competitors couldn't be analysed (`i.ytimg.com` blocked).

---

## 12. GPU vs CPU

| Task | CPU | GPU | Notes |
|---|---|---|---|
| Script, beat sheet, research | ✅ | n/a | LLM via API |
| TTS (Kokoro) | ✅ fine (~2× real-time) | faster | Not a bottleneck |
| Building the model, physics, rigging | ✅ | n/a | Seconds; pure Python |
| **Render: Workbench** | ✅ ~1–1.5 s/frame | faster | Flat look |
| **Render: Eevee** | ❌ ~10 s/frame | ✅ **est. ~0.5–1 s/frame at 1080p** (benchmark it) | **Main reason to use a GPU** |
| Render: Cycles | ❌ ~12 s+ | ✅ | Photoreal; slower than Eevee |
| AI models (image-to-3D, AI rigging, ComfyUI video) | ❌ | ✅ required | Only if you use them |
| Compositing and encode | ✅ | n/a | Minutes |

**Recommendation:** run locally on any **NVIDIA RTX GPU with 12 GB or more** (3060/4070 class) and
switch `ENGINE = "BLENDER_EEVEE"` in lock.py. Rent a GPU (Vast/RunPod) only for batch renders or
heavy AI work. The scripts don't change.

---

## 13. Where ComfyUI fits (and doesn't)

**Not as the pipeline's main tool.** ComfyUI is built around AI models; it adds nothing to Blender
rendering, physics or timing, and routing Blender through it makes the pipeline more fragile. Run
the pipeline as plain Python (or have Claude Code run it).

**Use ComfyUI only for:**
- the Explorer and capsule cinematic shots (your current brand style)
- backgrounds, textures, thumbnail bases
- image-to-3D for **static** props (Hunyuan3D)

**Avoid** AI restyling of the Blender renders: it brings back flicker and drifting geometry, which is
the advantage you'd be giving up.

---

## 14. Rigging

On a rented GPU, rigging is **Python driving Blender, run headless**. Rigging is CPU work;
the GPU is for rendering.

| Subject | How | Per video? |
|---|---|---|
| Machines | Parenting + constraints + drivers + simulation (as in the lock video) | Generated by script |
| **Explorer character** | Rig **once**: Rigify (built into Blender, scriptable), Mixamo, or an AI auto-rigger (Tripo, Meshy, open-source UniRig). Keep a library of reusable moves (point, float, turn) | **No** |
| Imported models | Part-name → joint-type mapping script + human check | Per model |

**Setup on a rented GPU:**
- A Docker image with Blender, both Python environments and Kokoro.
- One `run_pipeline.py` that runs each stage and stops at each checkpoint.
- Preview stills on a simple web page.
- Optionally Claude Code over SSH. Prefect only if you later need a dashboard with retries.

---

## 15. Story writing: voice and plan

### 15a. Channel voice guide (how Explained From Within sounds)
- Calm, curious, precise. **Never hype.** Talk to the viewer as "you" ("Watch what happens when you…").
- **One new term per sentence**, and it's **shown on screen the moment it's said.**
- At most about 20 words between visual changes.
- Signature moves: "Let's look inside", a slow-motion **"watch"** moment on the key mechanism, and the closing line *"Hidden processes, made visible."*
- Option: the **Explorer as narrator**, a guide inside the machine. This ties the Blender episodes to your brand.
- Hedge what isn't certain ("in many padlocks"); don't claim specific brands without a source.

### 15b. Story plan (beat sheet), required for every episode
| # | Section | Job | Lock example |
|---|---|---|---|
| 1 | Hook (0–15 s) | A paradox plus a glimpse of the payoff shot | "A dial attached to nothing", with a flash of gates aligning |
| 2 | Outside | Name at most 4 parts | shackle, body, dial, index |
| 3 | Reveal | Ghost or cutaway view | transparent body |
| 4 | The problem | Why it's hard | "the fence can't drop" |
| 5 | Mechanism | Step by step, each with a "watch" moment | pins/flys picking up wheels |
| 6 | Payoff | The moment it works, slowed + highlighted | gates align, fence drops |
| 7 | Twist | One surprising fact | tolerance: "not really 64,000" |
| 8 | Recap | Real time, best angle | full sequence from above |
| 9 | Close | Tagline | "Hidden processes, made visible." |

**Every sentence becomes a beat** with these columns:
`narration | on screen | highlight | label | camera | sound effect | source`.

### 15c. Enforced by the pipeline (to build)
- **Word-level timing** (forced alignment on the TTS audio), so events are keyed to words, e.g. *"spring"* → cut, highlight, label at that moment.
- **Narration-to-visuals check:** the build fails if a technical term is spoken without a matching part, highlight or label within about 1 s. This would have caught the v1 spring/ramp/notch problem.

### 15d. Spoken voice
Kokoro is fine for testing. For the channel, use **your own recorded voice** (most trusted) or a
consistent cloned voice of yours, and disclose synthetic voices in the description.

---

## 16. Scaling to complex models

The limit depends on **how the parts move**, not how many parts there are.

| Tier | Examples | Method | Effort |
|---|---|---|---|
| **1. Rigid mechanisms code can build** | gearboxes, differentials, clock escapements, 4-stroke engines, pumps, escalators, locks | **Mechanism library**: gear pair, rack, cam/follower, crank-slider, chain path, spring (helix that compresses), ratchet, linkage solver. Complex machines are combinations of these | Medium at first, then low per episode |
| **2. Imported CAD assemblies** | transmissions, jet engines | STEP import + part → joint mapping from the same library | Per model, human-checked |
| **3. Organic or deforming** | body topics, fluids, combustion | Sculpted/bought models, Blender simulations, or AI | High; better suited to the AI micro-journey style |

**Where it breaks down:** non-rigid motion (fluids, cloth, flexing), huge assemblies without clean part
names, and processes where the physics itself is the story (heat, chemistry).

---

## 17. To-do / roadmap

### P0: storytelling (next)
- [ ] Add `VOICE_GUIDE.md` and a beat-sheet template to the pipeline
- [ ] Word-level timing via forced alignment; events keyed to words
- [ ] Narration-to-visuals check that fails the build
- [ ] **Lock v2:** model the spring, ramp and shackle notch, with cutaway shots when each is mentioned; rewrite the script from the beat sheet

### P1: visuals
- [ ] Eevee materials (metal, painted parts), ground shadow, depth of field, nicer studio lighting
- [ ] Switch engine by config; benchmark on your local GPU
- [ ] Designed thumbnail template

### P2: scale
- [ ] Mechanism library (gears, cams, crank-slider, springs, chains, ratchets)
- [ ] Second episode to prove reuse (gearbox or 4-stroke engine)
- [ ] Test the CadQuery/OCP STEP → per-part import headless
- [ ] Licence ledger file per episode

### P3: operations
- [ ] Docker image + `run_pipeline.py` with checkpoints
- [ ] Preview web page for Gate 2
- [ ] Optional: Explorer character rigged once, with a move library

### Channel (your actions)
- [ ] Fix the sunburn title typo; remove title suffixes
- [ ] Decide the main pillar (recommended: Manufacturing/Materials)
- [ ] Retitle with the competitor formula
- [ ] Listen to the v1 voice; decide on your own voice vs cloned vs Kokoro
- [ ] Get the lock mechanism checked against a teardown before publishing v1/v2

---

## 18. Open questions and decisions

| Question | Status |
|---|---|
| Main pillar | Recommended Manufacturing/Materials. **Yours to decide** |
| Narrator voice | Kokoro for now; own or cloned voice recommended |
| Explorer in the Blender episodes? | Suggested; not decided |
| Local GPU model | Unknown; 12 GB+ NVIDIA recommended |
| Real padlock internals (brand-specific) | **Unverified**; currently hedged as generic |
| Next build | Lock v2 (storytelling fixes) or a second mechanism to prove scaling |

---

## 19. References

**Channels:**
- Explained From Within: https://www.youtube.com/@explainedfromwithin
- Jared Owen: https://www.youtube.com/@JaredOwen
- Stories Behind Everything: https://www.youtube.com/@StoriesBehindEverything-j6g
- History of Simple Things: https://www.youtube.com/@historyofsimplethings
- Made Vision: https://www.youtube.com/@MadeVision-TV
- Inside the Secret Factory: https://www.youtube.com/@MadeInSecrecy
- Factorama: https://www.youtube.com/@Factorama_eng
- The Infographics Show: https://www.youtube.com/@TheInfographicsShow
- Life According to Science: https://www.youtube.com/@LifeAccordingtoScience
- The Walking Effect: https://www.youtube.com/@TheWalkingEffect
- Fasted Fred: https://www.youtube.com/@ItsFastedFred
- DoodleProof: https://www.youtube.com/@DoodleProof
- Institute of Human Anatomy: https://www.youtube.com/@theanatomylab
- Kurzgesagt: https://www.youtube.com/@kurzgesagt

**Tools and background:**
- Jared Owen interview (BlenderNation): https://www.blendernation.com/2018/11/19/meet-the-artist-jared-owen/
- Space Needle post (BlenderNation): https://www.blendernation.com/2020/04/02/video-whats-inside-the-space-needle/
- BlenderMCP: https://github.com/ahujasid/blender-mcp
- STEP Importer for Blender: https://extensions.blender.org/add-ons/step-importer/
- Hunyuan3D in ComfyUI: https://docs.comfy.org/tutorials/partner-nodes/hunyuan3d/hunyuan3d-3-0
- Kokoro ONNX: https://github.com/thewh1teagle/kokoro-onnx

**Licences and policy:**
- GrabCAD model use: https://help.grabcad.com/article/246-how-can-models-be-used-and-shared
- Sketchfab → Fab migration: https://dev.epicgames.com/documentation/fab/migrating-assets-to-fab
- Onshape public docs (forum): https://forum.onshape.com/discussion/comment/43955
- CGTrader licence (forum): https://www.cgtrader.com/forum/selling-buying-3d-models/license-question
- YouTube inauthentic-content update: https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/

**Mechanism background:**
- Rotary combination lock (Wikipedia): https://en.wikipedia.org/wiki/Rotary_combination_lock
- How Combination Locks Work (HowStuffWorks): https://home.howstuffworks.com/home-improvement/home-diy/combination-lock.htm
