#!/usr/bin/env python3
"""Run revisioned, deterministic OpenSCAD mesh and intersection checks.

The JSON configuration supplies project geometry and expectations. This runner
does not infer physical clearance, load capacity, or printability from a mesh.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any


REPO = Path(__file__).resolve().parents[1]
OPENSCAD = REPO / "bin" / "openscad"
# bin/openscad runs the OpenSCAD snapshot with the Manifold backend.
ENGINE = "manifold"
EMPTY_MESSAGE = "Current top level object is empty."
# Manifold returns exactly touching faces as zero-volume slivers where CGAL
# returns empty, so a Manifold collision needs more overlap than this.
CONTACT_VOLUME_MM3 = 1e-3
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SCAD_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def repo_path(value: str) -> Path:
    path = (REPO / value).resolve()
    if not path.is_relative_to(REPO):
        raise ValueError(f"Path must remain within the kit: {value}")
    return path


def relative(path: Path) -> str:
    return str(path.relative_to(REPO))


def check_name(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SAFE_NAME.fullmatch(value):
        raise ValueError(f"{label} must be a simple filename component")
    return value


def scad_literal(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return json.dumps(value, allow_nan=False)
    if isinstance(value, str):
        return json.dumps(value)
    raise ValueError(f"Unsupported OpenSCAD -D value: {value!r}")


def run_scad(source: Path, selector: str, mode: str, output: Path,
             defines: dict[str, Any], timeout: int) -> subprocess.CompletedProcess[str]:
    command = [str(OPENSCAD), "--hardwarnings", "-D", f"{selector}={scad_literal(mode)}"]
    for name, value in sorted(defines.items()):
        if not SCAD_IDENTIFIER.fullmatch(name) or name == selector:
            raise ValueError(f"Invalid or duplicate OpenSCAD parameter: {name}")
        command += ["-D", f"{name}={scad_literal(value)}"]
    command += ["-o", str(output), str(source)]
    return subprocess.run(command, cwd=REPO, capture_output=True, text=True,
                          timeout=timeout, check=False)


def off_summary(output: Path) -> dict[str, int]:
    """Validate basic ASCII OFF structure; manifold checks belong to the project."""
    with output.open(encoding="utf-8") as stream:
        def data_line() -> list[str]:
            for line in stream:
                words = line.split("#", 1)[0].split()
                if words:
                    return words
            raise ValueError("truncated OFF data")

        header = data_line()
        if header[0] != "OFF":
            raise ValueError("missing OFF header")
        counts = header[1:] if len(header) > 1 else data_line()
        if len(counts) < 2:
            raise ValueError("missing OFF vertex/face counts")
        vertex_count, face_count = int(counts[0]), int(counts[1])
        if vertex_count < 3 or face_count < 1:
            raise ValueError("empty or implausible OFF counts")
        for _ in range(vertex_count):
            words = data_line()
            if len(words) < 3 or not all(math.isfinite(float(v)) for v in words[:3]):
                raise ValueError("invalid OFF vertex")
        for _ in range(face_count):
            words = data_line()
            count = int(words[0])
            if count < 3 or len(words) < count + 1:
                raise ValueError("invalid OFF face")
            indices = [int(v) for v in words[1:count + 1]]
            if len(set(indices)) != count or any(
                index < 0 or index >= vertex_count for index in indices
            ):
                raise ValueError("invalid OFF face indices")
    return {"vertex_count": vertex_count, "face_count": face_count}


def solid_summary(output: Path) -> dict[str, Any]:
    """Topology of an OFF mesh: a printable part needs every edge shared by
    exactly two faces in opposite directions, and one connected body. Parts
    that touch only along a line or at a point fail one of these."""
    words = [line.split("#", 1)[0].split() for line in output.read_text().splitlines()]
    words = [w for w in words if w]
    counts = words[0][1:] if len(words[0]) > 1 else words[1]
    start = 1 if len(words[0]) > 1 else 2
    vertex_count, face_count = int(counts[0]), int(counts[1])
    faces = [[int(v) for v in w[1:int(w[0]) + 1]]
             for w in words[start + vertex_count:start + vertex_count + face_count]]
    directed: dict[tuple[int, int], int] = {}
    edge_faces: dict[tuple[int, int], list[int]] = {}
    for index, face in enumerate(faces):
        for a, b in zip(face, face[1:] + face[:1]):
            directed[(a, b)] = directed.get((a, b), 0) + 1
            edge_faces.setdefault((min(a, b), max(a, b)), []).append(index)
    bad_edges = sum(1 for faces_on_edge in edge_faces.values() if len(faces_on_edge) != 2)
    misoriented = sum(1 for (a, b), n in directed.items()
                      if n != 1 or directed.get((b, a), 0) != 1)
    parent = list(range(len(faces)))

    def root(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    # Join faces across manifold edges only, so line contacts split bodies.
    for faces_on_edge in edge_faces.values():
        if len(faces_on_edge) == 2:
            parent[root(faces_on_edge[0])] = root(faces_on_edge[1])
    bodies = len({root(i) for i in range(len(faces))})
    return {"nonmanifold_edges": bad_edges, "misoriented_edges": misoriented,
            "bodies": bodies,
            "single_solid": bad_edges == 0 and misoriented == 0 and bodies == 1}


def reimports_cleanly(output: Path, timeout: int) -> bool:
    """Feed the exported mesh back into a boolean. Manifold may accept a mesh
    whose bodies meet only along a line, so the edge and body checks above
    still matter."""
    with tempfile.TemporaryDirectory(prefix="scad-reimport-") as scratch:
        probe = Path(scratch) / "reimport.scad"
        probe.write_text(f"union() {{ import({json.dumps(str(output))}); "
                         "translate([1e4, 0, 0]) cube(1); }\n")
        result = subprocess.run([str(OPENSCAD), "-o", str(Path(scratch) / "out.off"),
                                 str(probe)], cwd=REPO, capture_output=True,
                                text=True, timeout=timeout, check=False)
    log = result.stdout + result.stderr
    return result.returncode == 0 and "CGAL error" not in log and "ERROR" not in log


def off_volume(output: Path) -> float:
    """Enclosed volume of an OFF mesh (divergence theorem, fan triangulation)."""
    words = [line.split("#", 1)[0].split() for line in output.read_text().splitlines()]
    words = [w for w in words if w]
    counts = words[0][1:] if len(words[0]) > 1 else words[1]
    start = 1 if len(words[0]) > 1 else 2
    vertex_count, face_count = int(counts[0]), int(counts[1])
    points = [tuple(float(v) for v in w[:3]) for w in words[start:start + vertex_count]]
    total = 0.0
    for w in words[start + vertex_count:start + vertex_count + face_count]:
        face = [points[int(v)] for v in w[1:int(w[0]) + 1]]
        (ax, ay, az) = face[0]
        for (bx, by, bz), (cx, cy, cz) in zip(face[1:], face[2:]):
            total += (ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx)
                      + az * (bx * cy - by * cx)) / 6
    return abs(total)


def expect_off(result: subprocess.CompletedProcess[str], output: Path) -> dict[str, int]:
    if result.returncode != 0 or not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(
            f"OpenSCAD export failed ({output.name}, exit {result.returncode}):\n"
            f"{result.stdout}{result.stderr}"
        )
    try:
        return off_summary(output)
    except (UnicodeError, ValueError, IndexError) as exc:
        raise RuntimeError(f"Malformed OFF export {output}: {exc}") from exc


def has_intersection(result: subprocess.CompletedProcess[str], output: Path
                     ) -> tuple[bool, float | None]:
    log = result.stdout + result.stderr
    if result.returncode == 1 and EMPTY_MESSAGE in log and not output.exists():
        return False, None
    if result.returncode == 0:
        expect_off(result, output)
        volume = off_volume(output)
        return volume > CONTACT_VOLUME_MM3, volume
    raise RuntimeError(
        f"OpenSCAD could not classify intersection ({output.name}, "
        f"exit {result.returncode}):\n{log}"
    )


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text())
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError("Expected a schema_version 1 JSON object")
    check_name(config.get("revision"), "revision")
    selector = config.get("selector", "mode")
    if not isinstance(selector, str) or not SCAD_IDENTIFIER.fullmatch(selector):
        raise ValueError("selector must be an OpenSCAD identifier")
    if not isinstance(config.get("exports"), list) or not config["exports"]:
        raise ValueError("exports must be a nonempty list")
    if not isinstance(config.get("intersections", []), list):
        raise ValueError("intersections must be a list")
    names = []
    for entry in config["exports"] + config.get("intersections", []):
        if not isinstance(entry, dict):
            raise ValueError("Each export/intersection must be an object")
        names.append(check_name(entry.get("name"), "case name"))
        if not isinstance(entry.get("mode"), str):
            raise ValueError("Each case needs a mode string")
        if not isinstance(entry.get("defines", {}), dict):
            raise ValueError("defines must be an object")
        if not isinstance(entry.get("single_solid", False), bool):
            raise ValueError("single_solid must be a boolean")
    if len(names) != len(set(names)):
        raise ValueError("Export and intersection names must be unique")
    for entry in config.get("intersections", []):
        if not isinstance(entry.get("expected_collision"), bool):
            raise ValueError("Every intersection needs expected_collision: boolean")
    return config


def openscad_version() -> str:
    result = subprocess.run([str(OPENSCAD), "--version"], capture_output=True,
                            text=True, timeout=60, check=False)
    return (result.stdout + result.stderr).strip()


def main(config_file: Path, jobs: int) -> int:
    config_file = config_file.resolve()
    config = load_config(config_file)
    revision = config["revision"]
    source = repo_path(config["source"])
    dependencies = [repo_path(item) for item in config.get("dependencies", [])]
    output_dir = repo_path(config["output_dir"])
    report_name = check_name(config.get("report", f"geometry-check-{revision}.json"),
                             "report")
    if not report_name.endswith(".json"):
        raise ValueError("report must end in .json")
    selector = config.get("selector", "mode")
    timeout = config.get("timeout_seconds", 180)
    if not isinstance(timeout, int) or timeout < 1:
        raise ValueError("timeout_seconds must be a positive integer")
    for path in [source, *dependencies]:
        if not path.is_file():
            raise ValueError(f"Missing source/dependency: {path}")
    if not OPENSCAD.is_file():
        raise ValueError(f"Missing OpenSCAD launcher: {OPENSCAD}")
    source_sha256 = {
        relative(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [source, *dependencies]
    }
    config_sha256 = hashlib.sha256(config_file.read_bytes()).hexdigest()
    post_check = repo_path(config["post_check"]) if "post_check" in config else None
    post_check_sha256 = (hashlib.sha256(post_check.read_bytes()).hexdigest()
                         if post_check else None)

    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    def export(entry: dict[str, Any]) -> dict[str, Any]:
        output = output_dir / f"{entry['name']}-{revision}.off"
        result = run_scad(source, selector, entry["mode"], output,
                          entry.get("defines", {}), timeout)
        mesh_summary = expect_off(result, output)
        summary = {"name": entry["name"], "mode": entry["mode"],
                   "mesh": relative(output), "bytes": output.stat().st_size,
                   **mesh_summary}
        if entry.get("single_solid", False):
            topology = solid_summary(output)
            topology["reimports_cleanly"] = reimports_cleanly(output, timeout)
            topology["reimport_engine"] = ENGINE
            topology["single_solid"] = (topology["single_solid"]
                                        and topology["reimports_cleanly"])
            summary["topology"] = topology
            if not topology["single_solid"]:
                raise RuntimeError(
                    f"{entry['name']} is not one manifold solid: {topology}")
        return summary

    # Exports and CSG cases are independent OpenSCAD runs, so they share one
    # pool. The slowest CSG case (by the previous report) starts first, then the
    # exports, then the other cases slowest first. The post-check runs as soon as
    # every export exists, while CSG cases continue.
    report_path = output_dir / report_name
    previous_seconds: dict[str, float] = {}
    try:
        previous_seconds = {c["name"]: float(c["elapsed_seconds"])
                            for c in json.loads(report_path.read_text())["cases"]}
    except (OSError, ValueError, KeyError, TypeError):
        pass
    intersections = config.get("intersections", [])
    csg_order = sorted(range(len(intersections)),
                       key=lambda i: -previous_seconds.get(intersections[i]["name"], 0))

    def run_post_check() -> Path | None:
        post_check_report = None
        if not post_check:
            return None
        if "post_check_report" in config:
            post_check_report = repo_path(config["post_check_report"])
            previous_report_mtime = (post_check_report.stat().st_mtime_ns
                                     if post_check_report.exists() else -1)
        result = subprocess.run([sys.executable, str(post_check)], cwd=REPO,
                                capture_output=True, text=True, timeout=timeout,
                                check=False)
        if result.returncode:
            raise RuntimeError(
                f"Project check failed (exit {result.returncode}):\n"
                f"{result.stdout}{result.stderr}"
            )
        if "post_check_report" in config:
            if not post_check_report.is_file():
                raise RuntimeError(f"Project check did not write {post_check_report}")
            if post_check_report.stat().st_mtime_ns <= previous_report_mtime:
                raise RuntimeError(f"Project check report is stale: {post_check_report}")
            data = json.loads(post_check_report.read_text())
            checks = data.get("checks")
            if not isinstance(checks, dict) or not checks or not all(
                isinstance(value, bool) and value for value in checks.values()
            ):
                raise RuntimeError(f"Project report checks did not all pass: {post_check_report}")
            print(f"{post_check_report}: {len(checks)} project checks passed")
        elif result.stdout:
            print(result.stdout, end="")
        return post_check_report

    with tempfile.TemporaryDirectory(prefix="scad-csg-") as scratch:
        def intersect(entry: dict[str, Any]) -> dict[str, Any]:
            output = Path(scratch) / f"{entry['name']}.off"
            begin = time.monotonic()
            result = run_scad(source, selector, entry["mode"], output,
                              entry.get("defines", {}), timeout)
            actual, volume = has_intersection(result, output)
            expected = entry["expected_collision"]
            return {
                "name": entry["name"], "mode": entry["mode"],
                "defines": entry.get("defines", {}),
                "expected_collision": expected, "observed_collision": actual,
                "overlap_volume_mm3": None if volume is None else round(volume, 6),
                "passed": actual == expected,
                "elapsed_seconds": round(time.monotonic() - begin, 2),
            }

        with ThreadPoolExecutor(max_workers=jobs) as pool:
            try:
                csg_futures = {i: pool.submit(intersect, intersections[i])
                               for i in csg_order[:1]}
                export_futures = [pool.submit(export, e) for e in config["exports"]]
                csg_futures.update({i: pool.submit(intersect, intersections[i])
                                    for i in csg_order[1:]})
                exported = [f.result() for f in export_futures]
                post_check_report = run_post_check()
                cases = [csg_futures[i].result() for i in range(len(intersections))]
            except BaseException:
                pool.shutdown(wait=True, cancel_futures=True)
                raise

    passed = all(item["passed"] for item in cases)
    for path in [source, *dependencies]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != source_sha256[relative(path)]:
            raise RuntimeError(f"Geometry source changed during check: {path}")
    if hashlib.sha256(config_file.read_bytes()).hexdigest() != config_sha256:
        raise RuntimeError(f"Configuration changed during check: {config_file}")
    if post_check and hashlib.sha256(post_check.read_bytes()).hexdigest() != post_check_sha256:
        raise RuntimeError(f"Project check changed during run: {post_check}")
    report = {
        "revision": revision,
        "config": relative(config_file),
        "config_sha256": config_sha256,
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source": relative(source), "source_sha256": source_sha256,
        "post_check": relative(post_check) if post_check else None,
        "post_check_sha256": post_check_sha256,
        "exported_meshes": exported,
        "post_check_report": relative(post_check_report) if post_check_report else None,
        "method": "OpenSCAD OFF export and Manifold intersection; empty exit 1 is expected",
        "engine": ENGINE, "openscad_version": openscad_version(),
        "contact_volume_mm3": CONTACT_VOLUME_MM3,
        "cases": cases, "all_cases_passed": passed,
        "jobs": jobs,
        "total_elapsed_seconds": round(time.monotonic() - started, 2),
        "interpretation": config.get("interpretation", ""),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report_path}: {sum(c['passed'] for c in cases)}/{len(cases)} CSG cases passed")
    return 0 if passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="schema-version 1 JSON config")
    parser.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 1,
                        help="concurrent OpenSCAD processes (default: CPU count)")
    args = parser.parse_args()
    try:
        if args.jobs < 1:
            raise ValueError("--jobs must be at least 1")
        sys.exit(main(args.config, args.jobs))
    except (OSError, RuntimeError, ValueError, TypeError, KeyError,
            subprocess.TimeoutExpired) as exc:
        print(f"SCAD geometry check failed: {exc}", file=sys.stderr)
        sys.exit(2)
