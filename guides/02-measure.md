# 2. Measure the real object

**You do:** measure the thing your part must fit, and take a few photos.
**The agent does:** asks for only the numbers it needs, records them in a table, and builds a model of the object.

Skip this step if your part does not have to fit anything.

## Tools

- **Digital calipers** are the best tool, and cheap. They measure to 0.1 mm
  or better. Close the jaws and press "zero" before measuring.
- A **steel ruler** works for sizes over about 50 mm, to about 0.5 mm.
- Measure twice. If two readings differ, give both.

## What the agent asks

The agent asks for **the smallest set of measurements that decides the
design**, not everything about the object. Each question says where and how
to measure, for example: *"Width of the keypad, side to side, at its widest
point, with calipers."* If something is symmetrical, it only needs one side.

Answer in your own words. "About 34.5, maybe 34.6" is useful. Say when you
are guessing.

## Photos

Take photos straight on, not at an angle, with a ruler in the picture for
scale. Take one from the front and one from the side, plus close-ups of
anything the part must fit around (buttons, screw holes, lights).

## What you get

- `MEASUREMENTS.md`: a table where every value has an ID (like `K1`), a
  source (your exact words), and a kind:
  - **measured**: you measured it;
  - **reported**: you stated it;
  - **assumed**: the agent's placeholder, which you should confirm.
- Often a **reference model**: a simple 3D copy of your object built only
  from that table. The agent checks it against the table automatically. It
  is never printed; it lets the agent check fits before you print.

When you are happy the table is right, say so. The agent then marks it
`complete` and will not change it without asking you.

## In the example

See the keypad's [MEASUREMENTS.md](../examples/keypad-sculpture/MEASUREMENTS.md).
Note how one short answer from the author ("Buttons protrube 0.9mm.", row B6)
decided how thin the cover over the keypad could be. The keypad model is
[keypad-reference.scad](../examples/keypad-sculpture/keypad-reference.scad),
checked by [check_keypad.py](../examples/keypad-sculpture/check_keypad.py).
Row B11 shows a value corrected later by a test print.
