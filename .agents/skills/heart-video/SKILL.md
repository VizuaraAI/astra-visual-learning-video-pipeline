---
name: heart-video
description: Create or revise the Heart visual-learning chapter while preserving synchronized contraction, valve motion, blood-marker transit, narration, and verified cardiac timing.
---

# Heart video

Treat `storyboards/heart.json` as authoritative. Use `src/heart_assets.py` for anatomy and `src/cardiac_motion.py` for synchronized motion.

Preserve the 72 bpm shared cardiac phase unless the user explicitly requests a new teaching cadence. AV and semilunar valve opening windows must not overlap. Blood markers may cross a valve plane only while that valve is visibly open.

Run `blender -b --factory-startup -t 2 --python tests/check_valve_transit.py` after changes to valves, markers, timing, or heart geometry. Preview affected shots before any cloud rerender.

Describe the heart as a procedural educational schematic, not patient imaging or a pressure/flow simulation.

## Learned corrections

Add concrete visual corrections from creator review here. Include the shot number when a rule is not universal.
