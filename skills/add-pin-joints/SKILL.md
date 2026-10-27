---
name: add-pin-joints
description: Split an OpenSCAD part into separately printed pieces joined permanently by glued hex pins, so each piece prints in its best orientation. Use for glued (superglue/epoxy) multi-part joints; not for bolted, removable or snap-fit joints.
---

# Add pin joints

Join separately printed pieces with hex pins and superglue or epoxy. Choose
each piece's print orientation first; the joints follow from that. The
library is [lib/pin-joints.scad](../../lib/pin-joints.scad). Its
[fit coupon](../../lib/pin-fit-coupon.scad) is a good first print on a new
printer or material.

## Decide before modeling

- **Where to split.** Put the interface where each piece can print flat or
  in its load-friendly pose. Avoid splitting through the most stressed section.
- **Each piece's print rotation.** Write it down as `rotate()` angles from
  assembly to print pose. The joint's hex roll depends on it.
- **Adhesive.** `ca` (superglue, default) or `epoxy`. Ask the user if unclear.
- **Pin source.** A loose pin printed lying flat is the default and the
  strongest across the joint. Use a printed-on stub (`pj_pin_stub`) only where
  the pin would print standing up anyway.

## Model the joint

From a project folder `initiatives/<name>/`: `use <../../lib/pin-joints.scad>`.

```scad
spec  = pj_spec(af=6, engage_a=12, engage_b=12, adhesive="ca");
joint = pj_frame(origin=[x,y,z], axis=[0,0,1], up=[0,1,0]);

difference() { part_a(); pj_at(joint) pj_socket(spec, "a"); }
difference() { part_b(); pj_at(joint) pj_socket(spec, "b"); }
pj_pin_print(spec);                       // loose pin, flat on the bed

pj_assert_pose(joint, "a", part_a_print_rot, "part A");
pj_assert_pose(joint, "b", part_b_print_rot, "part B");
```

- `origin` is on the interface plane; `axis` points into part B.
- **Define each joint once** and use it for both sockets and any pin.
- **Set `up` to the print-up direction (assembly coordinates) of the part
  that prints this hole sideways.** That puts a flat on the roof: a short
  bridge. A part that prints the hole vertically accepts any roll.
- Call `pj_assert_pose` for every socket in every print selector, with the
  same angles the selector passes to `rotate()`. Do not suppress a failure;
  change `up` or a print pose.

## Size it

| Choice | Starting point | Evidence |
| --- | --- | --- |
| Pin across flats | 6 mm | Only size tested |
| Clearance per side | `ca` 0.12, `epoxy` 0.16 mm: **starting values, print the coupon** | Example: 0.12 was best on the author's ASA printer. PLA/PETG untested |
| Engagement per side | ≥ 1.5 × `af` | Rule of thumb |
| Wall around the hole | ≥ 3 mm | Design rule, not a strength result |
| Pins per joint | 2+ where the joint must resist twisting | Design judgment |

Print [pin-fit-coupon.scad](../../lib/pin-fit-coupon.scad) in the user's
material (it has five clearances, 0.08 to 0.24 mm, labelled in hundredths),
then pass `clearance=` with the step the user picks. Record the result in
`my-printer.md` under fit results.

## Verify

Follow [check-scad-geometry](../check-scad-geometry/SKILL.md). For pin joints add:

- An `intersection()` of the seated pin and both parts: expect empty, plus an
  oversized-pin positive control (see the coupon's `interference` selector).
- The `pj_pose:` echo lines for every socket, recorded in the mesh report.
- Actual-mesh views of each socket in print pose: flat roof on top.

## Hand off

Export loose pins as their own STL with a quantity. In the print sheet: pins
lie flat as exported, no brim on pins, no supports for sockets. For
assembly: dry-fit every pin first; superglue goes in the socket with the pin
pushed home quickly; epoxy goes on the pin and socket. Clamp until set. Bump
the model revision when joint parameters change.
