# Strategy Notes — "Explained From Within"

Running log of decisions and evidence. Newest decisions at the bottom of each section.

## Niche decision

- Rejected: AI tools tutorials (needs screen recordings, not generative video),
  Gen Z finance (dominated by on-camera creators; numbers/charts unsuitable for video models).
- Chosen: **documentary / explainer — "what happens inside your body"**, cinematic 3D,
  long-form (10–13 min to start; test ~18–20 min once retention data exists), faceless,
  built with LTX-2.5 and MiniMax H3. Cadence target: 2–3 episodes / month.

## Evidence so far

- Generic "inside your body when you drink coffee" (3D anatomy framing): recent uploads < 500–1.6K views.
- Winners frame around **you + an action + time/limit**, not "how a process works".
- Big-channel hits (Dr. Berg 15M, Joe Fazer 2.43M) prove topic demand only (views/subs ≈ 0.5–0.6×).
- Only true small-channel outlier so far: **Think Science** (240K subs, 27 videos, 6.2M top hit).
- Benchmark #2 **Nucleus Medical Media** (6.9M subs, accurate 3D, no story, clinical titles, 3–6 min):
  recent median ~24.5K vs Think Science ~437K → accurate 3D alone does not earn recommendations.
  Its all-time #1 (340M) is framed "What Happens If You…". Evergreen searchable topics compound for years.
- Benchmark #3 **BodyLogic 3D** (125K subs, AI 3D, silent Shorts, one template): 2 viral hits = 78% of 261M views,
  recent median ~9.4K. AI 3D alone wins the lottery once, then decays. ~2,090 views per subscriber
  (vs Think Science ~117) → narration + story is what converts viewers into subscribers.
- Benchmark #4 **The Infographics Show** (15.5M, 2D, second-person story): story works without 3D;
  "What Happens When You Die?" 27M, "What Happens to Your Body…" 19M, "(Minute by Minute)" 20M,
  "Russian Sleep Experiment" 22M (sleep curiosity). Recent uploads 13–47 min.
- **Verdict:** story is the engine, 3D is the differentiator. Format validated across 4 channels
  (observational). Next evidence must come from our own episodes.
- Failure control **Digest 3D** (same launch month as Think Science): 126 videos, ~48-view recent median.
  Copied surface, not engine → see anti-patterns below.
- Length control **Inside Us** (170K, 3D, 11–15 min, textbook titles, no story): ~720 recent median →
  long-form alone does not work. Story + "you" framing is the engine (one package).
- **Research closed** at 6 channels (2 story winners, 4 no-story/copycat underperformers). Next evidence = our own episodes.

## Anti-patterns (from Digest 3D and BodyLogic 3D)

- Single-food topics ("eat X every day"), fear clickbait ("before it's too late 😱", "stop eating X until…")
- False authority ("Doctor Approved") or fake first-person ("I ate…") on a faceless channel
- 3–4 min videos (neither Short nor story-length)
- Volume over quality (~3/week templated) and one repeated template
- Positioning that sells the tool ("3D visualisation") instead of the viewer ("your body")
- Textbook framing ("What is [disease]?", "Anatomy of [organ]") — targets students searching, not viewers browsing

## Launch expectations and decision rule

- First episodes may get very few views. *(Revised 2026-09-30.)* Read CTR only once a video has
  ~1,000 impressions; the first four new-format uploads (EP004–EP007) set the channel's own baseline;
  5% CTR and 40% viewed are reference points, not targets.
- Review after six new-format episodes: if CTR and retention hold against the baseline but views don't,
  keep going (distribution lags); if CTR is low → fix titles/thumbnails; if retention is low → fix story/pacing.

## Format rules (current)

1. **Title:** "What Happens To Your Body When You [habit] ([hour by hour / day by day])"
   or an honest identity hook. No "miracle", no "N benefits", no single-food videos.
2. **Two-layer story:** outside (relatable person, second-person "you") ↔ inside (Explorer).
   Rhythm per checkpoint: Outside → Inside → Outside. ~35% outside / 65% inside.
3. **Hook in parallel:** narration hooks in the first 10 s while the visual story builds.
4. **Master metaphor** set up in the first minute, paid off at ~45–55% (the Explorer enters it).
5. **Objection handling** ~55%, practical section ~70–85%, "What we simplified" + caveats, callback close.
6. **Visual coding:** outside = warm, realistic; inside = cool, bioluminescent; persistent on-screen clock.
7. Host has no dialogue (narration only) — avoids lip-sync.
8. **No single template.** Vary topic type and structure; never recycle the same topic.
9. **Shorts are a funnel**, cut from each long episode (3–5 per episode), led by a true surprise/shock beat.
10. Channel description discloses AI-assisted visuals + fictional Explorer.

## Accuracy policy

- Two-layer sourcing: (1) association/institution (NIH/NHLBI, CDC, WHO, AHA, AASM, Johns Hopkins, Mayo, NHS),
  (2) primary research (PubMed, Cochrane) for mechanism details.
- Claim ledger per script: claim → source → evidence level → wording.
- Wording matches evidence ("in mice…", "research suggests…"). Never "approved by" an association.
- Optional: paid licensed reviewer (MD/RD) credited in the description.
- Accuracy = trust and defensibility, not the growth engine. Don't compete with medical studios on
  anatomical precision; compete on story, framing and length.
- Use competitors' transcripts as structural benchmarks only — never rewrite their scripts.

## Production mapping

| Asset | Model / mode |
|---|---|
| Explorer + capsule, Host | H3 I2VA: one first-frame plate per shot, re-anchored from locked reference sheets (corrected 2026-09-30) |
| Location transitions | F2V (first/last frame) |
| Environment B-roll | LTX-2.5 T2V/I2V (local, cheap in bulk) |
| Labels, numbers, clock, disclaimers | Editor — never generated |
| Control narration, music | Recorded/TTS narrator and a music bed at post-production (adopted 2026-09-30) |

## Episode 1 (draft, pending benchmark)

"What Happens To Your Body When You Don't Sleep (Hour by Hour)"
- Host: working adult, night before a product launch (narrated as "you").
- Master metaphor: "The Pressure Tank" (adenosine); caffeine holds the valve shut.
- Midpoint: hour 24, the coffee helps less and less as the tank keeps filling (no "stops working" absolute).
  Climax: hour 36, drowsy drive home, non-graphic and safety-led (microsleep; local sleep — rats and implanted-electrode patients).
- Science locks (2026-09-30): "about 0.05% blood alcohol", never "legal limit"; brain clearance during sleep is contested
  (Xie 2013 vs Miao 2024); hunger hormones = small study. This is now EP004 (EP001–EP003 are published).
- Callback: "Your body doesn't wait for 'after'."

Adjustment confirmed by benchmarks #1 and #4: winners narrate the Host as **"you"**, not a named character →
keep the Host as a consistent visual reference (internal name only), narrate in second person.
Full updated story sheet: COMPARISON-REPORT.md, Section 10.
