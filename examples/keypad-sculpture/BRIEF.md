<!-- Agent-written handoff supplied by the author on 2026-10-25, preserved verbatim.
     "The attached hand sketch" = reference/Keypad-sketch.jpeg. -->

# Wyze Keypad Sculptural Wall Mount

We are designing a 3D-printable, adhesive-mounted sculptural surround for an existing Wyze door-lock keypad. The attached hand sketch is the authoritative visual/compositional reference for this phase.

This project should proceed iteratively. **Do not attempt to design the finished printable object yet.**

## Design intent

This should feel like a small modernist/constructivist wall sculpture that happens to contain a functional keypad—not like a conventional electronics enclosure with decorative trim.

The composition consists of three primary visual elements:

1. **Yellow rib field** — currently represented only by its overall outer envelope.
2. **Black central mass** — a strong, forward-positioned geometric form containing/concealing the existing keypad.
3. **Baby-blue wrap** — a smaller organic/sculptural form that appears to drape, melt, or wrap over the upper-right portion of the black mass.

The existing gray Wyze plastic should eventually be visually suppressed so that the gray button faces become the principal visible parts of the original product.

There is deliberately a contrast in formal language:

- Yellow: disciplined, repetitive, directional.
- Black: rigid, monolithic, geometric.
- Blue: soft, organic, draped/melty.
- Gray keypad buttons: orderly functional controls.

## Known keypad geometry

Treat these dimensions as authoritative:

- Overall keypad body: **34.5 mm wide × 94.5 mm tall**
- Body corner radius: approximately **5 mm**
- Body depth: **25.7 mm**
- Essentially no taper.

Button geometry is known but is **not necessary for the initial blocking model**:

- Button diameter: **10.8 mm**
- 2 columns × 6 rows
- Horizontal pitch: **15.2 mm**
- Vertical pitch: **14.9 mm**
- Approximate upper-left button center relative to keypad upper-left: **X = 9.7 mm, Y = 9.7 mm**

The button layout can be implemented in a later phase when the actual faceplate is developed.

## Composition from hand sketch

Use the attached sketch as the primary reference rather than attempting to infer a better composition.

### Yellow field envelope

For blocking, represent the entire future yellow rib assembly as **one simple solid planar rhomboid/parallelogram-like form**.

Approximate sketch dimensions:

- Upper diagonal edge: **85 mm**
- Lower diagonal edge: **85 mm**
- Left extent/edge: approximately **135 mm**
- Right extent/edge: approximately **130 mm**

Match the *gesture and relative placement* in the sketch. These measurements are initial composition dimensions, not final manufacturing dimensions.

Do **not** create individual ribs yet.

### Black mass

Represent the black element as a simple solid geometric block surrounding the keypad.

Approximate sketch dimensions:

- Upper edge: **50 mm**
- Lower edge: **43 mm**
- Left edge: approximately **113 mm**
- Right edge: approximately **114 mm**

The black mass should follow the asymmetrical/slightly rhomboidal gesture shown in the sketch rather than becoming a generic centered rounded rectangle.

The actual 34.5 × 94.5 mm keypad should be represented as a simple reference solid positioned within it so we can judge scale and margins.

### Blue extended wrap

The sketch shows the intended location and gesture but deliberately does not dimension this element.

Use design judgment to create a **very simple blocking interpretation**.

The blue element originates around the upper portion of the black mass and wraps toward/around its upper-right corner. It should feel somewhat soft, drooping, or melty in contrast with the hard black geometry.

Do not add elaborate surface detail. At this stage we are evaluating its **silhouette, area, placement, and relationship to the black mass**.

## PHASE 1 — BLOCKING ONLY

This is the most important instruction.

Create an extremely simple OpenSCAD blocking model first.

Use three visually distinct solids:

- yellow = rib-field envelope
- black = central mass
- baby blue = wrap

Also include the keypad as a neutral/reference solid if useful.

Do not yet implement:

- individual yellow ribs
- mathematical wave deformation
- Bézier sweeps
- button holes
- finished faceplate
- adhesive pockets
- mounting hardware
- snap fits
- print tolerances
- fillets beyond what is useful for recognizing the forms
- detailed wall-mount engineering
- final part separation

Keep parameters near the top of the OpenSCAD source so that dimensions, offsets, angles, and relative positions can be changed quickly.

Generate renders showing at minimum:

1. straight-on/front elevation
2. approximately 30° oblique view
3. approximately 60° oblique view
4. side/profile view

The **front elevation is authoritative for composition during this phase**.

Stop after producing the blocking model and renders. Do not independently proceed into detailed design.

I will review the blockout and provide dimensional/compositional changes before we continue.

## Future direction — context only, DO NOT IMPLEMENT YET

Once the XY composition is approved, the solid yellow envelope will be replaced by approximately **8–12 parallel vertical ribs**.

Those ribs will not simply be straight rectangular bars at different depths. Each individual rib will have a smooth, continuously varying Z profile along its vertical axis.

Collectively, the ribs should produce a coherent wave-like sculptural field when viewed obliquely.

The conceptual model is that the **black central mass is a source of force or displacement acting upon an initially orderly field of yellow vertical ribs**. The individual rib undulations should therefore relate to one another rather than being random.

Possible later implementation may use BOSL2 Bézier/path sweeps or another suitable OpenSCAD technique. However, the mathematics must remain subordinate to the approved composition. Avoid generic sine-wave, equalizer, Voronoi, or "parametric art" aesthetics.

The eventual effect should be relatively disciplined from directly in front and reveal substantially more organic three-dimensional movement as the viewer moves off-axis.

Again: **this is future context only. Do not implement it during the initial blocking phase.**

## Workflow principle

Composition comes first.

Use parametric/mathematical techniques later to create behavior *between deliberately composed elements*, not to generate the composition itself.

For now, reproduce the attached composition as a simple, easily adjustable 3D blockout and stop for review.
