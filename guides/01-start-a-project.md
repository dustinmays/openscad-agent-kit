# 1. Start a project

**You do:** describe what you want to make, and answer a few questions.
**The agent does:** records your printer, creates a project folder and writes a short brief.

## Before you start

You have run `bin/setup` and `bin/doctor` says "All requirements OK"
([SETUP.md](../SETUP.md)). Your agent is open in the kit folder.

## Say what you want

Start with one or two sentences in your own words. Good starts:

- "I want a holder for my TV remote that screws under my desk."
- "I want a wall mount for my door keypad that looks like a small sculpture.
  Here's a sketch."
- "My vacuum's hose clip broke. Can we make a new one?"

If you have a **sketch** or **photo**, give it to the agent. A pencil sketch
photographed with your phone is perfect. Write any sizes you know right on
the sketch. Drag the image file into the terminal window, or save it in the
project's `reference/` folder once it exists.

## Your printer, once

The first time, the agent asks about your printer before anything else:

- **Printer model**, for example "Bambu Lab A1" or "Prusa MK4".
- **Bed size**: the largest part it can print, in millimetres. It is on the
  printer's web page or in its manual.
- **Nozzle size**: almost always 0.4 mm unless you changed it.
- **Material**: PLA or PETG. Unsure? PLA is the easier choice for most
  indoor things; PETG for parts that bend, get warm or live outside.

The agent writes your answers into [my-printer.md](../my-printer.md). You can
open that file and correct it any time.

## The agent's questions

Expect up to five, such as: What does it attach to? How big, roughly? Will it
carry weight, get hot or go outdoors? Is it fine to glue two pieces together?
"I don't know" is a fine answer; the agent will pick a sensible default and
tell you.

## What you get

A folder `initiatives/<your-project>/` containing:
- a short `BRIEF.md` in your words;
- `status.md`, which always says where things stand.

Nothing is designed yet. The next step is either measuring the object it must
fit ([guide 2](02-measure.md)) or going straight to rough shapes
([guide 3](03-blockouts.md)).

## In the example

The keypad project started with a pencil sketch with a few sizes on it, and
the keypad's dimensions. Read the brief:
[examples/keypad-sculpture/BRIEF.md](../examples/keypad-sculpture/BRIEF.md).
Its most important line: *"Do not attempt to design the finished printable
object yet."* A rough model comes first.
