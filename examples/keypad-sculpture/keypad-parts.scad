// Wyze keypad sculpture — PRINTABLE PARTS (example: originally printed in ASA on a 0.6 mm nozzle)
// Final geometry for the three printed parts, built on parts-blockout.scad
// rev 4 (included, unchanged, so the blockout stays reproducible):
//   yellow  ribs + plate + 2 ridged keys, 11 door magnet pockets
//   shell   one black shell: 0.8 skin, button/LED holes, snug keypad walls
//   blue    drape glued to the shell front, located by 2 printed hex stubs
// Coupon-validated values are inherited, not redefined here (observations.md
// 2026-10-25): skin 0.8, button holes Ø11.6, keypad fit 0.15/side, magnet
// pockets Ø6.3 × 1.9, ridge interference 0.25, LED hole at B11.
//
// v1 finishing (work/004): the blue's stacked front layers become one smooth
// rounded cap whose bed side is clipped at 45° (prints face-down without
// supports); 0.4 mm elephant-foot chamfer on the shell's front perimeter;
// 0.4 mm mouth chamfer on the door pockets (they open on the bed); the blue
// keeps the blockout silhouette and Z range.
//
// Units: mm. Elevation frame (blockout.scad): X right, Y up, Z out of the door
// (door Z = 0), origin = yellow field's lower-left corner. Print poses put the
// bed at Z = 0.
//
// Selector: `piece` (the included files already use `part` and `show`;
// `part = "none"` silences parts-blockout's own scene).

include <parts-blockout.scad>
use <../../lib/pin-joints.scad>
part = "none";

parts_revision = 1;

piece = "assembly";   // assembly | yellow | shell | blue | keypad | keypad_buttons | keypad_led
                      // reference: blockout_drape
                      // print pose: yellow_print | shell_print | blue_print
                      // magnets: door_magnets | key_magnets_yellow | key_magnets_shell
                      // check-only: x_* (intersections; see geometry-check-config-v1.json)
exploded = false;     // [yellow, keypad, shell, blue] lift as parts-blockout
env_grow = 0.14;      // x_shell_keypad_env: keypad envelope growth per side (gap probe)

// ---------- Finishing ----------
shell_chamfer = 0.4;  // 45° on the shell's front outer edge (bed face, elephant foot)
pocket_chamfer = 0.4; // 45° mouth on the door pockets (bed face)
cap_r = blue_proud;   // blue front rounding radius: whole 3 mm cap
cap_z = shell_front_z;              // cap base = blue back over the shell (30.5)
blue_z0 = h_under + drape_lift + black_depth - blue_side_drop;   // 18.5, droop bottom
blue_front_z = cap_z + cap_r;       // 33.5 (unchanged)

// ---------- Post tops ----------
// Near post 2 a rib rises above the post top (to ≈7) and into the shell's
// magnet (found by x_magnets). Above each post top the yellow is cleared to
// Ø key_relief_d, and the shell fills the same zone (0.15 smaller per side)
// so its magnet pocket has full walls. Ridge feet continue down to the
// plate so no ridge bottom hangs over a rib gap.
key_fill_d   = key_socket_d + 2 * 0.8;          // 10.9: shell wall ring kept by x_key_wall
key_relief_d = key_fill_d + 2 * rib_clear;      // 11.2

// ---------- Blue to shell: printed hex stubs (pin-joints library v2) ----------
// The stubs print standing up on the blue's back (blue face-down) and drop
// into vertical blind sockets in the shell front. AF 3: the wall between the
// keypad cavity and the shell edge is ≈6.7 mm, too narrow for the tested AF 6.
// Clearance = `ca` preset 0.12/side (example: calibrated on the author's ASA AF 6 coupon only).
pin_spec = pj_spec(af = 3, engage_a = 0, engage_b = 4, adhesive = "ca",
                   end_chamfer = 0.4, mouth_chamfer = 0.3, vent_depth = 0);
pin_embed = 0.5;
// The droop slides down over the shell's top and right sides: glue clearance
// per side (same `ca` slip value; ASA example). The back of the cap sits on the shell
// front (Z 30.5), the main glue face.
blue_clear = 0.12;
pin_xy = [[57, 118], [55, 136]];
// Part A = blue (stub), part B = shell; axis points into the shell (-Z).
function pin_joint(p) = pj_frame(origin = [each p, cap_z], axis = [0, 0, -1], up = [0, 1, 0]);

// Print rotations (applied before the bed translation).
yellow_rot = [0, 0, 0];
shell_rot  = [180, 0, 0];
blue_rot   = [180, 0, 0];
print_y    = 170;     // shift after the X flip so the flipped parts sit at +Y

$fn = 40;

// ---------- Parts ----------
module yellow_final() {
    difference() {
        union() {
            yellow_part();
            for (p = key_xy) translate([each p, 0])   // ridge feet, plate to rib-top level
                intersection() { ridges(ridge_interference, backing_depth - 0.1, h_under + ridge_lead + 0.1);
                                 translate([0, 0, backing_depth - 0.1]) cylinder(d = 20, h = h_under - backing_depth + 0.2); }
        }
        for (p = door_mag_xy) translate([each p, -1])
            cylinder(d1 = door_pocket[0] + 2 * (pocket_chamfer + 1), d2 = door_pocket[0], h = pocket_chamfer + 1);
        for (p = key_xy) intersection() {   // under the shell only
            translate([each p, key_top]) cylinder(d = key_relief_d, h = 50);
            black_prism(key_top - 1, 60);
        }
    }
}

module shell_chamfer_hull() {
    // The black outline is convex, so a hull gives an exact 45° front chamfer.
    hull() {
        black_prism(shell_back_z - 1, shell_front_z - shell_chamfer);
        black_prism(shell_front_z - 0.01, shell_front_z, -shell_chamfer);
    }
}

module shell_final() {
    difference() {
        intersection() {
            union() {
                shell(pins = false);
                for (p = key_xy) intersection() {
                    translate([each p, key_top + 0.05]) cylinder(d = key_fill_d, h = 50);
                    difference() { black_prism(shell_back_z, shell_front_z); keypad_cavity(shell_back_z - 1, keypad_face_z); }
                }
            }
            shell_chamfer_hull();
        }
        for (p = key_xy) translate([each p, key_top + 0.05]) cylinder(d = key_pocket[0], h = key_pocket[1]);
        for (p = pin_xy) pj_at(pin_joint(p)) pj_socket(pin_spec, "b");
    }
}

// Blue profile, revolved: a vertical side of depth `down`, then a quarter
// circle of radius r whose last 45° (toward the front) is a straight chamfer.
// One minkowski of the inset outline with this solid gives the droop walls
// and the rounded cap from the same polygon, so no ledge forms where they meet.
module teardrop(r, down) {
    a = [for (t = [0 : 7.5 : 45]) [r * cos(t), r * sin(t)]];
    // $fn 40: 32 and 48 leave vertex pairs 1e-9 mm apart that merge into slivers in STL.
    rotate_extrude($fn = 40) polygon(concat([[0, -down], [r, -down]], a, [[0, r * sqrt(2)]]));
}

module blue_smooth() {
    // Same outline, droop and Z range as blue_wrap(); one rounded cap.
    intersection() {
        minkowski() {
            translate([0, 0, cap_z - 0.01]) linear_extrude(0.01) offset(delta = -cap_r) blue_outline();
            teardrop(cap_r, cap_z - blue_z0);
        }
        translate([-50, -50, blue_z0]) cube([300, 300, blue_front_z - blue_z0]);
    }
}

module blue_final() {
    difference() {
        blue_smooth();
        black_prism(-1, shell_front_z, blue_clear);
        translate([0, 0, 0.3]) yellow_clearance();
    }
    for (p = pin_xy) pj_at(pin_joint(p)) pj_pin_stub(pin_spec, pin_embed);
}

module key_magnets_yellow() { yellow_magnets(); }
module key_magnets_shell()  { shell_magnets(); }

// ---------- Print poses (bed Z = 0) ----------
module yellow_print() { rotate(yellow_rot) yellow_final(); }
module shell_print()  { translate([0, print_y, shell_front_z]) rotate(shell_rot) shell_final(); }
module blue_print()   { translate([0, print_y, blue_front_z]) rotate(blue_rot) blue_final(); }

// ---------- Scene ----------
module plift(i) { translate([0, 0, exploded ? explode_gap[i] : 0]) children(); }

if (piece == "assembly") {
    color("#f2c230") plift(0) yellow_final();
    plift(1) keypad_placed();
    color("#2a2a2e") plift(2) shell_final();
    color("#9fd3f2") plift(3) blue_final();
}
if (piece == "yellow")       yellow_final();
if (piece == "shell")        shell_final();
if (piece == "blue")         blue_final();
if (piece == "keypad")       keypad_placed();
if (piece == "keypad_buttons") translate([0, 0, keypad_back_z]) keypad_in_elevation("buttons");
if (piece == "blockout_drape") drape();   // parts-blockout v4 blue, for the silhouette check
if (piece == "keypad_led")   translate([0, 0, keypad_back_z]) keypad_in_elevation("led");
if (piece == "yellow_print") yellow_print();
if (piece == "shell_print")  shell_print();
if (piece == "blue_print")   blue_print();
if (piece == "door_magnets")       door_magnets();
if (piece == "key_magnets_yellow") key_magnets_yellow();
if (piece == "key_magnets_shell")  key_magnets_shell();
if (piece == "blue_print" || piece == "shell_print")
    for (p = pin_xy) {
        pj_assert_pose(pin_joint(p), "b", shell_rot, str("shell socket ", p));
    }

// ---------- Interference and wall probes (each returns only the overlap) ----------
// Expected empty unless noted. Coincident glue faces (blue on shell) and
// seats (keypad on ribs, skin on keypad) touch only.
if (piece == "x_shell_keypad") intersection() { shell_final(); keypad_placed(); }
// Keypad side gap: the keypad outline grown by env_grow, over its full side
// height minus the corner rounding zones. Empty at 0.14, full at 0.16 => 0.15.
if (piece == "x_shell_keypad_env") intersection() {
    shell_final();
    translate([0, 0, keypad_back_z + 1]) linear_extrude(keypad_face_z - keypad_back_z - 2)
        offset(delta = env_grow) keypad_outline();
}
// Shell vs yellow with the ridges excluded (ring around each post removed).
if (piece == "x_shell_yellow") intersection() {
    shell_final();
    difference() { yellow_final(); for (p = key_xy) translate([each p, h_under - 0.01]) difference() {
        cylinder(d = key_socket_d + 2, h = 2); cylinder(d = key_d - 0.01, h = 3); } }
}
if (piece == "x_ridge_bite")   // expected NON-empty: the intended crush interference
    intersection() { shell_final(); for (p = key_xy) translate([each p, 0]) ridges(ridge_interference, h_under, key_top); }
if (piece == "x_keypad_yellow") intersection() { keypad_placed(); yellow_final(); }
if (piece == "x_blue_yellow")   intersection() { blue_final(); yellow_final(); }
if (piece == "x_blue_keypad")   intersection() { blue_final(); keypad_placed(); }
if (piece == "x_blue_shell")    intersection() { blue_final(); shell_final(); }
// Key sockets keep >= 0.8 mm shell wall to the outside and the keypad cavity.
if (piece == "x_key_wall")
    difference() {
        for (p = key_xy) translate([each p, h_under + 0.3]) cylinder(d = key_d + 2 * (rib_clear + 0.8), h = 1);
        difference() { black_prism(-1, 50); keypad_cavity(-2, 60); }
    }
// Shell magnet pockets keep >= 0.8 mm wall (Ø6.3 + 1.6 inside the shell).
if (piece == "x_shell_pocket_wall")
    difference() {
        for (p = key_xy) translate([each p, key_top + 0.3]) cylinder(d = key_pocket[0] + 1.6, h = 1.2);
        difference() { black_prism(-1, 50); keypad_cavity(-2, 60); }
    }
// Door pockets keep >= 1 mm of plate around them (above the mouth chamfer).
if (piece == "x_pocket_margin")
    difference() {
        for (p = door_mag_xy) translate([each p, 0.5]) cylinder(d = door_pocket[0] + 2, h = 1);
        backing_plate();
    }
// Key-post magnet pockets keep >= 0.8 mm wall to the Ø9 post.
if (piece == "x_post_pocket_wall")
    difference() {
        for (p = key_xy) translate([each p, key_top - key_pocket[1] + 0.2]) cylinder(d = key_pocket[0] + 1.6, h = 1.5);
        keys(ridged = false);
    }
// Pin sockets keep >= 0.8 mm of shell around the hex bore (below the mouth).
if (piece == "x_pin_wall")
    difference() {
        for (p = pin_xy) translate([each p, cap_z - pj(pin_spec, "engage_b") - pj(pin_spec, "bottom_gap") - 0.8])
            cylinder(r = pj_hole_af(pin_spec) / sqrt(3) + 0.8, h = pj(pin_spec, "engage_b") + pj(pin_spec, "bottom_gap") + 0.8 - 0.5);
        shell(pins = false);
    }
// Magnets (Ø6 × 1.9, inset 0.01 from the coincident pocket floor/roof) vs every printed part.
if (piece == "x_magnets") intersection() {
    union() {
        for (p = door_mag_xy) translate([each p, 0.01]) cylinder(d = door_mag[0], h = door_mag[1] - 0.02);
        for (p = key_xy) translate([each p, key_top - key_mag[1] + 0.01]) cylinder(d = key_mag[0], h = key_mag[1] - 0.02);
        for (p = key_xy) translate([each p, key_top + 0.06]) cylinder(d = key_mag[0], h = key_mag[1] - 0.02);
    }
    union() { yellow_final(); shell_final(); blue_final(); }
}
if (piece == "x_control")   // expected NON-empty: black envelope vs yellow
    intersection() { black_prism(shell_back_z - 1, shell_front_z); yellow_final(); }

echo(str("keypad parts v", parts_revision, " (blockout v", parts_blockout_revision,
         "): shell front Z=", shell_front_z, " blue front Z=", blue_front_z,
         " button top Z=", keypad_face_z + button_proud));
