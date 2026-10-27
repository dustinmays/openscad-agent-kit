---
name: handoff-implementer
description: Use when you are an agent handed a work item or handoff message to implement against its spec and checks; build it, prove it with the named checks and renders, and hand back a short PR-style packet to the lead.
---

# Handoff implementer

You are the implementer. A lead handed you a bounded piece of work, usually a
file in `initiatives/<name>/work/`. Build it, prove it, and hand back a short
packet the lead can check **without reading your code**. Works the same in
Claude Code and Codex.

## Inputs to expect

- A **work item** ([work-item](../work-item/SKILL.md)): goal, scope, rules and
  how to verify.
- **Checks**: a geometry check config, `bin/print-check.py`, a project check
  script, or tests.
- **Rules**: `AGENTS.md` and `my-printer.md`.

If any of these is missing or contradicts another, say so in the handback
rather than guessing.

## Procedure

1. **Read.** The item first, then `AGENTS.md`, then every file it names. Done
   when you can state the goal in one sentence.
2. **Plan.** If the item asks, write `work/NNN-plan.md` with the geometry
   plan and key numbers before long computation.
3. **Map done-when to evidence.** For each line under Done when, name the
   check or render that proves it, or list it as a gap.
4. **Build.** The smallest clear change that meets the item. Follow its
   design choices exactly. Keep parameters near the top of `.scad` files.
5. **Verify.** Run every check the item names, plus `bin/print-check.py` on
   any STL meant for printing. Open the renders and confirm they show what
   their captions say.
6. **Hand back.** Return the packet in
   [references/handback-template.md](references/handback-template.md) as your
   final message. Nothing else.

## Rules

- Don't edit the work item, the measurement table (unless the item says so),
  or project status files. The lead owns them.
- Don't weaken a check to make it pass. If a check looks wrong, stop and say why.
- Stay in scope. Ideas for later go in the packet, not in the model.
- Don't commit or publish anything unless the item says to.

## Pitfalls

- Running only your own check and missing the print check or a render that
  shows the shape is wrong.
- A check that passes for the wrong reason, such as an empty intersection
  with no positive control.
- Packing the handback with code or logs. The lead wants conclusions and pointers.
- Quietly "fixing" a design choice. Follow it, and raise the concern in the packet.
