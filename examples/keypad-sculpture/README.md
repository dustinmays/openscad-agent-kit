# Worked example: keypad sculpture

A wall sculpture that holds a real door-lock keypad (a Wyze keypad). It has a
yellow rib field that goes on the door, a black shell that the keypad
pushes into, and a soft blue drape glued to the shell. The author designed it
with an agent using this kit's process, printed it and assembled it.

Every guide in [`guides/`](../../guides/) points to one step of this example.
[STORY.md](STORY.md) tells the whole process in order, in plain English.

## What is here

| File | What it is | Process step |
| --- | --- | --- |
| [BRIEF.md](BRIEF.md) | The original brief, from a hand sketch | [Start](../../guides/01-start-a-project.md) |
| `reference/` | The sketch and keypad photos | [Start](../../guides/01-start-a-project.md) |
| [MEASUREMENTS.md](MEASUREMENTS.md) | Measurement table of the real keypad | [Measure](../../guides/02-measure.md) |
| [keypad-reference.scad](keypad-reference.scad), [check_keypad.py](check_keypad.py) | Model of the real keypad, checked against the table | [Measure](../../guides/02-measure.md) |
| [blockout.scad](blockout.scad), [render_blockout.py](render_blockout.py) | Rough block model from the sketch, with review views | [Blockouts](../../guides/03-blockouts.md) |
| [ribs-blockout.scad](ribs-blockout.scad), [render_rib_variants.py](render_rib_variants.py) | Variants side by side, for picking one | [Blockouts](../../guides/03-blockouts.md) |
| [parts-blockout.scad](parts-blockout.scad), [coupons.py](coupons.py) | Part split and the fit coupons cut from it | [Fit coupons](../../guides/04-fit-coupons.md) |
| [keypad-parts.scad](keypad-parts.scad), [build_parts.py](build_parts.py) | The printable parts | [Printable parts](../../guides/05-printable-parts.md) |
| [geometry-check-config-v1.json](geometry-check-config-v1.json), [check_parts.py](check_parts.py) | Geometry checks: fits and clearances | [Printable parts](../../guides/05-printable-parts.md) |
| [PRINT.md](PRINT.md) | Print and assembly sheet | [Print handoff](../../guides/06-print-handoff.md) |
| [observations.md](observations.md) | What the author reported after printing | [Report results](../../guides/07-report-results.md) |
| [DESIGN.md](DESIGN.md) | Axes, assumptions and every design decision, with quotes | all steps |

The example was printed on the author's printer in ASA (example only). Values
that came from that print are labelled as such. Your printer's values come
from [my-printer.md](../../my-printer.md) and from your own coupons.

## Regenerate

Run these from the kit root (the folder with `README.md` and `bin/`). They
make the meshes in `exports/` and the pictures in `renders/`. All of them
together take about a minute.

```sh
bin/python examples/keypad-sculpture/render_blockout.py
bin/python examples/keypad-sculpture/render_rib_variants.py
bin/python examples/keypad-sculpture/check_keypad.py
bin/python examples/keypad-sculpture/coupons.py
bin/python bin/scad-geometry-check.py examples/keypad-sculpture/geometry-check-config-v1.json
bin/python examples/keypad-sculpture/build_parts.py
bin/python bin/print-check.py examples/keypad-sculpture/exports/coupons-v4/*.stl examples/keypad-sculpture/exports/parts-v1/*.stl --report examples/keypad-sculpture/exports/parts-v1/print-check-v1.json
```

What each line does:

1. Blockout views: `renders/blockout-v3/`, five views of the block model.
2. Rib-field variants and the side-by-side board: `renders/ribs-blockout-v4/compare-v4.png`.
3. The keypad model, checked against `MEASUREMENTS.md`: `renders/keypad-reference-v3/`.
4. Fit coupons as STL, with views: `exports/coupons-v4/`, `renders/coupons-v4/`.
5. Geometry check: 16 clearance and collision cases, plus 8 measurements on the
   meshes. It writes `exports/parts-v1/checks/geometry-check-v1.json`.
6. The three printable parts as STL in print pose, with assembled, exploded
   and print-pose views: `exports/parts-v1/`, `renders/parts-v1/`.
7. The pre-print check on every STL, against the bed in `my-printer.md`.

`exports/` and `renders/` are not kept in Git (they change on every run),
so a fresh copy of the kit has none until you run these. Run them in this
order: `build_parts.py` needs the geometry check's meshes.

Look at the pictures after you regenerate. A command that succeeds only proves
that a file was written. The pictures show whether the shape is right.
