# Setup on a Mac

About 10–20 minutes, most of it downloads. You do this once.

## What you need

- A Mac. Apple Silicon (M1 or later) or Intel both work.
- An internet connection.
- Your Mac password (for installing software).
- An agent: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or
  [Codex](https://github.com/openai/codex). Install it with its own
  instructions and sign in before you start.

## 1. Open Terminal in the kit folder

Terminal is the Mac app where you type commands. Open it from
**Applications → Utilities → Terminal**, or press ⌘-Space and type
"Terminal".

Type `cd ` (with a space after it), drag the kit folder from Finder onto the
Terminal window, and press Return. Terminal now works "in" the kit folder.
To check, type `ls` and press Return; you should see `README.md`, `bin` and
the other files listed.

## 2. Run the setup script

Type this and press Return:

```sh
bin/setup
```

It does three things, and skips anything already installed:

1. **Homebrew** is the standard Mac tool for installing developer software.
   If you don't have it, the script asks before installing it. Homebrew asks
   for your Mac password; the letters do not appear as you type, which is normal.
2. **OpenSCAD** is the program that turns the model files into 3D shapes.
   The script installs the *development snapshot*, which has a much faster
   geometry engine (Manifold) than the older official release.
3. **Python packages**: numpy and Pillow, used by the check and picture
   scripts. They go into a private folder, `.venv`, inside the kit, so nothing
   else on your Mac changes.

At the end it runs the doctor (next step).

If your Mac says OpenSCAD "cannot be opened because the developer cannot be
verified", open **System Settings → Privacy & Security**, scroll down, click
**Open Anyway** for OpenSCAD, then run `bin/setup` again.

## 3. Check with the doctor

```sh
bin/doctor
```

Each line starts with `OK`, `FIX` or `note`:

- `OK`: that part works.
- `FIX`: something is missing. The next line says the one thing to do. Do
  it, then run `bin/doctor` again.
- `note`: optional or a reminder; nothing is broken.

When the last line says **All requirements OK**, you are done. A note that
`my-printer.md` is still the template is expected: the agent fills it in with
you at the start of your first project.

## 4. Start your agent

In the same Terminal window, in the kit folder, type `claude` or `codex` and
press Return. Then tell it what you want to make. Continue with
[guides/01-start-a-project.md](guides/01-start-a-project.md).

## If something goes wrong

- Run `bin/doctor` and do what the `FIX` lines say.
- Ask the agent: "bin/doctor says … what should I do?" It can read the
  output and help.
- An older OpenSCAD (for example the 2021 release) in your Applications folder
  will fail the doctor's Manifold check. Move it to the Trash and run
  `bin/setup` again.
- To start over with the Python packages, delete the `.venv` folder in the
  kit and run `bin/setup` again.
