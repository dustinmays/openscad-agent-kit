---
name: start-a-project
description: Use when the user wants to make something new ("I want to make X that fits my Y"). Interviews them, records the printer if needed, creates the project folder with a brief and status, and sets up the first blockout. The first skill to use in this kit.
---

# Start a project

Turn "I want to make X" into a project folder an agent can resume cold, and
stop before any detailed modeling. The user is often not a programmer: ask in
plain words, one short batch at a time, and explain any term you must use.

Guide for people: [guides/01-start-a-project.md](../../guides/01-start-a-project.md).
Worked example: [the keypad brief](../../examples/keypad-sculpture/BRIEF.md).

## Steps

1. **Printer first, if unknown.** Open [my-printer.md](../../my-printer.md).
   If it says `Status: template`, your first message asks only for printer
   model, bed size, nozzle and material, with no design questions mixed in.
   Write the answers there and set `Status: filled in`. If the user
   does not know a value, keep the default (0.4 mm nozzle, PLA or PETG) and
   say so.
2. **Interview**, in a later message once the printer is recorded. Ask at
   most 5 questions, the ones that decide the design:
   - What is it for, and where does it go?
   - What real object must it fit or hold? (If any, plan measurements with
     [environment-reference](../environment-reference/SKILL.md).)
   - How big, roughly? What must it look like? Ask for a sketch or photos;
     a phone photo of a pencil sketch is ideal.
   - Loads or handling: will it be stepped on, carried, outdoors or in heat?
     (Heat or sun points to PETG rather than PLA.)
   - One piece, or is assembly (glue, screws, magnets) fine?
3. **Create the folder** `initiatives/<short-name>/` with:
   - `README.md`: what it is, what success looks like, what is out of scope;
   - `BRIEF.md`: the user's words and your summary of the intent, with
     "blockout only" as the first phase;
   - `status.md`: goal, current position, next step;
   - `log.md`: one dated line, "created";
   - `reference/`: the user's sketches and photos (kept out of Git).
   Add a line to [PROJECT_STATE.md](../../PROJECT_STATE.md) under Active.
4. **Plan measurements** if the part must fit a real object. Ask only for
   the values the first blockout needs.
5. **Next:** the first blockout with
   [blockout-and-review](../blockout-and-review/SKILL.md). Say so to the user
   in one sentence, and ask whether to go ahead.

## Rules

- No printable geometry, fits or tolerances in this step.
- Quote the user's words when you record a requirement; mark your own
  interpretation as yours.
- Keep files short. Create only the files listed; others come when needed.
