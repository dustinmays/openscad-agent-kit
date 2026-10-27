---
name: independent-design-review
description: Run a fresh-agent, advisory review of an early OpenSCAD design, with an unaided first look, up to three questions to the user, and a short revised look. Use for placement and fit-to-the-real-object checks before a print; not for load or release analysis.
---

# Independent design review

A fresh reviewer sees what the author agent stopped seeing, but it knows only
what the packet shows. The review is advisory: it never queues a print or
blocks work.

## Before you start

1. **Name the stage.** An early blockout means shape, placement and fit to
   the real object only. Leave loads, materials and printability for later.
2. **Make the packet state what the reviewer needs.** Put these in one folder
   (for example `initiatives/<name>/review/`) with a short `PACKET.md`:
   - the renders to judge, with captions;
   - design intent where there are real alternatives, recorded or marked open;
   - whether the model is the real shape or a schematic stand-in;
   - the coordinate origin of every quoted number, with one worked example;
   - the measurement table revision in use (see
     [environment-reference](../environment-reference/SKILL.md)), with each
     value labelled reported, measured, assumed or unresolved.
3. **Isolate the reviewer.** Start a fresh session that sees only that
   folder: a Claude Code subagent given only those paths, or a new Codex or
   Claude Code session in a second terminal window, opened in a copy of the
   folder. It should not see the chat, earlier reviews or the source files.

## Prompt sequence

Give the reviewer these steps, in order. Keep the prompt under one page.

1. **Initial look**: `INITIAL.md`, three observations or fewer, under 150
   words, each citing the image or note behind it. Finalize before asking
   anything; never revise it.
2. **Ask the user**: up to three focused questions, multiple choice with
   free text where it helps. Wait for real answers; do not infer them.
3. **Revised look**: `REFINED.md`, 180 words or fewer: what changed, the
   intended placement, and what still needs a photo or measurement. Keep
   observations, the user's answers and the reviewer's inferences separate.

### Asking good questions

- Pick what could change the design: the real shape the model only
  approximates, then open design choices, then what a photo actually shows.
- Show the evidence beside each question ("In `front.png` the bracket sits
  here. Is that where you want it?"), with two or three options, the
  reviewer's recommendation first.
- Ask neutrally, one decision per question. Record a skipped answer as
  "unanswered" and carry it into `REFINED.md`.

## After the review

- **Fact-check** consequential claims against the meshes and measurements
  before acting. Reviewers make confident mistakes.
- **Keep passes separate:** do not rewrite the first look in hindsight.
- **Respect the user's time:** their part should take about 3–4 minutes.
- **Record** in the project log what the reviewer caught unaided, what only
  the questions surfaced, and what it got wrong.
