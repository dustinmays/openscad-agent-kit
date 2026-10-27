// Reusable sacrificial triangle. mm, OpenSCAD snapshot (Manifold); no top-level geometry.
// X: thin fin direction. +Y: toward attachment face. Z: up from print bed.
// face_y approximates a curved surface only at the centerline; verify actual CSG.

function _fin_levels(height,tab_count,levels) =
    is_undef(levels) ? [for(i=[0:tab_count-1]) i*(height-2)/(tab_count-1)] : levels;

module _fin_across_x(width) {
    translate([-width/2,0,0])
        multmatrix([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]])
            linear_extrude(height=width,convexity=10) children();
}

module breakaway_fin_core(face_y=0,height=90,depth=32,fin_thickness=0.6,
                          gap=0.6,foot_width=8,foot_height=0.4,foot_setback=0.5) {
    front=face_y-gap;
    rear=front-depth;
    assert(height>0 && depth>foot_setback && foot_setback>=0);
    assert(fin_thickness>0 && gap>0 && foot_height>=0);
    assert(foot_width>fin_thickness);
    union() {
        _fin_across_x(fin_thickness)
            polygon([[rear,0],[front,0],[front,height]]);
        if(foot_height>0)
            translate([-foot_width/2,rear,0])
                cube([foot_width,depth-foot_setback,foot_height]);
    }
}

module breakaway_fin_tabs(face_y=0,height=90,depth=32,gap=0.6,tab_width=0.5,
                          tab_height=0.4,overlap=0.15,tab_count=6,levels=undef) {
    zs=_fin_levels(height,tab_count,levels);
    // Keep the union inside the narrowing fin even for short/deepness variants.
    join=min(0.05,depth*(height-max(zs)-tab_height)/(2*height));
    assert(height>2+tab_height && depth>0 && gap>0);
    assert(tab_count>=2 && floor(tab_count)==tab_count);
    assert(tab_width>0 && tab_height>0 && overlap>0 && len(zs)>0);
    assert(min(zs)>=0 && max(zs)+tab_height<height);
    assert(join>0.001,"Move the top contact lower or increase the fin depth.");
    for(z=zs)
        translate([-tab_width/2,face_y-gap-join,z])
            cube([tab_width,gap+overlap+join,tab_height]);
}

module breakaway_fin(face_y=0,height=90,depth=32,fin_thickness=0.6,gap=0.6,
                     foot_width=8,foot_height=0.4,foot_setback=0.5,
                     tab_width=0.5,tab_height=0.4,overlap=0.15,
                     tab_count=6,levels=undef) {
    // A narrower tab avoids coincident tab/fin side faces in this construction.
    assert(tab_width<fin_thickness);
    union() {
        breakaway_fin_core(face_y,height,depth,fin_thickness,gap,
                           foot_width,foot_height,foot_setback);
        breakaway_fin_tabs(face_y,height,depth,gap,tab_width,tab_height,
                           overlap,tab_count,levels);
    }
}
