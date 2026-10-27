---
name: project-operating-model
description: Use when creating or maintaining a project. Keep project context navigable, lightweight, and easy for agents to rediscover.
---

# Project Operating Model

Use this structure for long-running projects that accumulate context over time, such as a series of 3D-printed designs.

The goal is not to keep every detail in the agent's active context. The goal is to make the right information cheap to rediscover.

## Core Principles

1. Use progressive disclosure.
2. Separate durable knowledge from active work.
3. Separate current state from historical records.
4. Distinguish facts from human observations.
5. Avoid duplicate competing copies of information.
6. Create files and directories only when they become useful.
7. No-change is a valid outcome; do not create documentation churn.

## Standard Project Structure

```text
project/
├── README.md
├── AGENTS.md
├── PROJECT_STATE.md
│
├── docs/
│   └── AGENTS.md                  # optional; only if behavior differs here
│
├── initiatives/
│   ├── AGENTS.md                  # optional shared initiative rules
│   │
│   └── example-initiative/
│       ├── README.md
│       ├── AGENTS.md              # optional local rules
│       ├── status.md
│       ├── log.md
│       ├── observations.md
│       └── deferred/
│           └── item.md
│
└── archive/
    └── initiatives/
```

Do not create empty directories or placeholder files merely to satisfy the structure.

## Agent Instruction Files

`AGENTS.md` files define agent behavior. They must not become general project documentation.

The root `AGENTS.md` should describe rules such as:

- how to navigate the project
- which files are authoritative
- how to distinguish facts from observations
- when to update state
- when to promote knowledge into `docs/`
- how to avoid unnecessary file churn

Nested `AGENTS.md` files are optional. Add one only when a folder has behavior that differs from its parent.

Typical locations are:

```text
project/AGENTS.md
project/docs/AGENTS.md
project/initiatives/AGENTS.md
project/initiatives/example-initiative/AGENTS.md
```

Do not add an `AGENTS.md` to every folder by default.

## Root Files

### `README.md`

The project front door.

It should briefly explain:

- what the project is
- its scope
- major goals and constraints
- where important information lives
- links to the most relevant files

Keep it stable and concise. It is not a chronological diary.

### `PROJECT_STATE.md`

A small routing file showing the current state of the project.

Use sections such as:

```markdown
# Project State

Updated: YYYY-MM-DD

## Active

- [Initiative name](initiatives/example-initiative/) — current position

## Blocked

- [Initiative name](initiatives/example-initiative/) — blocking condition

## Dormant

- [Initiative name](initiatives/example-initiative/) — why it is paused

## Recently Completed

- [Initiative name](archive/initiatives/example-initiative/)
```

Keep this file small. Older completed initiatives belong in `archive/initiatives/`.

## Durable Knowledge

### `docs/`

`docs/` answers:

> What do we know?

Use it for reusable, relatively canonical project knowledge, including:

- measurements
- specifications
- established constraints
- compatibility information
- validated findings
- durable decisions
- reference material

Documents may use frontmatter such as:

```yaml
---
status: current
created: YYYY-MM-DD
updated: YYYY-MM-DD
superseded_by:
related:
---
```

Suggested statuses:

- `current` — believed accurate and usable
- `superseded` — intentionally replaced by newer information
- `stale` — may no longer be accurate; verify before relying on it
- `historical` — accurately describes a previous state but is not current

Age alone does not make information stale.

## Initiatives

An initiative is a bounded effort to:

- accomplish something
- investigate something
- make a decision
- change part of the project
- resolve an uncertainty

Initiatives should eventually become completed, abandoned, dormant, or archived.

Typical lifecycle:

```text
proposed → active → blocked/dormant → completed/abandoned
```

An initiative folder contains the working context for that effort.

### Initiative `README.md`

The initiative README should answer:

- What are we trying to accomplish?
- Why does it matter?
- What counts as success?
- What constraints apply?
- What is explicitly out of scope?

Keep it relatively stable.

### Initiative `status.md`

`status.md` is the current, rewriteable snapshot of the initiative.

It should contain enough information for an agent to resume work without reading the entire history.

Recommended sections:

```markdown
# Current Status

Last updated: YYYY-MM-DD

## Goal

What this initiative is trying to accomplish.

## Current Position

What is currently known, decided, or underway.

## Constraints

- Important limitation
- Required compatibility
- Budget, timing, safety, or scope constraint

## Open Questions

- Unresolved question
- Missing evidence
- Decision still required

## Next Likely Action

The most useful next step if work resumes.
```

Rewrite `status.md` after meaningful transitions. Do not use it as an append-only journal.

### Initiative `log.md`

`log.md` is the append-only historical record.

Use dated sections:

```markdown
## YYYY-MM-DD

- Meaningful action taken
- Finding or decision recorded
- State transition
```

Do not load `log.md` merely to understand the current state. Read it when historical reconstruction is necessary.

### Initiative `observations.md`

`observations.md` contains append-only human observations, experiences, intuitions, and subjective impressions.

Observations are evidence, not automatically verified facts.

Example:

```markdown
## YYYY-MM-DD

The front wheel felt unstable on rough descents today.
This may justify investigating additional front-end control.
```

Do not promote observations directly into canonical documentation without validation.

### Initiative `deferred/`

`deferred/` is an attention queue for useful but currently out-of-scope material.

Create it only when needed. Deferred items stay inside the relevant initiative rather than interrupting the active work.

Use it to prevent two problems:

1. losing potentially useful discoveries
2. derailing current work with tangents

A deferred item should have minimal metadata:

```yaml
---
created: YYYY-MM-DD
status: deferred
tags:
  - relevant-topic
related:
  - related-initiative-or-document
revisit_when:
  - selecting the final option
  - beginning the next phase
---
```

Then include a short explanation of the deferred idea.

A deferred item is not canonical knowledge. When its trigger occurs, investigate it, promote it, discard it, or defer it again.

## Navigation Order

When entering a project, use progressive disclosure:

```text
README.md
  ↓
PROJECT_STATE.md
  ↓
nearest relevant AGENTS.md
  ↓
initiative README.md and status.md
  ↓
relevant docs/
  ↓
logs, observations, deferred items, or archive only when needed
```

Do not recursively read the entire project tree by default.

## Knowledge Lifecycle

Information generally moves through these stages:

```text
human observation
  ↓
initiative working knowledge
  ↓
validation or confirmation
  ↓
durable reusable knowledge
  ↓
canonical documentation in docs/
```

When a finding becomes useful beyond one initiative:

1. promote it into `docs/`
2. update the canonical document
3. reference the canonical location from the initiative
4. remove or avoid duplicate competing copies

Prefer links and references over repeated copies of the same fact.

## Updating State

When meaningful initiative state changes:

1. rewrite the initiative's `status.md`
2. update `PROJECT_STATE.md` if the initiative changed between active, blocked, dormant, or completed
3. append a concise entry to `log.md` if historical reconstruction may matter

Do not update files merely because time has passed.

## Closing an Initiative

When an initiative is completed or abandoned:

1. identify durable findings
2. promote reusable knowledge into `docs/`
3. finalize `status.md`
4. record the final outcome in `log.md`
5. update `PROJECT_STATE.md`
6. move the initiative to:

```text
archive/initiatives/
```

The archive should remain discoverable but should not normally be part of active context.

## Maintenance Rules

Maintenance is event-driven, not calendar-driven.

Review or update project files when:

- new evidence contradicts existing information
- related work touches the material
- an initiative changes state
- an initiative closes
- a canonical fact changes
- duplicate or conflicting documentation appears

Do not reorganize the project merely because a file is old.

After working in a project, explicitly determine whether:

- durable knowledge changed
- initiative state changed
- a deferred item should be created
- historical context should be recorded
- no documentation change is necessary

No-change is a valid result.

## Common Mistakes to Avoid

- Reading the entire project tree before starting.
- Treating `status.md` as an append-only log.
- Treating `log.md` as the current state.
- Treating observations as verified facts.
- Putting project knowledge into `AGENTS.md`.
- Creating nested `AGENTS.md` files without behavior differences.
- Leaving completed initiatives in the active project-state list indefinitely.
- Promoting unvalidated observations directly into `docs/`.
- Creating deferred items without a reason or `revisit_when` trigger.
- Maintaining duplicate copies of the same authoritative information.
- Rewriting files when nothing meaningful changed.

## Design Goal

The project filesystem should function as an external cognitive environment:

- understandable by a human
- navigable by an agent
- lightweight to maintain
- resistant to context bloat
- capable of preserving useful history
- easy to evolve incrementally

The fundamental rule is:

> Make the right information cheap to rediscover rather than keeping all information permanently present.
