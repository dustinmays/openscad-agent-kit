"""Export the keypad reference parts as OFF, check them from the meshes, render views.

Run from the kit root:
    python3 examples/keypad-sculpture/check_keypad.py [--no-render]

Checks read the exported meshes (SCAD frame: origin body lower-left on the
back plane, Y up). Expected values come from MEASUREMENTS.md rev 2; the
parameterised values (recess inset/depth ASSUMED, button proud B6) are read
from the SCAD source so the check follows whatever is set there.
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
SOURCE = here / "keypad-reference.scad"
BLOCKOUT = here / "blockout.scad"
TOL = 0.05

# MEASUREMENTS.md rev 2
K1, K2, K3, K8 = 34.5, 94.5, 25.7, 2.0
B1, B3, B4, B5 = 10.8, 15.2, 14.9, (9.7, 9.7)
BLOCKOUT_KEYPAD_LL = (19, 33.5)

COLORS = {"body": [167, 169, 172], "buttons": [90, 91, 94],
          "led": [110, 220, 130], "velcro": [232, 226, 208]}
BLOCKOUT_COLORS = {"yellow": [242, 194, 48], "black": [40, 40, 44],
                   "blue": [159, 211, 242]}


def scad_param(name):
    m = re.search(rf"^{name}\s*=\s*([-\d.]+);", SOURCE.read_text(), re.M)
    return float(m.group(1))


def int_param(path, name):
    return int(re.search(rf"^{name}\s*=\s*(\d+);", Path(path).read_text(), re.M).group(1))


REVISION = int_param(SOURCE, "keypad_reference_revision")
BLOCKOUT_REV = int_param(BLOCKOUT, "blockout_revision")
MESH_DIR = here / "exports" / f"keypad-reference-v{REVISION}"
RENDER_DIR = here / "renders" / f"keypad-reference-v{REVISION}"
REPORT = MESH_DIR / f"keypad-check-v{REVISION}.json"


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


def export_all():
    """(output name, source, defines) for every mesh this script needs."""
    jobs = []
    for p in COLORS:
        jobs.append((f"{p}-v{REVISION}.off", SOURCE, {"part": f'"{p}"'}))
        jobs.append((f"{p}-elevation-v{REVISION}.off", SOURCE,
                     {"part": f'"{p}"', "in_elevation": "true", "export_frame": "true"}))
    for p in [*BLOCKOUT_COLORS, "keypad"]:
        jobs.append((f"blockout-{p}-v{BLOCKOUT_REV}.off", BLOCKOUT,
                     {"part": f'"{p}"', "export_frame": "true"}))
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    procs = []
    for out, src, defines in jobs:
        args = [str(repo / "bin" / "openscad"), "--hardwarnings", "-o", str(MESH_DIR / out)]
        for k, v in defines.items():
            args += ["-D", f"{k}={v}"]
        procs.append(subprocess.Popen(args + [str(src)], stdout=subprocess.DEVNULL,
                                      stderr=subprocess.PIPE, text=True))
    for p in procs:
        _, err = p.communicate()
        if p.returncode:
            raise SystemExit(err)


def components(vertices, faces):
    """Split a triangle mesh into connected bodies (vertices merged by position)."""
    key = np.round(vertices, 5)
    _, ids = np.unique(key, axis=0, return_inverse=True)
    ids = ids.ravel()
    parent = list(range(ids.max() + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for f in ids[faces]:
        for b in f[1:]:
            ra, rb = find(f[0]), find(b)
            if ra != rb:
                parent[rb] = ra
    roots = np.array([find(ids[f[0]]) for f in faces])
    return [faces[roots == r] for r in np.unique(roots)]


def volume_centroid(vertices, faces):
    a, b, c = (vertices[faces[:, i]] for i in range(3))
    vol = np.einsum("ij,ij->i", a, np.cross(b, c)) / 6
    return (vol[:, None] * (a + b + c) / 4).sum(0) / vol.sum(), vol.sum()


def check():
    inset = scad_param("recess_inset")
    depth = scad_param("recess_depth")
    proud = scad_param("button_proud")
    checks, data = {}, {}

    def close(a, b, tol=TOL):
        return bool(np.all(np.abs(np.asarray(a, float) - np.asarray(b, float)) <= tol))

    # Body
    bv, bf = read_off(MESH_DIR / f"body-v{REVISION}.off")
    lo, hi = bv.min(0), bv.max(0)
    data["body_bbox"] = (hi - lo).round(3).tolist()
    checks["body_bbox_K1_K2_K3"] = close(lo, [0, 0, 0]) and close(hi, [K1, K2, K3])
    checks["body_single_component"] = len(components(bv, bf)) == 1
    # Recess: the only vertices off the back plane below Z 3 are the recess floor.
    low = bv[(bv[:, 2] > 1e-3) & (bv[:, 2] < 3)]
    floor_z = np.unique(low[:, 2].round(4))
    floor = low[np.isclose(low[:, 2], depth, atol=1e-3)]
    data["recess_floor_z"] = floor_z.tolist()
    data["recess_floor_xy_bbox"] = [floor[:, :2].min(0).round(3).tolist(),
                                    floor[:, :2].max(0).round(3).tolist()]
    checks["recess_depth"] = len(floor_z) == 1 and close(floor_z[0], depth)
    checks["recess_inset"] = (close(floor[:, :2].min(0), [inset, inset])
                              and close(floor[:, :2].max(0), [K1 - inset, K2 - inset]))
    back = bv[np.isclose(bv[:, 2], 0, atol=1e-4)]
    # Back rim ring must still reach the outline (recess is not a through-cut).
    checks["back_rim_present"] = close(back[:, :2].min(0), [0, 0]) and close(
        back[:, :2].max(0), [K1, K2])

    # Buttons
    uv, uf = read_off(MESH_DIR / f"buttons-v{REVISION}.off")
    comps = components(uv, uf)
    table = [(B5[0] + (i % 2) * B3, B5[1] + (i // 2) * B4) for i in range(12)]
    expected = sorted([(x, K2 - y) for x, y in table], key=lambda p: (-p[1], p[0]))
    found = []
    for cf in comps:
        c, _ = volume_centroid(uv, cf)
        vv = uv[np.unique(cf)]
        found.append({"centroid_xy": c[:2].round(4).tolist(),
                      "dia_x": round(float(np.ptp(vv[:, 0])), 3),
                      "z": [round(float(vv[:, 2].min()), 3), round(float(vv[:, 2].max()), 3)]})
    found.sort(key=lambda d: (-round(d["centroid_xy"][1], 1), d["centroid_xy"][0]))
    errors = [math.dist(f["centroid_xy"], e) for f, e in zip(found, expected)]
    data["buttons"] = [{"index": i, "table_xy": list(t), **f, "error_mm": round(e, 4)}
                       for i, (t, f, e) in enumerate(zip(table, found, errors))]
    checks["buttons_12_components"] = len(comps) == 12
    checks["button_centroids_within_0.05"] = len(comps) == 12 and max(errors) <= TOL
    checks["button_diameter_B1"] = all(close(f["dia_x"], B1, 0.1) for f in found)
    checks["button_tops_K3_plus_B6"] = all(close(f["z"][1], K3 + proud) for f in found)

    # LED (context): inside the flat face, clear of the buttons, at the face plane.
    lv, lf = read_off(MESH_DIR / f"led-v{REVISION}.off")
    lc, _ = volume_centroid(lv, lf)
    led_r = np.ptp(lv[:, 0]) / 2
    flat = K8 + led_r
    data["led_centroid_xy_scad"] = lc[:2].round(3).tolist()
    data["led_z"] = [round(float(lv[:, 2].min()), 3), round(float(lv[:, 2].max()), 3)]
    checks["led_inside_flat_face"] = bool(
        flat <= lc[0] <= K1 - flat and flat <= lc[1] <= K2 - flat
        and lv[:, 2].min() < K3 < lv[:, 2].max())
    checks["led_clear_of_buttons"] = min(math.dist(lc[:2], e) for e in expected) > B1 / 2 + led_r

    # Velcro (optional part): on the recess floor, inside the recess outline.
    vv, _ = read_off(MESH_DIR / f"velcro-v{REVISION}.off")
    data["velcro_z"] = [round(float(vv[:, 2].min()), 3), round(float(vv[:, 2].max()), 3)]
    checks["velcro_in_recess"] = bool(vv[:, 2].max() >= depth and np.all(vv[:, :2].min(0) >= inset)
                                      and np.all(vv[:, :2].max(0) <= [K1 - inset, K2 - inset]))

    # Elevation placement vs blockout keypad (both in export frame: X, -Z_wall, Y).
    ev, _ = read_off(MESH_DIR / f"body-elevation-v{REVISION}.off")
    kv, _ = read_off(MESH_DIR / f"blockout-keypad-v{BLOCKOUT_REV}.off")
    data["elevation_body_bbox"] = [ev.min(0).round(3).tolist(), ev.max(0).round(3).tolist()]
    data["blockout_keypad_bbox"] = [kv.min(0).round(3).tolist(), kv.max(0).round(3).tolist()]
    checks["elevation_matches_blockout_keypad"] = close(ev.min(0), kv.min(0)) and close(
        ev.max(0), kv.max(0))
    checks["elevation_lower_left"] = close(ev.min(0)[[0, 2]], BLOCKOUT_KEYPAD_LL)

    report = {
        "revision": f"v{REVISION}",
        "source": str(SOURCE.relative_to(repo)),
        "measurements": "MEASUREMENTS.md rev 2 (draft)",
        "assumed": {"recess_inset_K7": inset, "recess_depth_K6": depth},
        "reported": {"button_proud_B6": proud},
        "blockout_revision": BLOCKOUT_REV,
        "tolerance_mm": TOL,
        "pass": all(checks.values()),
        "checks": {k: bool(v) for k, v in checks.items()},
        "data": data,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    return report


def render():
    spec = importlib.util.spec_from_file_location(
        "renderer", repo / "bin" / "render-views.py")
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    kp = [(*read_off(MESH_DIR / f"{p}-v{REVISION}.off"), COLORS[p])
          for p in ["body", "buttons", "led"]]
    sub = (f"Keypad reference v{REVISION} | 34.5 x 94.5 x 25.7 | buttons proud "
           f"{scad_param('button_proud')} (B6) | recess 2 in, 1.75 deep (ASSUMED K7/K6)")
    s = 1 / math.sqrt(3)
    views = [  # SCAD frame: Y up, Z out of the face
        ([0, 0, 1], "front", "FRONT (face, button 1 upper-left)", (700, 1300)),
        ([0.45, 0.3, -1], "back", "BACK OBLIQUE (2 mm-inset recess, 1.75 deep)", (800, 1300)),
        ([1, 0, 0], "side-right", "RIGHT SIDE (laid face-up; keypad top at right)", (1100, 500)),
        ([s, -s, s], "front-iso", "FRONT ISO", (1000, 1300)),
    ]
    paths = []
    for eye, slug, title, size in views:
        out = RENDER_DIR / f"{slug}-v{REVISION}.png"
        renderer.render(kp, eye, size, title, sub, out)
        paths.append(out)
    # Elevation overlay: blockout v2 masses + reference keypad (export frame).
    over = [(*read_off(MESH_DIR / f"blockout-{p}-v{BLOCKOUT_REV}.off"), c) for p, c in BLOCKOUT_COLORS.items()]
    over += [(*read_off(MESH_DIR / f"{p}-elevation-v{REVISION}.off"), COLORS[p])
             for p in ["body", "buttons", "led"]]
    out = RENDER_DIR / f"elevation-overlay-v{REVISION}.png"
    renderer.render(over, [0, -1, 0], (900, 1300), "FRONT ELEVATION OVERLAY",
                    f"Blockout v{BLOCKOUT_REV} masses + keypad_in_elevation() reference v{REVISION} "
                    "(lower-left 19, 33.5); blue wrap drawn over keypad", out)
    paths.append(out)
    return paths


if __name__ == "__main__":
    export_all()
    report = check()
    for name, ok in report["checks"].items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print("report:", REPORT.relative_to(repo))
    if "--no-render" not in sys.argv:
        for p in render():
            print("render:", p.relative_to(repo))
    sys.exit(0 if report["pass"] else 1)
