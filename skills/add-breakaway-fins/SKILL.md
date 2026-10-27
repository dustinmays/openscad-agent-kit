---
name: add-breakaway-fins
description: Assess and add sacrificial fins and small breakaway tabs that steady tall or narrow OpenSCAD prints on the bed. Use for removable print braces and their feasibility; not for permanent structural ribs.
---

# Add breakaway fins

Create a removable print aid that braces a tall part and widens its bed
contact, while keeping the finished part's mating surfaces intact. Keep the
ordinary model and export, and make the braced version an explicit extra.

## Think about feasibility first

Before modeling, ask: **will fins remove the need for supports, or only
steady the part?** Look for floating islands, projecting features and
overhangs in the print orientation; bracing the main body does not support
those. Compare with ordinary slicer supports or a simpler orientation. If
fins cannot reasonably reach the user's goal, say so early.

## Design the connection, not just the triangle

Read the project's design notes and the actual model first. Work in its print
orientation, with the bed at Z = 0.

- Extend a triangular fin from a bed-side leg up to a high attachment area.
  A triangle that narrows upward grows straight from the bed without support.
- Leave an air gap between the fin's vertical edge and the part. Connect
  through a few short, isolated tabs rather than welding the whole edge.
- Keep overlaps shallow and additive; do not cut notches into the part.
- A thin foot improves the fin's own bed grip. On curved faces, check the
  foot's corners as well as the fin's centre line.
- Size the fin and tabs for the user's nozzle (see `my-printer.md`). With a
  0.4 mm nozzle, start with a 0.8 mm fin (two lines), a 0.4 mm gap, tabs about
  0.5 × 0.4 mm, and a foot 8 × 0.4 mm. These are starting values. A feature
  narrower than one line may vanish from the slicer's toolpaths.
- Prefer a few more, smaller contacts over a few large ones; five small tabs
  release more cleanly than three big ones.

## Editable helper

Use [lib/breakaway-fin.scad](../../lib/breakaway-fin.scad) with
`use <../../lib/breakaway-fin.scad>`. Its local axes are X across the thin
fin, +Y toward the part's attachment face, and Z up from the bed. `face_y` is
the local face position; transform the whole helper for another orientation.
The defaults in the file are the original example's values; pass your own
`fin_thickness`, `gap` and tab settings.

- `breakaway_fin_core()`: the triangle and foot without contacts.
- `breakaway_fin_tabs()`: the contacts alone, for inspection.
- `breakaway_fin()`: the whole sacrificial support.

Union it with the part only in a print-only selector.

## Verify in proportion

- Run `bin/print-check.py` on the braced STL. Look at the footprint, the air
  gap, the contacts and the removal access in actual-mesh renders. When
  clearance is uncertain, intersect the core with the part: only the tabs
  should touch.
- Do not claim support-free printing because slicing succeeded with supports
  off. Say which overhangs still need support and what was actually tested.

In the print sheet: remove **the whole fin and foot before assembly**, clip
stubborn tabs rather than forcing the part, and sand the nubs. Say whether a
slicer preview and a physical breakaway test were done.
