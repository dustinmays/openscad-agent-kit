# Designing OpenSCAD parts for printability

Reference for agents and curious users. It applies to every project here.
The [design-for-printability skill](../skills/design-for-printability/SKILL.md)
points to the section you need. Numbers here are **starting values for a
typical 0.4 mm nozzle printer with PLA or PETG**. The user's own values live
in [my-printer.md](../my-printer.md), and their own coupon results override
everything below.

## The user's printer comes first

Read `my-printer.md` before any printable geometry. If it is still the
template, ask the user for the model, bed size, nozzle and material, and
record them. Plan against their bed size minus any unusable areas, and leave
room for a brim (5 mm per side is a safe allowance). Keep geometry decisions
separate from slicer settings: the model sets shapes; the slicer sets
temperatures, speeds and infill.

## Defaults for a 0.4 mm nozzle

| Feature | Starting value | Why |
| --- | --- | --- |
| Layer height | 0.2 mm | Common default; thin skins should be whole layers |
| Minimum wall | 0.8 mm (2 lines); 1.2 mm or more for strength | Thinner walls may vanish in the slicer |
| Minimum standing pin or rib | 1.2 mm wide | Thinner features wobble and break |
| Engraved or embossed text | ≥ 0.5 mm deep, ≥ 4 mm tall, bold font | Smaller text fills in |
| Sliding fit clearance | 0.15–0.25 mm per side | Print a coupon to confirm |
| Snug push fit | 0.1–0.15 mm per side | Print a coupon to confirm |
| Hole for a 3 mm screw, vertical | 3.2–3.4 mm | Printed holes come out small |
| Magnet pocket | magnet diameter + 0.2–0.3 mm, depth + 0.1 mm | Print a coupon to confirm |
| Small clearance between moving parts | ≥ 0.3 mm | Narrower gaps can fuse |

Holes print smaller and outside walls slightly larger than modeled. A fit
clearance is a starting value until a [fit coupon](../skills/fit-coupons/SKILL.md)
on the user's printer confirms it.

## Choosing PLA or PETG

- **PLA**: the easiest to print. Stiff, crisp detail, little warping, no
  enclosure needed. It softens around 55–60 °C, so avoid cars, sunny windows,
  dishwashers and anything near heat.
- **PETG**: tougher and less brittle, handles heat up to about 70–75 °C and
  outdoor use better. It strings more, bridges a little worse, and sticks
  very hard to smooth PEI beds (use glue stick or a textured sheet). Fits
  can come out a little tighter than PLA, so print the coupon in PETG.
- When unsure: PLA for indoor objects and test prints, PETG for parts that
  flex, take impacts, get warm or live outside.

## Start with orientation and function

Choose each part's print orientation before designing roofs, overhangs and bed
contact. Put the print pose in its own selector with the bed at Z = 0, and
keep functional geometry shared between the assembly and print selectors so
the print variant cannot silently change a fit.

- Layers are weakest when pulled apart. Orient so the main load runs along
  the layers, not across them. A hook printed standing up snaps at a layer
  line; printed lying flat it does not.
- The face on the bed comes out flat and smooth (or textured, matching the
  sheet). Put a visible face there if it is flat.
- Large flat areas on the bed help adhesion; small contact plus height
  means a part can be knocked over.

## Overhangs, bridges and supports

- **Overhangs**: a face that leans out over empty space prints cleanly up to
  about 45° from vertical. `bin/print-check.py` uses 50° by default (45° plus
  facet tolerance); change it in `my-printer.md`.
- **Bridges**: a flat ceiling between two supports prints across gaps of
  about 5–10 mm. The check accepts flat ceilings up to 7 mm across by default.
- **Avoid supports by design**: chamfer the underside of overhangs at 45°,
  use a teardrop shape for horizontal holes (a circle with a 45° peaked roof),
  and split a part so each piece prints flat.
- If supports are needed, say where, and run `bin/print-check.py --allow-supports`
  so the overhangs become a warning. Supported faces come out rough.
- **Elephant's foot**: the first layers squish outward. Add a 0.4 mm × 45°
  chamfer on bed-side edges that must fit something.

## Warping and bed contact

Corners lifting is a common failure, worse for long flat parts and in PETG
on a cold or draughty printer.

- Round external corners slightly, and avoid long thin bed outlines when a
  shorter shape would work.
- A brim (3–5 mm) helps long or small-footprint parts; add it in the slicer,
  not the model, and count it in the bed size.
- Small round "mouse ear" pads at sharp corners help too. They are cut off after printing.
- Bed contact is a geometric number, not measured adhesion. Clean the bed
  (dish soap and water, or isopropyl alcohol) before blaming the model.

## Split parts and assembly

Split a part when one piece would need heavy supports, would not fit the bed,
or needs different orientations for different features.

- Design the assembly motion first: how does each piece go on, and in what
  order? Check that the last piece can actually get into place.
- Glued permanent joints: [add-pin-joints](../skills/add-pin-joints/SKILL.md).
- Removable joints: magnets in pockets, screws into heat-set inserts, or
  snap fits. Each needs a coupon.
- For repeated parts, check that the same print rotated (not mirrored) fills
  every position, or export left and right versions on purpose.

## Holes, pockets and fits

- A **vertical** hole (axis along Z) prints round. Add 0.2–0.4 mm to the
  diameter for a clearance fit.
- A **horizontal** hole needs a roof. Use a teardrop profile with its peak
  toward +Z in the print pose, or a flat bridge roof for small holes.
- Pockets for magnets or nuts: keep the floor and side walls at least 0.8 mm,
  and 1.2 mm where they take load. Use a hex pocket for a nut so it cannot turn.
- Measure the real hardware with calipers; do not trust the packet.

## Thin and tall parts

A tall thin part can wobble or be knocked over by the nozzle. Options: a brim,
a wider foot, printing it lying down, or a removable fin
([add-breakaway-fins](../skills/add-breakaway-fins/SKILL.md)).

## Model and verify the actual result

Keep meaningful dimensions near the top of the source. Overlap solids that
must fuse by a small `eps` ([MANIFOLD.md](MANIFOLD.md)). After geometry changes:

1. Export the print-pose STL as ASCII.
2. Run `bin/print-check.py` on it (one body, closed, flat on Z = 0, inside
   the bed, overhangs).
3. For fits and clearances, run a geometry check with a positive control
   ([check-scad-geometry](../skills/check-scad-geometry/SKILL.md)).
4. Render the actual mesh in print pose, from above and from below, and look
   at it.
5. Record what was checked on the mesh, what was seen in the slicer, and what
   was printed, separately.

A mesh check is geometric evidence. Print strength, adhesion and fit need a
print.

## Worked example

The [keypad sculpture](../examples/keypad-sculpture/STORY.md) shows a thin
skin printed face down as whole layers, chamfers against elephant's foot,
flat-roofed pin sockets, magnet pockets and crush ridges tuned with a coupon.
Its fit numbers were measured on the author's printer (in ASA, an example
only); they are not defaults.
