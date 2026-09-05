# Production notes

## 2026-09-05 — intake

- User authorized end-to-end execution of supplied brief, including cloud rendering up to approximately USD 150 per video. Show checkpoints without waiting for approval.
- Required masters: faithful 891.083333-second Class 9 cell chapter; original approximately eight-minute heart chapter; original approximately eight-minute DNA chapter. All 1920×1080, 24 fps, H.264/AAC; no music.
- Source assets remain in Downloads. Do not commit credentials or copy the credential-bearing brief into deliverables.
- Actual machine: macOS / M1, 8 GB RAM, 7-core integrated GPU, about 27 GiB available disk. Python 3.11.8, Blender 5.2.1, ffmpeg and ffprobe already installed. Isolated Python environment in work/.venv.
- Source cell video: 1280×720, 24 fps, H.264/AAC, 891.083333 s. Chemistry reference: 640×360, 24 fps, H.264/AAC, 792.208333 s.
- Stage: inspecting references and verifying read-only service access. No cloud compute or speech generation started.
- Safety of unrelated jobs: use unique production app/volume names; do not stop or change other Modal applications.

## Local production checkpoint

- Retrieved the source Hindi automatic captions with yt-dlp and archived them without alteration.
- Both supplied services authenticated successfully after stripping prose punctuation from credential fields. No credentials are stored in the repository.
- Authored 83 cell shots, 24 heart shots, 24 DNA shots. The originals contain 6,591 and 6,740 requested narration characters respectively.
- Built original geometry, interface and render scripts; local frames render successfully. Corrected sphere normals, heart cavities, capillary cutaway orientation and missing-font symbols during QA.
- Final local test pass is running in work/previews-final. Six heart-flow test frames will need refreshing for the latest camera push after that pass.
- Cloud app and speech scripts are prepared but have NOT been deployed or invoked. Cloud spend is still zero.

## Preview QA refinement

- All initial local frames completed. Final refresh now uses a fresh Blender process per shot to avoid memory accumulation on this machine.
- Refined heart valve leaflet motion with shape keys, added camera pushes along flow routes, enlarged cell organelle close-ups, and added RNA processing/export/translation movements.
- Active finishing coordinator: work/after_previews.py; read work/refresh-previews.log and work/after-previews.log. Gate completion file: work/local-previews-complete.json.
- After visual inspection, show all three contact sheets (cell includes four paged sheets) BEFORE deploying Modal or generating ElevenLabs speech. Then run a 48-frame benchmark each for cell shot 44, heart shot 2 and DNA shot 9 in run bench.
- Run authorized commands through work/run_authorized.py, which reads credentials from the supplied local brief without printing or storing them. No secrets appear in the delivered repository.
- No paid cloud activity has yet started. Source audio has been decoded locally to work/cell-original.wav.

## Local preview gate passed

- All 131 shot previews generated and visually inspected on six paged contact sheets. Most frames use 960×540 / 12 samples; the final expensive cell close-ups use 640×360 / 6 samples. These are local composition tests, not master render settings.
- Preview outputs and nonblank/dimension checks are saved under tests/.
- Next: show contact sheets in chat, deploy the isolated Modal app, run the small cloud benchmark, and generate the original narrations.

## Cloud/speech checkpoint started

- All test contact sheets were shown in chat before paid activity.
- Deploying the isolated Modal app; both original narration jobs are generating in parallel.
- Logs: work/modal-deploy.log, work/narration-heart.log, work/narration-dna.log. Narration cache: work/audio/.
- The full render has NOT been dispatched. Run and inspect the bench outputs first.

## Benchmarks and final audio edit

- Three 48-frame, native 1080p benchmarks completed successfully: cell 464.74 s / $0.293, heart 411.19 s / $0.259, DNA 519.10 s / $0.327 estimated resource use. Their full-HD representative frames were visually inspected.
- A second three-clip benchmark (`bench-gpu-denoise`) is queued with CUDA-accelerated OpenImageDenoise. The compositor remains disabled/CPU; OptiX is never used. This tests performance without changing sampling or geometry.
- Two speech passes were generated. The first scripts requested 13,681 total characters and were too long. Shortened final scripts requested 11,694 characters. Both passes consumed credits and must be included in the final cost report.
- Final audio uses pitch-preserving tempo correction: heart 1.18871386×, DNA 1.25246096×. Exact video durations are 480.333333 s and 480.5 s. Cell remains 891.083333 s.
- The active audio cache is `work/audio`; discarded speech is in `work/audio-long-draft`. Do not rerun `build_manifest.py` because that would reset final shot durations.
- The environment cannot play audio back to the model; speech timing/alignment and signal checks are possible, but do not claim a human listening review.
- `src/compare.py` is prepared to generate 20 matching-timestamp pairs, four comparison sheets and a complete side-by-side video after the cell master is downloaded.
- The full render is still pending the second benchmark. Use the deployed function and volume only; never change other Modal apps.

## Capacity troubleshooting / resume here

- The first three benchmarks are complete and shown, total estimated resource use $0.879. The second L40S-only tests remained pending with no assigned task ID; cancellation was requested only for those three calls. Modal still displays them as pending, so count any eventual artifacts if they run.
- New test run `bench-fallback` allows L40S, A10 or L4 and GPU-accelerated OpenImageDenoise. Calls are saved in work/bench-calls/bench-fallback-calls.json. No fallback result yet at this checkpoint.
- Modal reported 83 visible containers from other work and zero from our app. We have not stopped or changed any other app.
- A temporary autoscaler override was applied ONLY to our `render_chunk`: min_containers=1, max_containers=18, buffer_containers=0, scaledown_window=2. **Reset min_containers=0 after workers begin / before ending work** so an idle GPU is not retained.
- Final manifests/audio upload is running via work/final-upload.log. The full production dispatch has not occurred yet.
- Full pass reservations at 240-frame chunks: cell127chunks/$134.97, heart60chunks/$85.33, DNA69chunks/$83.83. Worker time scales by actual fallback GPU price while respecting the same reservation.
- src/monitor_production.py can automatically assemble and download each completed chapter after full dispatch. Run with --run v1 --cache work/production --masters outputs/masters. It does not dispatch renders or retry failures.
- Final packaging helpers: src/verify_media.py, src/compare.py, src/report.py. The report helper requires verified masters.

## Fresh production deployment

- Read-only Modal billing report confirms $0.89786051 for our first benchmark app during 08:00–09:00 UTC. Saved in work/modal-app-billing.json. The final report can include the provider's hourly usage report, which excludes an incomplete current hour.
- All later tests plus a two-frame direct probe remained unassigned. Stopped ONLY our idle app ap-O5BZDszAvBGXxHaP9alFNg (vl-execu-20260905), cancelling its pending work and clearing the temporary minimum-container override. The dedicated volume and successful tests remain.
- New production app: vl-execu-20260905-prod. Same dedicated volume, GPU fallbacks, native full HD/48samples; smaller reservations of 2 CPU cores and 8 GiB memory. This tests fresh scheduling without altering another app.
- New base rate estimate $0.00058596/s on L40S. Final budget reservations should be recalculated from current manage.py before dispatch.

## Confirmed GPU saturation; CPU tests running

- Read-only EnvironmentList reports 83 active tasks and 50 active GPUs, with no environment-specific concurrency cap and no spend limit reached. The 50 active GPUs match Modal Team's standard workspace GPU concurrency limit. Stop speculative redeployments: GPU capacity is occupied by other work.
- Current production app id ap-RvkiVA9OXXB5zfPoxrMqN8. GPU tests in bench-prod remain queued. The original app was successfully stopped with --yes; only our own app was affected. No min-container override remains active.
- Added render_chunk_cpu with 32 CPU cores, 16 GiB memory, max8workers. Same native 1080p/48sample Cycles art, CPU OpenImageDenoise. Resource rate estimate $0.00045472/s.
- Two CPU test calls are now actively running: heart shot2 and DNAshot9, first48frames, run bench-cpu. Calls work/bench-calls/bench-cpu-calls.json. Read results with manage.py status --run bench-cpu --cache work/bench-cpu-results --download.
- CPU dispatch is supported with manage.py dispatch ... --worker cpu. After inspecting benchmarks, use this for originals if measured projection fits budget. Cell can wait for GPU capacity or be CPU-tested if warranted.
- Full render is still NOT dispatched. Final manifests and all audio ARE uploaded. All local art, scripts, final narration and exact final timing remain ready.

## Original masters dispatched — active production

- Heart CPU benchmark: 48frames/314.12s/$0.14284 estimated. DNA CPU benchmark: 48frames/209.41s/$0.09522 estimated. Actual 1080p frames visually inspected and accepted; picture quality matches the original approved compositions.
- Both complete original chapters are being dispatched to CPU workers in run v1 (240-frame chunks). Heart60calls complete; DNA69calls follow in the same work/jobs/v1-calls.json ledger. Logs work/dispatch-heart.log and work/dispatch-dna.log.
- CPU autoscaler override max_containers=24, min_containers=0, buffer0. All24workers were observed active. This affects only our CPU function. Static source default is8; retain this override in reproducibility notes.
- Local assembly/download observer is running: work/production-monitor.log, work/production/production-state.json, outputs/masters. Source src/monitor_production.py. It must stay active through all three completed masters.
- Cell CPU test is separate run bench-cpu-cell, 12frames of expensive shot44. Await its measured cost before deciding CPU versus GPU. Cell full master has NOT been dispatched. GPU benchmark run bench-prod remains queued behind 50GPU use from other work.
- Do NOT rerun build_manifest.py or change the artwork during the full production pass.

## Cell device decision and automatic gate

- Cell CPU test completed: 12frames/407.50s/$0.18530. Its expensive close-up extrapolates far above the per-video cap, so cell will use the GPU backend. CPU tests are counted in spend despite being rejected for production.
- Automatic cell gate is running via src/dispatch_after_benchmark.py. Command: --chapter cell --benchmark bench-prod --cache work/bench-prod-results --jobs work/jobs. Log work/cell-dispatch-gate.log.
- Gate waits for the completed 48-frame GPU benchmark, verifies MP4 checksum, 1080p/24fps/48frames and a nonblank representative frame, checks full-length projection <=$135, then dispatches all127cellGPUchunks into the existing v1 ledger. It cannot exceed the controller's $134.96 reservation. If it fails, read its log and handle the concrete issue; do not assume cell is dispatched.
- Both original masters: all129calls have been dispatched successfully. 24CPUworkers active, early completed chunks saved with zero failures. Assembly/download observer remains active.
- Important active processes: production monitor (work/production-monitor.log) and cell gate (work/cell-dispatch-gate.log). No paid subscription or other app settings were changed.


## Additional workspace and final quality revision

The user supplied and explicitly authorized profile `rajatdandekar`, now verified and active. The billing API confirmed a USD 250 plan fee and zero month-to-date compute before this production. One pre-existing idle app (`example-commands`) was present and was left untouched. New isolated app `vl-execu-20260905-quality` and volume `vl-execu-20260905-quality-data` are deployed with up to 32 GPU workers. No credentials are stored in this repository.

The original workspace continues only the cell GPU pass (`v1`). Superseded heart/DNA CPU call cancellation was requested for the exact 129 IDs in the local dispatch ledger. Completed and canceled work must remain in the spend audit. A restarted observer downloads only the cell master, preventing old CPU outputs from overwriting the final originals.

Quality revision `quality-v2` uses 128 Cycles samples and adaptive threshold 0.02 for heart and DNA. Corrected cardiac motion shares a single phase between contraction and valve opening. The final timings and narration are unchanged. Dedicated 48-frame quality benchmarks precede the full pass. Checkpoint frames for all 131 compositions and earlier cloud tests were already completed before this revision.

After both quality benchmarks passed, the quality function autoscaler was raised from 32 to 48 GPU workers (min/buffer zero) to use the otherwise idle Team workspace. The source decorator remains configurable via `VL_GPU_WORKERS`; deployment defaults are documented.

All 21,386 cell frames completed without worker failure. Cell assembly completed and its 370,270,425-byte master downloaded with SHA-256 verification. All 11,532 DNA frames also completed; assembly is in progress. The local observer now catches the built-in TimeoutError returned by Modal polling, as well as the SDK-specific error; durable cloud calls were unaffected by its restart.

A final science-motion review found blood markers could cross closed valves. Heart shots 5, 10 and 13 (zero-based) were corrected: crossings are centered on the open phase, AV flow uses three spaced markers and valve-transiting discs remain flat. Blender geometry checks sampled ten seconds at 240 Hz and confirmed the valve was fully open for all 1,428 sampled transit intersections. A 128-sample repair pass runs in our separate `vl-execu-20260905-valve-fix` app, same quality volume, run `valve-repair`. A fresh combined run `quality-final` will reuse all unaffected chunks and replace only those shots. No old heart master is downloaded. Both base and replaced work remain in the cost audit.
