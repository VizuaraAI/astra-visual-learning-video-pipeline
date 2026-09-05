# Astra Visual Learning Video Pipeline

This is the complete reusable pipeline used with GPT-6 Astra to create today's Cell, Heart, and DNA educational videos in the visual language of the reference YouTube channel.

You do not need to be a programmer. Codex can study a reference, write the storyboard, build procedural Blender scenes, create narration, render previews, repair weak shots, and assemble a final MP4. The video creator supplies the teaching goal, reference material, and creative feedback.

## What is included

| Chapter | Storyboard | Main visual code | Narration/source |
|---|---|---|---|
| Cell | `storyboards/cell.json` | `src/render_scene.py`, `src/assets.py` | `scripts/cell-reference-timed.txt` |
| Heart | `storyboards/heart.json` | `src/heart_assets.py`, `src/cardiac_motion.py` | `scripts/heart.hi.md` |
| DNA | `storyboards/dna.json` | `src/dna_assets.py` | `scripts/dna.hi.md` |

The repo also includes fonts, narration audio, cloud-rendering code, preview tools, test evidence, cost records, provenance, and the full production history.

## 1. Download Codex

1. Download the ChatGPT desktop app from the [official app page](https://learn.chatgpt.com/docs/app).
2. Sign in and choose **Codex**.
3. Clone this repository, then open its folder in Codex.
4. Start a **New chat**.

## 2. Select Astra and effort 1

At the bottom of the Codex composer:

1. Choose **GPT-6 Astra**.
2. Choose **Low** reasoning—the lowest Astra setting, sometimes shown as effort **1**.
3. Use Low/1 for normal video creation. Increase it only for a difficult scientific, visual, or pipeline problem.

Astra officially supports low, medium, high, xhigh, and max reasoning. See the [official Astra guide](https://developers.openai.com/api/docs/guides/latest-model). If Astra is not available on the collaborator's account yet, use the strongest Codex model shown and follow the same workflow.

## 3. Install the production tools

Install Python 3.11+, Blender 5.2.1, ffmpeg/ffprobe, and Git. Then run in Codex's terminal:

```bash
python -m venv .venv
source .venv/bin/activate             # macOS/Linux
# .venv\Scripts\activate              # Windows PowerShell
python -m pip install -r requirements.txt
blender --version
ffmpeg -version
```

For full rendering, create a [Modal](https://modal.com/) account. ElevenLabs is optional: the example narration is already included, but new narration needs an ElevenLabs key.

## 4. Give Astra the creative brief

Put these in the repository or drag them into the Codex chat:

- reference video or permitted reference link;
- final script, or the topic and learning outcome;
- existing narration audio, if any;
- colors, fonts, logo rules, language, and target duration;
- desired delivery, such as `1920x1080, 24 fps, YouTube-ready MP4`.

Paste this prompt:

```text
Use this repository's Astra visual-learning pipeline to create an educational
chapter about [TOPIC]. Study the supplied reference for its visual grammar,
pacing, camera language, labels, and transitions. Use original procedural
geometry.

First create a shot-by-shot storyboard and narration timing. Then render cheap
local preview frames and a contact sheet. Stop before any paid cloud render and
show me the previews, scientific assumptions, estimated runtime, and estimated
cost. After I approve the preview, render the final 1920x1080 video, verify its
audio/video properties, and produce the master plus a contact sheet.
```

The paid-render checkpoint catches creative mistakes before GPU spending starts.

## 5. Analyze, storyboard, and build

Ask Astra to record the reference's teaching sequence, shot boundaries, cameras, transitions, palette, lighting, label style, narration rhythm, and scientific simplifications in `docs/STYLE_ANALYSIS.md`.

Copy the closest JSON file in `storyboards/` to `storyboards/<topic>.json`. Each shot should define duration, narration, camera, labels, visible action, and teaching purpose.

```text
Use storyboards/cell.json as the schema. Create storyboards/<topic>.json from
my script. Attach every spoken idea to a visible action. Add no visual detail
that does not help the learner understand the current sentence.
```

Reuse `src/render_scene.py` and `src/geometry.py`. Put new topic-specific procedural geometry in `src/<topic>_assets.py`. The existing Cell, Heart, and DNA modules are working examples.

## 6. Make cheap previews first

Replace `heart` with the chapter name:

```bash
blender -b -t 4 --python src/render_scene.py -- \
  --manifest storyboards/heart.json \
  --all-previews --width 960 --samples 12 \
  --output cache/previews

python src/interface.py \
  --preview-dir cache/previews \
  --output tests/local-frames
```

Review composition, text size, timing, missing geometry, intersections, colors, and scientific meaning. Repeat until the contact sheet looks good.

## 7. Prepare narration

For new ElevenLabs speech, set `ELEVENLABS_API_KEY` in the environment—never in Git:

```bash
python src/narrate.py heart --cache cache/audio --generate
```

Heart and DNA narration is bundled in `assets/narration/`; Cell reference audio is in `assets/cell-reference-audio.m4a`. The [engineering guide](docs/ENGINEERING_GUIDE.md) contains the exact voice and conversion settings.

## 8. Benchmark before the full cloud render

Authenticate Modal and use unique resource names:

```bash
export VL_APP=vl-my-topic
export VL_VOLUME=vl-my-topic-data
export VL_GPU_WORKERS=4

python -m modal deploy src/cloud.py
python src/manage.py upload --audio cache/audio
python src/manage.py dispatch --run my-topic-benchmark \
  --chapter heart --benchmark --samples 128 --cache cache/bench
python src/manage.py status --run my-topic-benchmark \
  --cache cache/bench --download
```

Inspect the returned frame, runtime, and cost. Launch production only after that benchmark is acceptable.

## 9. Render, assemble, and verify

```bash
export VL_GPU_WORKERS=24
python src/manage.py dispatch --run my-topic-final \
  --chapter heart --samples 128 --chunk 240 --cache cache/jobs
python src/monitor_production.py --run my-topic-final \
  --cache cache/production --masters masters --chapters heart
python src/verify_media.py --masters masters --output contact-sheets
```

Cloud chunks survive a disconnected laptop, have checksums, and cannot assemble with missing or overlapping frame ranges. Still watch the whole master with headphones before YouTube upload. Check narration sync, cuts, label spelling, audio, color continuity, black frames, and science.

## If a video is not good, improve its skill file

The repo includes a separate creative-memory skill for each item:

- `.agents/skills/cell-video/SKILL.md`
- `.agents/skills/heart-video/SKILL.md`
- `.agents/skills/dna-video/SKILL.md`

Add specific, observable corrections only to the affected video's file:

```markdown
## Learned corrections

- Keep labels inside the title-safe 10% margin.
- Hold the final camera position for 18 frames after a label appears.
- In shot 7, show the membrane opening before particles cross it.
- Use the channel teal only for the active teaching object.
```

Then tell Astra:

```text
The preview is weak because [specific problem]. Update the <topic>-video skill
with a reusable correction, apply it to the storyboard or renderer, and make a
new low-cost preview. Do not start a paid render.
```

For a new series, copy the closest skill folder, rename it, update the YAML `name` and `description`, and add only recurring rules unique to that series. Avoid vague rules such as “make it better.”

## Repository map

```text
.agents/skills/       Per-video creative memory for Astra
assets/               Fonts and reusable narration/reference audio
docs/                 Tutorial depth, style, provenance, and delivery details
scripts/              Narration scripts and reference timing
src/                  Blender, cloud render, assembly, and QA code
storyboards/           Authoritative shot manifests
tests/                 Preview evidence and verification records
```

Raw frames, generated caches, secrets, and master MP4s are intentionally ignored. Store final videos in GitHub Releases, Drive, or YouTube rather than normal Git history.

## Production rules

- Always preview and benchmark before a full GPU render.
- Name a cost ceiling in the prompt; 128-sample renders can consume meaningful cloud budget.
- Use only reference material, voices, audio, and logos you have permission to use.
- These are teaching schematics. Have a subject-matter reviewer approve new medical or molecular claims.
- Never commit API keys or account tokens.

For exact architecture, production commands, budgets, rendering settings, and the Heart valve repair, read [docs/ENGINEERING_GUIDE.md](docs/ENGINEERING_GUIDE.md). For authorship and source context, read [docs/PROVENANCE.md](docs/PROVENANCE.md).
