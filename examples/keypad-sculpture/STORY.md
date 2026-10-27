# How the keypad sculpture was made

This is the short story of one real project, from a sketch to an assembled
print. It took two days of conversation with an agent. Each step names the
guide that teaches it.

## 1. A sketch and a brief ([Start](../../guides/01-start-a-project.md))

The author had a hand sketch (`reference/Keypad-sketch.jpeg`) and the
keypad's size. An agent wrote it up as [BRIEF.md](BRIEF.md). The most
important line in the brief was "blocking only": stop after a rough model and
wait for review. Nothing printable yet.

## 2. Blockout v1 to v3 ([Blockouts](../../guides/03-blockouts.md))

The agent traced the sketch into three plain solids (yellow, black and blue),
plus a grey stand-in for the keypad. It rendered five views from the real
mesh: front, 30°, 60°, side and 35° from the left.

The author's reactions drove each revision:
- v1 "looks pretty good", but narrow the yellow bottom and stretch the blue down.
- v2 "That's good."
- v3 raised the blue so it clears a button and the status light.

Each change bumped `blockout_revision`, and the agent kept the old renders.

## 3. Measuring the real keypad ([Measure](../../guides/02-measure.md))

The agent started [MEASUREMENTS.md](MEASUREMENTS.md). Each value has an ID, a
source (often the author's exact words) and a kind: reported, measured,
assumed or context. It asked only for the numbers that decided something.
Example: the buttons stand 0.9 mm proud of the face, and that set how thin
the cover over the face could be.

Then the agent built [keypad-reference.scad](keypad-reference.scad), a model
of the keypad itself, and [check_keypad.py](check_keypad.py), which reads the
mesh and checks it against the table. 14 of 14 checks passed.

## 4. Picking between variants ([Blockouts](../../guides/03-blockouts.md))

For the rib field, the agent made three variants: gentle, steep and
directional. They used the same cameras, so the only thing that differed
between pictures was the design. The author picked C. Later the author picked
backing plate option 1 out of four ("I think 1 (safest) is the one").

[DESIGN.md](DESIGN.md) records each pick with the date and the quote.

## 5. Splitting into parts, then coupons ([Fit coupons](../../guides/04-fit-coupons.md))

The parts blockout split the model into three prints: a yellow plate, a black
shell and a blue drape. They are held together by magnets and glue.

Before printing the large parts, the agent cut two small **coupons** from the
real geometry:
- **The top of the shell:** it tests the skin, the button holes, the light hole and the wall fit.
- **A locating post:** it has three crush-ridge strengths, 0.15, 0.25 and
  0.35 mm, marked with 1, 2 and 3 dots.

The author printed them (originally in ASA). Everything fit except
the light hole, which was "1 mm left and 0.5 mm up" from where it should be.
"Tightness 2 was best". Both results went into the model and the table.

## 6. Printable parts with checks ([Printable parts](../../guides/05-printable-parts.md))

[keypad-parts.scad](keypad-parts.scad) turned the approved blockout into
print-ready parts:
- each part in print pose, flat on the bed;
- chamfers against elephant's foot;
- printed hex pins to locate the blue.

Two checks ran before anything was printed:
- **The geometry check:** 16 collision and clearance cases, including
  deliberate "should collide" controls, plus 8 measurements on the meshes. It
  found a rib that poked into a magnet pocket, which was fixed.
- **The pre-print check:** one body each, flat on the bed, inside the bed, and
  no unsupported overhangs.

## 7. PRINT.md ([Print handoff](../../guides/06-print-handoff.md))

[PRINT.md](PRINT.md) lists the files, the slicer notes, the magnet polarity
trick and the assembly order. It was written so that the person at the
printer does not need the chat history.

## 8. Results ([Report results](../../guides/07-report-results.md))

"Fully printed and constructed without issues!" The author's words went into
[observations.md](observations.md) as they were said. What was still not
reported, such as how well the door magnets hold over time, was listed too.
