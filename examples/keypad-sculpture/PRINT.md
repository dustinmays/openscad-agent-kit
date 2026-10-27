# Print and assembly — keypad parts v1

Current revision: **v1** (`keypad-parts.scad`, `parts_revision = 1`).

This is the print sheet from the original build, kept as an example of a
`PRINT.md` ([print-handoff skill](../../skills/print-handoff/SKILL.md)).
The example parts were printed on the author's printer in ASA with a 0.6 mm nozzle (example only).
On a 0.4 mm nozzle with PLA or PETG, use your own values from
[my-printer.md](../../my-printer.md) and the [printing guide](../../guides/05-printable-parts.md):
the 0.8 mm skin is still 4 layers at 0.2 mm, and PETG wants the same brims.
The slicer settings below were written before slicing and are assumptions.

## Files

All files are ASCII STL, already in print pose (bed at Z = 0), in `exports/parts-v1/`.
They appear after you run the [regenerate commands](README.md#regenerate).

| Part | File | Size X × Y × Z (mm) | Volume | Pose |
| --- | --- | --- | --- | --- |
| Yellow ribs + plate | `yellow-v1.stl` | 74.2 × 165.3 × 24.0 | 56.9 cm³ | plate back on the bed, ribs up |
| Black shell | `shell-v1.stl` | 49.1 × 119.6 × 26.5 | 45.2 cm³ | front face down: the 0.8 mm skin is the first 4 layers |
| Blue drape | `blue-v1.stl` | 32.2 × 69.4 × 15.0 | 4.9 cm³ | front face down, 2 hex stubs pointing up |

Checks:
- Pre-print mesh check: `exports/parts-v1/print-check-v1.json` (from `bin/print-check.py`).
- Geometry check: `exports/parts-v1/checks/geometry-check-v1.json` and `parts-geometry-v1.json`.
- Renders: `renders/parts-v1/`.

## Slicer (all parts)

- **Layers:** 0.2 mm, including the first layer, so the shell skin is exactly 4 layers.
- **Supports:** none. Every downward face is no flatter than 45°, apart from small flat roofs that bridge:
  - yellow: the 11 door-magnet pocket roofs, Ø6.3;
  - shell: the 2 pin-socket ends, 3.2 mm hex.
- **Yellow:** 5 mm brim. It is a long, flat plate (the author's ASA example used an enclosure; PLA does not need one).
- **Shell:** 3 mm brim if the corners lift. The bed face is the visible front, so trim the brim cleanly; the 0.4 mm chamfer helps.
- **Blue:** 3 mm brim. The bed contact is small and the droop walls stand 15 mm.
- **Crush ridges:** the 8 ridges on the two yellow posts are 1.2 mm wide. Check in the preview that they print (Arachne / thin walls on).
- **Bed exclusions:** keep every part clear of any area of the bed you cannot use (see `my-printer.md`).

## Magnets: 15 × 6 × 1.9 mm

| Where | Count | Polarity |
| --- | --- | --- |
| Yellow plate back (door pockets) | 11 | any. They grip the steel door, faces flush with the plate back |
| Yellow post tops | 2 | **marked face up** (visible) |
| Shell socket roofs | 2 | **marked face down**, into the pocket (hidden) |

**Marking:** stack all 4 key magnets in one column and put a marker dot on the top face of each. Every dot is then the same pole. A dot-up yellow magnet attracts a dot-hidden shell magnet.

**Check before the glue sets:** the shell must pull down onto the posts. If it pushes away, flip the shell magnets.

## Assembly order

1. **Prepare the parts.** Remove the brims. Dry-fit the keypad into the shell: it should push in snugly from the open back, with the buttons sitting in the holes.
2. **Door magnets.** Put a small drop of CA (superglue) on each pocket floor and press the magnet in flush. Let it cure.
3. **Yellow post magnets.** Press them in dot up with CA and let them cure.
4. **Shell magnets.** Put CA in each shell pocket and press the magnet in dot first. Before it sets, test the pull against the yellow posts (see the check above).
5. **Blue to shell.**
   - Dry-fit first: the 2 hex stubs drop into the sockets in the shell front, and the droop slides over the shell's top and right sides with 0.12 mm per side clearance.
   - Glue: put CA on the shell front where the blue sits and a drop in each socket, press the blue home quickly, then clamp or hold until set.
6. **Mount.** Mount the yellow on the door with its magnets.
7. **Close up.** Push the keypad into the shell, then press the shell straight onto the yellow: the posts go into the sockets, the ridges grip and the magnets clamp.
8. **Removal.** Pull the shell straight off, toward you.
9. **Keypad out.** Pinch the keypad sides through the two finger notches and slide it out of the open back.

These glue steps are general practice: no glued joint in this project has been tested yet.

## What v1 changed from the approved blockout (parts-blockout rev 4)

Coupon-validated values are unchanged: skin 0.8, button holes Ø11.6, keypad fit 0.15 mm per side, magnet pockets Ø6.3 × 1.9, ridge interference 0.25, LED at B11.

- **Blue front:** the stepped front is now one smooth rounded cap, R 3, with the same silhouette and Z range.
  - Its bed side is a 45° chamfer, so it prints face-down without supports.
  - The droop has 0.12 mm per side clearance to the shell.
  - The Ø3 round pins are replaced by 2 printed hex stubs (pin-joints library, AF 3, 4 mm engagement, `ca` clearance 0.12).
- **Shell:** 0.4 mm 45° chamfer on the front outer edge, against elephant's foot.
- **Door pockets:** 0.4 mm mouth chamfer, because they open on the bed.
- **Post tops:**
  - A rib near post 2 rose into the shell magnet: 0.2 mm³ overlap, found by the new magnet probe. The blockout had this too.
  - Fix: the yellow is now cleared to Ø11.2 above each post top, under the shell only. The shell fills the same zone at Ø10.9, so its magnet pocket has full walls.
  - The ridge feet now continue down to the plate, so no ridge bottom hangs over a rib gap.

## Regenerate

See the [example README](README.md#regenerate).

## Results

- **2026-10-26:** the author printed and assembled v1 "without issues". The pin fit, blue clearance, post tops and chamfers held up in practice.
- **Not reported yet:** the slicer settings used, and the door magnet hold.
