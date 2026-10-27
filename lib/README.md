# Reusable OpenSCAD pieces

Use these from a project with `use <../../lib/NAME.scad>`.

| File | What it is | Skill |
| --- | --- | --- |
| [pin-joints.scad](pin-joints.scad) | Hex pins and sockets for gluing separately printed pieces together | [add-pin-joints](../skills/add-pin-joints/SKILL.md) |
| [pin-fit-coupon.scad](pin-fit-coupon.scad) | Test print: five pin clearances, 0.08–0.24 mm per side | [fit-coupons](../skills/fit-coupons/SKILL.md) |
| [breakaway-fin.scad](breakaway-fin.scad) | Removable fin that steadies a tall part on the bed | [add-breakaway-fins](../skills/add-breakaway-fins/SKILL.md) |

Clearances in these files are **starting values**. Print the coupon on your
own printer and material, then use the step that fits best.

A good first print on a new printer is the pin fit coupon:

```sh
bin/openscad --export-format asciistl -D 'part="vertical-block"' -o initiatives/first-print/exports/pin-coupon-vertical-v1.stl lib/pin-fit-coupon.scad
```

The `part` options are listed at the top of the file (`plate` prints the
blocks and pins together; each block or `pin` exports alone).
