---
name: work-item
description: Use when handing work to another agent (a subagent, a second Claude Code or Codex session) or to the user; when reviewing what came back; or when resuming split work cold. Covers writing work items (handoffs with a state), tracking them, and asking the user for decisions in one place.
---

# Work item

A work item is a handoff file with a state. It lets work be delegated,
paused, reviewed and resumed without any chat session holding it together.
You are usually the **lead**: you write items, hand them out, review what
comes back, and protect the user's attention. The receiving agent uses
[handoff-implementer](../handoff-implementer/SKILL.md).

This is optional. Most designs need one agent, and no work items at all. See
the [multi-agent runbook](../../guides/runbook-multi-agent.md) for when it helps.

## Where things live

- `initiatives/<name>/work/NNN-slug.md`: one file per item, from
  [the template](references/work-item-template.md). Numbers are never reused.
- `initiatives/<name>/status.md`, section `## Needs the user`: the only place
  you ask the user for a decision.

## States

| State | Means |
|---|---|
| `ready` | Can start now |
| `running` | An agent is working on it |
| `waiting` | Can't proceed; `waiting_on` says why |
| `review` | Output exists and its checks passed; not yet accepted |
| `failed` | Checks failed or the agent stopped; see Log |
| `accepted` | The user (or the lead, if the item allows it) accepted it |
| `superseded` | Replaced; `superseded_by` names the new item |

**Only the lead edits the item file**, including its state and Log. The
receiving agent reports through its handback.

`waiting_on` tells the kind of wait: another item id (a dependency), `user`
(paused for a decision on purpose), or anything else external (a print, a
measurement).

## Procedure

1. **Write.** Copy the template. Fill only sections with real content. Done
   when a fresh agent could start from the file and the files it lists, with
   no chat history. For modeling work, add the constraints brief from
   [scad-design-handoff](../scad-design-handoff/SKILL.md).
2. **Confirm with the user.** Before handing it out, show the user the goal,
   done-when, what the agent may decide alone and when it must stop and ask,
   with your recommended answer for each. Then set `confirmed: YYYY-MM-DD user`.
3. **Hand it out.** Set `state: running`, `executor` and a Log line, then
   give the agent one message: "Read `initiatives/<name>/work/NNN-slug.md`
   and do it. Use the handoff-implementer skill; hand back its packet." The
   agent can be a Claude Code subagent, or a new Claude Code or Codex session
   in a second terminal window opened in this folder.
4. **Review the handback.** Read the packet's Verdict, Not verified and Needs
   a call ([shared core](references/handback-packet.md)). Re-run the item's
   check yourself and look at the renders. Then set `review`, `failed`, or
   `waiting_on: user`. Put a one-line result in the Log.
5. **Ask the user only through Needs the user.** One entry per decision, at
   most 3, each with options and your recommendation.
6. **Resume cold.** Read `status.md`, then every item that is not `accepted`
   or `superseded`. For anything `running`, check whether its outputs exist
   before running it again.

## Rules

- One item, one id. A retry is a new Log line. If the goal changes, write a
  new item and mark the old one `superseded`.
- Keep these separate: the agent replied, output exists, checks passed,
  the user accepted.
- Log lines are append-only and dated.
- Do not ask the user many small questions; batch them and recommend answers.
