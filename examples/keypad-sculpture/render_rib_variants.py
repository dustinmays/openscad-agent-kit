"""Export rib-field blockout parts as OFF per variant and render views from the meshes.

Run from the kit root:
    python3 examples/keypad-sculpture/render_ribs.py [plate-1 .. plate-4 C-backed-inset A B C]

Default: the Stage 4 plate options plate-1..4 plus a compare sheet. Reports, from
the meshes, the yellow part's connected bodies and volume and, for backed
labels, each rib's overlap with the plate (longest Y run with >= 2 mm X overlap).
"""
import importlib.util
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
repo = here.parents[1]
SOURCE = here / "ribs-blockout.scad"
REVISION = int(re.search(r"^ribs_blockout_revision\s*=\s*(\d+);",
                         SOURCE.read_text(), re.M).group(1))
spec = importlib.util.spec_from_file_location(
    "renderer", repo / "bin" / "render-views.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

PARTS = {  # name: RGB
    "ribs": [242, 194, 48],
    "black": [40, 40, 44],
    "blue": [159, 211, 242],
    "keypad_body": [167, 169, 172],
    "keypad_buttons": [90, 91, 94],
}
PLATES = {1: "soft inset", 2: "drip", 3: "blue echo", 4: "pool"}
VARIANTS = {  # label: (-D defines, caption)
    **{f"plate-{n}": ({"variant": '"C"', "backing": "true", "plate_style": str(n)},
                      f"C backed, organic plate {n}: {name}") for n, name in PLATES.items()},
    "C-backed-inset": ({"variant": '"C"', "backing": "true", "plate_style": "0"},
                       "C directional + 3 mm backing plate inset 6 mm at the ends (comb edge)"),
    "A": ({"variant": '"A"', "backing": "false"}, "A gentle: peak 18, long falloff (L 30)"),
    "B": ({"variant": '"B"', "backing": "false"}, "B steep pile-up: peak 24, short falloff (L 10)"),
    "C": ({"variant": '"C"', "backing": "false"},
          "C directional: B ahead of up-left motion, gentle (14, L 30) in the wake"),
}
PLATE_TINT = [196, 150, 30]  # review tint for the plate, same yellow part
CHECK_PARTS = ["plate", "ribs_bare"]  # exported for the overlap check only
RIB_COUNT, RIB_PITCH, RIB_WIDTH = 10, 7.8, 4  # as in ribs-blockout.scad
check = importlib.util.spec_from_file_location("check_keypad", here / "check_keypad.py")
check_keypad = importlib.util.module_from_spec(check)
check.loader.exec_module(check_keypad)  # reuse components() and volume_centroid()


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


def mesh_dir(v):
    return here / "exports" / f"ribs-blockout-v{REVISION}" / v


def export(variants):
    jobs = []
    for v in variants:
        defines = VARIANTS[v][0]
        mesh_dir(v).mkdir(parents=True, exist_ok=True)
        names = [*PARTS, *(CHECK_PARTS if defines["backing"] == "true" else [])]
        for name in names:
            out = mesh_dir(v) / f"{name}-v{REVISION}.off"
            args = [str(repo / "bin" / "openscad"), "-o", str(out),
                    "-D", f'show="{name}"', "-D", "export_frame=true"]
            for k, val in defines.items():
                args += ["-D", f"{k}={val}"]
            jobs.append(subprocess.Popen(args + [str(SOURCE)], stdout=subprocess.DEVNULL,
                                         stderr=subprocess.PIPE, text=True))
    for job in jobs:
        _, err = job.communicate()
        if job.returncode:
            raise SystemExit(err)


def view(angle, elevation=0):
    """Eye direction: orbit `angle` degrees right of front, raised `elevation` degrees."""
    a, e = math.radians(angle), math.radians(elevation)
    return [math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)]


def footprint(path, px=10):
    """Elevation XY footprint of a mesh as a boolean mask, `px` pixels per mm.

    Export frame: elevation X = x, elevation Y = z.
    """
    from PIL import Image, ImageDraw
    v, f = read_off(path)
    img = Image.new("1", (90 * px, 180 * px), 0)
    draw = ImageDraw.Draw(img)
    for tri in v[f][:, :, [0, 2]] * px:
        draw.polygon([tuple(p) for p in tri], fill=1)
    return np.asarray(img, bool)  # [row = Y, column = X]


def rib_overlaps(v, px=10):
    """Per rib: longest contiguous Y run (mm) where it overlaps the plate by >= 2 mm in X."""
    plate = footprint(mesh_dir(v) / f"plate-v{REVISION}.off", px)
    ribs = footprint(mesh_dir(v) / f"ribs_bare-v{REVISION}.off", px)
    runs = []
    for i in range(RIB_COUNT):
        xc = RIB_PITCH / 2 + i * RIB_PITCH
        cols = slice(round((xc - RIB_WIDTH / 2) * px), round((xc + RIB_WIDTH / 2) * px))
        ok = (ribs[:, cols] & plate[:, cols]).sum(1) >= 2 * px - 1  # 1 px raster slack
        best = cur = 0
        for flag in ok:
            cur = cur + 1 if flag else 0
            best = max(best, cur)
        runs.append(best / px)
    return runs


VIEWS = [
    (view(0), "front-elevation", "FRONT ELEVATION", (900, 1300)),
    (view(30), "oblique-30", "OBLIQUE 30° FROM RIGHT", (1000, 1300)),
    (view(60), "oblique-60", "OBLIQUE 60° FROM RIGHT", (1000, 1300)),
    (view(90), "side-right", "RIGHT SIDE PROFILE (wall at right)", (700, 1300)),
    (view(45, 45), "above-right-45", "45° FROM ABOVE-RIGHT", (1100, 1100)),
]
PLATE_VIEWS = VIEWS[:3]  # Stage 4: front, 30°, 60°


def compare_sheet(labels, out):
    """Rows = labels, columns = front and 30° renders."""
    from PIL import Image
    rows = [[Image.open(here / "renders" / f"ribs-blockout-v{REVISION}" / l / f"{s}-v{REVISION}.png")
             for s in ("front-elevation", "oblique-30")] for l in labels]
    w = max(sum(i.width for i in r) for r in rows)
    sheet = Image.new("RGB", (w, sum(max(i.height for i in r) for r in rows)), "white")
    y = 0
    for r in rows:
        x = 0
        for i in r:
            sheet.paste(i, (x, y))
            x += i.width
        y += max(i.height for i in r)
    sheet.save(out)

if __name__ == "__main__":
    variants = [a for a in sys.argv[1:] if a in VARIANTS] or [f"plate-{n}" for n in PLATES]
    export(variants)
    for v in variants:
        parts = [(*read_off(mesh_dir(v) / f"{n}-v{REVISION}.off"), c) for n, c in PARTS.items()]
        allv = np.concatenate([p[0] for p in parts])
        ribs, rib_faces = parts[0][0], parts[0][1]
        bodies = len(check_keypad.components(ribs, rib_faces))
        _, volume = check_keypad.volume_centroid(ribs, rib_faces)
        # Export frame: X right, -Y out of the wall, Z up (elevation Y).
        print(f"{v}: max depth {-allv[:, 1].min():.1f}  rib max {-ribs[:, 1].min():.1f}  "
              f"yellow bodies {bodies}  yellow volume {volume / 1000:.1f} cm3  X {allv[:, 0].min():.1f}..{allv[:, 0].max():.1f}")
        out = here / "renders" / f"ribs-blockout-v{REVISION}" / v
        out.mkdir(parents=True, exist_ok=True)
        if VARIANTS[v][0]["backing"] == "true":
            runs = rib_overlaps(v)
            print(f"   rib overlap runs (mm, >= 2 mm X): {[round(r, 1) for r in runs]}  "
                  f"min {min(runs):.1f}  {'OK' if min(runs) >= 10 else 'FAIL'} (need >= 10)")
        sub = f"Rib field blockout v{REVISION} | {VARIANTS[v][1]}"
        if v.startswith("plate-"):
            # Review only: draw the plate darker so its outline reads from the
            # front. The yellow is still one solid (checked above on "ribs").
            parts = [(*read_off(mesh_dir(v) / f"ribs_bare-v{REVISION}.off"), PARTS["ribs"]),
                     (*read_off(mesh_dir(v) / f"plate-v{REVISION}.off"), PLATE_TINT),
                     *parts[1:]]
            sub += " | plate tinted darker for review"
        for eye, slug, title, size in (PLATE_VIEWS if v.startswith("plate-") else VIEWS):
            renderer.render(parts, eye, size, title, sub, out / f"{slug}-v{REVISION}.png")
        print("renders:", out.relative_to(repo))
    plates = [v for v in variants if v.startswith("plate-")]
    if len(plates) > 1:
        sheet = here / "renders" / f"ribs-blockout-v{REVISION}" / f"compare-v{REVISION}.png"
        compare_sheet(plates, sheet)
        print("compare:", sheet.relative_to(repo))
