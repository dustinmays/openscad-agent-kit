---
name: scad-design-handoff
description: Write the work item that hands an OpenSCAD design task to another agent, with a pre-digested constraints brief, shared geometry helpers and a checkable done-when. Use before dispatching modeling work; the work-item and handoff-implementer skills cover the protocol around it.
---

# SCAD design handoff

Builds on the [work-item](../work-item/SKILL.md) and
[handoff-implementer](../handoff-implementer/SKILL.md) skills, which define
states, dispatch and the hand-back packet. This skill adds what a modeling
agent needs so it spends its time on geometry, not on rediscovery.

Why: implementers lose most of their time re-deriving transforms, hitting a
missing Python package, and re-reading printability docs to recover printer
facts. Put those facts in the item.

## Start with a blockout stage

Every new design or big shape change begins with a **blockout**: 2–3 rough
variants from simple primitives, placed against the real object, rendered
from the same cameras. Detailed modeling starts only after the user picks.
See [blockout-and-review](../blockout-and-review/SKILL.md). Skip it only for
parameter-only revisions of an accepted shape.

## Write the item from [the template](assets/work-item-template.md)

Save it as `initiatives/<name>/work/NNN-<slug>.md`. Required sections:

1. **Goal**: one paragraph, and what is explicitly *not* included (prints).
2. **Read first**: exact files, what to take from each, and which are frozen
   or superseded. Link; do not paste.
3. **Constraints brief**: copy these facts *into the item*, citing the source:
   - printer, bed size, nozzle and material, from `my-printer.md`;
   - overhang limit and unusable bed areas;
   - fit values the user's coupons established (or "starting value, untested");
   - the coordinate origin for every quoted number, plus one worked example;
   - the measurement table revision in use.
4. **Shared helpers**: the module and function names to reuse. If a
   transform lives only in an old study file, move it into a shared `.scad`
   first.
5. **Tooling**: `bin/openscad` (snapshot, Manifold), `bin/python` with numpy
   and Pillow. Run `bin/doctor` once before dispatch and state the result.
6. **Design intent**: decisions already made, with date and who made them.
   Mark open choices as OPEN.
7. **Done when**: checkable, for example: the check config passes; the
   positive control collides; named gaps are reported; `bin/print-check.py`
   passes; renders are inspected from the evaluated meshes.
8. **Decide alone / Escalate / Don't touch**.
9. **Hand back**: the packet, plus the specific numbers you want.

## Make progress visible

Tell the agent, in the item:

- Save the geometry plan and key numbers to `work/NNN-plan.md` **before**
  long computation, then report one line per milestone.
- For large tasks, split into stages that each end in something you can look
  at, with one render each.

## Before dispatch

- [ ] The constraints brief matches `my-printer.md` today.
- [ ] Shared helpers exist and can be `use`d from the new file.
- [ ] `bin/doctor` passes.
- [ ] The user confirmed scope and escalation rules (`confirmed:` set).

## After the hand-back

The lead re-runs the check, looks at the renders, and updates the project's
`status.md` and `log.md`; the implementer does not.
