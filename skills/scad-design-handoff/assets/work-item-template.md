---
id: NNN
state: ready
waiting_on:
executor:
from:
confirmed:
updated:
---
# <Title>

## Goal

<One paragraph. State what is not queued, for example no print.>

## Read first

- `<file>`: <what to take from it; FROZEN / superseded>

## Constraints brief

- Printer: <model, bed size, unusable bed areas> (my-printer.md)
- Nozzle / material / overhang limit: <values> (my-printer.md)
- Fit values from the user's coupons: <values, or "starting value, untested">
- Origin and axes: <definition>. Worked example: <one number traced end to end>
- Environment reference: <file and version, frozen>

## Shared helpers

- `<module/function>` in `<file>`: <what it returns, units>

## Tooling available

- `bin/openscad` (snapshot, Manifold); `bin/python` with numpy and Pillow; `bin/doctor`: <result>

## Design intent (<who>, <date>)

1. <decision>
2. <open choice, marked OPEN>

## Stage A: blockout (stop for the user's pick)

2–3 primitive variants placed against the reference model, actual-mesh renders
from the same cameras, key gaps by arithmetic, one line per variant. Hand
back and wait.

## Stage B: detailed model

Starts after the pick.

## Done when

- <check config passes: positive control, expansion case, named gaps>
- <bin/print-check.py passes on every STL>
- <renders inspected from evaluated meshes>

## Progress rule

Write `work/NNN-plan.md` before long computation; append one line per milestone
to the Log below.

## Decide alone

- <list>

## Escalate to the user when

- <list>

## Don't touch

- <list>

## Hand back

<Packet plus specific numbers wanted.>

## Log
- <date>: created (ready) by <lead>.
