---
name: design-for-printability
description: Design or revise OpenSCAD parts for FDM printability on the user's printer, covering orientation, overhangs, bed contact, warping, holes and split-part assembly. Use for geometry decisions on any printable part; material settings alone belong in the slicer.
---

# Design for printability

Choose geometry and print orientation together, keeping the part's loads, fit
and assembly in mind. Favour the simplest useful change. Splitting a part,
adding feet or changing material is a choice to evaluate, not a default.

**First, read [my-printer.md](../../my-printer.md).** If it still says
`Status: template`, ask the user for printer model, bed size, nozzle and
material, and record the answers there before designing printable geometry.
Defaults when the user does not know: 0.4 mm nozzle, PLA or PETG, 0.2 mm layers.

Use the kit's [printability guide](../../docs/PRINTABILITY.md) as the reference.
Read only the relevant section:

| Design question | Guidance |
| --- | --- |
| Nozzle, layers, minimum wall and gap sizes | [Defaults for a 0.4 mm nozzle](../../docs/PRINTABILITY.md#defaults-for-a-04-mm-nozzle) |
| PLA or PETG? | [Choosing PLA or PETG](../../docs/PRINTABILITY.md#choosing-pla-or-petg) |
| Which way up, layer direction | [Orientation](../../docs/PRINTABILITY.md#start-with-orientation-and-function) |
| Overhangs, bridges, supports | [Overhangs and bridges](../../docs/PRINTABILITY.md#overhangs-bridges-and-supports) |
| Corners lifting, weak bed footprint | [Warping and bed contact](../../docs/PRINTABILITY.md#warping-and-bed-contact) |
| Separate parts, glued or magnetic joints | [Split parts](../../docs/PRINTABILITY.md#split-parts-and-assembly) and [add-pin-joints](../add-pin-joints/SKILL.md) |
| Holes, nuts, magnets, press fits | [Holes and recesses](../../docs/PRINTABILITY.md#holes-pockets-and-fits) |
| Is the fit right? | [fit-coupons](../fit-coupons/SKILL.md) |

## Apply and record the change

- Name the print orientation, the affected feature and the load path before
  editing. Put the print pose in its own selector with the bed at Z = 0.
- Keep fit clearances, wall thicknesses and radii as named parameters near
  the top of the file. Label clearances "starting value, print the coupon"
  until a coupon on the user's printer confirms them.
- Overlap solids that must fuse by a small `eps`; touching faces stay
  separate bodies in Manifold ([docs/MANIFOLD.md](../../docs/MANIFOLD.md)).
- Export release STLs as ASCII, then run `bin/print-check.py` on them. It
  reads the bed and limits from `my-printer.md`. Then look at actual-mesh
  renders of the print pose, including from below.
- Keep geometry checks, slicer results and physical results separate in
  the report. A mesh check is not a print.

Worked example: the keypad sculpture's [print sheet](../../examples/keypad-sculpture/PRINT.md)
and [parts source](../../examples/keypad-sculpture/keypad-parts.scad) (face-down
skin, chamfers against elephant's foot, flat-roofed pin sockets).
