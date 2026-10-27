---
name: discovery
description: Use when asked to scope, investigate or "figure out what needs doing" before any building starts; read-only investigation that ends with a short scoping note the lead or the user can plan work from.
---

# Discovery

You are the discoverer. Find out what the work really is, then leave a short
scoping note, so planning can start from a file instead of from this chat.
**You change nothing except the note.**

Often you become the lead afterward. The note is what makes that safe: work
can continue in this session, a fresh one, or a different agent.

## Inputs to expect

- A **request**, often loose. Restate it in one sentence before you start.
- **Project rules**: `AGENTS.md`, `my-printer.md`, `PROJECT_STATE.md`.
- **Existing material**: the project's `status.md`, `MEASUREMENTS.md`,
  `.scad` sources, photos, earlier work items.

If the request is too vague to investigate, ask one batched question.

## Procedure

1. **Read the rules first.** Note any limit that shapes the work.
2. **Investigate read-only.** Read sources, measurements and photos. Run
   existing commands only if they write nowhere but a scratch folder.
3. **Separate what you know from what you think.** Keep these apart:
   observed (you saw it), inferred (you reasoned to it), unknown (you could
   not tell), and decision needed (only the user can settle it). Record the
   reasoning behind each decision, not just the conclusion.
4. **Propose the shape of the work.** Name the steps, what each hands to the
   next, and how "done" will be checked. Prefer the fewest steps.
5. **Write the note** from [the template](references/scoping-note-template.md)
   as `initiatives/<name>/discovery.md`. Delete empty sections.
6. **Hand back.** The note's path, a one-sentence summary, and the decisions
   that need the user. Nothing else.

## Rules

- Read-only, apart from the note.
- Stay in scope; side discoveries go under open questions.
- Don't plan beyond the evidence. If you could not verify something, say so.
- Keep the note short enough to act on in a few minutes.
