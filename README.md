# openscad-agent-kit

Design 3D-printed parts by talking to an AI agent: from "I want to make X
that fits my Y" to a printed, checked part.

You describe what you want and answer questions. The agent (Claude Code or
Codex) writes the OpenSCAD model, shows you pictures of the real geometry,
checks the parts for printing problems, and gives you a print sheet. You
need no programming. You will need a Mac, a 3D printer and some patience for
a test print or two.

The defaults suit a typical printer with a 0.4 mm nozzle printing PLA or PETG.
You tell the agent about your own printer once, and it records it in
[my-printer.md](my-printer.md).

## Start in 5 minutes

1. **Get the kit onto your Mac.** On the kit's GitHub page, click
   **Code → Download ZIP**. Double-click the ZIP in your Downloads folder to
   unzip it, and move the folder somewhere you will find it again, such as
   `Documents/openscad-agent-kit`. Then open Terminal in that folder
   ([SETUP.md](SETUP.md) step 1 shows how).
   *If you use Git:* click **Use this template** to make your own copy on
   GitHub, then `git clone` it instead.
2. **Set up the tools.** Follow [SETUP.md](SETUP.md). It is one command:
   `bin/setup`. It installs OpenSCAD and the Python pieces, then runs
   `bin/doctor` to check that everything works.
3. **Open your agent in the folder.** In Terminal: `cd` into the kit folder,
   then type `claude` (Claude Code) or `codex` (Codex).
4. **Say what you want to make.** For example: *"I want to make a holder
   for my TV remote that screws under my desk."* The agent will ask about
   your printer first, then about the object.
5. **Read [guides/01-start-a-project.md](guides/01-start-a-project.md)** while
   you wait. It explains what happens next.

## How it works

| Step | Guide | What you do |
| --- | --- | --- |
| 1 | [Start a project](guides/01-start-a-project.md) | Describe the idea; share a sketch or photo |
| 2 | [Measure](guides/02-measure.md) | Measure the real object the part must fit |
| 3 | [Blockouts](guides/03-blockouts.md) | Pick from rough shapes; ask for changes |
| 4 | [Fit coupons](guides/04-fit-coupons.md) | Print a small test piece; say which fit is best |
| 5 | [Printable parts](guides/05-printable-parts.md) | The agent makes the parts and checks them |
| 6 | [Print handoff](guides/06-print-handoff.md) | Follow `PRINT.md` at the printer |
| 7 | [Report results](guides/07-report-results.md) | Tell the agent how it went |

Optional: [splitting work between several agents](guides/runbook-multi-agent.md).

## A worked example

[examples/keypad-sculpture/](examples/keypad-sculpture/) is a real project
made with this process: a wall sculpture that holds a door-lock keypad. It
went from a pencil sketch to three printed, assembled parts.
[STORY.md](examples/keypad-sculpture/STORY.md) tells how it went, and every guide points to its step.

## What is in here

- `bin/`: the tools (setup, doctor, OpenSCAD launcher, render and check scripts).
- `skills/`: instructions the agent loads for each step (Claude Code and Codex share them).
- `guides/`: short guides for you, the person.
- `docs/`: reference for printability and how files are organised.
- `lib/`: reusable OpenSCAD pieces: glued pin joints and breakaway print fins.
- `initiatives/`: your projects go here, one folder each.
- `examples/`: the worked example.

## Licence

MIT; see [LICENSE](LICENSE).
