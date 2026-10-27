# Agent instructions

This repository is a kit for designing 3D-printed parts in OpenSCAD with an
agent (Claude Code or Codex). The user may not be a programmer. Speak plainly,
ask one short batch of questions at a time, explain any term you must use,
and never assume they know Git, Python or OpenSCAD.

## Before printable work: the printer

At the start of every new project, open `my-printer.md` first. If it still
says `Status: template`, your first message to the user asks only the
printer questions, before any design question: printer model, bed size,
nozzle diameter and material. Do not mix design questions into that message;
ask them in the next one, after you record the answers in `my-printer.md` and
set `Status: filled in`. If the user does not know a value, keep the default
and tell them: 0.4 mm nozzle, PLA or PETG, 0.2 mm layers. No fits, print
poses or STL exports happen before the printer is recorded.

## How a design goes

Follow the process in `guides/`, using the matching skill at each step:

1. Start a project: `start-a-project`. One folder per design under `initiatives/<name>/`.
2. Measure the real object: `environment-reference`, then `device-reference-model`.
3. Blockout and pick: `blockout-and-review`. Stop and wait for the user's pick.
4. Fit coupons for uncertain fits: `fit-coupons`.
5. Printable parts with checks: `design-for-printability`, `check-scad-geometry`,
   and `add-pin-joints` or `add-breakaway-fins` when needed.
6. Print sheet: `print-handoff` writes `PRINT.md`.
7. Results: record the user's report in `observations.md` (`print-handoff`).

The worked example is `examples/keypad-sculpture/`; read its `STORY.md` once
to see the whole process. Do not copy its numbers into a new design. They
came from the author's printer and object.

## Skills

Skills live in `skills/<name>/SKILL.md`. This is the only copy.
`.claude/skills` (Claude Code) and `.agents/skills` (Codex) are symlinks to it.
Never copy a skill into those folders; edit `skills/` instead. Optional skills:
`study-support-fins-orientations` (needs Node, only for that study), and the
multi-agent skills `work-item`, `handoff-implementer`, `discovery` (see
`guides/runbook-multi-agent.md`). A normal design needs none of them.

## Tools

Run everything from the kit root.

- `bin/openscad`: OpenSCAD snapshot with the Manifold backend. Always use it,
  not another OpenSCAD.
- `bin/python`: Python with numpy and Pillow (the `.venv` from `bin/setup`).
- `bin/doctor`: checks the setup; run it first if a tool fails.
- `bin/render-views.py`: renders PNG views from real OFF/STL meshes.
- `bin/print-check.py`: the pre-print mesh check (one body, flat on the bed,
  inside the bed from `my-printer.md`, overhangs). Run it on every STL before
  telling the user it is ready to print.
- `bin/scad-geometry-check.py`: repeatable export and collision checks from a
  JSON config (`check-scad-geometry`).

Manifold rules: overlap solids that should fuse by a small `eps` (touching
faces stay separate bodies), and export print STLs as ASCII
(`--export-format asciistl`). See `docs/MANIFOLD.md`.

## Modeling rules

- Keep meaningful parameters near the top of each `.scad` file, with units,
  axes and assumptions in comments or the project's `DESIGN.md`.
- Keep a revision number near the parameters (`parts_revision = 2;`). Name
  every export, render and report with it (`bracket-v2.stl`,
  `print-check-v2.json`). Increment it when geometry or fit values change;
  keep earlier revisions.
- Exports go in `initiatives/<name>/exports/<purpose>-v<N>/`, images in
  `renders/<purpose>-v<N>/`. They are regenerated, not stored in Git.
- After any geometry change, regenerate the outputs and **look at the actual
  meshes**. A successful export proves only that a file was written. Open
  each render you show the user and confirm it shows what you say it shows.
- Fit clearances are starting values until the user's own coupon print
  confirms them. Say so.

## Records

Each project folder follows `skills/project-operating-model`:

- `status.md` is the current snapshot; rewrite it.
- `log.md` is append-only history.
- `observations.md` is append-only: the user's own words about prints and fits.
- `MEASUREMENTS.md` is the measurement table; once it is `complete`, change
  it only with the user's approval.

Keep evidence kinds apart: measured, reported by the user, assumed, checked
on the mesh, seen in the slicer, and printed. Never present an assumption or
a mesh check as a print result. Update `PROJECT_STATE.md` when a project
starts, pauses or finishes.

## Git

Photos, renders, meshes and print files stay out of Git (see `.gitignore`).
Do not force-add them. Commit only when the user asks.
