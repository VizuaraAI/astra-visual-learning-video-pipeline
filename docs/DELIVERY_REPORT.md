# Delivery report

Three masters were generated at native **1920×1080, 24 fps, H.264 with 48 kHz AAC narration**. No music was added. Automated checks passed for resolution, codecs, frame rate, exact frame count, duration, audio coverage/sample rate, full-file decoding and absence of sustained black frames. Timestamped contact sheets and the original/recreation comparison accompany the videos.

| Video | Duration | Frames | Measured render estimate |
|---|---:|---:|---:|
| The Fundamental Unit of Life | 14:51.08 | 21,386 | $16.52 |
| Human Heart and Circulation | 8:00.33 | 11,528 | $26.91 |
| DNA: From Gene to Protein | 8:00.50 | 11,532 | $6.73 |

## Cost

Total estimated worker resource cost with completed runtime records is **$50.15**. This includes all retained benchmarks, the superseded partial CPU heart pass, recorded unsuccessful attempts and the final production passes. Estimates multiply each worker's measured runtime by the published GPU, CPU and memory rates. They are **not a verified Modal invoice**. Canceled in-flight workers may not have written completion metrics, so their usage is captured by the provider snapshots below rather than this runtime estimate. Build/startup time, brief container idling, final assembly, storage and account credits can also change the billed amount. The detailed ledger is in `visual-learning-pipeline/tests/production-cost-records.json`.

The cell chapter was rendered in `vizuaraai`; the final heart and DNA chapters were rendered in the explicitly authorized `rajatdandekar` workspace. Its billing API confirmed an existing **$250 monthly plan charge** before rendering. That fixed plan charge is separate from this production's metered compute. The cell pass used 48 samples; the final originals use 128 samples with a stricter adaptive threshold. Superseded CPU outputs are excluded from the final masters. Three heart shots were then rerendered to align blood-cell transit with fully open valves; both the replaced chunks and the correction pass are counted in the cost audit.

ElevenLabs consumed **25,375 requested text characters** across both the discarded longer drafts and final scripts. The last subscription check reported zero current overage; existing plan credits were used. No per-request cash invoice was available. Reusing the bundled final FLAC tracks requires no new speech generation.

## Material deviations

- **Reference matching is interpretive.** The cell chapter retains the original audio, overall frame count and broad teaching progression. Its procedural models, camera paths, cuts, interface layout and some actions differ from the source. The reference supplies flattened pictures rather than its editable scene files, and the rebuild uses newly authored procedural scenes and a newly drawn interface. It is not a frame-identical recreation. The comparison shows both versions at the same timestamps.
- **Source science versus source fidelity.** The cell source narration contains scientific errors. It is retained to preserve the requested performance, while visible labels correct protein/lipid synthesis, selective transport, ER–Golgi vesicles, plastids, the nucleoid and cytoplasm/cytosol distinctions. The retained spoken source therefore is not fully scientifically corrected.
- **Model scope.** Assets are original 3D educational schematics. Heart anatomy is not patient imaging; molecular shapes are not atomic-coordinate reconstructions. Some inspection shots use camera movement around repeated assets, and several complex source actions are simplified.
- **Voice timing.** Final speech is generated from newly written Hindi scripts with English terms. Pitch-preserving tempo adjustment is 1.1887× for heart and 1.2525× for DNA to fit approximately eight minutes. Audio signal checks passed; the execution environment did not support a listening review.
- **Local environment.** The actual machine was an M1 Mac with 8 GB RAM. All 131 local composition test frames were shown before cloud spending, at reduced preview resolution. The final frames were rendered in the cloud at native full HD.

## Reproducibility

The repository contains original geometry generators, deterministic animation, final shot manifests, Hindi scripts and aligned subtitles, the final lossless narration, owned source audio, the interface/font assets, durable Modal dispatch/assembly tools and production checksums. Follow `visual-learning-pipeline/README.md`. Do not regenerate the placeholder manifests over the locked final timings.

Pricing reference: [Modal resource pricing](https://modal.com/pricing). Scientific references and full provenance are in the repository's `docs/STYLE_ANALYSIS.md` and `docs/PROVENANCE.md`.

**Provider-reported cloud usage for this production: $59.34**, across its isolated apps in both workspaces. Snapshots include the current UTC hour provisionally and were fetched between 2026-09-05T10:42:59.113471+00:00 and 2026-09-05T10:44:59.725140+00:00. They include metered usage from canceled workers. Account plan credits and the fixed subscription fee are not allocated to individual apps. Metering can settle later; this is provider usage as of retrieval, not a final invoice.
