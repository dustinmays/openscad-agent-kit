// Wyze keypad sculpture — PRINTABLE PART SPLIT, BLOCKOUT STAGE (not for printing)
// Splits the settled design (ribs-blockout.scad rev 4: variant C, backed,
// plate_style 1) into separately printed parts. Placement only: no final
// tolerances, fillets or print exports.
//   v1 (Stage A): glued black body + lift-off cover, keypad on Velcro.
//   v2 (Stage B, DESIGN decision 8): ONE black shell (0.8 mm skin, snug walls,
//       open back) captures the keypad on the rib tops; no Velcro. The shell,
//       with the blue glued on, pulls straight off the yellow; 2 magnet keys
//       locate and clamp it.
//   v3 (Stage C): crush ridges on the yellow posts; print-ready coupons (the author's ASA print, example only)
//       (shell fit coupon, post fit coupon) in print pose.
//
// Units: mm. Elevation frame of blockout.scad: X right, Y up, Z out of the
// door (door Z = 0); origin = yellow field's lower-left corner.
// `export_frame = true` rotates like the blockout (Z up, viewer toward +Y).
//
// The included files share one global namespace. This file reuses the
// blockout's `part` global as its selector. The blockout itself draws
// part = all | yellow | black | blue | keypad, so never use those names here.
// ribs-blockout's own scene is silenced with `show = "none"`.

include <ribs-blockout.scad>
show = "none";              // silence ribs-blockout.scad's scene (included)

parts_blockout_revision = 4;  // v4: LED hole moved 1 mm left, 0.5 mm up (coupon v3 print)

part     = "assembly";      // assembly | yellow_part | shell | drape | keypad_ref | coupon
                            // | yellow_magnets | shell_magnets | door_magnets
                            // print pose (bed Z = 0): shell_coupon_print | post_coupon_yellow_print
                            //   | post_coupon_black_print
                            // in use: shell_coupon_inuse | keypad_top_inuse | post_coupon_inuse_*
                            // check-only: probe_*
exploded = false;
explode_gap = [0, 35, 70, 70];   // Z lift: yellow, keypad, shell, drape (drape rides on the shell)
section  = "none";          // none | keypad (cut at keypad centre X) | seat (Z <= 8)

// ---------- Keypad captured by the shell (MEASUREMENTS rev 4) ----------
keypad_back_z = h_under;                 // back on the rib tops (H11: no Velcro)
keypad_face_z = keypad_back_z + 25.7;    // K3 -> 29.7
button_proud  = 0.9;                     // B6
snug          = 0.15;       // shell wall clearance per side around the keypad (starting value from the author's ASA example)
led_xy        = [37, 124.5];  // B11 in elevation; v3 coupon hole at [38, 124] was 1 mm right, 0.5 mm low
led_hole_d    = 2;

// ---------- Shell ----------
// Skin 0.8 = 4 layers at 0.2 mm (the author's example printer had a 0.6 mm nozzle), printed face-down as
// the first layers; in use it rests on the keypad face (backed everywhere).
skin        = 0.8;
button_hole = 11.6;         // B1 10.8 + 0.4 per side
shell_back_z  = h_under;    // back rim sits on the rib tops
shell_front_z = keypad_face_z + skin;    // 30.5; buttons 0.1 proud
rib_clear   = 0.15;         // shell notches / key sockets clear the yellow by this (X, Y)
drape_lift  = shell_front_z - (h_under + black_depth);   // blue rides on the shell (-1.5)

// Finger notches: cut through the left and right walls at the back so the
// keypad sides can be pinched and the keypad pulled out of the open back.
notch_y = [72, 88];         // Y span (keypad mid-height)
notch_h = 6;                // Z height from the back rim

// ---------- Magnets ----------
door_mag    = [6, 1.9];     // H4/H5
door_pocket = [6.3, 1.9];   // Ø, depth = magnet: face flush with the plate back (1.1 mm roof)
door_mag_xy = [[14, 25], [40, 30], [63, 43], [12, 60], [10, 100], [12, 122],
               [67, 70], [67, 110], [67, 142], [38, 80], [38, 125]];
// Shell keys: yellow posts rising above the rib tops into sockets in the
// shell's back rim. They carry the downward (shear) load; the 6 × 1.9 mm
// magnet pair in each only clamps. Only these two diagonal corners have
// room for a Ø9 post with ≥ 0.8 mm walls (bottom-left and top-right walls).
key_d    = 9;
key_top  = h_under + 1.5;   // post stands 1.5 above the rib tops
key_xy   = [[22, 27.5], [53, 133.5]];
key_mag  = door_mag;        // same 6 × 1.9 stock (H10: 20+)
key_pocket = door_pocket;
key_socket_d = key_d + 2 * rib_clear;   // 9.3, cut by yellow_clearance()

// Crush ridges (Stage C) on the yellow posts, not in the shell sockets:
// external ridges print sharper than internal ones (seen with the author's 0.6 mm nozzle, example), can be
// measured with calipers, and the post coupon tests them directly. They run
// parallel to the pull (Z), so removal stays a straight pull; a 45° lead-in
// tops each ridge. Interference is radial, ridge tip vs socket wall.
ridge_count        = 4;
ridge_interference = 0.25;  // mm, radial; coupon step 2 chosen by the author (DESIGN 10)
ridge_w            = 1.2;   // ridge diameter (about two lines on the author's 0.6 mm nozzle, example; three 0.4 mm lines)
ridge_lead         = 0.4;   // lead-in height at the ridge top

// ---------- Blue to shell (placement only) ----------
drape_pin = [3, 2];         // Ø, engagement each side
drape_pin_xy = [[57.5, 118], [55, 136]];

// ---------- Fit coupon ----------
// Top end of the shell: rows 1–2 (buttons 1–4), LED, top wall; walls cut to
// 8 mm so it prints fast and still tests the snug fit on three sides.
coupon_y = [95, 146];
coupon_z = [shell_front_z - 8.8, shell_front_z + 1];

$fn = 40;

// ---------- Parts ----------
module black_prism(z0, z1, grow = 0) {
    translate([0, 0, z0]) linear_extrude(z1 - z0)
        offset(delta = grow) rounded_poly(black_pts, black_corner_r);
}

module keypad_cavity(z0, z1) {
    translate([0, 0, z0]) linear_extrude(z1 - z0) offset(delta = snug) keypad_outline();
}

// Ridges around a post axis from z0 to z1; tip radius = socket radius + i.
module ridges(i, z0, z1) {
    rc = key_socket_d / 2 + i - ridge_w / 2;
    for (k = [0 : ridge_count - 1]) rotate(45 + 360 * k / ridge_count) translate([rc, 0, z0]) {
        cylinder(d = ridge_w, h = z1 - z0 - ridge_lead);
        translate([0, 0, z1 - z0 - ridge_lead]) cylinder(d1 = ridge_w, d2 = ridge_w - 2 * ridge_lead, h = ridge_lead);
    }
}

module keys(ridged = true) {
    for (p = key_xy) translate([each p, 0]) {
        translate([0, 0, backing_depth - 0.1]) cylinder(d = key_d, h = key_top - backing_depth + 0.1);
        if (ridged) ridges(ridge_interference, h_under, key_top);
    }
}

module yellow_part() {
    difference() {
        union() { ribs(); backing_plate(); keys(); }
        for (p = door_mag_xy) translate([each p, -1]) cylinder(d = door_pocket[0], h = door_pocket[1] + 1);
        for (p = key_xy) translate([each p, key_top - key_pocket[1]]) cylinder(d = key_pocket[0], h = key_pocket[1] + 1);
    }
}

module yellow_clearance() {
    // The yellow grown by rib_clear in X and Y (and lifted 0.05): shell
    // notches and key sockets slide straight off +Z.
    for (d = [[0, 0], [rib_clear, 0], [-rib_clear, 0], [0, rib_clear], [0, -rib_clear]])
        translate([each d, 0.05]) union() { ribs(); backing_plate(); keys(ridged = false); }
}

module shell(pins = true) {
    difference() {
        black_prism(shell_back_z, shell_front_z);
        keypad_cavity(shell_back_z - 1, keypad_face_z);
        yellow_clearance();
        for (i = [0 : 11]) translate([each keypad_ll + keypad_button_centre_scad(i), keypad_face_z - 1])
            cylinder(d = button_hole, h = 5);
        translate([each led_xy, keypad_face_z - 1]) cylinder(d = led_hole_d, h = 5);
        for (p = key_xy) translate([each p, key_top + 0.05]) cylinder(d = key_pocket[0], h = key_pocket[1]);
        // Finger notches through both side walls at the back.
        translate([-10, notch_y[0], shell_back_z - 1]) cube([100, notch_y[1] - notch_y[0], notch_h + 1]);
        if (pins) for (p = drape_pin_xy) translate([each p, shell_front_z - drape_pin[1]])
            cylinder(d = drape_pin[0] + 0.3, h = drape_pin[1] + 1);
    }
}

module drape() {
    // Blue wrap glued onto the shell; trimmed off the shell volume and clear
    // of the ribs so it pulls off +Z with the shell.
    difference() {
        translate([0, 0, h_under + drape_lift]) blue_wrap();
        black_prism(-1, shell_front_z);
        translate([0, 0, 0.3]) yellow_clearance();
        for (p = drape_pin_xy) translate([each p, shell_front_z - 1])
            cylinder(d = drape_pin[0] + 0.3, h = drape_pin[1] + 1);
    }
}

module coupon() {
    intersection() {
        shell(pins = false);
        translate([-10, coupon_y[0], coupon_z[0]]) cube([100, coupon_y[1] - coupon_y[0], coupon_z[1] - coupon_z[0]]);
    }
}

module keypad_placed() {
    translate([0, 0, keypad_back_z]) keypad_in_elevation("body");
    translate([0, 0, keypad_back_z]) keypad_in_elevation("buttons");
}

module door_magnets() {
    for (p = door_mag_xy) translate([each p, 0]) cylinder(d = door_mag[0], h = door_mag[1]);
}
module yellow_magnets() {
    for (p = key_xy) translate([each p, key_top - key_mag[1]]) cylinder(d = key_mag[0], h = key_mag[1]);
}
module shell_magnets() {
    for (p = key_xy) translate([each p, key_top + 0.05]) cylinder(d = key_mag[0], h = key_mag[1]);
}

// ---------- Print-ready coupons (Stage C, bed at Z = 0; originally printed in ASA) ----------
// Shell fit coupon: flipped face-down (skin = first layers), centred.
coupon_centre = [36, (coupon_y[0] + coupon_y[1]) / 2];
module shell_coupon_print() {
    translate([0, 0, shell_front_z]) rotate([180, 0, 0])
        translate([-coupon_centre[0], -coupon_centre[1], 0]) coupon();
}

// Post fit coupon: three ridged posts (interference steps) on a base whose top
// is the rib-top plane, plus one black socket block like the shell's rim.
post_steps   = [0.15, 0.25, 0.35];   // radial ridge interference per post
post_pitch   = 16;
post_base    = [3 * 16 + 10, 20, 3];   // X, Y, thickness
post_h       = key_top - h_under;      // 1.5 above the base top, as on the yellow
block        = [20, 20, 6];
dot_d = 1.6; dot_h = 0.4;              // embossed step marks: 1, 2, 3 dots

module post_coupon_yellow() {
    t = post_base[2];
    difference() {
        union() {
            translate([0, 0, 0]) linear_extrude(t) offset(r = 3) offset(delta = -3)
                square([post_base[0], post_base[1]]);
            for (n = [0 : 2]) translate([5 + post_pitch / 2 + n * post_pitch, 8, 0]) {
                translate([0, 0, t - 0.1]) cylinder(d = key_d, h = post_h + 0.1);
                ridges(post_steps[n], t, t + post_h);
                for (k = [0 : n]) translate([(k - n / 2) * 2.6, 9, t - 0.1])
                    cylinder(d = dot_d, h = dot_h + 0.1);
            }
        }
        for (n = [0 : 2]) translate([5 + post_pitch / 2 + n * post_pitch, 8, t + post_h - key_pocket[1]])
            cylinder(d = key_pocket[0], h = key_pocket[1] + 1);
    }
}

// Socket block, mating face at Z 0 (as the shell rim on the rib tops).
module post_coupon_black() {
    difference() {
        translate([-block[0] / 2, -block[1] / 2, 0]) cube(block);
        translate([0, 0, -1]) cylinder(d = key_socket_d, h = post_h + 0.05 + 1);
        translate([0, 0, post_h + 0.05 - 0.01]) cylinder(d = key_pocket[0], h = key_pocket[1] + 0.01);
    }
}
module post_coupon_black_print() {
    // Roof on the bed; the stepped socket opens upward.
    translate([0, 0, block[2]]) rotate([180, 0, 0]) post_coupon_black();
}

module post_coupon_magnets() {
    for (n = [0 : 2]) translate([5 + post_pitch / 2 + n * post_pitch, 8, post_base[2] + post_h - key_mag[1]])
        cylinder(d = key_mag[0], h = key_mag[1]);
}

// ---------- Scene ----------
module lift(i) { translate([0, 0, exploded ? explode_gap[i] : 0]) children(); }

module clip() {
    kx = keypad_ll[0] + keypad_w / 2;   // keypad centre X
    if (section == "keypad")
        intersection() { children(); translate([-50, -50, -50]) cube([kx + 50, 300, 200]); }
    else if (section == "seat")
        intersection() { children(); translate([-50, -50, -1]) cube([200, 300, 9]); }
    else children();
}

module scene() {
    clip() {
        if (part == "assembly" || part == "yellow_part")    color("#f2c230") lift(0) yellow_part();
        if (part == "assembly" || part == "keypad_ref")     lift(1) keypad_placed();
        if (part == "assembly" || part == "shell")          color("#2a2a2e") lift(2) shell();
        if (part == "assembly" || part == "drape")          color("#9fd3f2") lift(3) drape();
        if (part == "yellow_magnets") lift(0) yellow_magnets();
        if (part == "shell_magnets")  lift(2) shell_magnets();
        if (part == "door_magnets")   door_magnets();
        if (part == "coupon")         coupon();
    }
    if (part == "shell_coupon_print")       shell_coupon_print();
    if (part == "post_coupon_yellow_print") post_coupon_yellow();
    if (part == "post_coupon_black_print")  post_coupon_black_print();
    // In use: shell coupon over the keypad's top end (elevation frame).
    if (part == "shell_coupon_inuse")       coupon();
    if (part == "keypad_top_inuse")
        intersection() { keypad_placed(); translate([-10, coupon_y[0] - 5, 0]) cube([100, 60, 40]); }
    // In use: black block seated on the middle post, cut through the post axes.
    post_cut = [[-1, 8, -1], [post_base[0] + 2, 20, 20]];   // keep the far half: cut face looks at the viewer
    if (part == "post_coupon_inuse_yellow")
        intersection() { post_coupon_yellow(); translate(post_cut[0]) cube(post_cut[1]); }
    if (part == "post_coupon_inuse_black")
        intersection() { translate([5 + post_pitch * 1.5, 8, post_base[2] + 0.05]) post_coupon_black();
                         translate(post_cut[0]) cube(post_cut[1]); }
    if (part == "post_coupon_inuse_magnets")
        intersection() { union() { post_coupon_magnets();
                             translate([5 + post_pitch * 1.5, 8, post_base[2] + post_h + 0.1]) cylinder(d = key_mag[0], h = key_mag[1]); }
                         translate(post_cut[0]) cube(post_cut[1]); }
    // Interference probes (check script): each must come out empty except the control.
    // Shell vs yellow without the ridges must be clear; the ridges alone must
    // bite into the shell (the intended interference).
    if (part == "probe_shell_yellow")
        intersection() { shell(); difference() { yellow_part(); for (p = key_xy) translate([each p, h_under - 0.01]) difference() {
            cylinder(d = key_socket_d + 2, h = 2); cylinder(d = key_d - 0.01, h = 3); } } }
    if (part == "probe_ridge_bite")    intersection() { shell(); for (p = key_xy) translate([each p, 0]) ridges(ridge_interference, h_under, key_top); }
    if (part == "probe_shell_keypad")  intersection() { shell(); keypad_placed(); }
    if (part == "probe_keypad_yellow") intersection() { keypad_placed(); yellow_part(); }
    if (part == "probe_drape_yellow")  intersection() { drape(); yellow_part(); }
    if (part == "probe_drape_shell")   intersection() { drape(); shell(); }
    // Key sockets keep >= 0.8 mm of shell wall to the outside and the cavity.
    if (part == "probe_key_wall")
        difference() {
            for (p = key_xy) translate([each p, h_under + 0.3]) cylinder(d = key_d + 2 * (rib_clear + 0.8), h = 1);
            difference() { black_prism(-1, 50); keypad_cavity(-2, 60); }
        }
    // Door pockets keep >= 1 mm of plate around them.
    if (part == "probe_pocket_margin")
        difference() {
            for (p = door_mag_xy) translate([each p, 0.5]) cylinder(d = door_pocket[0] + 2, h = 1);
            backing_plate();
        }
    if (part == "probe_control")       intersection() { black_prism(shell_back_z - 1, shell_front_z); yellow_part(); }
}

if (export_frame) rotate([90, 0, 0]) scene();
else scene();

echo(str("parts blockout v", parts_blockout_revision,
         ": keypad face Z=", keypad_face_z, " shell front Z=", shell_front_z,
         " button top Z=", keypad_face_z + button_proud,
         " drape front Z=", h_under + drape_lift + black_depth + blue_proud));
