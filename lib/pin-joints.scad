// Hex pin joints for permanently glued multi-part prints.
// mm, OpenSCAD snapshot (Manifold). No top-level geometry: `use <pin-joints.scad>`.
//
// Joint frame (local): origin on the interface plane between part A and part B.
//   +Z  pin axis, pointing into part B (part A lies on -Z).
//   +Y  normal of the "roof" hex flat. For a hole printed sideways, make this
//       the print-up direction of that part so the roof is a short flat bridge.
//   Hex flats sit at +/-Y and +/-60 deg from it; vertices point along +/-X.
// Every hole and pin is placed through the same joint frame, so the two parts
// cannot disagree about position or hex roll. Guide: skills/add-pin-joints/SKILL.md.

function pj_version() = 2;

// --- Spec ------------------------------------------------------------------

// Adhesive presets: [clearance per side, glue grooves per engaged side].
// Starting values, not calibrated for your printer: print pin-fit-coupon.scad
// in your material and pass clearance= with the step that fits best.
// Example only: on the author's printer (ASA) 0.12 was the best slip fit.
// Epoxy is one coupon step looser (provisional, unglued). PLA/PETG untested.
function pj_preset(adhesive) =
    adhesive == "ca"      ? [0.12, 0] :
    adhesive == "epoxy"   ? [0.16, 2] :
    adhesive == "solvent" ? [0.10, 0] :
    assert(false, str("pj_preset: unknown adhesive ", adhesive)) undef;

function pj_spec(af=6, engage_a=10, engage_b=10, adhesive="ca", clearance=undef,
                 bottom_gap=0.6, vent_width=1.2, vent_depth=0.6,
                 mouth_chamfer=0.4, end_chamfer=0.5, foot_chamfer=0.3,
                 grooves=undef, groove_width=1.0, groove_depth=0.4) =
    let(p = pj_preset(adhesive))
    [["af", af], ["engage_a", engage_a], ["engage_b", engage_b],
     ["adhesive", adhesive],
     ["clearance", is_undef(clearance) ? p[0] : clearance],
     ["bottom_gap", bottom_gap], ["vent_width", vent_width],
     ["vent_depth", vent_depth], ["mouth_chamfer", mouth_chamfer],
     ["end_chamfer", end_chamfer], ["foot_chamfer", foot_chamfer],
     ["grooves", is_undef(grooves) ? p[1] : grooves],
     ["groove_width", groove_width], ["groove_depth", groove_depth]];

function pj(spec, key) =
    let(i = search([key], spec)[0])
    assert(i != [], str("pj: unknown spec key ", key)) spec[i][1];

function pj_hole_af(spec) = pj(spec, "af") + 2*pj(spec, "clearance");
function pj_pin_length(spec) = pj(spec, "engage_a") + pj(spec, "engage_b");
// Roof bridge of a sideways hole is one hex side.
function pj_roof_span(spec) = pj_hole_af(spec)/sqrt(3);

// --- Joint frame -----------------------------------------------------------

function pj_unit(v) = v/norm(v);

// 4x4 local->assembly matrix. `up` is projected perpendicular to `axis`.
function pj_frame(origin=[0,0,0], axis=[0,0,1], up=[0,1,0]) =
    let(z = pj_unit(axis), y0 = up - (up*z)*z)
    assert(norm(y0) > 1e-6, "pj_frame: up must not be parallel to axis")
    let(y = pj_unit(y0), x = cross(y, z))
    [[x[0], y[0], z[0], origin[0]],
     [x[1], y[1], z[1], origin[1]],
     [x[2], y[2], z[2], origin[2]],
     [0, 0, 0, 1]];

module pj_at(joint) multmatrix(joint) children();

// --- Print-orientation check ---------------------------------------------

// Same convention as rotate([ax, ay, az]): X, then Y, then Z.
function pj_rotation(a) =
    let(cx=cos(a[0]), sx=sin(a[0]), cy=cos(a[1]), sy=sin(a[1]),
        cz=cos(a[2]), sz=sin(a[2]))
    [[cz,-sz,0],[sz,cz,0],[0,0,1]] * [[cy,0,sy],[0,1,0],[-sy,0,cy]]
        * [[1,0,0],[0,cx,-sx],[0,sx,cx]];

// Classify a socket in the part's print pose. `side` is "a" or "b";
// `print_rot` is the rotate() angle vector that takes assembly to print pose.
//   vertical-open-top   blind end at the bottom, open upward
//   vertical-bridged    blind end is a ceiling; bottom_gap absorbs any sag
//   sideways-flat-roof  roof is one flat: a short bridge (preferred sideways)
//   sideways-point-roof roof faces at <=30 deg from horizontal: will droop
//   tilted              axis neither vertical nor horizontal
function pj_socket_pose(joint, side, print_rot=[0,0,0], tol=1e-3) =
    let(R = [for(i=[0:2]) [for(j=[0:2]) joint[i][j]]],
        M = pj_rotation(print_rot)*R,
        dir = (side == "a" ? -1 : 1)*(M*[0,0,1]),
        flat_up = max([for(k=[0:2]) abs((M*[cos(90+60*k), sin(90+60*k), 0])[2])]))
    abs(dir[2]) > 1-tol ? (dir[2] < 0 ? "vertical-open-top" : "vertical-bridged") :
    abs(dir[2]) < tol   ? (flat_up > 1-tol ? "sideways-flat-roof" : "sideways-point-roof") :
    "tilted";

function pj_pose_ok(pose) = pose != "sideways-point-roof" && pose != "tilted";

// Fails the render unless the socket prints cleanly in that pose.
module pj_assert_pose(joint, side, print_rot=[0,0,0], label="joint", allow_tilt=false) {
    pose = pj_socket_pose(joint, side, print_rot);
    echo(str("pj_pose: ", label, " side ", side, ": ", pose));
    assert(pj_pose_ok(pose) || (allow_tilt && pose == "tilted"),
           str("pj: ", label, " side ", side, " prints as ", pose,
               "; set the joint's up vector to this part's print-up direction"));
}

// --- 2D profiles -----------------------------------------------------------

// Hex with flats at +/-Y.
module pj_hex(af) circle(d=2*af/sqrt(3), $fn=6);

// Pin profile: the -Y flat is the print-bed face. Its two long edges are
// chamfered so elephant's foot does not widen the pin.
module pj_pin_profile(af, foot) {
    r = af/sqrt(3);
    h = af/2;
    if (foot > 0)
        polygon([[r,0], [r/2,h], [-r/2,h], [-r,0],
                 [-r/2-foot/2,-h+foot*sqrt(3)/2], [-r/2+foot,-h],
                 [r/2-foot,-h], [r/2+foot/2,-h+foot*sqrt(3)/2]]);
    else
        pj_hex(af);
}

// --- Pin -------------------------------------------------------------------

// Pin segment along local Z from z0 to z1. Chamfers apply to free ends only.
module pj_pin_segment(spec, z0, z1, chamfer0=true, chamfer1=true) {
    af = pj(spec, "af");
    c = pj(spec, "end_chamfer");
    foot = pj(spec, "foot_chamfer");
    eps = 0.01;
    assert(z1 - z0 > 2*c + 2*eps);
    difference() {
        hull() {
            translate([0,0,z0])
                linear_extrude(eps) offset(delta=chamfer0 ? -c : 0) pj_pin_profile(af, foot);
            translate([0,0,z0 + (chamfer0 ? c : 0)])
                linear_extrude(z1 - z0 - (chamfer0 ? c : 0) - (chamfer1 ? c : 0))
                    pj_pin_profile(af, foot);
            translate([0,0,z1 - eps])
                linear_extrude(eps) offset(delta=chamfer1 ? -c : 0) pj_pin_profile(af, foot);
        }
        pj_grooves(spec, z0, z1);
    }
}

// Glue-key grooves, evenly spaced inside each engaged side of the interface.
module pj_grooves(spec, z0, z1) {
    n = pj(spec, "grooves");
    w = pj(spec, "groove_width");
    af = pj(spec, "af");
    if (n > 0)
        for (side = [-1, 1], i = [1:n]) {
            engage = pj(spec, side < 0 ? "engage_a" : "engage_b");
            z = side*engage*i/(n + 1);
            if (z - w/2 > z0 && z + w/2 < z1)
                translate([0,0,z - w/2])
                    linear_extrude(w) difference() {
                        offset(delta=1) pj_hex(af);
                        offset(delta=-pj(spec, "groove_depth")) pj_hex(af);
                    }
        }
}

// Loose pin in joint coordinates (spans both parts).
module pj_pin(spec) pj_pin_segment(spec, -pj(spec, "engage_a"), pj(spec, "engage_b"));

// Loose pin in print pose: lying on its -Y flat, axis along Y, bed at Z=0.
module pj_pin_print(spec)
    translate([0,0,pj(spec, "af")/2]) rotate([90,0,0]) pj_pin(spec);

// Pin printed onto part A, protruding into part B. `embed` overlaps part A.
module pj_pin_stub(spec, embed=0.5)
    pj_pin_segment(spec, -embed, pj(spec, "engage_b"), false, true);

// --- Sockets (subtract these) ---------------------------------------------

// Hex hole from the mouth at z=0 to z=length, with vent along the -Y flat.
// Mouth chamfers at z=0 and, if `far_mouth`, at z=length.
module pj_hex_bore(spec, length, far_mouth=false) {
    af = pj_hole_af(spec);
    mc = pj(spec, "mouth_chamfer");
    out = 0.5;
    union() {
        translate([0,0,-out]) linear_extrude(length + out + (far_mouth ? out : 0)) pj_hex(af);
        for (end = far_mouth ? [0, 1] : [0])
            translate([0,0,end*length]) scale([1,1,end == 1 ? -1 : 1]) hull() {
                translate([0,0,-out]) linear_extrude(out) offset(delta=mc) pj_hex(af);
                translate([0,0,mc]) linear_extrude(0.01) pj_hex(af);
            }
        if (pj(spec, "vent_depth") > 0)
            translate([-pj(spec, "vent_width")/2, -af/2 - pj(spec, "vent_depth"), -out])
                cube([pj(spec, "vent_width"), pj(spec, "vent_depth") + 0.1,
                      length + out + (far_mouth ? out : 0)]);
    }
}

// Blind socket in joint coordinates for part "a" (extends -Z) or "b" (+Z).
module pj_socket(spec, side) {
    assert(side == "a" || side == "b");
    depth = pj(spec, side == "a" ? "engage_a" : "engage_b") + pj(spec, "bottom_gap");
    scale([1,1,side == "a" ? -1 : 1]) pj_hex_bore(spec, depth);
}

// Through bore for test coupons, from z=0 to z=length, both mouths chamfered.
module pj_through(spec, length) pj_hex_bore(spec, length, far_mouth=true);
