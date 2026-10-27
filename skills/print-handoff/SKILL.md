---
name: print-handoff
description: Use when printable parts are checked and ready for the user to print. Write the project's PRINT.md (files, slicer notes, assembly steps, what to report) from the template, then record what the user reports in observations.md and feed it back into the model.
---

# Print handoff

`PRINT.md` is the sheet the user follows at the printer and the workbench.
They should not need the chat history to use it. The loop closes when their
report lands in `observations.md` and changes the next revision.

Guides for people: [06 print handoff](../../guides/06-print-handoff.md) and
[07 reporting results](../../guides/07-report-results.md).
Worked example: the keypad [PRINT.md](../../examples/keypad-sculpture/PRINT.md)
and [observations.md](../../examples/keypad-sculpture/observations.md).

## Before writing it

- Every STL is exported as ASCII, in print pose, with the revision in its name.
- `bin/print-check.py` passes on every STL; save its report beside them
  (`--report exports/parts-v1/print-check-v1.json`).
- The geometry check passes, if the project has one.
- You opened the print-pose renders, including the view from below.

## Template

```markdown
# Print and assembly — <project> v<N>

Current revision: **v<N>** (`<source>.scad`, `<name>_revision = <N>`).
Printer and material: from my-printer.md (<model>, <nozzle> mm, <material>).

## Files
| Part | File | Size X × Y × Z (mm) | Qty | Pose on the bed |
|---|---|---|---|---|

Checks: `exports/<...>/print-check-v<N>.json` (PASS), renders in `renders/<...>/`.

## Slicer
- Layers, walls, infill: <values, and why if they matter>
- Supports: <none, or where and why>
- Brim: <which parts, how wide>
- Anything to look for in the preview: <thin features, bridges>

## Hardware and other parts
<magnets, screws, glue, with sizes and counts>

## Assembly
1. <dry-fit first>
2. <one action per step, in order>

## What to report back
- Did each part print cleanly? Any lifting, stringing or failed bridges?
- How did each fit feel: loose, right or tight?
- A photo of anything that looks wrong.

## Results
- <date>: <filled in after the print>
```

Write steps a beginner can follow: say which side faces up, what "snug"
should feel like, and when to stop and ask. Say plainly which settings are
untested assumptions.

## After the print

1. Copy the user's report into `observations.md` under a dated heading,
   quoting their words. Below it, list what it shows and what it does not
   (for example "door magnet hold not reported yet").
2. Add a one-line result under Results in `PRINT.md`.
3. Anything that changes geometry (a hole off by 1 mm, a fit too tight)
   goes into the model and `MEASUREMENTS.md`, with a revision bump and a
   new PRINT.md revision. Earlier revisions and their files stay.
4. Update `status.md`, and `PROJECT_STATE.md` if the project is finished.
