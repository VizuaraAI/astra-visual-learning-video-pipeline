# Visual Learning: reference analysis and production plan

## Evidence

Inspected both supplied MP4s, a 30-second overview of each, the complete cell video sampled every five seconds, its Hindi caption track, and its audio. Cell source: 891.083333 s / 24 fps / 1280×720. Chemistry source: 792.208333 s / 24 fps / 640×360. Published cell source: https://www.youtube.com/watch?v=n3x7gczAISE . Caption provenance: YouTube `hi-orig` JSON3 retrieved with yt-dlp. These are automatic captions and contain recognition errors; preserve the original audio for exact words and pauses.

## House language

The chapter opens with a purple title and a blue translucent topic/timeline panel. It establishes the whole model, identifies a component, moves closer, shows an action, pauses, and returns to the whole. English terms stay on screen while the Hindi teacher explains them. The register is direct: “आइए…”, “एनिमेशन में हम देखते हैं…”, “इसे…कहा जाता है.” It favors an observable sequence and a definition over dramatic rhetoric.

Objects occupy an almost black charcoal stage. Biology largely floats without a floor; chemistry sometimes uses a lit wood laboratory surface. Key lighting is broad and frontal with comparatively restrained shadows. Cell membranes are ochre, cytoplasm pale blue, nuclei violet, rough ER rose, smooth ER and Golgi orange, mitochondria cream/green, plastids green. Small reflective/specular features establish depth, though the source meshes are visibly low resolution.

The interface uses white sans-serif type, teal outlined skewed section tags, navy translucent pointed organelle labels, thin arrows, and red framed function panels. The gold diamond channel mark sits at the upper right. Labels are scene anchored in the organelle tour and screen anchored for definitions. Camera motion is mainly slow orbit, push, pull and pan. Objects open or peel apart to reveal structure; particles explain passage through a membrane. Cuts and fades introduce new concepts, while patient holds leave time to inspect.

The narration is a female Hindi teaching voice with English science terms. There is no continuous music bed in the inspected passages. A silence detector at −40 dB with a 150 ms minimum finds 293 pauses in the cell master, median 0.310 s, totaling 290.886 s; this includes short internal pauses, longer visual holds and the ending. The original track will be reused for the recreation. Original chapters use Anika—Engaging Teacher, ElevenLabs multilingual v2, `hi`, with deliberate inter-shot holds and no music.

## Rebuild direction

Keep the dark stage, original cell chapter order, audio duration, main cue times, palette families, chapter panels and label grammar. Rebuild geometry procedurally: double membranes, layered organelle cutaways, dense chromatin, ribosomes, folded cisternae, cristae, grana, vessels, valve leaflets and molecular structures. Add restrained subsurface response, microtexture, polished edges and warm/cool separation. Limit depth of field so the scientific subject stays readable. Movement must reveal a structure or process rather than merely rotate a decorative model.

The heart chapter follows a red blood cell through the right heart, lungs, left heart and body. It then explains valves, pressure, the heartbeat, vessels, capillary exchange and double circulation. A small persistent legend distinguishes oxygen-rich and oxygen-poor blood; blue is a diagram convention, actual blood is red. The cutaway places anatomical right on screen left in the frontal view. The left ventricular wall is thicker. Flow paths connect the correct chambers and valves.

The DNA chapter travels from the nucleus to a helix, a gene, transcription, RNA processing and export, then into a ribosome. It shows complementary bases, antiparallel strands, 5′→3′ synthesis, codons, tRNA, peptide bonds and protein folding. The example coding sequence is ATG GCT TTT GAA TGA, yielding AUG GCU UUU GAA UGA and Met–Ala–Phe–Glu–Stop. Models are pedagogical molecular representations, not atomic-coordinate reconstructions; scale and time are intentionally compressed.

## Science reconciliation

The requirement to retain the exact reference script conflicts with correcting errors in that script. Preserve its audio and caption archive, and give visible corrections at the relevant times: membrane selectivity is not a blanket ban on external material; ribosomes/RER make proteins while SER makes lipids; ER–Golgi transport uses vesicles; chloroplasts and chromoplasts are distinct plastid types; prokaryotes have a nucleoid rather than a nucleus without a membrane; cytoplasm is a cell region, not a membrane. Include these departures in the final report. Source spelling and automatic-caption errors must not propagate into new English labels.

## Execution and checkpoints

1. Local manifest, Hindi scripts, exact reference caption archive and reproducible asset builders.
2. Local test frame for every planned shot; contact sheets checked for framing, readability and geometry. Show these before paid rendering or speech generation.
3. Deploy only the unique `vl-execu-20260905` Modal app and `vl-execu-20260905-data` volume. Run a small GPU benchmark, inspect its output and estimate total cost before batches.
4. Render resumable scene chunks with CPU compositing and OpenImageDenoise. Commit each completed chunk to the volume; use durable deployed function calls and inspect volume contents as the source of progress truth. Limit our GPU concurrency so other work can continue.
5. Produce H.264/AAC 1920×1080 24 fps masters, contact sheets and a time-aligned side-by-side. Inspect sampled frames and validate stream specs, durations, audio and joins.

## Source references

- NCERT Life Processes: https://ncert.nic.in/textbook/pdf/jesc105.pdf
- NCERT Molecular Basis of Inheritance: https://ncert.nic.in/textbook/pdf/lebo105.pdf
- NIH/NHLBI blood-flow and chamber/valve topology: https://www.nhlbi.nih.gov/health/heart/blood-flow
- NIH/NHLBI cardiac conduction: https://www.nhlbi.nih.gov/health/heart/heart-beats
- NHGRI transcription: https://www.genome.gov/genetics-glossary/Transcription
- NHGRI RNA and RNA processing: https://www.genome.gov/about-genomics/educational-resources/fact-sheets/ribonucleic-acid-fact-sheet
- NHGRI codons: https://www.genome.gov/genetics-glossary/Codon
- NHGRI translation: https://www.genome.gov/genetics-glossary/Translation
- NHGRI tRNA: https://www.genome.gov/genetics-glossary/Transfer-RNA-tRNA
- Blender 5.2.1: https://www.blender.org/releases/5-2/
- Modal durable function execution: https://modal.com/docs/guide/functions
- Modal resource rates: https://modal.com/pricing
