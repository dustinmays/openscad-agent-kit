---
name: device-reference-model
description: Use when a design must fit or hold a real object (a device, tool, fixture) and you need an OpenSCAD model of that object built only from the measurement table, plus a script that checks the model's meshes against the table.
---

# Device reference model

Model the real object the design must fit, so fits and clearances can be
checked against something better than memory. The reference model is never
printed. It is built **only** from [MEASUREMENTS.md](../environment-reference/SKILL.md)
values, and a script proves the meshes match the table.

Worked example: [keypad-reference.scad](../../examples/keypad-sculpture/keypad-reference.scad)
and [check_keypad.py](../../examples/keypad-sculpture/check_keypad.py), which
compares the exported meshes with the body and button rows of the
[keypad table](../../examples/keypad-sculpture/MEASUREMENTS.md).

## Build the model

1. Use the table's coordinate frame, and say it in the file header with one
   worked example ("button 1 centre = (9.7, 9.7) from the upper-left corner").
2. Put every dimension in a parameter block at the top, each with a comment
   naming its table row (`body_w = 34.5;  // K1`). `assumed` rows get a
   comment saying so.
3. Give each part a selector (`part = "body" | "buttons" | "led"`) so the
   check and the renders can export them separately.
4. Provide a placement module (for example `keypad_in_elevation()`) that the
   design files `use`, so the design and its check share one position.
5. Keep a revision number, and say which table revision it uses.

## Check it against the table

Write `check_<object>.py` in the project. It:
- exports each part with `bin/openscad` to OFF;
- reads the meshes (use `read_off` from [bin/render-views.py](../../bin/render-views.py));
- measures what the table states: bounding sizes, hole or button centres from
  vertex rings, corner radii, depths;
- compares each with the table value, within a stated tolerance (0.05 mm
  works for modeled values);
- writes a JSON report with one boolean per check, and exits non-zero on any
  failure;
- renders the model from the front and the side, and overlays it on the
  blockout, so the user can compare it with a photo.

Take measured and reported values from the table (or a copy in the script
that names the table revision), not from the `.scad` file being checked.
Only `assumed` values may be read from the source, and the report should say so.

## Use it

- Use the reference model in the design's geometry check: "shell versus
  keypad" must not collide, and a slightly grown keypad should (that is the
  positive control). See [check-scad-geometry](../check-scad-geometry/SKILL.md).
- When a coupon print shows a measurement was wrong (the keypad example's
  LED hole was 1 mm off), add a corrected row to the table, update the model,
  and re-run the check.
