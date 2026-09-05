# Visual Learning procedural chapter production

Three narrated educational 3D chapters, built from original mathematical meshes in Blender 5.2.1. This repository contains the scripts, shot manifests, interface renderer, cloud renderer and production records. No paid models, stock music or generated raster models are used. The Barlow font is bundled under its SIL Open Font License.

## Start here

- `docs/STYLE_ANALYSIS.md`: reference observations, plan and science reconciliation.
- `scripts/heart.hi.md` and `scripts/dna.hi.md`: original Hindi narration.
- `scripts/cell-reference.hi.json3`: unmodified retrieved automatic caption track.
- `scripts/cell-reference-timed.txt`: readable reference caption timing.
- `storyboards/*.json`: authoritative shot order, frame counts, teaching labels and narration.
- `RUNNING_NOTES.md`: resumable production log.
- `tests/local-frames/`: pre-cloud test frames and contact sheets.
- `docs/PROVENANCE.md`: source ownership context, original asset authorship and scientific scope.
- `assets/narration/*.flac`: exact final speech edits; no new speech request is needed to reuse them.

## Runtime

Use Python 3.11+, Blender 5.2.1 and ffmpeg/ffprobe on PATH. Python dependencies: `modal`, `requests`, `Pillow`, `numpy`, `yt-dlp`. Install in a virtual environment. The implementation is portable across macOS, Windows and Linux; the delivered run used an 8 GB M1 Mac for tests and Modal L40S GPUs for production rendering.

```bash
python -m venv .venv
# Activate using the appropriate shell command for your OS.
python -m pip install -r requirements.txt
# Keep the delivered final manifests for an exact rerender.
blender -b -t 4 --python src/render_scene.py -- --manifest storyboards/heart.json --all-previews --width 960 --samples 12 --output cache/previews
python src/interface.py --preview-dir cache/previews --output tests/local-frames
```

`build_manifest.py` restores the authored twenty-second placeholder timing for original chapters. Narration generation recalculates final frame counts; do not rerun the manifest builder after narration unless intentionally resetting the edit.

## Speech

Set `ELEVENLABS_API_KEY` in your environment, without committing it. The narrator is `9FTUWXd0yHJL1ZiZ71RK` (Anika—Engaging Teacher), `eleven_multilingual_v2`, `language_code=hi`. No voice cloning is performed. Speech is cached per shot; existing files are reused. Call this only after the test-frame checkpoint.

```bash
python src/narrate.py heart --cache cache/audio --generate
python src/narrate.py dna --cache cache/audio --generate
```

The recreation uses audio extracted from the owned reference to retain its exact delivery and pauses. The delivered timelines are locked at 891.083333 s (cell), 480.333333 s (heart) and 480.5 s (DNA). Reuse the bundled audio:

```bash
mkdir -p cache/audio
ffmpeg -i assets/cell-reference-audio.m4a -t 891.083333 -ar 48000 -ac 2 cache/audio/cell.wav
ffmpeg -i assets/narration/heart.flac cache/audio/heart.wav
ffmpeg -i assets/narration/dna.flac cache/audio/dna.wav
```

## Cloud rendering

Authenticate Modal using its standard environment variables or named account configuration. The delivered cell pass used workspace `vizuaraai`, app `vl-execu-20260905-prod`, volume `vl-execu-20260905-data`. The final heart and DNA pass used the user's newly authorized `rajatdandekar` profile, app `vl-execu-20260905-quality`, volume `vl-execu-20260905-quality-data`. App/volume selection is explicit. Never stop unrelated apps. Do not commit credentials.

```bash
# Select your authorized profile first; these names create isolated resources.
export VL_APP=vl-execu-20260905-quality
export VL_VOLUME=vl-execu-20260905-quality-data
export VL_GPU_WORKERS=48
python -m modal deploy src/cloud.py
python src/manage.py upload --audio cache/audio
python src/manage.py dispatch --run bench-quality --chapter heart --benchmark --samples 128 --cache cache/bench
python src/manage.py dispatch --run bench-quality --chapter dna --benchmark --samples 128 --cache cache/bench
python src/manage.py status --run bench-quality --cache cache/bench --download
# Inspect actual cloud frames and timings before the full pass.
python src/manage.py dispatch --run quality-v2 --chapter heart --samples 128 --chunk 240 --cache cache/jobs
python src/manage.py dispatch --run quality-v2 --chapter dna --samples 128 --chunk 240 --cache cache/jobs
python src/monitor_production.py --run quality-v2 --cache cache/production --masters masters --chapters heart dna
# A fresh cell rerender can use the same app and its own run.
python src/manage.py dispatch --run cell-rerender --chapter cell --samples 48 --chunk 240 --cache cache/jobs
python src/monitor_production.py --run cell-rerender --cache cache/cell-production --masters masters --chapters cell
```

These calls use a deployed function and `spawn()`, so jobs survive a disconnected client. The cloud worker writes an encoded chunk, a representative actual frame and a JSON completion record, then commits the volume. Progress comes from those records rather than a process log. Assembly refuses missing, overlapping or incomplete frame ranges. Completed chunks are idempotent; each chunk has a SHA-256 checksum. Never mix artifacts from different source revisions in the same run directory.

Production uses native 1920×1080 at 24 fps, Cycles CUDA, adaptive sampling, GPU OpenImageDenoise, no GPU compositor, H.264 CRF 16 and AAC 192 kb/s. The retained cell pass uses 48 samples at a 0.045 adaptive threshold. The final heart and DNA pass uses 128 samples at a stricter 0.02 threshold. L40S is preferred, with A10 and L4 fallbacks. Each worker reserves two CPU cores and 8 GiB RAM, and records its assigned GPU and rate. Temporary PNGs occupy worker scratch space; encoded chunks persist on the volume. The initial app permits 18 GPU workers; the final quality app was raised to 48. CPU test and partial heart production records remain in the cost audit, but that superseded CPU work is not used in the final masters.

All cardiac valve shape keys and myocardial contraction share a 72 beats/minute phase. AV valves close during contraction and the semilunar/AV opening windows do not overlap; invariant checks are retained in `tests/cardiac-timing-check.json`. Motion is a teaching schematic rather than a pressure/flow simulation.

## Budget and limitations

The dispatch controller conservatively reserves at most USD 135 per video for one complete rendering pass, leaving headroom within the brief's approximately USD 150 per video limit. The original cell reservation is $134.96; each 128-sample quality pass reserves at most $135. The user subsequently authorized freely using GPUs on the additional $250-plan workspace. This plan fee is distinct from metered compute. These are ceilings rather than predicted bills. A lower-priced fallback receives more wall time within the same dollar reservation. The controller will not automatically rerender failed work. Review measured costs and reservations before repairs. Reports estimate resource cost from measured runtime and published rates; the provider invoice remains the authority for actual billing, cold starts and account-specific credits.

## Verify and compare

```bash
python src/verify_media.py --masters masters --output contact-sheets
python src/compare.py --reference /path/to/owned-cell-reference.mp4 --master masters/cell.mp4 --output comparison --video
```

The complete comparison video uses the macOS `h264_videotoolbox` encoder. On another platform, replace that encoder with `libx264` and a suitable preset; the comparison sheets are portable. All comparison timestamps are explicitly listed in `src/compare.py`.

The models are educational representations with deliberately expanded microscopic detail, shortened process times and nonliteral scale. The heart is a procedural anatomical schematic, not patient imaging. Molecular meshes are not atomic-coordinate reconstructions. Review the final deviations report for the exact extent of reference matching and scientific annotations. No claim of pixel-identical reconstruction is implied by a matching output duration.


## Delivered valve-transit correction

Final heart master `quality-final` reuses the 128-sample `quality-v2` pass except zero-based shots 5, 10 and 13. Those shots were rerendered as `valve-repair` using the final source in this repository. `stage_repaired_chapter` copies the chosen complete chunks into a fresh run and refuses gaps/overlaps. The final source can simply render the whole heart in one fresh run; the extra staging step is only needed to reproduce the incremental delivery workflow.

```bash
blender -b --factory-startup -t 2 --python tests/check_valve_transit.py
# For an incremental correction of an existing quality-v2 run:
export VL_APP=vl-execu-20260905-valve-fix
export VL_VOLUME=vl-execu-20260905-quality-data
export VL_GPU_WORKERS=12
python -m modal deploy src/cloud.py
python src/manage.py dispatch --run valve-repair --chapter heart --samples 128 --shots 5 10 13 --cache cache/repair/jobs
python src/finalize_repair.py --cache cache/repair --base-cache cache/production --masters masters
```

The actual geometry test sampled ten seconds at 240 Hz and checked every marker intersecting a valve plane. The minimum valve opening during all 1,428 sampled intersections was 1.0 (fully open). See `tests/valve-transit-check.json`. Markers illustrate one-way transit; they are not a computational fluid-dynamics simulation.
