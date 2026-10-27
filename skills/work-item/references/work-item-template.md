# Work item template

Copy to `work/NNN-slug.md`. Delete any section without real content.

```markdown
---
id: NNN
state: ready            # ready | running | waiting | review | failed | accepted | superseded
waiting_on:             # item id, `user`, or an external thing; only when waiting
executor:               # agent session name, `process: <command>`, or `user`
from:                   # who wrote it (lead session name)
confirmed:              # YYYY-MM-DD user, set only after they answer the confirmation form; handoffs are blocked until then
updated: YYYY-MM-DD
superseded_by:          # only when superseded
---
# <Goal in one line>

## Goal
<One or two sentences: what done looks like, and why it matters.>

## Read first
- `path`: <why>

## Done when
- `<check command>` passes
- `bin/print-check.py` passes on every STL; renders inspected
- <any check a human must make>

## Decide alone
- <choices the executor may make without asking>

## Escalate to the user when
- <conditions that need his judgment; stop and hand back>

## Don't touch
- <files, tests, or areas owned by someone else>

## Hand back
The role skill's packet (handoff-implementer; shared core in `skills/work-item/references/handback-packet.md`), plus: <anything item-specific>.

## Log
- YYYY-MM-DD HH:MM TZ: created (ready)
```
