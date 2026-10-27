---
name: check-scad-geometry
description: Build and run repeatable OpenSCAD mesh and CSG intersection checks for a parametric part. Use when a design needs revisioned, machine-readable geometry or clearance evidence; physical fit and print approval remain separate.
---

# Check OpenSCAD geometry

Use the kit's [geometry checker](../../bin/scad-geometry-check.py) for
repeatable mesh exports and exact Boolean intersection cases. Keep the
physical dimensions, coordinate system, component modes and expected outcomes
beside the model. The [keypad example config](../../examples/keypad-sculpture/geometry-check-config-v1.json)
is a working example with 16 cases and a project check; it is not a source of
dimensions for other projects.

## Set up a project check

1. Give the SCAD source selectable modes for each component to inspect and
   each `intersection()` to test. An intersection mode must return only the
   overlap solid. Use a separate, nonprinting reference scene when useful.
2. Create a revisioned JSON config beside the model with `schema_version: 1`,
   `revision`, kit-relative `source` and `output_dir`, and a nonempty
   `exports` list of `{name, mode}` objects. Set `selector` if the source uses
   a parameter other than `mode`. List included SCAD files in `dependencies`
   so the report hashes every geometry source that matters.
3. Add `intersections` entries with `name`, `mode`, `expected_collision` and
   optional `defines` (OpenSCAD `-D` values). Include a deliberately colliding
   **positive control** so an all-empty result cannot silently pass.
4. For dimensions, alignment or other project-specific assertions, add a
   Python `post_check` and optional `post_check_report`. The runner calls it
   after exports and requires a nonzero exit for failures. If a report is
   given, its `checks` object must contain boolean values, all true. Read the
   evaluated meshes; reading source parameters only verifies the inputs.

A minimal config, with a positive control:

```json
{
  "schema_version": 1,
  "revision": "v1",
  "source": "initiatives/my-project/assembly.scad",
  "dependencies": ["initiatives/my-project/parts.scad"],
  "output_dir": "initiatives/my-project/exports/checks",
  "exports": [{"name": "part", "mode": "part", "single_solid": true}],
  "intersections": [
    {"name": "normal-clearance", "mode": "part-reference-intersection", "expected_collision": false},
    {"name": "positive-control", "mode": "part-reference-intersection", "defines": {"reference_growth": 20}, "expected_collision": true}
  ]
}
```

Run from the kit root:

```sh
bin/python bin/scad-geometry-check.py initiatives/my-project/geometry-check-config-v1.json
```

The runner uses `bin/openscad --hardwarnings` (Manifold), exports revisioned
OFF meshes, runs the project check and writes a JSON report with source and
config hashes, case outcomes and timing. Cases run in parallel (`--jobs 1`
for serial); results do not depend on order.

Mark every printable part export `"single_solid": true`. The runner then
requires one connected body and every edge shared by exactly two oppositely
oriented faces. It does not measure wall thickness; inspect sections where
parts join.

Two Manifold rules matter (see [docs/MANIFOLD.md](../../docs/MANIFOLD.md)):
exactly touching faces intersect as zero-volume slivers, so a collision needs
more than 0.001 mm³ of overlap; and solids that only touch face to face stay
separate bodies, so overlap unions by a small `eps`.

## Interpret results

An empty intersection proves nonoverlap **only for the modeled solids at the
chosen parameter values**. A schematic reference model cannot prove real
clearance. Record physical measurements, slicer evidence and print results
separately. Re-run after geometry or fit parameters change, increment the
revision for a changed design, and keep earlier reports.
