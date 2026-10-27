// Wyze keypad — REFERENCE MODEL (environment object, not a printable part)
// Every number comes from MEASUREMENTS.md rev 2 (row IDs in comments) or is marked
// ASSUMED / context.
//
// Units: mm.
// SCAD frame (this file): X right, Y UP, Z out of the face. Origin = body's
//   LOWER-left corner on the back plane (Z = 0). Seen from the front.
// Table frame (MEASUREMENTS.md "Frame"): same X and Z, Y DOWN from the body's
//   upper-left corner. Convert table -> SCAD only through kp_scad():
//   kp_scad([x, y]) = [x, keypad_h - y].
//   Worked example: button 1 table (9.7, 9.7) -> SCAD (9.7, 84.8);
//   unlock key table (24.9, 84.2) -> SCAD (24.9, 10.3).
// `export_frame = true` rotates [90,0,0] like blockout.scad (Z up, viewer
// looking toward +Y) for render_blockout.py-style views; the numbers do not change.
//
// Use from other files:  use <keypad-reference.scad>
//   wyze_keypad(part)        part = body | buttons | led | velcro | all
//   keypad_button_centre(i)  table frame, i = 0..11 row-major from button 1
//   keypad_in_elevation()    keypad placed in blockout.scad's elevation frame

keypad_reference_revision = 3;   // v3: LED moved per coupon print (B11); v2: B6 0.9

part = "all";          // all | body | buttons | led | velcro
export_frame = false;
show_velcro = false;   // add the velcro stack to part = "all"
in_elevation = false;  // place via keypad_in_elevation() (blockout frame)

// ---------- Body ----------
keypad_w     = 34.5;   // K1 body width (X)
keypad_h     = 94.5;   // K2 body height (Y)
keypad_depth = 25.7;   // K3 back to face, excluding buttons; K5 no taper
keypad_r     = 5;      // K4 plan-view corner radius (±1)
face_round   = 2;      // K8 front face-to-side edge rounding (assumed, ±1)

recess_inset = 2;      // ASSUMED — MEASUREMENTS K7 pending (inset from body edge)
recess_depth = 1.75;   // ASSUMED — K6 reported 1.5–2, midpoint used

// ---------- Buttons ----------
button_d       = 10.8;   // B1
button_cols    = 2;      // B2
button_rows    = 6;      // B2
button_pitch_x = 15.2;   // B3
button_pitch_y = 14.9;   // B4
button1        = [9.7, 9.7];  // B5 table frame (±0.5)
button_proud   = 0.9;    // B6 reported (MEASUREMENTS rev 2)
button_round   = 0.5;    // B7 context: flat top, soft edge (display only)
button_embed   = 0.2;    // overlap into the face so part "all" fuses

// ---------- Status LED (context, display aid) ----------
led_centre = [18, 3.5];  // B11 (coupon-corrected from B9 [19, 4]), table frame
led_d      = 1.5;        // B10 context (±1)
led_proud  = 0.1;        // display only: lifts the disc so it shows in renders

// ---------- Velcro stack (optional) ----------
velcro_thickness = 3.5;  // H1 3–4, midpoint; sits on the recess floor (H2)
velcro_margin    = 1;    // ASSUMED: footprint = recess outline inset 1 mm

// ---------- Blockout placement ----------
elevation_ll = [19, 33.5];  // blockout.scad v3 keypad_ll (unchanged since v2) (approved composition)

$fn = 48;
eps = 0.01;

// ---------- Frame helpers ----------
function kp_scad(p) = [p[0], keypad_h - p[1]];
function keypad_button_centre(i) =
    [button1[0] + (i % button_cols) * button_pitch_x,
     button1[1] + floor(i / button_cols) * button_pitch_y];
function keypad_button_centre_scad(i) = kp_scad(keypad_button_centre(i));

// ---------- Geometry ----------
module rounded_rect(size, r) {
    offset(r = r) offset(delta = -r) square(size);
}

module plan_outline(inset = 0) {
    translate([inset, inset])
        rounded_rect([keypad_w - 2 * inset, keypad_h - 2 * inset], keypad_r - inset);
}

module body_solid() {
    steps = 8;
    // Straight sides up to the start of the rounding, then a quarter-round
    // front edge built by hulling inset slices (the plan outline is convex).
    hull() {
        linear_extrude(keypad_depth - face_round) plan_outline();
        for (k = [1 : steps]) let(a = 90 * k / steps)
            translate([0, 0, keypad_depth - face_round + face_round * sin(a) - eps])
                linear_extrude(eps) plan_outline(face_round * (1 - cos(a)));
    }
}

module body() {
    difference() {
        body_solid();
        translate([0, 0, -1]) linear_extrude(recess_depth + 1) plan_outline(recess_inset);
    }
}

module button() {
    // Soft top edge (B7, context): a short cylinder hulled with a rounded cap.
    h = button_embed + button_proud;
    hull() {
        cylinder(d = button_d, h = h - button_round);
        translate([0, 0, h - button_round])
            rotate_extrude() translate([button_d / 2 - button_round, 0])
                intersection() { circle(button_round); square(button_round); }
        cylinder(d = button_d - 2 * button_round, h = h);
    }
}

module buttons() {
    for (i = [0 : button_cols * button_rows - 1])
        translate([each keypad_button_centre_scad(i), keypad_depth - button_embed])
            button();
}

module led() {
    translate([each kp_scad(led_centre), keypad_depth - 0.2])
        cylinder(d = led_d, h = 0.2 + led_proud);
}

module velcro() {
    // Sits on the recess floor and stands proud of the back by H3.
    translate([0, 0, recess_depth + eps - velcro_thickness])
        linear_extrude(velcro_thickness) plan_outline(recess_inset + velcro_margin);
}

// Single-part exports stay uncoloured so the OFF files carry plain faces.
module tint(c, on) { if (on) color(c) children(); else children(); }

module wyze_keypad(part = "all") {
    if (part == "all" || part == "body")    tint("#a7a9ac", part == "all") body();
    if (part == "all" || part == "buttons") tint("#5a5b5e", part == "all") buttons();
    if (part == "all" || part == "led")     tint("#7ee08a", part == "all") led();
    if (part == "velcro" || (part == "all" && show_velcro)) tint("#e8e2d0", part == "all") velcro();
}

module keypad_in_elevation(part = "all") {
    // Blockout elevation frame: X right, Y up, Z out of wall, back on Z = 0.
    translate([each elevation_ll, 0]) wyze_keypad(part);
}

module scene() { if (in_elevation) keypad_in_elevation(part); else wyze_keypad(part); }

if (export_frame) rotate([90, 0, 0]) scene();
else scene();

echo(str("keypad reference v", keypad_reference_revision,
         " button1 scad=", keypad_button_centre_scad(0),
         " unlock scad=", keypad_button_centre_scad(11)));
