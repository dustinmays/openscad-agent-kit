# 3. Blockouts: rough shapes, then pick

**You do:** look at pictures of rough shapes and say what to change, or which one you like.
**The agent does:** builds the shape from simple blocks, renders it from fixed angles, and records your choice.

## What a blockout is

A blockout is a deliberately rough 3D model made of simple blocks. It shows
**size, proportion and placement** and nothing else: no rounded edges, no
holes, no screw fittings. Rough means quick, so changing your mind costs
minutes, not hours.

## What you will see

Pictures (PNG files in the project's `renders/` folder) of the real 3D
model from a few fixed angles: front, angled and side. Each part has its own
colour. A grey stand-in shows the real object, so you can judge the scale.

Open them in Preview (double-click), or ask the agent to describe them.

## How to give feedback

Short and concrete works best:

- "The bottom should be narrower, so this corner opens up."
- "Move the blue part down about 1 cm."
- "Bigger overall, maybe 20%."
- "That's good."

Everything is a number at the top of the model file, so "8 mm narrower" is a
quick change. Each change gets a new revision number (v1, v2, v3…), and the
old pictures are kept so you can compare.

## Choosing between variants

When there is a real choice, the agent makes 2–4 **variants** (A, B, C) and
puts them side by side on one board, all from the same angles. It gives you
one line per variant: what differs and the trade-off. Pick one, combine two
("A, but with C's top"), or ask for another round.

The agent writes your pick and your exact words into `DESIGN.md`, so the
decision is not lost.

## In the example

The keypad blockout took three rounds:
- **v1:** "looks pretty good", but narrow the bottom and stretch the blue down.
- **v2:** "That's good."
- **v3:** moved the blue clear of a button.

See [blockout.scad](../examples/keypad-sculpture/blockout.scad) and the
decisions in [DESIGN.md](../examples/keypad-sculpture/DESIGN.md). Later, the
rib field had three variants on one board. The author picked C, then
picked backing plate 1 of 4: *"I think 1 (safest) is the one."*
