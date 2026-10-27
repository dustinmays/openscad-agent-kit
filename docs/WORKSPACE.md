# Workspace conventions

How files are organised, so any agent (or you, later) can find things.

## Layout

| Folder | Holds |
| --- | --- |
| `initiatives/<name>/` | One design project: sources, notes, measurements |
| `examples/` | The worked example, read-only in spirit |
| `skills/` | Agent instructions; the only copy (`.claude/skills` and `.agents/skills` link here) |
| `guides/` | Plain-English guides for people |
| `docs/` | Reference that applies to every project |
| `lib/` | Reusable OpenSCAD libraries |
| `bin/` | Tools; run them from the kit root |

Inside a project:

- `*.scad` and `*.py` sources and the notes (`README.md`, `status.md`,
  `log.md`, `DESIGN.md`, `MEASUREMENTS.md`, `PRINT.md`, `observations.md`)
  sit at the top of the project folder.
- `reference/`: photos and sketches.
- `exports/<purpose>-v<N>/`: STL and OFF files and the JSON check reports.
- `renders/<purpose>-v<N>/`: PNG pictures.
- `work/`: work items, only if you use the optional multi-agent runbook.

Group generated files by purpose (`exports/coupons-v2/`, `exports/parts-v3/`,
`renders/blockout-v1/`).

## Revisions

- Each `.scad` source keeps a revision number near its parameters
  (`parts_revision = 3;`). Scripts read it and put `-v3` in every file
  they write.
- Increment it when geometry or fit values change. Keep the old outputs.
- `PRINT.md` names the current revision's files explicitly.
- The editable source file name stays the same across revisions.

## Running tools

Commands in notes and guides run **from the kit root**:

```sh
bin/python examples/keypad-sculpture/build_parts.py
bin/python bin/print-check.py initiatives/my-part/exports/part-v1/*.stl
```

`bin/python` uses the `.venv` that `bin/setup` created, so numpy and Pillow
are always available. Each project's scripts find the kit root from their own
location and call `bin/openscad`, `bin/render-views.py` and
`bin/print-check.py` from there.

## Git

If you use Git (optional, but it keeps a safe history of your designs):

- Track `.scad`, `.py`, `.md` and small `.json` reports.
- Photos, renders, STL/OFF/3MF meshes and G-code are ignored by
  `.gitignore`. They are regenerated from the sources, or kept on your Mac.
  Don't force-add them.
- The worked example's reference photos are the one exception: they ship
  with the kit.

## Evidence

Every claim about a part is one of these. Label which one it is:

- **measured**: the user measured the real object;
- **reported**: the user said so;
- **assumed**: a placeholder awaiting confirmation;
- **checked on the mesh**: from `bin/print-check.py`, a geometry check or a render;
- **seen in the slicer**: from the slicer preview;
- **printed**: from a real print, in `observations.md`.

A mesh check does not prove a print, and a successful export does not
prove the shape is right.
