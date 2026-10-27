# Design notes — blockout

## Axes and units

mm. `blockout.scad` is authored in front elevation: X right, Y up, Z out of
the wall (wall plane Z = 0). Origin is the yellow field's lower-left corner.
`export_frame=true` rotates to Z up, viewer toward +Y, for rendering.

## Keypad (authoritative, from the brief)

34.5 W × 94.5 H × 25.7 D mm, ≈5 mm corner radius, no taper. Buttons
(not modeled yet): Ø10.8, 2 × 6, pitch 15.2 H × 14.9 V, upper-left centre
9.7, 9.7 from the body's upper-left corner.

## Composition traced from the sketch

Sketch scale ≈ 10.1 px/mm (displayed image), checked against the 85, 130
and 135 mm marks. The blue keypad outline in the sketch measured 34 × 95 mm,
so the sketch is close to true scale.

| Element | Sketch says | Blockout v1 |
| --- | --- | --- |
| Yellow left / right edge | 135 / 130 | 135 / 130 (vertical) |
| Yellow top / bottom diagonal | 85 / 85 | 84.3 / 79.2 (v2: bottom-left inset 8; v1 86.3) |
| Black top / bottom edge | 50 / 43 | 50 / 43 |
| Blue droop tip Y | ≈97 | 73.5 (v2 stretch ×2 about Y 120.5) |
| Black left / right edge | 113 / 114 | 113 / ≈114.4 |
| Keypad lower-left | — | (19, 33.5) |

The two diagonals cannot both be 85 with edges of 135 and 130 and parallel
vertical sides; the difference is split.

## Placeholder assumptions (not from the sketch)

- Depths: yellow 10, black 28 (≥ keypad 25.7), blue 3 proud and drooping
  12 down the black's sides, hanging 2.5 past its edges.
- The keypad outline is cut through the black so the reference body shows.
- Blue inner edge is a 9-point trace of the hatched region, rounded 3 mm.

## Decisions (the author, 2026-10-25, after approving blockout v2)

1. **Keypad access:** the black front is a separate lift-off cover with button
   holes. The sculpture stays on the door; lift the cover and pull the keypad
   off its Velcro (H1, in the back recess K6) to reach the batteries.
2. **Status LED:** small hole through the cover, kept visible. The LED sits at
   about elevation (38, 124), right at the blue wrap's inner edge — the blue
   must clear it.
3. **Colours:** yellow, black and blue printed flat as separate parts and
   glued (pin joints available: [add-pin-joints](../../skills/add-pin-joints/SKILL.md)).
4. **Door mount:** 6 × 1.9 mm magnets (H4/H5); the author has 20+, so 8–12 can be
   spread across the back.

5. **Buttons** stand 0.9 mm proud of the face (B6), so the cover over the
   face can be at most ≈0.9 mm thick for the buttons to stay flush or proud.
6. **Blue clears the keypad controls** (blockout v3): ≈3.5 mm to button 2,
   ≈3.7 mm to the estimated LED.
7. The author, on retention: "Lift straight off the door for magent attach."
   Read as: the sculpture lifts straight off the steel door (magnets on the
   back). How the front cover is retained is still to confirm.

## Rib decisions (the author, 2026-10-25)

1. **Force idea: bow wave.** Ribs rise toward the viewer as they approach the
   black, like water piling against an object, and settle low at their far
   ends.
2. **No backing plate.** Ribs stand alone; the door shows in the gaps. A black
   spine, printed separately and glued, ties the ribs together.
3. **10 ribs** across the 78 mm field (7.8 mm pitch).
4. **Ribs pass behind the black.** They run full length; the black mass sits
   on top of them. So under the black the ribs dip low, and the black's back
   is raised by that height.

Lead's proposed method (for the blockout, not yet approved): one height field
over the elevation, driven by distance to the black outline, sampled along
each rib's centre line. Ribs therefore relate to each other (coherent field,
not per-rib waves), and the black's 9° edges tilt the crests so the field
moves off-axis while staying straight lines from the front.
Consequence to check: 6 mm magnets do not fit in a ~4 mm rib, so magnets
likely live in the spine(s).
5. **Rib field chosen (2026-10-25):** variant C (directional bow wave), on a
   3 mm yellow backing plate fused with the ribs into one yellow part. Plate
   outline = organic option 1 "soft inset" (`ribs-blockout.scad` revision 4,
   `plate_style = 1`): inside the rib outline so rib ends overhang it, with
   swelling/pinching edges. The author: "I think 1 (safest) is the one." Sliver
   rib 0 kept. No spine bars. Max depth 35 mm from the door; black front at
   Z 32 (ribs 4 mm high under the black).
6. **Cover retention (2026-10-25):** magnets. The author: "Magnet attachment
   will do. I've got smaller magnets which could make that easier. Same
   thicknes 1.9-2mm but 3 mm diameter" (H8/H9). Door mount stays 6 × 1.9 mm
   magnets (H4/H5) in the yellow plate.
7. **Material and cover skin (2026-10-25):** ASA (the author's material; example only). The author: "Yes it's ASA. I
   think we can attempt to print a very thin skin for now." → cover approach
   (a): thin skin (≈0.8–0.9 mm, ≤ B6 0.9) over the keypad face with button
   and LED holes, buttons flush or slightly proud. Treat as an experiment to
   print-test.
8. **No Velcro; one black part (2026-10-25).** the author: "if we design this to
   fit relatively tight and use magnets to hold the black part in place, the
   velcro may be unnecessary" and "black body could come off of the yellow
   with magnets. The black body and cover could be all one piece."
   → The black is one shell: 0.8 mm front skin with button/LED holes, walls
   hugging the keypad (snug fit), open back. The keypad is captured between
   the yellow rib tops and the skin, so its face height is set by printed
   geometry, not Velcro. The whole black shell (with the blue glued on)
   lifts off the yellow, held by magnets; locating features take the
   downward (shear) load. Replaces decision 1's separate cover and the
   Velcro of decision 2.
9. **Friction at the black–yellow interface (2026-10-25).** the author: "Looks
   perfect. Yes I do like a bit of a friction/ridge point in the interface
   with the black and yellow to ensure it holds together." → small crush
   ridges on the locating posts (or their sockets) so the shell grips the
   yellow in addition to the magnets. To be fit-tested with a coupon.
10. **Ridge interference 0.25 mm (2026-10-25)**, from the post coupon: The author
    "Tightness 2 was best". LED hole at B11 (coupon-corrected).
