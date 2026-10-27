#!/usr/bin/env python3
"""Rank print poses using Support Fins geometry and an explicit layer-axis proxy.

This is a screening tool. It does not predict printed strength, bed adhesion,
support release, slicer toolpaths, or physical fit.
"""

import argparse
import hashlib
import itertools
import json
import math
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}


def vector(value):
    try:
        result = tuple(float(part) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected three comma-separated numbers") from exc
    if len(result) != 3 or not all(math.isfinite(part) for part in result):
        raise argparse.ArgumentTypeError("expected three finite comma-separated numbers")
    return result


def angles(value):
    try:
        result = tuple(float(part) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected comma-separated angles") from exc
    if not result or not all(math.isfinite(part) for part in result):
        raise argparse.ArgumentTypeError("expected finite comma-separated angles")
    return tuple(dict.fromkeys(result))


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("expected a positive finite number")
    return number


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative finite number")
    return number


def rotated_z_component(axis, rotation):
    """Return Z after Support Fins' three.js XYZ rotation: Rx * Ry * Rz."""
    x, y, z = axis
    ax, ay, az = (math.radians(value) for value in rotation)
    cz, sz = math.cos(az), math.sin(az)
    x, y = cz * x - sz * y, sz * x + cz * y
    cy, sy = math.cos(ay), math.sin(ay)
    x, z = cy * x + sy * z, -sy * x + cy * z
    sx, cx = math.sin(ax), math.cos(ax)
    return sx * y + cx * z


def bounds(vertices):
    return [[min(vertex[i] for vertex in vertices), max(vertex[i] for vertex in vertices)]
            for i in range(3)]


def extents(limits):
    return [upper - lower for lower, upper in limits]


def volume_mm3(vertices, triangles):
    six_volume = 0.0
    for i, j, k in triangles:
        a, b, c = vertices[i], vertices[j], vertices[k]
        six_volume += (a[0] * (b[1] * c[2] - b[2] * c[1])
                       + a[1] * (b[2] * c[0] - b[0] * c[2])
                       + a[2] * (b[0] * c[1] - b[1] * c[0]))
    return abs(six_volume) / 6


def support_column_ratio(vertices, triangles):
    """Flag narrow bed-rooted support components; this is not a buckling model."""
    if not triangles:
        return 0.0
    parent = list(range(len(vertices)))

    def root(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for a, b, c in triangles:
        parent[root(b)] = root(a)
        parent[root(c)] = root(a)
    components = {}
    for a, b, c in triangles:
        group = components.setdefault(root(a), set())
        group.update((a, b, c))
    ratio = 0.0
    for indices in components.values():
        limits = bounds([vertices[index] for index in indices])
        width, depth, height = extents(limits)
        if height >= 20 and limits[2][0] <= 0.05:
            ratio = max(ratio, height / max(width, depth, 0.1))
    return ratio


def read_support_fins_3mf(path):
    """Read the part and support meshes written by the Support Fins CLI."""
    with zipfile.ZipFile(path) as archive:
        model = ET.fromstring(archive.read("3D/3dmodel.model"))
    meshes = {}
    for obj in model.findall(".//m:object", NS):
        vertices = [tuple(float(vertex.attrib[key]) for key in ("x", "y", "z"))
                    for vertex in obj.findall(".//m:vertex", NS)]
        triangles = [tuple(int(face.attrib[key]) for key in ("v1", "v2", "v3"))
                     for face in obj.findall(".//m:triangle", NS)]
        if not vertices or not triangles:
            continue  # The output also has a component assembly object.
        kind = "support" if obj.attrib.get("name", "").endswith(" supports") else "part"
        if kind in meshes:
            raise ValueError(f"multiple {kind} meshes in {path}")
        meshes[kind] = (vertices, triangles)
    if "part" not in meshes:
        raise ValueError(f"no part mesh in {path}")
    all_vertices = [vertex for vertices, _ in meshes.values() for vertex in vertices]
    part_vertices, part_faces = meshes["part"]
    support_vertices, support_faces = meshes.get("support", ([], []))
    return {
        "envelope_mm": [round(value, 3) for value in extents(bounds(all_vertices))],
        "part_volume_cm3": round(volume_mm3(part_vertices, part_faces) / 1000, 4),
        "support_volume_cm3": round(volume_mm3(support_vertices, support_faces) / 1000, 4)
        if support_faces else 0.0,
        "support_column_ratio": round(support_column_ratio(support_vertices, support_faces), 3),
        "part_triangles": len(part_faces),
        "support_triangles": len(support_faces),
    }


def pose_name(rotation):
    def format_angle(value):
        sign = "m" if value < 0 else "p" if value > 0 else ""
        return sign + f"{abs(value):g}".replace(".", "d")
    return "-".join(f"{axis}{format_angle(value)}"
                    for axis, value in zip("xyz", rotation))


def score_candidate(entry, args):
    stats = entry["stats"]
    mesh = entry["mesh"]
    envelope = mesh["envelope_mm"]
    available = (args.build_volume[0] - 2 * args.xy_clearance,
                 args.build_volume[1] - 2 * args.xy_clearance,
                 args.build_volume[2] - args.z_clearance)
    fits_box = all(size <= limit + 1e-6 for size, limit in zip(envelope, available))
    entry["fits_rectangular_envelope"] = fits_box
    entry["screen_pass"] = (fits_box and stats.get("unserved", 0) == 0
                            and stats.get("floating", 0) == 0)
    norm = math.sqrt(sum(component * component for component in args.critical_axis))
    crossing = abs(rotated_z_component(args.critical_axis, entry["rotation_deg"])) / norm
    strength = max(0.0, 1.0 - crossing)
    part = mesh["part_volume_cm3"]
    support = mesh["support_volume_cm3"]
    material = part / (part + support) if part + support else 0.0
    height = max(0.0, 1.0 - envelope[2] / available[2])
    stability = 1.0 / (1.0 + mesh["support_column_ratio"] / 10.0)
    weights = (args.weight_strength, args.weight_material,
               args.weight_height, args.weight_stability)
    weighted = sum(w * v for w, v in zip(weights, (strength, material, height, stability)))
    entry["proxies"] = {
        "span_in_layer_plane": round(strength, 4),
        "material_fraction_part": round(material, 4),
        "height_headroom_fraction": round(height, 4),
        "support_stability_proxy": round(stability, 4),
        "weighted_score": round(weighted / sum(weights), 4),
    }


def pareto(entries):
    """Keep poses not dominated on strength, support volume, height, and column ratio."""
    eligible = [entry for entry in entries if entry.get("screen_pass")]
    def values(entry):
        return (-entry["proxies"]["span_in_layer_plane"],
                entry["mesh"]["support_volume_cm3"],
                entry["mesh"]["envelope_mm"][2],
                entry["mesh"]["support_column_ratio"])
    for entry in eligible:
        target = values(entry)
        entry["pareto"] = not any(
            other is not entry and all(a <= b + 1e-6 for a, b in zip(values(other), target))
            and any(a < b - 1e-6 for a, b in zip(values(other), target))
            for other in eligible)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="one bare part STL in its known source pose")
    parser.add_argument("--cli", required=True, type=Path, help="Support Fins CLI .js or .mjs")
    parser.add_argument("--node", default=shutil.which("node"), help="Node 20.10+ executable")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--revision", default="v1", help="suffix for all generated files")
    parser.add_argument("--material", default="unspecified", help="report label; no material model")
    parser.add_argument("--critical-axis", required=True, type=vector,
                        help="source-pose direction to keep within layers, e.g. 0,0,1")
    parser.add_argument("--angles-x", type=angles, default=(-60, -30, 0, 30, 60))
    parser.add_argument("--angles-y", type=angles, default=(-60, -30, 0, 30, 60))
    parser.add_argument("--angles-z", type=angles, default=(0,))
    parser.add_argument("--build-volume", required=True, type=vector, help="X,Y,Z mm")
    parser.add_argument("--xy-clearance", type=nonnegative, default=5.0)
    parser.add_argument("--z-clearance", type=nonnegative, default=5.0)
    parser.add_argument("--layer-height", required=True, type=positive)
    parser.add_argument("--gap", required=True, type=positive, help="Support Fins gap in mm")
    parser.add_argument("--mode", choices=("auto", "full"), default="auto")
    parser.add_argument("--sway", action="store_true")
    parser.add_argument("--weight-strength", type=nonnegative, default=1.0)
    parser.add_argument("--weight-material", type=nonnegative, default=1.0)
    parser.add_argument("--weight-height", type=nonnegative, default=0.25)
    parser.add_argument("--weight-stability", type=nonnegative, default=0.5)
    args = parser.parse_args()
    if not args.node or not Path(args.node).is_file():
        parser.error("Node executable not found; pass --node")
    if not args.input.is_file() or not args.cli.is_file():
        parser.error("input STL and Support Fins CLI must exist")
    if args.input.suffix.lower() != ".stl":
        parser.error("this study currently accepts one bare STL")
    if any(value <= 0 for value in args.build_volume):
        parser.error("build-volume dimensions must be positive")
    if sum(value * value for value in args.critical_axis) == 0:
        parser.error("critical-axis must be nonzero")
    if sum((args.weight_strength, args.weight_material,
            args.weight_height, args.weight_stability)) == 0:
        parser.error("at least one score weight must be positive")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.revision):
        parser.error("revision must contain only letters, digits, underscores or hyphens")
    available = (args.build_volume[0] - 2 * args.xy_clearance,
                 args.build_volume[1] - 2 * args.xy_clearance,
                 args.build_volume[2] - args.z_clearance)
    if any(value <= 0 for value in available):
        parser.error("clearances leave no usable build volume")
    rotations = list(itertools.product(args.angles_x, args.angles_y, args.angles_z))
    prefix = re.sub(r"[^A-Za-z0-9_-]+", "-", args.input.stem).strip("-") or "part"
    report_path = args.output_dir / f"{prefix}-orientation-study-{args.revision}.json"
    outputs = [args.output_dir / f"{prefix}-pose-{pose_name(pose)}-{args.revision}.3mf"
               for pose in rotations]
    if len(set(outputs)) != len(outputs):
        parser.error("pose filenames collide; use distinct angles")
    existing = [path for path in [report_path, *outputs] if path.exists()]
    if existing:
        parser.error(f"output already exists: {existing[0]} (use a new revision)")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    version_run = subprocess.run([args.node, str(args.cli), "--version"],
                                 text=True, capture_output=True, timeout=20)
    if version_run.returncode:
        parser.error(f"Support Fins version check failed: {version_run.stderr.strip()}")
    report = {
        "schema": 1,
        "input": str(args.input.resolve()),
        "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "support_fins_cli": str(args.cli.resolve()),
        "support_fins_version": version_run.stdout.strip(),
        "settings": {
            "material_label": args.material,
            "critical_axis_source_pose": args.critical_axis,
            "build_volume_mm": args.build_volume,
            "xy_clearance_mm": args.xy_clearance,
            "z_clearance_mm": args.z_clearance,
            "layer_height_mm": args.layer_height,
            "support_gap_mm": args.gap,
            "mode": args.mode,
            "sway": args.sway,
            "weights": {"strength": args.weight_strength, "material": args.weight_material,
                        "height": args.weight_height, "stability": args.weight_stability},
            "angles_x": args.angles_x,
            "angles_y": args.angles_y,
            "angles_z": args.angles_z,
        },
        "limits": [
            "Layer alignment is a geometric proxy, not a strength prediction.",
            "Support volume is solid mesh volume, not sliced filament usage or print time.",
            "The rectangular envelope omits the cutter exclusion, brim, toolpaths and adhesion.",
            "A zero unserved count is an engine screening result, not a support-free print guarantee.",
            "Material label does not predict breakaway behavior; inspect the actual slicer profile.",
        ],
        "entries": [],
    }
    for index, (rotation, output) in enumerate(zip(rotations, outputs), 1):
        entry = {"rotation_deg": rotation, "output_3mf": str(output.resolve())}
        command = [args.node, str(args.cli), str(args.input), "--rot",
                   ",".join(f"{value:g}" for value in rotation), "--mode", args.mode,
                   "--gap", f"{args.gap:g}", "--layer-height", f"{args.layer_height:g}",
                   "--json", "-o", str(output)]
        if args.sway:
            command.append("--sway")
        try:
            run = subprocess.run(command, text=True, capture_output=True, timeout=180)
            if run.returncode:
                raise RuntimeError(run.stderr.strip() or run.stdout.strip()
                                   or f"Support Fins exited {run.returncode}")
            if not output.is_file():
                raise RuntimeError("Support Fins reported success without an output file")
            result = json.loads(run.stdout.strip().splitlines()[-1])
            entry["stats"] = result["stats"]
            entry["engine_report"] = result["report"]
            entry["mesh"] = read_support_fins_3mf(output)
            score_candidate(entry, args)
            print(f"[{index}/{len(rotations)}] {pose_name(rotation)}: "
                  f"{entry['engine_report']}; {entry['mesh']['support_volume_cm3']:.2f} cm3 support",
                  flush=True)
        except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired,
                zipfile.BadZipFile, ET.ParseError) as exc:
            entry["error"] = str(exc)
            print(f"[{index}/{len(rotations)}] {pose_name(rotation)}: ERROR {exc}",
                  file=sys.stderr, flush=True)
        report["entries"].append(entry)
    pareto(report["entries"])
    eligible = [entry for entry in report["entries"] if entry.get("screen_pass")]
    eligible.sort(key=lambda entry: entry["proxies"]["weighted_score"], reverse=True)
    report["screen_pass_count"] = len(eligible)
    report["pareto_poses"] = [entry["rotation_deg"] for entry in eligible
                              if entry.get("pareto")]
    report["weighted_recommendation"] = eligible[0]["rotation_deg"] if eligible else None
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Report: {report_path}")
    print(f"Screen pass: {len(eligible)}/{len(rotations)}; "
          f"weighted recommendation: {report['weighted_recommendation']}")
    return 0 if eligible else 1


if __name__ == "__main__":
    sys.exit(main())
