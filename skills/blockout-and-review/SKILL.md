---
name: blockout-and-review
description: Use to turn a sketch, photo or brief into a rough OpenSCAD blockout of simple solids, render same-camera review views and side-by-side comparison boards from the real meshes, and record which variant the user picked. Use before any detailed or printable modeling, and for every big shape change.
---

# Blockout and review

A **blockout** is a deliberately rough model from simple solids (cubes,
cylinders, hulls, extruded outlines) that shows size, proportion and
placement. It lets the user judge the composition in minutes, before any
time goes into fillets, holes or fits.

Guide for people: [guides/03-blockouts.md](../../guides/03-blockouts.md).
Worked example: [blockout.scad](../../examples/keypad-sculpture/blockout.scad)
with [render_blockout.py](../../examples/keypad-sculpture/render_blockout.py),
and the variant board from [render_rib_variants.py](../../examples/keypad-sculpture/render_rib_variants.py).

## From sketch or photo to blockout

1. **Find the scale.** Use a dimension written on the sketch or a known
   object in the photo. Write the scale you found (for example "10.1 px/mm,
   checked against the 85 and 130 mm marks") in `DESIGN.md`.
2. **Trace the main outlines** into points, in millimetres, in one stated
   frame (for example "front elevation: X right, Y up, origin at the
   lower-left corner"). Put every traced number in the parameter block at
   the top of the `.scad` file, so the user can ask for "8 mm narrower".
3. **One solid per visual element**, each selectable with a `part`
   parameter, and each in its own colour in the renders. Include a plain
   stand-in for the real object (or the reference model) to judge scale.
4. **Record what is traced and what is assumed.** Depths and anything the
   sketch does not show are placeholders; list them in `DESIGN.md`.
5. Keep a revision number near the top (`blockout_revision = 1;`).

Do not add holes, fillets, fits, print poses or tolerances yet.

## Review views

- Export each part with `bin/openscad` to OFF or STL and render with
  [bin/render-views.py](../../bin/render-views.py), so the picture shows the
  real mesh. Write a small `render_blockout.py` in the project, modeled on the
  example's.
- Use a fixed camera set, the same for every revision and variant: the main
  view the design is judged from (for a wall piece, the straight-on front),
  then 30° and 60° obliques and a side view.
- Name files with the revision: `renders/blockout-v2/front-v2.png`. Keep old
  revisions.

## Variants and comparison boards

When there is a real choice, make 2–4 variants in the same file, selected by
a parameter (`variant = "A";`). Render each with the same cameras, then paste
the views into one board, one row per variant, labelled with a letter and a
few words ("C: directional bow wave"). Pillow's `Image.paste` is enough; the
example's `compare_sheet()` shows how.

Give the user one line per variant: what differs and the main trade-off.
Then **stop and wait for the pick.**

## Recording the pick

- In `DESIGN.md`, under a dated decisions list: the pick, the user's exact
  words in quotes, and what it means for the model.
- Bump the revision when you apply their changes. The renders of earlier
  revisions stay as they are.
- In `status.md`: the current revision and the next step.

Before you show any render, open it yourself and check that it shows what the
caption says. Variants must look visibly different.
