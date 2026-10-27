// Hex pin fit coupon: clearance sweep in vertical and sideways holes.
// mm, OpenSCAD snapshot (Manifold). Bed is Z=0 for every print selector.
// Print once per material (for example PLA, then PETG). Labels are clearance per side in
// hundredths of a mm. Holes are through-bores so pins can be pushed back out.
use <pin-joints.scad>
// Export: bin/openscad --export-format asciistl -o exports/pin-fit-coupon-v1.stl lib/pin-fit-coupon.scad

coupon_revision = 1;
part = "plate"; // plate, vertical-block, sideways-block, pin, assembly-check,
                // interference, parameters
check_pin_af = 6;  // interference probe only; raise it for a positive control

pin_af = 6;               // pin across flats
clearances = [0.08, 0.12, 0.16, 0.20, 0.24]; // per side
block_thickness = 12;     // hole length through each block
pin_length = 20;          // pokes out both sides for push-out
pitch = 13;               // hole spacing along X
end_margin = 7.5;         // first/last hole center to block end
vertical_depth = 14;      // vertical block Y size
sideways_height = 17;     // sideways block Z size
hole_z = 9;               // sideways hole center height (above vent floor)
label_size = 4.2;
label_depth = 0.6;
pin_gap = 4;              // between printed pins on the plate
font = "Liberation Sans:style=Bold";

block_length = 2*end_margin + (len(clearances) - 1)*pitch;

function spec_for(c) = pj_spec(af=pin_af, engage_a=pin_length/2,
                               engage_b=pin_length/2, clearance=c);
function hole_x(i) = end_margin + i*pitch;
function label(c) = str(c < 0.095 ? "0" : "", round(c*100));

// Joint frames, defined once and used for both cutting and the pose check.
function vertical_joint(i) = pj_frame([hole_x(i), vertical_depth/2, 0], [0,0,1], [0,1,0]);
function sideways_joint(i) = pj_frame([hole_x(i), 0, hole_z], [0,1,0], [0,0,1]);

hole_wall = (vertical_depth - pj_hole_af(spec_for(max(clearances))))/2;
assert(hole_wall >= 3, "vertical block wall below 3 mm");
assert(hole_z - pj_hole_af(spec_for(max(clearances)))/2 - 0.6 >= 3, "floor below 3 mm");
assert(pitch - pj_hole_af(spec_for(max(clearances))) - 2*0.4 >= 4, "web between holes below 4 mm");

module vertical_block() {
    for (i = [0:len(clearances)-1]) pj_assert_pose(vertical_joint(i), "b", [0,0,0], str("vertical ", label(clearances[i])));
    difference() {
        cube([block_length, vertical_depth, block_thickness]);
        for (i = [0:len(clearances)-1])
            pj_at(vertical_joint(i)) pj_through(spec_for(clearances[i]), block_thickness);
        // Labels engraved in the front (-Y) face.
        for (i = [0:len(clearances)-1])
            translate([hole_x(i), label_depth, block_thickness/2]) rotate([90,0,0])
                linear_extrude(label_depth + 0.5)
                    label_text(clearances[i]);
    }
}

module sideways_block() {
    for (i = [0:len(clearances)-1]) pj_assert_pose(sideways_joint(i), "b", [0,0,0], str("sideways ", label(clearances[i])));
    difference() {
        cube([block_length, block_thickness, sideways_height]);
        for (i = [0:len(clearances)-1])
            pj_at(sideways_joint(i)) pj_through(spec_for(clearances[i]), block_thickness);
        // Labels engraved in the top face.
        for (i = [0:len(clearances)-1])
            translate([hole_x(i), block_thickness/2, sideways_height - label_depth])
                linear_extrude(label_depth + 0.5)
                    label_text(clearances[i]);
    }
}

// Rounded glyphs read better at this small engraving depth and avoid collinear sliver triangles
// that sharp shared baselines produced in the exported mesh.
module label_text(c)
    offset(r=0.15) text(label(c), size=label_size, font=font, halign="center", valign="center");

// Pins are identical; clearance lives in the holes.
module coupon_pin() pj_pin_print(spec_for(0));

module plate() {
    vertical_block();
    translate([0, vertical_depth + 6, 0]) sideways_block();
    for (i = [0:len(clearances)-1])
        translate([hole_x(i), vertical_depth + 6 + block_thickness + 6 + pin_length/2, 0])
            coupon_pin();
}

// Every pin seated in its hole (nominal, centered). For interference checks.
module seated_pins(af=pin_af) {
    s = pj_spec(af=af, engage_a=pin_length/2, engage_b=pin_length/2, clearance=0);
    for (i = [0:len(clearances)-1]) {
        pj_at(vertical_joint(i)) translate([0,0,block_thickness/2]) pj_pin(s);
        translate([0, vertical_depth + 6, 0])
            pj_at(sideways_joint(i)) translate([0,0,block_thickness/2]) pj_pin(s);
    }
}

module blocks() {
    vertical_block();
    translate([0, vertical_depth + 6, 0]) sideways_block();
}

if (part == "plate") plate();
else if (part == "vertical-block") vertical_block();
else if (part == "sideways-block") sideways_block();
else if (part == "pin") coupon_pin();
else if (part == "assembly-check") { blocks(); seated_pins(); }
// Expected empty at nominal size: pins clear every hole.
else if (part == "interference") intersection() { blocks(); seated_pins(check_pin_af); }
else if (part == "parameters")
    echo([["revision", coupon_revision], ["pin_af", pin_af], ["clearances", clearances],
          ["hole_afs", [for (c = clearances) pj_hole_af(spec_for(c))]],
          ["roof_spans", [for (c = clearances) pj_roof_span(spec_for(c))]],
          ["block_length", block_length], ["block_thickness", block_thickness],
          ["vertical_depth", vertical_depth], ["sideways_height", sideways_height],
          ["hole_z", hole_z], ["pin_length", pin_length], ["pitch", pitch],
          ["vent_depth", pj(spec_for(0), "vent_depth")],
          ["foot_chamfer", pj(spec_for(0), "foot_chamfer")],
          ["lib_version", pj_version()]]);
else assert(false, str("unknown part ", part));
