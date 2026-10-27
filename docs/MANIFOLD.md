# OpenSCAD with Manifold: rules that matter

The kit runs the OpenSCAD development snapshot with `--backend=manifold`
(`bin/openscad`). Manifold renders in seconds where the old engine took
minutes. It behaves differently in a few ways that affect printing and checks.

## 1. Overlap solids that should fuse

Two solids that only *touch* face to face stay **separate bodies** in the
output, even inside `union()`. A slicer may print them as two loose pieces,
and `bin/print-check.py` reports `one_body` as FAIL.

```scad
eps = 0.01;
union() {
  cube([20, 20, 5]);
  translate([0, 0, 5 - eps]) cube([10, 10, 10 + eps]);  // overlaps by eps
}
```

Use a small overlap (0.01–0.05 mm) wherever parts join. It does not change
the printed size in any way you can measure.

## 2. Export print files as ASCII STL

```sh
bin/openscad --export-format asciistl -o exports/part-v1/part-v1.stl part.scad
```

Manifold output can contain zero-area sliver triangles whose corners are
about a millionth of a millimetre apart. In ASCII STL (and OFF) they are
harmless. Binary STL rounds coordinates, which can merge those corners and
open holes in the mesh. Slicers usually repair this; strict checkers do not.
`bin/print-check.py` fails a binary STL.

## 3. Touching is not colliding

In a collision check (`intersection()` of two parts), exactly touching faces
return a zero-volume sliver instead of nothing. `bin/scad-geometry-check.py`
counts a collision only above 0.001 mm³ of overlap and records the volume.

## 4. OFF files carry colours

OFF exports from the snapshot add RGB colour values after each face. The
kit's readers (`bin/render-views.py`, `bin/scad-geometry-check.py`) read only
the vertex indices. Use them rather than a simple word-by-word parser.

## 5. Native PNG export

`openscad -o view.png` needs a graphics context and can fail when run from a
terminal or by an agent. The kit renders pictures from exported meshes with
`bin/render-views.py` instead, which also guarantees that the picture shows
the actual geometry.
