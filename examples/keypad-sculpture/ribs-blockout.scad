// Wyze keypad sculpture — YELLOW RIB FIELD BLOCKOUT (not a printable part)
// Replaces the solid yellow envelope with 10 vertical ribs whose depth follows
// a "bow wave" around the black mass. v1: three variants; the author picked C.
// v2 (Stage 2): C fused with a 3 mm yellow backing plate; no spine bars.
// v3 (Stage 3): plate inset so rib ends overhang it (comb edge).
// v4 (Stage 4): organic plate outlines (plate_style 1..4), echoing the blue wrap.
//
// Units: mm. Elevation frame of blockout.scad (included, not edited):
//   X right, Y up, Z out of the wall (wall plane Z = 0); origin = yellow
//   field's lower-left corner. `export_frame = true` rotates like the blockout.
// Ribs: straight and vertical from the front, clipped to the approved yellow
//   outline. Depth h(x, y) is ONE field driven by the signed distance to the
//   black outline, sampled along each rib's centre line (ribs are related).
// Approximation: distance is to the black's sharp quad; its 4 mm corner
//   rounding is ignored.

include <blockout.scad>
part = "none";              // silence blockout.scad's own model (included)
use <keypad-reference.scad>

ribs_blockout_revision = 4;   // v4: organic plate outlines (Stage 4)

variant = "C";              // A gentle | B steep pile-up | C directional (picked)
show    = "all";            // all | ribs | black | blue | keypad_body | keypad_buttons
                            // check-only: plate | ribs_bare
backing = true;             // yellow plate fused with the ribs; false = v1 ribs, no bars

// ---------- Ribs ----------
rib_count = 10;
rib_pitch = 7.8;            // 78 mm field / 10 (DESIGN "Rib decisions")
rib_width = 4;              // starting width
rib_step  = 1;              // profile sample spacing along Y

h_end   = 5;                // rib height at its far ends
h_under = 4;                // rib height under the black; black back sits here
under_ramp = 4;             // inside the black: peak -> under over this depth

// Variant parameters: [h_peak, falloff length L]
params_A     = [18, 30];    // gentle: lower crest, long falloff
params_B     = [24, 10];    // steep: tall crest tight to the black
params_wake  = [14, 30];    // C below/behind the black's motion
motion_dir   = [-0.45, 0.89];  // C: black moving up-left (unit vector)
motion_band  = 25;          // C: soft blend half-width about the black centroid

// ---------- Placement of the masses ----------
keypad_velcro_proud = 1.5;  // H3 range 1–2.5; keypad back above the black's back

// ---------- Backing plate (Stage 2, replaces the v1 spine bars) ----------
backing_depth = 3;          // Z 0–3 on the wall
plate_inset_ends = 6;       // plate top/bottom edges this far inside the
                            // envelope diagonals, measured along Y
// Left/right plate edges sit on the outer ribs' centre lines; the plate is
// also clipped to the approved yellow outline (the 8 mm bottom-left lean).

// Stage 4: organic outlines. Hand-placed control points (elevation XY),
// softened by rounding both convex and concave corners (plate_soft), then
// clipped to the yellow outline. 0 = the v3 straight inset plate.
plate_style = 1;    // 0 v3 inset | 1 soft inset | 2 drip | 3 blue echo | 4 pool
plate_soft  = [0, 6, 3.5, 4, 4];   // rounding radius per style
plate_pts = [
    [],
    // 1 soft inset: v3 footprint, edges swell and pinch; lobe at rib 0.
    [[9, 10], [30, 17], [50, 26], [68, 36], [73, 42], [75.5, 60], [72.5, 90],
     [75.5, 125], [75, 150], [70, 157], [50, 148], [30, 140], [10, 131],
     [3, 127], [2.5, 110], [5.5, 85], [8, 40]],
    // 2 drip: top like v3; the bottom edge sags into drips that lengthen to
    // the right, the longest under the blue's droop.
    [[10, 32], [19, 25], [22, 12], [25, 25], [37, 30], [40, 19.5], [43, 31],
     [58, 52], [62, 46], [64.5, 34], [67.5, 34], [70, 46], [74.6, 56],
     [74.6, 150], [70, 156], [40, 144], [10, 131], [3, 128], [2.8, 100],
     [4, 72], [8, 58]],
    // 3 blue echo: thin band along the top, heavy upper-right shoulder,
    // tapering droop down the right side.
    [[72, 42], [76, 50], [76.5, 120], [76.5, 150], [74, 160], [50, 148],
     [25, 138], [8, 132], [2.5, 128], [2.5, 114], [10, 116], [30, 121],
     [42, 118], [52, 108], [60, 95], [64, 80], [67, 60], [69, 46]],
    // 4 pool: behind the black, peeking past its outline, with lobes out to
    // the outer ribs; rib ends float free.
    [[16, 16], [36, 20], [56, 24], [62, 34], [66, 60], [70, 82], [75, 86],
     [75.5, 100], [70, 106], [65, 120], [64, 142], [55, 146], [40, 143],
     [20, 138], [10, 134], [8, 118], [3, 114], [2.8, 98], [7, 92], [9, 60],
     [10, 30]],
];

module soften(r) {
    // Round convex corners (outer pair) and concave corners (inner pair).
    offset(r = r) offset(delta = -r) offset(r = -r) offset(delta = r) children();
}

// ---------- Height field ----------
function smoothstep(e) = e <= 0 ? 0 : e >= 1 ? 1 : e * e * (3 - 2 * e);
function seg_dist(p, a, b) =
    let(ab = b - a, t = max(0, min(1, (p - a) * ab / (ab * ab)))) norm(p - (a + t * ab));
function cross2(a, b) = a[0] * b[1] - a[1] * b[0];
function inside_quad(p, q) =   // black_pts is counter-clockwise and convex
    min([for (i = [0 : 3]) cross2(q[(i + 1) % 4] - q[i], p - q[i])]) >= 0;
function signed_dist(p) =
    let(d = min([for (i = [0 : 3]) seg_dist(p, black_pts[i], black_pts[(i + 1) % 4])]))
    inside_quad(p, black_pts) ? -d : d;

black_centre = (black_pts[0] + black_pts[1] + black_pts[2] + black_pts[3]) / 4;

function variant_params(p) =
    variant == "A" ? params_A :
    variant == "B" ? params_B :
    // C: front of the motion gets B, the wake gets the gentle set.
    let(w = smoothstep(0.5 + (p - black_centre) * motion_dir / (2 * motion_band)))
        params_wake + (params_B - params_wake) * w;

function h(p) =
    let(s = signed_dist(p), v = variant_params(p), peak = v[0], L = v[1])
    s >= 0 ? h_end + (peak - h_end) * (1 - smoothstep(s / L))
           : h_under + (peak - h_under) * (1 - smoothstep(-s / under_ramp));

// ---------- Solids ----------
y_lo = min([for (p = yellow_pts) p[1]]) - 1;
y_hi = max([for (p = yellow_pts) p[1]]) + 1;

function rib_x(i) = rib_pitch / 2 + i * rib_pitch;

module rib(i) {
    xc = rib_x(i);
    ys = [for (y = [y_lo : rib_step : y_hi]) y];
    profile = concat([for (y = ys) [y, h([xc, y])]],
                     [[y_hi, 0], [y_lo, 0]]);
    intersection() {
        // Profile in (Y, Z), extruded across the rib width along X.
        translate([xc - rib_width / 2, 0, 0]) rotate([90, 0, 90])
            linear_extrude(rib_width) polygon(profile);
        translate([0, 0, -1]) linear_extrude(100) polygon(yellow_pts);
    }
}

module ribs() { for (i = [0 : rib_count - 1]) rib(i); }

module backing_plate() {
    // Rib heights stay measured from the wall; the plate overlaps their backs.
    x0 = rib_x(0);
    x1 = rib_x(rib_count - 1);
    // Points on the envelope's bottom and top diagonals at a given X.
    function bottom_y(x) = let(a = yellow_pts[0], b = yellow_pts[1])
        a[1] + (x - a[0]) * (b[1] - a[1]) / (b[0] - a[0]);
    function top_y(x) = let(a = yellow_pts[3], b = yellow_pts[2])
        a[1] + (x - a[0]) * (b[1] - a[1]) / (b[0] - a[0]);
    linear_extrude(backing_depth) intersection() {
        if (plate_style == 0)
            polygon([[x0, bottom_y(x0) + plate_inset_ends], [x1, bottom_y(x1) + plate_inset_ends],
                     [x1, top_y(x1) - plate_inset_ends], [x0, top_y(x0) - plate_inset_ends]]);
        else
            soften(plate_soft[plate_style]) polygon(plate_pts[plate_style]);
        polygon(yellow_pts);
    }
}

module scene() {
    // One yellow solid: ribs fused with the plate.
    if (show == "all" || show == "ribs")
        color("#f2c230") union() { ribs(); if (backing) backing_plate(); }
    if (show == "plate") backing_plate();
    if (show == "ribs_bare") ribs();
    translate([0, 0, h_under]) {
        if (show == "all" || show == "black") color("#1d1d1f") black_mass();
        if (show == "all" || show == "blue")  color("#9fd3f2") blue_wrap();
    }
    translate([0, 0, h_under + keypad_velcro_proud]) {
        if (show == "all" || show == "keypad_body")    keypad_in_elevation("body");
        if (show == "all" || show == "keypad_buttons") keypad_in_elevation("buttons");
    }
}

if (export_frame) rotate([90, 0, 0]) scene();
else scene();

echo(str("ribs blockout v", ribs_blockout_revision, " variant ", variant,
         " black front Z=", h_under + black_depth,
         " blue front Z=", h_under + black_depth + blue_proud));
