#!/usr/bin/env python3
"""Pre-print mesh check: is this STL ready to slice on *your* printer?

Run it on every STL you are about to print, from the kit root:
    bin/python bin/print-check.py exports/my-part/part-v1.stl
    bin/python bin/print-check.py a.stl b.stl --report exports/my-part/print-check-v1.json

For each file it checks, from the exported bytes:
  ascii_stl     the file is ASCII STL (binary STL rounding can open Manifold meshes)
  closed        every edge is shared by exactly two faces, in opposite directions
  one_body      a single connected body (parts that only touch are two bodies)
  flat_on_bed   lowest point at Z = 0, with real flat contact area on the bed
  fits_bed      inside the bed size read from my-printer.md (either way round in X/Y)
  overhangs     downward faces off the bed are no flatter than the overhang limit,
                or are flat ceilings no wider than the bridge limit, or are
                narrow strips (at most 2.5 nozzle widths across, for example
                engraved text or a small edge chamfer)

The bed, overhang and bridge limits come from my-printer.md (or --printer FILE).
Blank values use the defaults written in that file. This is a mesh screen, not
a slicer: it cannot see first-layer adhesion, thin walls the slicer drops, or
strength. Exit status is 0 only when every check on every file passes.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

KIT = Path(__file__).resolve().parents[1]
DEFAULTS = {"bed": (180.0, 180.0, 180.0), "nozzle": 0.4, "overhang": 50.0, "bridge": 7.0}
MIN_BED_CONTACT_MM2 = 20.0


def _field(text, label):
    """(your value, the file's [default ...] value) after `- <label>...:`."""
    m = re.search(rf"^\s*-\s*{re.escape(label)}[^:\n]*:(.*)$", text, re.M | re.I)
    if not m:
        return "", ""
    default = re.search(r"\[\s*default([^\]]*)\]", m.group(1), re.I)
    value = re.sub(r"\[[^\]]*\]", "", m.group(1))
    return value, default.group(1) if default else ""


def _numbers(value):
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", value)]


def read_printer(path):
    """Limits from my-printer.md: your value, else the [default ...] written in
    the file, else a built-in fallback. Returns (settings, notes about defaults)."""
    text = Path(path).read_text()
    out, notes = {}, []
    for key, label, need in (("bed", "Bed size", 3), ("nozzle", "Nozzle diameter", 1),
                             ("overhang", "Overhang limit", 1), ("bridge", "Longest bridge", 1)):
        value, default = _field(text, label)
        nums = _numbers(value)
        if len(nums) < need:
            nums = _numbers(default)
            if len(nums) < need:
                nums = list(DEFAULTS[key]) if need > 1 else [DEFAULTS[key]]
            shown = " x ".join(f"{n:g}" for n in nums[:need])
            notes.append(f"{label.lower()} not filled in; using the default {shown}")
        out[key] = tuple(nums[:3]) if need > 1 else nums[0]
    out["filled_in"] = bool(re.search(r"^Status:\s*filled", text, re.M | re.I))
    return out, notes


def read_ascii_stl(path):
    data = Path(path).read_bytes()
    if not data.lstrip()[:5].lower() == b"solid" or b"facet" not in data[:4096]:
        return None
    verts = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", data.decode()), float).reshape(-1, 3, 3)
    uniq, idx = np.unique(np.round(verts.reshape(-1, 3), 5), axis=0, return_inverse=True)
    f = idx.reshape(-1, 3)
    # Manifold can leave zero-area slivers whose corners are ~1e-6 mm apart.
    # Welding merges those corners; drop the collapsed triangles they leave.
    keep = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])
    return uniq, f[keep]


def components(faces):
    """Connected bodies of a triangle mesh (faces joined through shared vertices)."""
    parent = list(range(int(faces.max()) + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for f in faces:
        ra = find(f[0])
        for b in f[1:]:
            rb = find(b)
            if rb != ra:
                parent[rb] = ra
    roots = np.array([find(f[0]) for f in faces])
    return [faces[roots == r] for r in np.unique(roots)]


def closed(faces):
    edges = {}
    for t in faces:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges[(a, b)] = edges.get((a, b), 0) + 1
    return all(n == 1 and edges.get((b, a), 0) == 1 for (a, b), n in edges.items())


def overhangs(v, f, limit_deg, bridge_mm, narrow_mm):
    tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    area = np.linalg.norm(n, axis=1) / 2
    nz = n[:, 2] / np.maximum(2 * area, 1e-12)
    on_bed = np.all(np.abs(tri[:, :, 2]) < 1e-4, axis=1)
    down = (nz < -0.01) & ~on_bed
    # -nz is the sine of the face's angle from vertical.
    steep = down & (-nz > math.sin(math.radians(limit_deg)))
    islands = []
    if steep.any():
        for comp in components(f[steep]):
            p = v[np.unique(comp)]
            ext = p.max(0) - p.min(0)
            flat = bool(ext[2] < 0.05)
            narrow = bool(min(ext[0], ext[1]) <= narrow_mm)
            bridge = bool(flat and min(ext[0], ext[1]) <= bridge_mm)
            islands.append({"z": [round(float(p[:, 2].min()), 2), round(float(p[:, 2].max()), 2)],
                            "xy_extent": [round(float(ext[0]), 2), round(float(ext[1]), 2)],
                            "flat": flat, "narrow": narrow, "bridge": bridge,
                            "ok": narrow or bridge})
    return {"bed_contact_mm2": round(float(area[on_bed & (nz < -0.99)].sum()), 1),
            "downward_area_off_bed_mm2": round(float(area[down].sum()), 1),
            "too_flat_area_mm2": round(float(area[steep].sum()), 2),
            "islands": islands}


def volume(v, f):
    a, b, c = (v[f[:, i]] for i in range(3))
    return float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6)


def shown(path):
    """Path relative to the kit when inside it, so reports carry no home folders."""
    path = Path(path).resolve()
    try:
        return str(path.relative_to(KIT))
    except ValueError:
        return path.name


def check_file(path, printer, allow_supports=False):
    path = Path(path)
    r = {"file": shown(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "checks": {}}
    mesh = read_ascii_stl(path)
    r["checks"]["ascii_stl"] = mesh is not None
    if mesh is None:
        r["problem"] = "not ASCII STL: export with --export-format asciistl"
        r["pass"] = False
        return r
    v, f = mesh
    lo, hi = v.min(0), v.max(0)
    size = hi - lo
    bed = np.array(printer["bed"])
    oh = overhangs(v, f, printer["overhang"], printer["bridge"], 2.5 * printer["nozzle"])
    r.update({"size_xyz_mm": [round(float(x), 2) for x in size], "min_z": round(float(lo[2]), 4),
              "volume_cm3": round(volume(v, f) / 1000, 2), "triangles": int(len(f)), **oh})
    r["bodies"] = len(components(f))
    fits = bool((size[0] <= bed[0] and size[1] <= bed[1] or size[0] <= bed[1] and size[1] <= bed[0])
                and size[2] <= bed[2])
    bad_islands = [i for i in oh["islands"] if not i["ok"]]
    r["checks"].update({
        "closed": closed(f),
        "one_body": r["bodies"] == 1,
        "flat_on_bed": bool(abs(lo[2]) < 1e-4 and oh["bed_contact_mm2"] >= MIN_BED_CONTACT_MM2),
        "fits_bed": fits,
        "overhangs": not bad_islands or allow_supports,
    })
    if bad_islands and allow_supports:
        r["warning"] = f"{len(bad_islands)} overhang region(s) need supports (allowed with --allow-supports)"
    r["pass"] = all(r["checks"].values())
    return r


def main(argv=None):
    p = argparse.ArgumentParser(description="Pre-print mesh check for ASCII STL files.")
    p.add_argument("stl", nargs="+", type=Path)
    p.add_argument("--printer", type=Path, default=KIT / "my-printer.md",
                   help="printer file to read limits from (default: my-printer.md at the kit root)")
    p.add_argument("--report", type=Path, help="write a JSON report here")
    p.add_argument("--allow-supports", action="store_true",
                   help="report overhangs as a warning, because you will print with supports")
    a = p.parse_args(argv)
    if not a.printer.is_file():
        print(f"print-check: printer file not found: {a.printer}", file=sys.stderr)
        return 2
    printer, notes = read_printer(a.printer)
    for n in notes:
        print(f"note: {n}")
    if not printer["filled_in"]:
        print("note: my-printer.md is still the template; ask the agent to fill it in with you")
    report = {"tool": "bin/print-check.py", "printer_file": shown(a.printer),
              "printer": {k: v for k, v in printer.items()}, "defaults_used": notes,
              "not_a_slicer": "Mesh screen only; slice and preview before printing.", "files": []}
    for stl in a.stl:
        if not stl.is_file():
            print(f"FAIL {stl}: file not found")
            report["files"].append({"file": shown(stl), "pass": False, "problem": "not found"})
            continue
        r = check_file(stl, printer, a.allow_supports)
        report["files"].append(r)
        print(f"{'PASS' if r['pass'] else 'FAIL'} {stl.name}  "
              f"{' x '.join(f'{s:g}' for s in r.get('size_xyz_mm', []))} mm")
        for name, ok in r["checks"].items():
            print(f"  {'ok  ' if ok else 'FAIL'} {name}")
        if not r["checks"].get("fits_bed", True):
            print(f"       part does not fit the bed {' x '.join(f'{b:g}' for b in printer['bed'])} mm")
        for i in r.get("islands", []):
            if not i["ok"]:
                print(f"       overhang at Z {i['z'][0]}-{i['z'][1]}, {i['xy_extent'][0]} x {i['xy_extent'][1]} mm")
        for key in ("problem", "warning"):
            if key in r:
                print(f"       {r[key]}")
    report["pass"] = all(r["pass"] for r in report["files"])
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(json.dumps(report, indent=2) + "\n")
        print(f"report: {a.report}")
    print("PASS" if report["pass"] else "FAIL")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
