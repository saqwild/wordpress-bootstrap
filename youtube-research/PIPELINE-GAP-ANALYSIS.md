# Pipeline Gap Analysis — vidgen_minimax vs research findings

**Date:** 2026-09-29
**Repo reviewed:** `saqwild/vidgen_minimax` @ `e2905ef` (read-only)
**Compared against:** [COMPARISON-REPORT.md](COMPARISON-REPORT.md) (6-channel benchmark)

---

## 1. Headline

The pipeline is **already strong on process and accuracy** — stricter than what I had proposed. It does not
need rebuilding. The gaps are almost all **upstream packaging and story-model decisions** that the benchmark
research says drive views:

| Area | Pipeline today | Research says | Gap |
|---|---|---|---|
| Accuracy, sourcing, compliance, QA | Claim + visualization ledgers, coverage scan, compliance gate, independent script review, validators | Required for trust and policy | ✅ None — keep |
| **Title framing** | Mechanism + object ("How a Platelet Plug Forms Inside a Tiny Cut") | "What Happens To Your Body When You…" + time structure / honest identity hook | ❌ Major |
| **When packaging is decided** | Title chosen after picture lock (stage 06) | Title/thumbnail concept is part of the engine → decide at ideation | ❌ Major |
| **Story model** | Explorer + audio-only Control, familiar trigger, no human Host, no second person | Second-person two-layer story (Host outside ↔ inside) | ❌ Major |
| **Topic selection** | Mechanism-first (platelet plug, glass bottle, battery, concrete) | Viewer-action-first (sleep, coffee, fasting, identity) | ❌ Major |
| Pillar rollout | EP001–EP004 rotate across 4 pillars | Launch focused on one pillar | ⚠️ Owner decision |
| Benchmark method (01b) | Top-3 most-viewed topic videos (coverage + opening) | Size-adjusted: views ÷ subscribers, recency, small-channel outliers, one failure example | ⚠️ Medium |
| "No arbitrary countdowns" rule | Could block hour-by-hour structure | Real, sourced timelines are a winning format | ⚠️ Clarify |
| Post-release feedback | 48 h / 7 d snapshots mentioned in launch plan only | KPI thresholds + decision rule feeding next ideation | ❌ Missing stage |
| Shorts | Optional; one teaser at 06a | 3–5 Shorts per episode as a funnel, led by a true surprise beat | ⚠️ Medium |
| Runtime / clip unit | ~600 s, 40 × 15 s clips, one action per clip | 10–13 min start | ✅ Aligned |
| Disclosure, non-graphic, no medical advice, Explorer only observes | In bible and channel.json | Aligned with anti-clickbait findings | ✅ Keep |

---

## 2. What the pipeline already covers (map of my proposed stages)

| My proposed stage | Existing stage(s) | Status |
|---|---|---|
| Story Definition Sheet | 01 ideation (premise) + 01b coverage scan | Partial — no Host/want/stakes/metaphor/surprise fields |
| Script, two-layer | 03a writer (explained-from-within-story-writer skill) | Partial — Explorer/Control only, no Outside layer |
| Claim ledger | 02 research + 02a sourcing + 02b compliance | ✅ Stronger than proposed |
| Shot list (I2V/F2V/T2V) | 04d shot plan + 04e storyboard | ✅ (I2VA first-frame, one action per 15 s clip) |
| Character references | 04b character refs + 04c scene refs (Nano Banana) | ✅ — needs a Host role if adopted |
| Generation | 04f prompts + 04g upload package + 04h pilot QA + 05 ingest | ✅ With validators and canary |
| Quality check | 05a render QA + 07 final QA | ✅ |
| Voice and assembly | Native H3 audio + 06a Remotion/ffmpeg assembly | ✅ (no separate narration by design) |
| Shorts and metadata | 06 metadata (SEO.md) + teaser at 06a | Partial — packaging late, Shorts minimal |
| Analytics feedback | — | ❌ Missing |

---

## 3. Conflicts in detail and proposed changes

### C1 — Title framing (SEO.md §4, keyword-to-title contract)

- **Today:** title derived from the primary search phrase: mechanism + familiar object
  (EP001 "How a Platelet Plug Forms Inside a Tiny Cut"; EP002 "How Glass Bottles Are Made: Molten Glass to Bottle").
- **Evidence:** this is the framing of the underperforming controls (Nucleus ~0.004×, Inside Us ~0.004×).
  The winners use "What Happens (to Your Body) When You…", "(Hour/Minute by Minute)", honest identity hooks.
- **Change:** add a **viewer-outcome formula** as the default for Inside Your Body:
  `What Happens [To Your Body / Inside You] When You [everyday action] ([time structure])`,
  keeping the primary keyword in the description, chapters and, where natural, the title.
  Keep the mechanism formula for search-driven evergreen topics (~1 in 5).

### C2 — Packaging decided too late (SEO.md §9 steps 5–7, stage 06)

- **Today:** three title options "before script lock when possible"; final title after picture lock.
- **Change:** at **01 ideation**, require a working title + thumbnail concept (viewer-outcome formula),
  checked against the 01b benchmark; lock the title promise at 03b. Stage 06 only finalises wording.

### C3 — Story model (EPISODE_SPEC, SCRIPT_BRIEF, SCRIPT_CRAFT, CAST, story-writer skill)

- **Today:** familiar trigger → Explorer enters → mechanism → return outside. Speech = Explorer radio
  questions + audio-only Control explanations. No human in the outside world beyond the trigger.
- **Evidence:** both sustained winners run a **second-person human story in parallel** with the explanation;
  all four underperformers don't.
- **Change (fits existing constraints):**
  - Add **CAST-002 Host** — an outside-world person, visual only, no dialogue, one visible character per frame
    (compatible with `maximum_visible_characters: 1`; Host and Explorer never share a frame).
  - **Control speaks to "you"** (second person) as the narrator — keeps the native-H3 audio policy;
    no post narration layer needed.
  - Script table gains a **Layer** column (Outside / Inside) and the rhythm Outside → Inside → Outside per checkpoint.
  - Story Definition Sheet fields added to the premise: Host, want, trigger, stakes, outside beats,
    master metaphor (the Explorer enters it), midpoint turn, objection, surprise beat, callback.

### C4 — Topic selection (01 ideation, launch seeds, SEO.md pillar table)

- **Today:** mechanism-first seeds (platelets, glass, battery, concrete).
- **Change:** ideation must name the **viewer action or identity** first, then the mechanism that explains it.
  Example: not "How adenosine builds sleep pressure" but "What Happens To Your Body When You Don't Sleep (Hour by Hour)",
  with adenosine as the master-metaphor mechanism.

### C5 — Pillar rollout (PILOT_AND_EPISODE_FORMATS, MONETIZATION_PLAN)

- **Today:** EP001 body → EP002 manufacturing → EP003 technology → EP004 materials, to test transfer.
- **Research:** mixed pillars early make it harder for YouTube to learn the audience.
- **Recommendation:** owner's call. Suggested: pause pillar rotation after EP002; run the next 4–6 on
  Inside Your Body with the new framing; compare KPIs against EP001/EP002.

### C6 — Benchmark method (pipeline/youtube_benchmark.md + tools/youtube_benchmark_validator.py)

- **Today:** three highest-viewed directly relevant videos → opening behaviour + coverage topics.
- **Gap:** "highest-viewed" is biased to big channels (the Dr. Berg / Joe Fazer trap).
- **Change:** record channel subscribers and upload age per candidate; compute views ÷ subscribers;
  require at least one **small-channel outlier** (≥ 5× views/subs) and one **low performer** on the same
  topic as a contrast. Keep coverage-topic scan as is.

### C7 — "Avoid arbitrary countdowns" (EPISODE_SPEC, story-writer skill)

- **Change:** clarify that **sourced real-time timelines** (hour 16 / 24 / 36) are allowed and encouraged;
  only invented deadlines/countdowns are banned.

### C8 — No post-release stage

- **Add `08-post-release-review`** (not an owner-gated render stage; an analytics record):
  48 h and 7 d snapshots (impressions, CTR, AVD %, retention at 0:15/0:30, traffic sources, subs gained).
  Decision rule (revised 2026-09-30): CTR read only after ~1,000 impressions; the first four new uploads set the
  baseline; below baseline CTR → packaging; below baseline retention → story/pacing; both OK but low views → continue.
  Output feeds the next episode's 01 ideation.

### C9 — Shorts (PILOT_AND_EPISODE_FORMATS, 06a)

- **Change:** 3–5 Shorts per episode as standard, each opening on one true surprise beat, linked to the
  long-form via Related Video.

---

## 4. Risks of the changes

| Risk | Mitigation |
|---|---|
| Host = a second identity to lock (Nano Banana drift) | Own reference sheet; re-anchor from one approved image (existing rule) |
| Control as second-person narrator across 40 native-audio clips → voice drift | Pilot QA (04h) already gates; test on a 3–4 clip canary first |
| Outside shots reduce inside runtime | ~35/65 split; outside shots are simpler to render |
| Validators assume current script table | Update coverage validator / story-writer checks together with the bible |
| Changing everything at once hides what worked | Change packaging + story model on one episode, keep the rest identical |

---

## 5. Recommended rollout

1. **Get EP001 (and EP002 when live) analytics** — impressions, CTR, AVD, retention curve, traffic sources.
   This is the first real evidence on the owner's own channel.
2. Apply C1, C2, C4, C7 (documents only — low risk).
3. Apply C3 (Host + second-person Control) and pilot it on the next body episode
   ("What Happens To Your Body When You Don't Sleep (Hour by Hour)").
4. Add C8 (post-release stage) and C6 (benchmark upgrade) — these touch `channel.json`
   `pipeline_stages` and a validator, so they need owner approval per AGENTS.md.
5. Compare the new episode's KPIs with EP001/EP002 before rolling out further.

## 6. Files that would change

| Change | Files |
|---|---|
| C1, C2 | `bible/SEO.md` §4/§9, `pipeline/stages/01-ideation.md`, `pipeline/stages/06-distribution-metadata.md` |
| C3 | `bible/CAST.md`, `bible/CHARACTER_BIBLE.md`, `bible/EPISODE_SPEC.md`, `bible/SCRIPT_BRIEF.md`, `bible/SCRIPT_CRAFT.md`, `local_skills/explained-from-within-story-writer/SKILL.md`, `channel.json` → `cast` (owner) |
| C4 | `pipeline/stages/01-ideation.md`, `channel.json` → `launch` seeds (owner), `bible/SEO.md` pillar table |
| C5 | `bible/PILOT_AND_EPISODE_FORMATS.md`, `bible/MONETIZATION_PLAN.md` (owner decision) |
| C6 | `pipeline/youtube_benchmark.md`, `tools/youtube_benchmark_validator.py`, its test |
| C7 | `bible/EPISODE_SPEC.md`, story-writer skill |
| C8 | new `pipeline/stages/08-post-release-review.md`, schema, `channel.json` → `pipeline_stages` (owner), `pipeline/PIPELINE.md` |
| C9 | `bible/PILOT_AND_EPISODE_FORMATS.md`, `pipeline/stages/06a-postproduction-assembly.md` |
