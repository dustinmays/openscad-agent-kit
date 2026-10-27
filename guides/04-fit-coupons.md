# 4. Fit coupons: test the fit with a small print

**You do:** print one or two small test pieces and say which fit is best.
**The agent does:** cuts the test pieces from the real design, marks the steps, and puts your pick back into the model.

## Why

Every printer prints holes a little smaller and walls a little fatter than
the model says, by an amount that depends on the printer, the material and
the settings. A **fit coupon** is a small piece cut from your real part,
around just the part that has to fit. It prints in minutes, so you find out
before a print that takes hours.

## What a coupon looks like

Usually a small block with the same feature in **three strengths**, from
loose to tight, marked with **1, 2 and 3 dots**. For example: three pegs
with 0.15, 0.25 and 0.35 mm of grip. You try each one and tell the agent the
dot count that felt right.

## Printing it

The agent tells you the file (an `.stl` in the project's `exports/` folder),
which way up it goes (already set; just don't rotate it in the slicer) and
whether it needs supports (usually not).

1. Open the STL in your slicer (for example PrusaSlicer, Bambu Studio,
   OrcaSlicer or Cura).
2. Use your normal settings for your material.
3. Print it and let it cool before testing.

## Testing and reporting

Do what the agent asked: push it on, pull it off, press the buttons through
it. Then report in plain words:

- "2 dots was best; 1 was loose, 3 was too tight to push on."
- "The hole for the light is about 1 mm too far right."
- "Everything fits; the magnets went in snugly."

Directions ("too far right") are fine. Say which way you were looking at it.

## What happens next

The agent puts your pick into the model and your words into the project's
`observations.md`. If a measurement was off, it corrects the measurement
table too. If the result applies to all your projects (for example "glue pins
fit best at 0.12 mm in PETG"), it also notes it in
[my-printer.md](../my-printer.md).

A good first coupon on a new printer is the pin-joint fit test in
[lib/pin-fit-coupon.scad](../lib/pin-fit-coupon.scad) (see [lib/README.md](../lib/README.md)).

## In the example

The keypad project printed two coupons before the real parts. See
[coupons.py](../examples/keypad-sculpture/coupons.py). The author reported:
*"Magnets fit well and so does the housing and the buttons are fine. Only
small issue is the indicator light hole on the face plate needs to move left
1mm and up 0.5mm."* and *"Tightness 2 was best."* Both went straight into the
model ([observations.md](../examples/keypad-sculpture/observations.md)).
