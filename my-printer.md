# My printer

Status: template (not filled in yet)

The agent fills this in with you before your first printable part: it asks
you for each value below and writes your answers here. You can also edit it
yourself: replace each ___ with your value. Change the status line to `Status: filled in` when it is done.

`bin/print-check.py` reads the bed size from this file. A blank value uses the
default in brackets.

## Printer

- Printer model: ___
- Bed size X × Y × Z (mm): ___ [default 180 × 180 × 180, smaller than most printers]
- Nozzle diameter (mm): ___ [default 0.4 mm]
- Areas of the bed you cannot use (for example a purge or cutter corner): ___ [default none]

## Material

- Material you print most: ___ [default PLA or PETG]
- Other materials you have: ___
- Enclosure (yes or no): ___ [default no]

## Slicer

- Slicer (for example PrusaSlicer, Bambu Studio, OrcaSlicer, Cura): ___
- Layer height you usually use (mm): ___ [default 0.2]
- Overhang limit for the mesh check, in degrees from vertical: ___ [default 50, which is 45° plus faceting]
- Longest bridge to accept without supports (mm): ___ [default 7]

## Fit results from your own coupons

Your printer's real clearances come from your coupon prints, not from this
template. Add one line per result, with the date and the coupon file:

- (none yet)
