# Handback packet template

Write it like the body of a PR description. Keep it under about 300 words. No code blocks except short command output.

This extends the shared core in `skills/work-item/references/handback-packet.md`. Its Verdict, Verified, Not verified and Needs a call sections replace the Summary, Verification, Stopped or deviated and Open questions sections below; keep the rest.

```markdown
## Verdict
<checks out | checks out, with adjustments | does not check out | stopped>. <One sentence on why.>

## Not verified
- <what the tests and checks cannot see, or you could not run>

## Summary
<2–3 sentences: what you built, and whether it's done or stopped.>

## Scenario → test map
| Scenario | Tests | Result |
|---|---|---|
| <scenario name> | `test_a`, `test_b` | pass |
| <scenario name> | (gap: <outcome with no test>) | — |

## Files changed
- `path/to/file.py`: <what it does, one line>

## Verification
- `<check command>` → `<result line, e.g. 12 passed in 8s>`
- `<script command>` → <one-line summary of its output>

## Decisions beyond the handoff
- <choice, and why> (or "None")

## Stopped or deviated
- <what, and why> (or "None")

## Open questions and risks
- <question or risk for the lead> (or "None")

## Where to look first
- `path:line`: <the 1–3 spots most worth a human glance, and why>
```
