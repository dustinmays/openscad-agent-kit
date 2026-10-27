"""Export the fit coupons as ASCII STL, check the meshes, render them.

Run from the kit root:
    bin/python examples/keypad-sculpture/coupons.py

Coupons are small cut-outs of the real parts that test one fit each: the
shell coupon (keypad face skin, button and LED holes, wall fit) and the post
coupon (crush-ridge steps 0.15 / 0.25 / 0.35 mm marked with 1 / 2 / 3 dots).
Mesh checks are bin/print-check.py with limits from my-printer.md. Writes
exports/coupons-v<rev>/coupon-check-v<rev>.json. Not a slicer check.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


here = Path(__file__).resolve().parent
repo = here.parents[1]
SOURCE = here / "parts-blockout.scad"
REVISION = int(re.search(r"^parts_blockout_revision\s*=\s*(\d+);",
                         SOURCE.read_text(), re.M).group(1))
OUT_STL = here / "exports" / f"coupons-v{REVISION}"
OUT_PNG = here / "renders" / f"coupons-v{REVISION}"
MESH = here / "exports" / f"coupons-v{REVISION}" / "inuse"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


renderer = load("renderer", repo / "bin" / "render-views.py")
ck = load("check_keypad", here / "check_keypad.py")  # read_off
pc = load("print_check", repo / "bin" / "print-check.py")  # check_file, read_printer

COUPONS = {  # STL name: (part, colour)
    f"shell-fit-coupon-v{REVISION}": ("shell_coupon_print", [52, 52, 58]),
    f"post-fit-coupon-yellow-v{REVISION}": ("post_coupon_yellow_print", [242, 194, 48]),
    f"post-fit-coupon-black-v{REVISION}": ("post_coupon_black_print", [52, 52, 58]),
}
INUSE = {  # OFF name: (part, colour) in the model frame
    "shell_coupon_inuse": [52, 52, 58], "keypad_top_inuse": [167, 169, 172],
    "post_coupon_inuse_yellow": [242, 194, 48], "post_coupon_inuse_black": [52, 52, 58],
    "post_coupon_inuse_magnets": [205, 208, 214],
}


def openscad(out, part, fmt=None):
    args = [str(repo / "bin" / "openscad"), "-o", str(out), "-D", f'part="{part}"']
    if fmt:
        args += ["--export-format", fmt]
    r = subprocess.run(args + [str(SOURCE)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)


read_ascii_stl = pc.read_ascii_stl


if __name__ == "__main__":
    OUT_STL.mkdir(parents=True, exist_ok=True)
    OUT_PNG.mkdir(parents=True, exist_ok=True)
    MESH.mkdir(parents=True, exist_ok=True)
    printer, notes = pc.read_printer(repo / "my-printer.md")
    report = {"revision": f"v{REVISION}", "source": str(SOURCE.relative_to(repo)),
              "printer": printer, "defaults_used": notes,
              "not_a_slicer": "Mesh screen only (bin/print-check.py); slice and preview before printing.",
              "coupons": {}}
    for name, (part, _) in COUPONS.items():
        stl = OUT_STL / f"{name}.stl"
        openscad(stl, part, "asciistl")
        r = pc.check_file(stl, printer)
        report["coupons"][name] = r
    report["pass"] = all(c["pass"] for c in report["coupons"].values())
    (OUT_STL / f"coupon-check-v{REVISION}.json").write_text(json.dumps(report, indent=2) + "\n")
    for name, r in report["coupons"].items():
        print(("PASS " if r["pass"] else "FAIL ") + name, r["size_xyz_mm"], "mm",
              [k for k, ok in r["checks"].items() if not ok] or "")
    print("PASS" if report["pass"] else "FAIL")

    # Renders: print pose from the exact STLs; in use from model-frame meshes.
    for name, (_, colour) in COUPONS.items():
        v, f = read_ascii_stl(OUT_STL / f"{name}.stl")
        renderer.render([(v, f, colour)], [0.5, -1, 0.7], (900, 750), f"PRINT POSE: {name}",
                        "bed at Z = 0 | from the exact STL", OUT_PNG / f"{name}-print.png")
    for part in INUSE:
        openscad(MESH / f"{part}.off", part)
    shell_use = [(*ck.read_off(MESH / f"{p}.off"), INUSE[p]) for p in ("shell_coupon_inuse", "keypad_top_inuse")]
    # Model frame: Z out of the door. Eye from front-right-below so the walls show.
    renderer.render(shell_use, [0.5, -0.6, 1], (900, 800), "IN USE: shell coupon on the keypad top end",
                    "Skin 0.8 on the keypad face, buttons 1-4 through Ø11.6, LED Ø2, walls +0.15/side",
                    OUT_PNG / f"shell-fit-coupon-v{REVISION}-inuse.png")
    post_use = [(*ck.read_off(MESH / f"{p}.off"), INUSE[p]) for p in
                ("post_coupon_inuse_yellow", "post_coupon_inuse_black", "post_coupon_inuse_magnets")]
    renderer.render(post_use, [0.25, -1, 0.35], (1100, 700),
                    "IN USE: black block on post 2 (cut through the post axes)",
                    "Posts 1/2/3 = ridge interference 0.15/0.25/0.35 mm (1/2/3 dots); magnets face to face",
                    OUT_PNG / f"post-fit-coupon-v{REVISION}-inuse.png")
    print("renders:", OUT_PNG.relative_to(repo))
    sys.exit(0 if report["pass"] else 1)
