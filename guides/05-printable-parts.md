# 5. Printable parts, with checks

**You do:** look at the pictures and approve the parts.
**The agent does:** turns the approved blockout into print-ready parts, checks them, and shows you how each sits on the bed.

## What changes from the blockout

The agent adds what printing needs: holes, the fits from your coupon, small
chamfers on edges, and joints if the design is in several pieces. Each part
gets a **print pose**: the way up it sits on the bed. The STL files come out
already in that pose.

## Checks the agent runs before you print

- **Pre-print check** (`bin/print-check.py`) on every STL:
  - one solid piece;
  - flat on the bed;
  - fits your bed (from `my-printer.md`);
  - no steep overhangs that would need supports.
- **Geometry check** for parts that fit together or around your object:
  they must not collide where they should not, and must touch where they
  should. A deliberate "should collide" test proves the check is working.
- **Pictures of the real meshes**, in print pose, from above and below.

These are checks on the 3D model. They do not replace looking at the slicer
preview, and they cannot promise the print will succeed.

## Orientation, supports and brims (PLA and PETG)

You don't need to decide these, but it helps to know why the agent chose them:

- **Which way up.** Prints are weakest between layers. A hook or clip should
  lie flat so its bending runs along the layers. A flat visible face often
  goes face down on the bed, where it comes out smooth.
- **Supports.** Faces that lean out more than about 45° need supports, which
  leave rough marks. The agent designs around them where it can (45°
  chamfers, teardrop holes, splitting into pieces). If supports are needed,
  `PRINT.md` says where.
- **Brims.** A brim is a thin skirt around the first layer that stops corners
  lifting. Use one (3–5 mm) for long flat parts, tall thin parts and most
  PETG prints. Trim it off afterwards.
- **PLA or PETG?** PLA: easiest, crisp, but softens in a hot car or a sunny
  window. PETG: tougher and more heat-resistant, strings a little, and sticks
  very hard to smooth beds (use glue stick or a textured sheet as a release
  layer).

More detail for the curious: [docs/PRINTABILITY.md](../docs/PRINTABILITY.md).

## What you get

- STL files in `exports/<parts>-v<N>/`, named with the revision.
- A check report beside them, ending in `PASS`.
- Pictures: assembled, exploded, and each part in print pose.

## In the example

The keypad's three parts are in
[keypad-parts.scad](../examples/keypad-sculpture/keypad-parts.scad).
[build_parts.py](../examples/keypad-sculpture/build_parts.py) exports them
and runs the checks. The geometry check
([config](../examples/keypad-sculpture/geometry-check-config-v1.json)) found a
rib poking into a magnet pocket, which was fixed before printing. To run it
all yourself, use the commands under "Regenerate" in the
[example README](../examples/keypad-sculpture/README.md#regenerate).
