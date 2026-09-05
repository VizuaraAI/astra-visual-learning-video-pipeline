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

Authenticate Modal using its standard environment variables or account configuration. Use workspace `vizuaraai`. The app and volume names are deliberately isolated from the other session: `vl-execu-20260905-prod` and `vl-execu-20260905-data`. Never stop unrelated apps. Do not commit credentials.

```bash
python -m modal deploy src/cloud.py
python src/manage.py upload --audio cache/audio
python src/manage.py dispatch --run bench --benchmark --cache cache/bench
python src/manage.py status --run bench --cache cache/bench --download
# Inspect the actual cloud frames and timings before the full pass.
python src/manage.py dispatch --run v1 --chapter heart --worker cpu --chunk 240 --cache cache/jobs
python src/manage.py dispatch --run v1 --chapter dna --worker cpu --chunk 240 --cache cache/jobs
python src/manage.py dispatch --run v1 --chapter cell --worker gpu --chunk 240 --cache cache/jobs
python src/manage.py status --run v1 --cache cache/status
python src/monitor_production.py --run v1 --cache cache/production --masters masters
```

These calls use a deployed function and `spawn()`, so jobs survive a disconnected client. The cloud worker writes an encoded chunk, a representative actual frame and a JSON completion record, then commits the volume. Progress comes from those records rather than a process log. Assembly refuses missing, overlapping or incomplete frame ranges. Completed chunks are idempotent; each chunk has a SHA-256 checksum. Never mix artifacts from different source revisions in the same run directory.

Production uses native 1920×1080 at 24 fps, Cycles CUDA, 48 samples with adaptive sampling, GPU-accelerated OpenImageDenoise, no GPU compositor, H.264 CRF 16 and AAC 192 kb/s. L40S is preferred, with A10 and L4 fallbacks. Each worker reserves two CPU cores and 8 GiB RAM, and records the assigned GPU and its rate. Only temporary PNG frames occupy worker scratch storage; encoded chunks persist on the volume. The GPU function is capped at 18 containers and queues behind other jobs. Heart and DNA production use the CPU function (32 CPU cores, 16 GiB, CPU OpenImageDenoise); a production autoscaler override permits 24 CPU workers. The CPU decorator defaults to eight workers for a smaller rerun.

## Budget and limitations

The dispatch controller conservatively reserves at most USD 135 per video for one complete rendering pass, leaving headroom within the brief's approximately USD 150 per video limit. For the delivered edit with 240-frame chunks, the reservations are $134.96 (cell), $79.57 (heart) and $78.03 (DNA). These are ceilings rather than predicted bills. A lower-priced fallback receives more wall time within the same dollar reservation. The controller will not automatically rerender failed work. Review measured costs and reservations before repairs. Reports estimate resource cost from measured runtime and published rates; the provider invoice remains the authority for actual billing, cold starts and account-specific credits.

## Verify and compare

```bash
python src/verify_media.py --masters masters --output contact-sheets
python src/compare.py --reference /path/to/owned-cell-reference.mp4 --master masters/cell.mp4 --output comparison --video
```

The complete comparison video uses the macOS `h264_videotoolbox` encoder. On another platform, replace that encoder with `libx264` and a suitable preset; the comparison sheets are portable. All comparison timestamps are explicitly listed in `src/compare.py`.

The models are educational representations with deliberately expanded microscopic detail, shortened process times and nonliteral scale. The heart is a procedural anatomical schematic, not patient imaging. Molecular meshes are not atomic-coordinate reconstructions. Review the final deviations report for the exact extent of reference matching and scientific annotations. No claim of pixel-identical reconstruction is implied by a matching output duration.
