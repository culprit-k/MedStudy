# Kidney Anatomy Skills Lab

## Purpose and safety boundary

The Hands-on Skills Lab loads a standalone kidney teaching component rather than a flat board with floating target dots. It remains an educational prototype, not a medical device, validated anatomy atlas, or surgical simulator.

## Model implementation

The scene uses original procedural Three.js geometry. It includes a bean-like outer renal silhouette with a medial indentation and a toggleable schematic cutaway showing a cortex rim, simplified renal pyramids, calyces, renal pelvis, ureter, and red/blue vessel paths. Camera orbit/zoom, instrument movement, surface/cutaway visibility, target acquisition, and a two-point alignment drill are wired into the UI.

The component deliberately does **not** download an unverified third-party organ mesh at runtime. This avoids an unverified external dependency and prevents the interface from claiming a source model or licence that has not been validated.

## Anatomical limitations

This is **not a sourced, segmented, clinically validated 3D kidney mesh**. The shape, proportions, vessel paths, branching, internal relationships, and collecting system are schematic and have not been reviewed against an anatomical reference by a qualified reviewer. The cutaway is not a true volumetric section of the surface and its structures are not registered to internal anatomical meshes. It should not be described as anatomically accurate, used for diagnosis or operative planning, or substituted for an approved anatomy atlas.

The alignment drill measures target order and visual coordination only. It does not represent needle driving, tissue puncture, knot tying, calibrated forces, haptics, or suturing competence. The instrument does not provide validated tissue collision or damage prediction.

## Regression checks

From the repository root:

```bash
python -m unittest discover -s tests -p 'test_kidney_anatomy_lab.py' -v
```

These tests check UI wiring and disclosure text; they do not establish anatomical accuracy or clinical suitability.

## Work needed for a genuinely realistic atlas

1. Select a segmented kidney mesh with a licence that explicitly permits the intended use and distribution; preserve source and attribution details.
2. Prefer separate structures for cortex, medulla/pyramids, calyces, pelvis, ureter, arteries, and veins, with documented units and reference landmarks.
3. Have qualified anatomy reviewers verify geometry, labels, branching, and spatial relationships.
4. Register all internal structures and collision geometry to the chosen surface mesh, with automated landmark/scale checks.
5. Implement mesh collision and tissue interaction as separate engineering tasks and validate them independently.
