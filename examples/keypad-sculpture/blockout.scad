// Wyze keypad sculptural wall mount — PHASE 1 COMPOSITION BLOCKOUT
// Not a printable part. Three colour masses plus a keypad reference solid.
//
// Units: mm. Authoring frame = front elevation, as seen in the hand sketch:
//   X right, Y up, Z out of the wall toward the viewer (wall plane Z = 0).
// Origin: lower-left corner of the yellow field.
// `export_frame = true` rotates the whole model so Z is up and the viewer
// looks toward +Y (used by render_blockout.py); the authoring numbers do not change.
//
// Corner coordinates were traced from reference/Keypad-sketch.jpeg at about
// 10.1 px/mm and then nudged to the sketch's written dimensions. See DESIGN.md.

blockout_revision = 3;

part = "all";          // all | yellow | black | blue | keypad
export_frame = false;

// ---------- Yellow rib-field envelope (one planar quad for now) ----------
yellow_width      = 78;    // horizontal distance between the two vertical edges
yellow_left_h     = 135;   // left vertical edge
yellow_right_h    = 130;   // right vertical edge
yellow_top_rise   = 32;    // top diagonal rises this much left -> right
yellow_bottom_inset = 8;   // bottom-left corner moves right; narrows the bottom
                           // and opens the bottom-right angle (v2)
yellow_depth      = 10;    // Z thickness of the envelope
// Bottom rise follows: top_rise + left_h - right_h. Diagonals ≈ 84 / 86 mm.

// ---------- Black central mass ----------
black_bl          = [14, 20];   // lower-left corner
black_bottom_len  = 43;         // lower edge
black_bottom_ang  = 9;          // deg, lower edge rises to the right
black_left_h      = 113;        // left edge height
black_left_lean   = -2;         // X shift of top-left vs bottom-left
black_top_len     = 50;         // upper edge
black_top_ang     = 9.2;        // deg, upper edge rises to the right
black_corner_r    = 4;          // softening of the outline corners
black_depth       = 28;         // Z thickness; must exceed keypad_depth

// ---------- Keypad reference (authoritative measured body) ----------
keypad_w      = 34.5;
keypad_h      = 94.5;
keypad_r      = 5;
keypad_depth  = 25.7;
keypad_ll     = [19, 33.5];     // lower-left corner, from the sketch outline
show_keypad_window = true;      // cut the keypad outline through the black front

// ---------- Blue wrap ----------
// Outline points (elevation XY). Inner edge traced from the sketch hatching;
// outer points sit `blue_overhang` beyond the black's top and right edges.
blue_overhang  = 2.5;   // how far the wrap hangs past the black edges
blue_proud     = 3;     // how far the wrap stands in front of the black face
blue_side_drop = 12;    // how far the wrap droops down the black's side faces
blue_soft      = 3;     // outline rounding radius
blue_layers    = 4;     // stacked offsets that round the front edge

// v3: raised to clear button 2 (top Y 123.7) and the status LED (≈38, 124)
// with ≥1.5 mm margin; v2 points were [33,129] [35.5,125.5] [39,123] [46,122] [51,120.5].
blue_inner_top = [      // from the top edge, curving across to the right side
    [30.5, 137.5], [33, 131], [36, 129], [40, 128],
    [46, 127], [51, 125.5]
];
// Droop down the black's right side: [inset from black right edge, Y as sketched].
// Y is stretched downward about blue_pivot_y by blue_stretch (1 = sketch).
blue_side    = [[6, 114], [5, 106.5], [4.5, 97]];  // tip ≥ 2·blue_soft wide or rounding erases it
blue_pivot_y = 120.5;
blue_stretch = 2;       // v2: tip from Y 97 down to ≈73.5

// ---------- Derived geometry ----------
yellow_bottom_rise = yellow_top_rise + yellow_left_h - yellow_right_h;
yellow_pts = [
    [yellow_bottom_inset, 0],
    [yellow_width, yellow_bottom_rise],
    [yellow_width, yellow_bottom_rise + yellow_right_h],
    [0, yellow_left_h]
];

black_br = black_bl + black_bottom_len * [cos(black_bottom_ang), sin(black_bottom_ang)];
black_tl = black_bl + [black_left_lean, black_left_h];
black_tr = black_tl + black_top_len * [cos(black_top_ang), sin(black_top_ang)];
black_pts = [black_bl, black_br, black_tr, black_tl];

function lerp(a, b, t) = a + (b - a) * t;
// Outward normal offset for the right edge (BR -> TR) and the top edge (TL -> TR).
function unit(v) = v / norm(v);
right_dir = unit(black_tr - black_br);
right_out = [right_dir[1], -right_dir[0]];
top_dir   = unit(black_tr - black_tl);
top_out   = [-top_dir[1], top_dir[0]];
tr_out    = black_tr + (right_out + top_out) * blue_overhang;

function black_right_x(y) =
    black_br[0] + (y - black_br[1]) * (black_tr[0] - black_br[0]) / (black_tr[1] - black_br[1]);
blue_side_pts = [for (p = blue_side)
    let(y = blue_pivot_y - (blue_pivot_y - p[1]) * blue_stretch)
        [black_right_x(y) - p[0], y]];
blue_inner = concat(blue_inner_top, blue_side_pts);
blue_start = blue_inner[0];
// Outer edge hangs blue_overhang past the black's right edge at each droop level.
blue_side_out = [for (i = [len(blue_side_pts) - 1 : -1 : 0])
    [black_right_x(blue_side_pts[i][1]) + blue_overhang, blue_side_pts[i][1]]];
blue_pts = concat(
    blue_inner,
    blue_side_out,
    [tr_out,
     lerp(black_tl, black_tr, 0.7) + top_out * blue_overhang,
     blue_start + top_out * blue_overhang * 0.6]
);

// ---------- Solids ----------
module rounded_poly(pts, r) {
    offset(r = r) offset(delta = -r) polygon(pts);
}

module yellow_field() {
    linear_extrude(yellow_depth) polygon(yellow_pts);
}

module keypad_outline() {
    translate(keypad_ll)
        offset(r = keypad_r) offset(delta = -keypad_r)
            square([keypad_w, keypad_h]);
}

module keypad_ref() {
    linear_extrude(keypad_depth) keypad_outline();
}

module black_mass() {
    difference() {
        // Starts slightly inside the yellow so the masses overlap rather than touch.
        translate([0, 0, 0.01]) linear_extrude(black_depth - 0.01)
            rounded_poly(black_pts, black_corner_r);
        if (show_keypad_window)
            translate([0, 0, -1]) linear_extrude(black_depth + 2) keypad_outline();
    }
}

module blue_outline() {
    offset(r = blue_soft) offset(delta = -blue_soft) polygon(blue_pts);
}

module blue_wrap() {
    z0 = black_depth - blue_side_drop;
    step = blue_proud / blue_layers;
    // Body down the sides, then a softened front cap built from shrinking layers.
    translate([0, 0, z0]) linear_extrude(blue_side_drop + 0.01) blue_outline();
    for (i = [0 : blue_layers - 1])
        translate([0, 0, black_depth + i * step])
            linear_extrude(step + 0.01)
                offset(r = -blue_soft * pow((i + 1) / blue_layers, 2)) blue_outline();
}

module tint(c) { if (part == "all") color(c) children(); else children(); }

module model() {
    // Single-part exports stay uncoloured so the OFF files carry plain faces.
    if (part == "all" || part == "yellow") tint("#f2c230") yellow_field();
    if (part == "all" || part == "black")  tint("#1d1d1f") black_mass();
    if (part == "all" || part == "blue")   tint("#9fd3f2") blue_wrap();
    if (part == "all" || part == "keypad") tint("#a7a9ac") keypad_ref();
}

if (export_frame) rotate([90, 0, 0]) model();
else model();

echo(str("blockout v", blockout_revision,
         " yellow diag top=", norm(yellow_pts[3] - yellow_pts[2]),
         " bottom=", norm(yellow_pts[1] - yellow_pts[0]),
         " black right=", norm(black_tr - black_br),
         " black bottom=", norm(black_br - black_bl)));
