"""Export blockout parts as OFF meshes and render review views from the actual meshes.

Run from the kit root:
    python3 examples/keypad-sculpture/render.py
"""
import importlib.util
import math
import subprocess
from pathlib import Path

import numpy as np

REVISION = 3
here = Path(__file__).resolve().parent
repo = here.parents[1]
spec = importlib.util.spec_from_file_location(
    "renderer", repo / "bin" / "render-views.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

PARTS = {  # name: RGB
    "yellow": [242, 194, 48],
    "black": [40, 40, 44],
    "blue": [159, 211, 242],
    "keypad": [167, 169, 172],
}


def read_off(path):
    """Line-based OFF reader; Manifold exports may append per-face RGB values."""
    lines = [l.split() for l in Path(path).read_text().splitlines() if l.strip()]
    assert lines[0] == ["OFF"]
    nv, nf = int(lines[1][0]), int(lines[1][1])
    vertices = np.asarray(lines[2:2 + nv], float)[:, :3]
    faces = []
    for row in lines[2 + nv:2 + nv + nf]:
        poly = list(map(int, row[1:1 + int(row[0])]))
        faces.extend([[poly[0], poly[j], poly[j + 1]] for j in range(1, len(poly) - 1)])
    return vertices, np.asarray(faces, dtype=int)


def export(mesh_dir):
    mesh_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    for name in PARTS:
        out = mesh_dir / f"{name}-v{REVISION}.off"
        jobs.append(subprocess.Popen(
            [str(repo / "bin" / "openscad"), "-o", str(out),
             "-D", f'part="{name}"', "-D", "export_frame=true",
             str(here / "blockout.scad")],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True))
    for job in jobs:
        _, err = job.communicate()
        if job.returncode:
            raise SystemExit(err)


def view(angle):
    """Eye direction for a horizontal orbit `angle` degrees right of front."""
    a = math.radians(angle)
    return [math.sin(a), -math.cos(a), 0]


if __name__ == "__main__":
    mesh_dir = here / "exports" / f"blockout-v{REVISION}"
    out = here / "renders" / f"blockout-v{REVISION}"
    out.mkdir(parents=True, exist_ok=True)
    export(mesh_dir)
    parts = [(*read_off(mesh_dir / f"{n}-v{REVISION}.off"), c)
             for n, c in PARTS.items()]
    for name, (v, _, _) in zip(PARTS, parts):
        lo, hi = v.min(0), v.max(0)
        print(f"{name:7s} X {lo[0]:6.1f}..{hi[0]:6.1f}  "
              f"out-of-wall {-hi[1]:5.1f}..{-lo[1]:5.1f}  Z {lo[2]:6.1f}..{hi[2]:6.1f}")
    sub = f"Blockout v{REVISION} | yellow envelope, black mass, blue wrap, gray keypad reference"
    views = [
        (0, "front-elevation", "FRONT ELEVATION (authoritative)", (900, 1300)),
        (30, "oblique-30", "OBLIQUE 30° FROM RIGHT", (1000, 1300)),
        (60, "oblique-60", "OBLIQUE 60° FROM RIGHT", (1000, 1300)),
        (90, "side-right", "RIGHT SIDE PROFILE (wall at right)", (700, 1300)),
        (-35, "oblique-left-35", "OBLIQUE 35° FROM LEFT", (1000, 1300)),
    ]
    for angle, slug, title, size in views:
        renderer.render(parts, view(angle), size, title, sub,
                        out / f"{slug}-v{REVISION}.png")
    print("renders:", out)
