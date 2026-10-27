# Runbook: splitting work between agents (optional)

**Optional.** You never need this for a normal design: one agent in one
terminal handles the whole process. Use it when a project has two pieces of
work that can run at the same time, or when you want a second agent to check
the first one's work with fresh eyes.

Examples: one agent models the reference object while another builds the
blockout; a fresh agent reviews a design before you print it.

## The idea in one paragraph

The main agent (the **lead**) writes each piece of work into a file called a
**work item**. Another agent reads only that file, does the work, and sends
back a short **handback**: what it did, how it checked it, and what it could
not check. Because everything is in files, nothing depends on one chat
window staying open. The skills that define this are
[work-item](../skills/work-item/SKILL.md) (for the lead) and
[handoff-implementer](../skills/handoff-implementer/SKILL.md) (for the other agent).

## Steps

1. **Ask the lead to split the work.** For example: *"Use the work-item
   skill. Write a work item for the reference model so another agent can do
   it while you do the blockout."* The lead writes
   `initiatives/<project>/work/001-<slug>.md` and shows you the goal, the
   "done when" checks, and when the other agent must stop and ask. Confirm
   or change them.
2. **Start the second agent.** Pick one:
   - **Claude Code subagent**: the easiest. Tell the lead: *"Hand work item
     001 to a subagent."* It runs in the background in the same window, and
     you see only its handback.
   - **A second terminal window**: open a new Terminal window (⌘N), `cd`
     into the kit folder, and start `claude` or `codex` there. Paste:
     *"Read initiatives/<project>/work/001-<slug>.md and do it. Use the
     handoff-implementer skill; hand back its packet."* Use this when you
     want to watch it work or use Codex for one part.
   - **Codex**: works the same way in a second window. It reads `AGENTS.md`
     and the same skills (through `.agents/skills`).
3. **Bring the handback to the lead.** A subagent's handback arrives
   automatically. From a second window, copy the agent's final message into
   the lead's window. The lead re-runs the checks, looks at the renders,
   and tells you the result in a line or two.
4. **Decide.** The lead asks you only for real decisions, collected in the
   project's `status.md` under "Needs the user", with a recommendation each.

## Rules that keep it safe

- Two agents should never edit the same file at the same time. Each work
  item says which files it may touch.
- Only the lead updates `status.md`, `log.md` and the work item itself.
- "The agent says it's done" is not "it's checked". The lead re-runs the
  check before telling you.
- If an agent stops or its window closes, nothing is lost: the work item and
  its outputs are on disk. Ask the lead to resume from the work item.

## Fresh-eyes review

For a review before printing, ask the lead to use the
[independent-design-review](../skills/independent-design-review/SKILL.md)
skill. It gives a new agent only the renders and key facts, so its first
look is not coloured by the conversation.

## Scoping a vague idea

For a big or fuzzy idea, the [discovery](../skills/discovery/SKILL.md) skill
has an agent investigate first and write a short scoping note, without
changing anything, so you can decide what to build.
