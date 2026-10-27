---
name: fit-coupons
description: Use before printing a large part that depends on an uncertain fit (snug holder, press fit, button holes, magnet pockets, sliding joint). Cut small test pieces from the real part geometry, add stepped clearances marked with dots, export and check them, and record which step the user picked.
---

# Fit coupons

A **fit coupon** is a small piece cut from the real part, printed in a few
minutes to test one uncertain fit before committing hours of filament. Every
printer and material prints holes a little differently, so a clearance only
becomes trustworthy after a coupon on the user's own printer.

Guide for people: [guides/04-fit-coupons.md](../../guides/04-fit-coupons.md).
Worked example: [coupons.py](../../examples/keypad-sculpture/coupons.py) and the
coupon section of [parts-blockout.scad](../../examples/keypad-sculpture/parts-blockout.scad).
Generic coupon: [lib/pin-fit-coupon.scad](../../lib/pin-fit-coupon.scad).

## Design the coupon

1. **One question per coupon area.** "Does the keypad slide into the shell
   snugly?" "Which ridge strength holds the shell?" List the fits that are
   uncertain; skip the ones a previous coupon already settled.
2. **Cut it from the real geometry.** `intersection()` the actual part with a
   box around the feature, so the coupon tests exactly what will be printed.
   Same print orientation as the full part.
3. **Step the uncertain value.** Usually three steps around the starting
   value, for example 0.15, 0.25 and 0.35 mm. Mark the steps with 1, 2 and 3
   raised or engraved **dots**, since digits are hard to read at this size.
   Put the steps in a list parameter so the coupon and the part share them.
4. **Keep it small and flat:** under about 15 minutes of printing, with
   enough material around the feature to behave like the real part.
5. Export the coupon as ASCII STL in print pose. Run `bin/print-check.py` on
   it and render it in print pose and "in use" (seated on the real object
   or its mate).

Starting clearances for a 0.4 mm nozzle (PLA/PETG), to centre the steps on:
sliding fit 0.15–0.25 mm per side, snug push fit 0.1–0.15 mm per side, press
fit 0 to −0.1 mm. These are starting values, not results.

## Hand it to the user

Tell them, in plain words: which file to print, how (orientation, no
supports), what to try (push it on, pull it off, check that each button moves
freely), and what to report ("which dot count felt best, and anything that
was off, with direction and roughly how many mm").

## Record the result

- The user's words go in the project's `observations.md`, quoted.
- The chosen value goes into the model's parameter block, with a comment:
  `ridge_interference = 0.25;  // coupon v3 step 2, user's pick`.
- A corrected measurement (for example a hole 1 mm off) becomes a new row in
  `MEASUREMENTS.md` with kind `measured (fit test)`.
- A result that applies to every project on this printer (for example "pin
  clearance 0.12 in PETG") also goes under "Fit results" in `my-printer.md`.
- Bump the model revision.
