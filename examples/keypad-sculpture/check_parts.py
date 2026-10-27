"""Project check for keypad-parts.scad v1, run by bin/scad-geometry-check.py.

Reads the model-frame meshes the runner exported (elevation frame: Z out of
the door) and checks, on the meshes:
  - skin: every sampled point of the keypad face that is not a hole is covered
    by exactly one shell layer from Z 29.7 to 30.5 (0.8 mm);
  - button holes: Ø11.6 and concentric with each keypad reference button;
  - LED hole: Ø2 and centred on the keypad reference LED (B11);
  - blue: same silhouette and Z range as the parts-blockout v4 drape.
Writes exports/parts-v1/checks/parts-geometry-v1.json with boolean checks.
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

here = Path(__file__).resolve().parent
DIR = here / "exports" / "parts-v1" / "checks"
REV = "v1"
spec = importlib.util.spec_from_file_location("check_keypad", here / "check_keypad.py")
ck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck)  # read_off, components

FACE_Z, FRONT_Z, SKIN = 29.7, 30.5, 0.8
BUTTON_HOLE_D, LED_HOLE_D = 11.6, 2.0
TOL = 0.02  # mm, facet and float tolerance on positions and radii


def mesh(name):
    return ck.read_off(DIR / f"{name}-{REV}.off")


def ray_z(v, f, x, y):
    """Z of every crossing of the vertical line through (x, y)."""
    t = v[f]
    a, b, c = t[:, 0, :2], t[:, 1, :2], t[:, 2, :2]
    p = np.array([x, y])
    d = (b[:, 1] - c[:, 1]) * (a[:, 0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (a[:, 1] - c[:, 1])
    ok = np.abs(d) > 1e-12
    d = np.where(ok, d, 1)
    l1 = ((b[:, 1] - c[:, 1]) * (p[0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (p[1] - c[:, 1])) / d
    l2 = ((c[:, 1] - a[:, 1]) * (p[0] - c[:, 0]) + (a[:, 0] - c[:, 0]) * (p[1] - c[:, 1])) / d
    l3 = 1 - l1 - l2
    hit = ok & (l1 >= 0) & (l2 >= 0) & (l3 >= 0)
    z = l1 * t[:, 0, 2] + l2 * t[:, 1, 2] + l3 * t[:, 2, 2]
    return np.unique(np.round(z[hit], 4))


def centres(v, f):
    out = []
    for comp in ck.components(v, f):
        p = v[np.unique(comp)]
        out.append((p.min(0)[:2] + p.max(0)[:2]) / 2)
    return out


def rim(v, centre, z, rmax):
    """Shell vertices on the plane z within rmax of centre: the hole rim."""
    on = np.abs(v[:, 2] - z) < 1e-3
    d = np.linalg.norm(v[:, :2] - centre, axis=1)
    p = v[on & (d < rmax)][:, :2]
    if len(p) < 8:
        return None, None
    c = p.mean(0)
    return c, float(np.linalg.norm(p - c, axis=1).mean())


def footprint(v, f, px=10):
    img = Image.new("1", (100 * px, 180 * px), 0)
    draw = ImageDraw.Draw(img)
    for tri in v[f][:, :, :2] * px:
        draw.polygon([tuple(q) for q in tri], fill=1)
    return np.asarray(img, bool)


def main():
    sv, sf = mesh("shell")
    bv, bf = mesh("keypad_buttons")
    lv, lf = mesh("keypad_led")
    kv, _ = mesh("keypad")
    buttons = centres(bv, bf)
    led = centres(lv, lf)
    report = {"revision": REV, "frame": "elevation (Z out of the door)", "checks": {}, "values": {}}
    checks, values = report["checks"], report["values"]

    # Button and LED holes, from the rim vertices on the front and skin planes.
    holes = []
    for i, c in enumerate(buttons):
        for z in (FRONT_Z, FACE_Z):
            hc, r = rim(sv, c, z, BUTTON_HOLE_D / 2 + 0.5)
            holes.append({"button": i + 1, "z": z, "offset": None if hc is None else float(np.linalg.norm(hc - c)),
                          "diameter": None if r is None else 2 * r})
    values["button_holes"] = holes
    checks["buttons_found_12"] = len(buttons) == 12
    checks["button_holes_d11.6_concentric"] = all(
        h["offset"] is not None and h["offset"] < TOL and abs(h["diameter"] - BUTTON_HOLE_D) < 2 * TOL for h in holes)
    led_holes = []
    for z in (FRONT_Z, FACE_Z):
        hc, r = rim(sv, led[0], z, LED_HOLE_D / 2 + 0.4)
        led_holes.append({"z": z, "centre": None if hc is None else hc.round(3).tolist(),
                          "offset": None if hc is None else float(np.linalg.norm(hc - led[0])),
                          "diameter": None if r is None else 2 * r})
    values["led_reference_centre"] = led[0].round(3).tolist()
    values["led_hole"] = led_holes
    checks["led_found_1"] = len(led) == 1
    checks["led_hole_d2_on_reference"] = all(
        h["offset"] is not None and h["offset"] < TOL and abs(h["diameter"] - LED_HOLE_D) < 2 * TOL for h in led_holes)

    # Skin: sample the keypad face on a 2 mm grid, skipping holes and the
    # rounded outline edge.
    lo, hi = kv.min(0), kv.max(0)
    samples, bad = 0, []
    for x in np.arange(lo[0] + 2, hi[0] - 2, 2.0):
        for y in np.arange(lo[1] + 2, hi[1] - 2, 2.0):
            p = np.array([x, y])
            if min(np.linalg.norm(p - c) for c in buttons) < BUTTON_HOLE_D / 2 + 0.3:
                continue
            if np.linalg.norm(p - led[0]) < LED_HOLE_D / 2 + 0.3:
                continue
            z = ray_z(sv, sf, x, y)
            samples += 1
            if not (len(z) == 2 and abs(z[0] - FACE_Z) < 1e-3 and abs(z[1] - FRONT_Z) < 1e-3):
                bad.append([round(x, 1), round(y, 1), z.tolist()])
    values["skin_samples"] = samples
    values["skin_bad_samples"] = bad[:10]
    checks["skin_0.8_everywhere_sampled"] = samples > 300 and not bad
    checks["keypad_face_at_29.7"] = abs(kv[:, 2].max() - (FACE_Z + 0.9)) < 1e-3  # button tops = face + B6

    # Blue: silhouette and Z range against the blockout drape.
    nv, nf = mesh("blue")
    ov, of = mesh("blockout_drape")
    a, b = footprint(nv, nf), footprint(ov, of)
    diff = float((a ^ b).sum()) / max(1, b.sum())
    values["blue_z_range"] = [float(nv[:, 2].min()), float(nv[:, 2].max())]
    values["blockout_drape_z_range"] = [float(ov[:, 2].min()), float(ov[:, 2].max())]
    values["blue_silhouette_diff_fraction"] = round(diff, 4)
    checks["blue_z_range_kept"] = (abs(nv[:, 2].min() - ov[:, 2].min()) < 1e-3 and abs(nv[:, 2].max() - ov[:, 2].max()) < TOL)  # blockout layers overlap by 0.01
    checks["blue_silhouette_kept_1pct"] = diff < 0.01

    report["checks"] = {k: bool(ok) for k, ok in checks.items()}
    checks = report["checks"]
    out = DIR / f"parts-geometry-{REV}.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    for k, ok in checks.items():
        print(("PASS " if ok else "FAIL ") + k)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
