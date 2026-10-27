# Handback packet: shared core

Every role hands back this core, then its own sections (see the role skill's `references/handback-template.md`). The packet exists so the lead and the user can decide without rereading the work. Write it like a PR description: conclusions and pointers, under about 300 words, no diffs, no long logs.

```markdown
## Verdict
<One of: checks out | checks out, with adjustments | does not check out | stopped>. <One sentence on why.>

## Verified
- `<command>` → `<result>` (what was actually run, and what it showed)

## Not verified
- <what the checks cannot see, was skipped, or you could not run>

## Assumptions and decisions beyond the handoff
- <choice or assumption, and why> (or "None")

## Needs a call
- <decision for the lead or the user, with your recommendation> (or "None")

## Where to look first
- `path:line`: <the 1–3 spots most worth a human glance, and why>
```

## Rules

- **Verdict first.** Use "checks out" only when every item under Done when passed on a run you can name. Otherwise say what is off.
- **"Not verified" is never decoration.** Name the real gaps (inputs no case covers, behavior only checked by the agent's own reading, anything the executor could not run). If you cannot think of any, say what the checks cannot prove.
- **Evidence is commands and results**, not "I confirmed". The lead re-runs the check; the packet tells them which one.
- **Don't summarize your own reasoning.** The reviewer and the human judge the work and the spec, not your story about it.

## How the lead reads it

Read Verdict, Not verified and Needs a call. Re-run the check. Read code only if the check fails, the verdict is not "checks out", or the user asks. Pass the user only what needs their judgment: the Needs a call items, and any Not verified gap that matters to them.
