# Measurements

Status: **draft** · Revision: **5** · Updated: 2026-10-25

Canonical reference for the Wyze keypad, mounting hardware and the approved
composition. Kinds and change rules follow the
[environment-reference skill](../../skills/environment-reference/SKILL.md).
Photos: `reference/keypad.jpeg`, `reference/keypad-device.jpeg`.

## Frame

Keypad frame, as seen from the front with buttons facing the viewer:
X right, Y **down** from the body's upper-left corner, Z out of the face.
Origin = upper-left corner of the body outline at the back plane (Z = 0).
Button 1 is upper-left; the "unlock" key is lower-right.
Worked example: button 1 centre = (9.7, 9.7); button 2 = (24.9, 9.7);
lower-right unlock key = (24.9, 9.7 + 5 × 14.9) = (24.9, 84.2).

## Wyze keypad body

| ID | Quantity | Value | Unit | Source | Uncertainty | Kind |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | Body width (X) | 34.5 | mm | Brief (the author) | — | reported |
| K2 | Body height (Y) | 94.5 | mm | Brief | — | reported |
| K3 | Body depth (Z), back to face, excluding buttons | 25.7 | mm | Brief | — | reported |
| K4 | Plan-view corner radius | 5 | mm | Brief: "approximately" | ±1 | reported |
| K5 | Taper front to back | none | — | Brief: "essentially no taper" | — | reported |
| K6 | Back recess depth | 1.5–2 | mm | the author: "The back of the device is slightly recesed. ~1.5-2mm." | ±0.25 | reported |
| K7 | Back recess outline (inset from body edge) | | mm | Not yet captured; model as 2 mm inset | — | pending |
| K8 | Front face edge rounding (face-to-side) | ≈2 | mm | Photos show a soft front edge | ±1 | assumed |
| K9 | Shell seam position from face (side band) | ≈7 | mm | `keypad-device.jpeg`; display only | ±2 | context |

## Buttons

| ID | Quantity | Value | Unit | Source | Uncertainty | Kind |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | Button diameter | 10.8 | mm | Brief | — | reported |
| B2 | Layout | 2 cols × 6 rows | — | Brief; photos | — | reported |
| B3 | Horizontal pitch | 15.2 | mm | Brief | — | reported |
| B4 | Vertical pitch | 14.9 | mm | Brief | — | reported |
| B5 | Button 1 centre from body upper-left (X, Y) | 9.7, 9.7 | mm | Brief: "approximate" | ±0.5 | reported |
| B6 | Button height proud of face | 0.9 | mm | the author: "Buttons protrube 0.9mm." | — | reported |
| B7 | Button face profile | flat, soft edge | — | Photos | — | context |
| B8 | Key legend, row-major from top (L, R) | 1 2 / 3 4 / 5 6 / 7 8 / 9 0 / lock unlock | — | `keypad.jpeg` | — | reported |
| B9 | Status LED centre (X, Y) | ≈19, 4 | mm | Estimated from `keypad.jpeg`, between buttons 1 and 2 near top edge | ±2 | context |
| B11 | Status LED hole centre, corrected (X, Y) | 18, 3.5 | mm | Coupon v3 printed at (19, 4); the author: "needs to move left 1mm and up 0.5mm". Elevation (37, 124.5). Assumes left/up as seen from the front | ±0.25 | measured (fit test) |
| B10 | Status LED diameter | ≈1.5 | mm | Photo | ±1 | context |

Derived checks: column centres X 9.7 and 24.9 (right margin 9.6, ≈ symmetric);
row centres Y 9.7 … 84.2 (bottom margin 10.3).

## Mounting hardware

| ID | Quantity | Value | Unit | Source | Uncertainty | Kind |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Velcro stack thickness (two adhesive halves mated) | 3–4 | mm | the author: "A wad of adhesive velcro (two sides stuck together) will be about 3-4mm thick." | — | reported |
| H2 | Velcro location | in the keypad back recess (K6) | — | the author | — | reported |
| H3 | Velcro stack proud of keypad back | 1–2.5 | mm | H1 − K6 | range | derived |
| H4 | Magnet diameter | 6 | mm | the author | — | reported |
| H5 | Magnet thickness | 1.9 | mm | the author | — | reported |
| H6 | Magnet count, grade, pull force | | — | Not yet decided | — | pending |
| H7 | Mounting surface | flat steel door | — | the author | — | reported |
| H8 | Small magnet diameter (cover retention) | 3 | mm | the author: "smaller magnets ... Same thicknes 1.9-2mm but 3 mm diameter" | — | reported |
| H9 | Small magnet thickness | 1.9–2 | mm | the author, same quote | — | reported |
| H11 | Velcro in use | no — superseded by snug black shell (DESIGN decision 8); H1–H3 kept for history | — | the author 2026-10-25 | — | reported |
| H10 | Magnet counts in stock | 6 mm: 20+; 3 mm: not stated | — | the author | — | reported |

## Approved composition (blockout v3)

Design geometry, not measurements. v2 approved by the author 2026-10-25 ("That's
good."); v3 only raises the blue's inner edge to clear button 2 and the LED,
as the author asked ("yes for 3 blue"). Source of truth is the parameter block in
[blockout.scad](blockout.scad) at `blockout_revision = 3`; summary in
[DESIGN.md](DESIGN.md). Elevation frame there: X right, Y **up**, origin at
the yellow field's lower-left corner; keypad lower-left at (19, 33.5).

| ID | Quantity | Value | Unit | Kind |
| --- | --- | --- | --- | --- |
| C1 | Yellow left / right edge height | 135 / 130 | mm | approved |
| C2 | Yellow width; top rise; bottom-left inset | 78; 32; 8 | mm | approved |
| C3 | Black edges top / bottom / left / right | 50 / 43 / 113 / ≈114.4 | mm | approved |
| C4 | Blue droop tip Y (elevation frame) | 73.5 | mm | approved |
| C6 | Blue gap to button 2 / status LED (B9) | 3.5 / 3.7 | mm | derived (blockout v3 mesh) |
| C5 | Depths: yellow / black / blue proud | 10 / 28 / 3 | mm | assumed (placeholders) |

## Change log

- 2026-10-25, rev 1: table created from the brief, the author's chat reports and
  the photos. Status draft.
- 2026-10-25, rev 2: B6 filled (0.9 mm, the author). Composition section moved to
  blockout v3 (blue raised; C6 added).
- 2026-10-25, rev 3: added H8–H10 (3 × 1.9–2 mm magnets for the cover).
- 2026-10-25, rev 4: H11 — Velcro dropped; keypad captured by the black shell.
- 2026-10-25, rev 5: B11 LED position from the shell coupon print; supersedes B9 for design.
