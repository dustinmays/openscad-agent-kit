#!/usr/bin/env python3
"""Render coloured review views of real meshes with a small software rasterizer.

Use it to see what OpenSCAD actually produced (OFF or STL exports), not an
illustration. Needs numpy and Pillow (bin/setup installs them).

As a command, from the kit root:
    bin/python bin/render-views.py part.stl --out renders/part.png
    bin/python bin/render-views.py a.off:242,194,48 b.off:52,52,58 \\
        --eye 0.5,-1,0.8 --title "FRONT" --out renders/front.png

As a module (the file name has a hyphen, so load it by path):
    spec = importlib.util.spec_from_file_location("render_views", kit / "bin" / "render-views.py")
    rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
    rv.render([(vertices, faces, [r, g, b])], eye, (w, h), title, subtitle, out_png)

The eye vector points from the model toward the viewer. Z is up in the image
unless the eye looks straight down Z.
"""
import argparse
import re
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "DejaVuSans.ttf",
]


def read_off(path):
    """Line-based OFF reader. OpenSCAD snapshot exports may append per-face
    RGB values after the indices, so read only `count` indices per face."""
    lines = [l.split("#", 1)[0].split() for l in Path(path).read_text().splitlines()]
    lines = [l for l in lines if l]
    assert lines[0][0] == "OFF", f"{path} is not an OFF file"
    counts, start = (lines[0][1:], 1) if len(lines[0]) > 1 else (lines[1], 2)
    nv, nf = int(counts[0]), int(counts[1])
    vertices = np.asarray([r[:3] for r in lines[start:start + nv]], float)
    faces = []
    for row in lines[start + nv:start + nv + nf]:
        poly = list(map(int, row[1:1 + int(row[0])]))
        faces.extend([[poly[0], poly[j], poly[j + 1]] for j in range(1, len(poly) - 1)])
    return vertices, np.asarray(faces, dtype=int)


def read_stl(path):
    """ASCII or binary STL -> (unique vertices, triangle indices)."""
    data = Path(path).read_bytes()
    text = data[:512].lstrip().lower()
    if text.startswith(b"solid") and b"facet" in data[:2048]:
        verts = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", data.decode()), float)
    else:
        n = struct.unpack("<I", data[80:84])[0]
        rec = np.frombuffer(data[84:84 + 50 * n], dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
        verts = rec["v"].reshape(-1, 3).astype(float)
    key = np.round(verts, 5)
    uniq, idx = np.unique(key, axis=0, return_inverse=True)
    return uniq, idx.reshape(-1, 3)


def read_mesh(path):
    return read_stl(path) if str(path).lower().endswith(".stl") else read_off(path)


def _font(size):
    for name in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)   # Pillow 10.1+
    except TypeError:
        return ImageFont.load_default()


def render(parts, eye, size, title, subtitle, out):
    """parts: list of (vertices Nx3, faces Mx3, [r, g, b]). Writes a PNG to `out`."""
    eye = np.asarray(eye, float); eye /= np.linalg.norm(eye)
    up_hint = np.array([0, 1, 0]) if abs(eye[2]) > .999 else np.array([0, 0, 1])
    right = np.cross(up_hint, eye); right /= np.linalg.norm(right)
    up = np.cross(eye, right)
    allv = np.concatenate([p[0] for p in parts])
    projected = allv @ np.array([right, up, eye]).T
    w, h = size
    scale = min((w - 110) / max(np.ptp(projected[:, 0]), 1e-9),
                (h - 150) / max(np.ptp(projected[:, 1]), 1e-9))
    center = (projected[:, :2].min(0) + projected[:, :2].max(0)) / 2
    canvas = np.full((h, w, 3), [247, 248, 250], np.uint8)
    zbuf = np.full((h, w), -np.inf)
    light = right * -.4 + up * .65 + eye * .8; light /= np.linalg.norm(light)
    for vertices, faces, base_color in parts:
        xyz = vertices @ np.array([right, up, eye]).T
        xy = (xyz[:, :2] - center) * [scale, -scale] + [w / 2, h / 2 + 28]
        for face in faces:
            tri = xy[face]; a, b, c = tri
            lo = np.maximum(np.floor(tri.min(0)).astype(int), 0)
            hi = np.minimum(np.ceil(tri.max(0)).astype(int), [w - 1, h - 1])
            if np.any(lo > hi):
                continue
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(den) < 1e-12:
                continue
            xx, yy = np.meshgrid(np.arange(lo[0], hi[0] + 1) + .5, np.arange(lo[1], hi[1] + 1) + .5)
            u = ((b[1] - c[1]) * (xx - c[0]) + (c[0] - b[0]) * (yy - c[1])) / den
            v = ((c[1] - a[1]) * (xx - c[0]) + (a[0] - c[0]) * (yy - c[1])) / den
            q = 1 - u - v
            depth = u * xyz[face[0], 2] + v * xyz[face[1], 2] + q * xyz[face[2], 2]
            sl = np.s_[lo[1]:hi[1] + 1, lo[0]:hi[0] + 1]
            mask = (u >= -1e-8) & (v >= -1e-8) & (q >= -1e-8) & (depth > zbuf[sl])
            normal = np.cross(vertices[face[1]] - vertices[face[0]], vertices[face[2]] - vertices[face[0]])
            normal = normal / max(np.linalg.norm(normal), 1e-12)
            shade = .48 + .52 * max(0, np.dot(normal, light))
            color = np.array(base_color) * shade
            region = canvas[sl]; region[mask] = np.clip(color, 0, 255).astype(np.uint8)
            dep_region = zbuf[sl]; dep_region[mask] = depth[mask]
    img = Image.fromarray(canvas); draw = ImageDraw.Draw(img)
    draw.text((25, 18), title, fill="#263944", font=_font(28))
    draw.text((25, 56), subtitle, fill="#52636d", font=_font(17))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def _parse_part(arg):
    path, _, rgb = arg.partition(":")
    colour = [int(c) for c in rgb.split(",")] if rgb else [242, 194, 48]
    return (*read_mesh(path), colour)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Render a PNG view of one or more OFF/STL meshes.")
    p.add_argument("meshes", nargs="+", help="mesh file, optionally with :R,G,B colour")
    p.add_argument("--out", required=True, help="PNG to write")
    p.add_argument("--eye", default="0.5,-1,0.8", help="view direction toward the viewer (x,y,z)")
    p.add_argument("--size", default="1000x900", help="image size WxH")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    a = p.parse_args()
    try:
        parts = [_parse_part(m) for m in a.meshes]
    except (OSError, AssertionError, ValueError) as exc:
        sys.exit(f"render-views: could not read a mesh: {exc}")
    w, h = (int(x) for x in a.size.lower().split("x"))
    title = a.title or ", ".join(Path(m.partition(":")[0]).name for m in a.meshes)
    render(parts, [float(x) for x in a.eye.split(",")], (w, h), title, a.subtitle, a.out)
    print(a.out)
