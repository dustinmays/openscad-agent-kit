---
name: project-operating-model
description: Use when creating or maintaining a project. Keep project context navigable, lightweight, and easy for agents to rediscover.
---

# Project Operating Model

Use the filesystem as persistent project context. Make the right information
cheap to rediscover; avoid loading or duplicating the entire history.

Read the [full operating model](references/project-operating-model.md) when
setting up project structure, changing its lifecycle or deciding where knowledge
belongs. It covers the file roles, lifecycle, deferred-item metadata and the
closing workflow. In this kit, each design project is an initiative under
`initiatives/`; [start-a-project](../start-a-project/SKILL.md) creates one.

## Resume work with progressive disclosure

Read the root README and PROJECT_STATE, then relevant agent instructions and the
initiative README/status. Load only relevant canonical documents next. Read
logs, observations, deferred material and archives when the task requires them.
An existing project can adopt this incrementally; missing files do not require
creating placeholders or a wholesale documentation rewrite.

## Maintain the right kind of record

- Keep agent behavior in `AGENTS.md`, stable project scope in README files,
  current routing in `PROJECT_STATE.md`, and reusable canonical knowledge in
  `docs/`.
- Rewrite initiative `status.md` for current state. Append meaningful history to
  `log.md` and human evidence to `observations.md`; do not equate observations
  with validated facts.
- Create initiative-local `deferred/` items only for useful out-of-scope material
  with a reason and a revisit trigger. Create nested instructions only for
  behavior that differs from the parent.
- Promote validated findings useful beyond one initiative into `docs/`; link to
  the canonical location and avoid competing copies.
- When initiative state changes, update its status and project routing as needed;
  append a log entry if historical reconstruction matters.
- When closing work, preserve durable findings, finalize state/history and move
  the initiative under `archive/initiatives/`. Keep the archive discoverable.

After work, explicitly decide whether knowledge, state, history or deferred work
changed. No-change is a valid outcome. Maintenance follows meaningful events,
not the calendar, and age alone does not make information stale.
