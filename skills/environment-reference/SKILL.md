---
name: environment-reference
description: Use when a part must fit a real object (a device, shelf, bike, door) and its measurements, photos or reference model need to be planned, recorded, reviewed or changed.
---

# Environment reference

Capture the real-world object a design must fit, so any later agent can
rebuild it and the user can spot-check it against the real thing. This is
the step after the brief and before design geometry depends on the object.

Worked example: [MEASUREMENTS.md](../../examples/keypad-sculpture/MEASUREMENTS.md)
of the keypad sculpture. For a model of the object itself, see
[device-reference-model](../device-reference-model/SKILL.md).

## Outputs, per project

- `MEASUREMENTS.md`: the canonical measurement table, with a status header.
- `reference/`: photos named by measurement ID or by view, for example
  `K1-width-ruler.jpg`. Photos stay out of Git (see `.gitignore`).
- Later, a reference model built only from the table (see device-reference-model).

## Steps

1. **Plan.** List the values the design question needs. Ask for the smallest
   set that decides it: one side when the object is symmetric (record the
   other as an assumed mirror), the tightest spot rather than several, and
   nothing already answered by existing rows or photos. Add measurements later
   only when a decision needs them. Include a short photo list, with a ruler or
   caliper in frame for scale.
2. **Ask.** Give the user a short worksheet in chat, or write
   `reference/worksheet.md` with one labelled line per value to fill in. Say
   which tool to use (ruler, calipers) and where to measure. Plain words: "the
   width of the keypad, side to side, at the widest point".
3. **Record.** Copy the answers into `MEASUREMENTS.md`, quoting the user's
   words in the source column.
4. **Model.** Build or revise the reference model from the table. Keep
   measured, derived, assumed and context-only geometry visibly distinct.
5. **Approve.** The user reviews the table and an overlay render. Only their
   explicit approval changes the table status to `complete`.

## The table

Each row has: stable ID, quantity, value, unit, source, uncertainty and
kind. Add side or station columns when the object needs them. Kinds:

- `measured`: the user measured it; record the method.
- `reported`: the user stated it; the method is unknown.
- `derived`: computed from other rows; name them.
- `assumed`: an agent or design assumption awaiting confirmation.
- `context`: approximate, for display only; never used for clearance.
- `pending`: wanted but not yet captured.
- `measured (fit test)`: learned from a coupon print.

For `reported` values, keep the user's exact words next to the agent's
interpretation. IDs are never reused or renumbered. Leave unknowns blank and
say why. Every table states its coordinate frame, with one worked example.

## Change rules

The table is append-mostly. Agents may add rows and fill `pending` rows from
the user's answers.

- While the status is `draft`, an agent may correct an obvious transcription
  error and must note it in the table's change log.
- While the status is `complete`, do not edit or delete a row without the
  user's explicit approval. To propose a change, add a new row that names the
  row it would replace, mark it `proposed`, and ask.
- Record approval in the change log with the date, the table revision and
  the user's words. Increment the revision whenever an approved value
  changes, and tell downstream work which revision it now uses.

A geometry check that passes against the table is only as good as the table.
