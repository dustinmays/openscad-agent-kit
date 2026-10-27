---
name: study-support-fins-orientations
description: Optional. Screen FDM print orientations of a long part with the Support Fins CLI (needs Node 20.10+ and a Support Fins checkout), balancing layer direction, bed size and removable support geometry. Never required for a normal design.
---

# Study Support Fins orientations (optional)

This is an optional add-on. A normal design never needs it: pick an
orientation with [design-for-printability](../design-for-printability/SKILL.md)
and check it with `bin/print-check.py`. Use this only for a long part where
a tilted pose might give better layer direction with modest supports, and only
if the user has Node and wants to try it.

The kit's [pose study script](../../bin/study-support-fins.py) runs the
[Support Fins](https://github.com/gittrahan/support-fins) command-line engine
over a grid of rotations and writes a 3MF per pose plus a JSON report. Treat
its ranking as a way to choose a few poses to inspect, not as a strength or
print recommendation.

## Set up the study (optional)

1. Check for Node 20.10 or newer (`node --version`). If it is missing, tell
   the user this tool is optional and offer to skip it. Do not install Node
   without asking.
2. The user downloads or clones Support Fins somewhere outside the kit; note
   the path of its CLI file (`plugins/cli/support-fins.js` in a checkout).
3. Export a **bare** ASCII STL of the part (no fins, no supports).
4. Read the bed size, nozzle and layer height from `my-printer.md`. Set
   `--critical-axis` to the direction the part must be strongest along, in
   the STL's coordinates.
5. Run `bin/python bin/study-support-fins.py --help`, then, for example:

   ```sh
   bin/python bin/study-support-fins.py initiatives/my-part/exports/part-v1.stl \
     --cli ~/support-fins/plugins/cli/support-fins.js \
     --output-dir initiatives/my-part/exports/orientation-study \
     --revision v1 --material PETG --critical-axis 0,0,1 \
     --build-volume 220,220,250 --layer-height 0.2 --gap 0.3
   ```

   Change `--revision` for each run; the script refuses to overwrite.

## Compare and inspect

- Filter out errors, floating parts, unsupported overhangs and poses that
  do not fit the bed. The rectangular bed check ignores unusable corners and
  brims.
- Compare the Pareto poses before trusting the weighted leader. Support
  volume is solid geometry, not filament or print time; the layer-direction
  score is a proxy, not a stress analysis.
- Open two or three finalists in the user's slicer with their real profile.
  Check first layers, thin supports and removal access. Compare with the
  simple flat or upright pose.

Record geometry results, slicer observations and print results separately.
