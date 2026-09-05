# Assets, narration and scientific interpretation

All cell, heart and molecular meshes are original procedural constructions in `src/geometry.py`, `src/assets.py`, `src/heart_assets.py` and `src/dna_assets.py`. They are educational diagrams rendered in three dimensions. No purchased models, patient scans, atomic-coordinate databases, historical portrait photographs or stock music are included.

The bundled Barlow fonts are distributed under the included SIL Open Font License. The palette, labels, lighting and framing interpret the visual language of the user's two supplied reference videos. The small VL diamond is a newly drawn mark.

## Source material supplied by the user

- **The Fundamental Unit of Life**, 720p MP4, 891.083333 seconds. This supplies the recreation's original narration, broad sequence and timing. Its AAC audio is preserved in `assets/cell-reference-audio.m4a`. The user supplied it as their owned reference.
- **Chemical Reactions and Equations**, 360p MP4, 792.208333 seconds. This supplies additional style observations only. Its picture and audio are not embedded in the new chapters.
- Automatic Hindi captions for the cell reference are archived unmodified in `scripts/cell-reference.hi.json3`, with a readable timing transcription alongside it. Automatic recognition errors remain in this archive. The audio itself, rather than an edited transcript, is used in the recreation.

## Original narration

The heart and DNA scripts were newly written in Hindi with English scientific vocabulary. Speech was generated using ElevenLabs `eleven_multilingual_v2`, the supplied Anika voice (`9FTUWXd0yHJL1ZiZ71RK`), and Hindi language mode. No cloning was performed. Acronyms and teaching codons were expanded into Hindi letter pronunciation for synthesis.

The delivered edit uses pitch-preserving tempo adjustment of 1.18871386× for heart and 1.25246096× for DNA. The final tracks are preserved losslessly in `assets/narration/*.flac`, so reproducing these edits does not require another paid speech request. Alignment-based Hindi SRT files accompany the original scripts. The initial longer speech drafts are not delivered but their consumption is counted in the cost report.

Automated audio checks measured approximately −16.4 LUFS for heart and −16.3 LUFS for DNA, with −1.5 dBFS true peaks. The execution environment did not support model audio playback, so no human listening review or pronunciation certification is claimed.

## Scientific scope

The primary educational references and correction decisions are listed in `STYLE_ANALYSIS.md`. The models simplify scale, timing and molecular detail. Heart chamber and vessel forms are schematic; the helix and ribosome are illustrative meshes rather than atomic reconstructions.

The cell recreation retains the source narration, including its errors, to preserve the requested source performance. Visible labels correct the distinction between ribosome/RER protein synthesis and SER lipid synthesis, selective membrane transport, vesicular ER–Golgi transport, plastid categories, the prokaryotic nucleoid, the cytoplasm/cytosol distinction and energy transfer. This reconciles part of the accuracy request but does not make the retained spoken source error-free.

The recreation matches overall duration and broad teaching progression. It does not reproduce every source cut, camera movement, label placement or model action exactly. The comparison deliverable makes these differences visible at matching timestamps.
