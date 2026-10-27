"""Export the printable parts as ASCII STL in print pose, check them, render views.

Run from the kit root, after the geometry check (its model-frame meshes are
reused for the assembled and exploded renders):
    bin/python bin/scad-geometry-check.py examples/keypad-sculpture/geometry-check-config-v1.json
    bin/python examples/keypad-sculpture/build_parts.py

The mesh checks are bin/print-check.py, with the bed size and overhang limits
read from my-printer.md: closed 2-manifold, one body, flat on Z = 0, inside
the bed, overhang/bridge screen. Writes exports/parts-v<rev>/mesh-check-v<rev>.json.
Run bin/print-check.py on the STLs yourself before slicing, too (see README).
This is not a slicer check.
"""
import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
repo = here.parents[1]
SOURCE = here / "keypad-parts.scad"
REV = int(re.search(r"^parts_revision\s*=\s*(\d+);", SOURCE.read_text(), re.M).group(1))
OUT = here / "exports" / f"parts-v{REV}"
CHECKS = OUT / "checks"
PNG = here / "renders" / f"parts-v{REV}"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


renderer = load("renderer", repo / "bin" / "render-views.py")
ck = load("check_keypad", here / "check_keypad.py")      # read_off, components, volume_centroid
pc = load("print_check", repo / "bin" / "print-check.py")  # check_file, read_printer, read_ascii_stl

YELLOW, BLACK, BLUE = [242, 194, 48], [52, 52, 58], [159, 211, 242]
GREY, DARK = [167, 169, 172], [90, 91, 94]
PARTS = {  # STL name: (piece, colour, pose note)
    f"yellow-v{REV}": ("yellow_print", YELLOW, "plate back on the bed"),
    f"shell-v{REV}": ("shell_print", BLACK, "front face down (skin = first 4 layers)"),
    f"blue-v{REV}": ("blue_print", BLUE, "front face down, hex stubs up"),
}


def openscad(out, piece, fmt=None):
    args = [str(repo / "bin" / "openscad"), "--hardwarnings", "-o", str(out), "-D", f'piece="{piece}"']
    if fmt:
        args += ["--export-format", fmt]
    r = subprocess.run(args + [str(SOURCE)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    return [l for l in r.stderr.splitlines() if "pj_pose" in l]


def to_view(v, lift=0.0):
    """Elevation frame (Z out of the door) -> renderer frame (Z up, -Y toward the viewer)."""
    v = v + [0, 0, lift]
    return np.c_[v[:, 0], -v[:, 2], v[:, 1]]


def view(angle, elevation=0):
    a, e = math.radians(angle), math.radians(elevation)
    return [math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)]


if __name__ == "__main__":
    needed = [CHECKS / f"{n}-v{REV}.off" for n in ("yellow", "shell", "blue", "keypad", "keypad_buttons")]
    if not all(p.is_file() for p in needed):
        sys.exit("build_parts.py needs the geometry check's meshes first. From the kit root, run:\n"
                 "  bin/python bin/scad-geometry-check.py examples/keypad-sculpture/geometry-check-config-v1.json")
    OUT.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    printer, notes = pc.read_printer(repo / "my-printer.md")
    report = {"revision": f"v{REV}", "source": str(SOURCE.relative_to(repo)),
              "printer": printer, "defaults_used": notes,
              "not_a_slicer": "Mesh screen only (bin/print-check.py); slice and preview before printing.",
              "parts": {}}
    meshes = {}
    for name, (piece, colour, note) in PARTS.items():
        stl = OUT / f"{name}.stl"
        poses = openscad(stl, piece, "asciistl")
        r = pc.check_file(stl, printer)
        meshes[name] = pc.read_ascii_stl(stl)
        r["pose"] = note
        if poses:
            r["pin_poses"] = [p.split("ECHO: ")[-1].strip('"') for p in poses]
        report["parts"][name] = r
    report["pass"] = all(p["pass"] for p in report["parts"].values())
    (OUT / f"mesh-check-v{REV}.json").write_text(json.dumps(report, indent=2) + "\n")
    for name, r in report["parts"].items():
        print(("PASS " if r["pass"] else "FAIL ") + name, r["size_xyz_mm"], "mm",
              [k for k, ok in r["checks"].items() if not ok] or "")
    print("PASS" if report["pass"] else "FAIL")

    # Print poses, from the exact STLs.
    for name, (piece, colour, note) in PARTS.items():
        v, f = meshes[name]
        renderer.render([(v, f, colour)], [0.5, -1, 0.8], (1000, 1000), f"PRINT POSE: {name}",
                        f"{note} | bed Z = 0 | from the exact STL", PNG / f"{name}-print.png")
        renderer.render([(v, f, colour)], [0.4, -1, -0.7], (1000, 1000), f"PRINT POSE FROM BELOW: {name}",
                        "bed-side faces", PNG / f"{name}-print-below.png")

    v, f = meshes[f"blue-v{REV}"]
    renderer.render([(v, f, BLUE)], [0.15, -0.35, 1], (1000, 1000), f"PRINT POSE FROM ABOVE: blue-v{REV}",
                    "2 hex stubs (AF 3, 4 mm) stand on the cap back; they drop into the shell sockets",
                    PNG / f"blue-v{REV}-print-above.png")

    # Assembled and exploded, from the geometry check's model-frame meshes.
    m = {n: ck.read_off(CHECKS / f"{n}-v{REV}.off") for n in ("yellow", "shell", "blue", "keypad", "keypad_buttons")}
    def scene(lifts=None):
        lifts = lifts or {}
        return [(to_view(m[n][0], lifts.get(n, 0)), m[n][1], c) for n, c in
                (("yellow", YELLOW), ("keypad", GREY), ("keypad_buttons", DARK), ("shell", BLACK), ("blue", BLUE))]
    sub = f"Keypad parts v{REV} | yellow, black shell, blue; keypad reference in grey"
    for slug, title, eye, size in [("front", "ASSEMBLED FRONT", view(0), (900, 1300)),
                                   ("oblique-30", "ASSEMBLED 30° FROM RIGHT", view(30), (1000, 1300)),
                                   ("oblique-60", "ASSEMBLED 60° FROM RIGHT", view(60), (1000, 1300)),
                                   ("side-right", "ASSEMBLED RIGHT SIDE (door at right)", view(90), (700, 1300))]:
        renderer.render(scene(), eye, size, title, sub, PNG / f"assembled-{slug}-v{REV}.png")
    renderer.render(scene({"keypad": 35, "shell": 70, "blue": 95}), view(30, 25), (1100, 1300),
                    "EXPLODED 30° (pull straight off the door)",
                    "yellow on the door | keypad on the rib tops | shell over it | blue glued to the shell",
                    PNG / f"exploded-v{REV}.png")
    print("renders:", PNG.relative_to(repo))
    sys.exit(0 if report["pass"] else 1)
