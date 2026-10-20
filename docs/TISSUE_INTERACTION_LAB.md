# Tissue Interaction Lab — Technical Status

## Purpose

This page is an educational software prototype inside the existing MedStudy Streamlit app. It is not a medical device, a validated surgical simulator, or a replacement for supervised skills training.

## Current implementation

### Browser 3D layer

- Three.js 0.128.0 renders the surface, layered teaching slabs, practice instrument, incision traces, and visual closure stitches.
- The surface is a 54 × 38 subdivided plane (55 × 39 vertices).
- Probe contact applies a local radial displacement to the surface grid.
- Physics is implemented in the shared, dependency-free `components/tissue_physics_engine.js` module and connected to the Three.js mesh.
- Each grid node has displacement and velocity state. A damped restoring spring pulls nodes toward rest; neighbor coupling spreads deformation across adjacent nodes.
- The solver substeps frame deltas at approximately 1/120 s, enforces a fixed boundary rim, clamps displacement to 0.18 arbitrary units, and checks for non-finite state. Vertex normals update when the surface changes.
- Deterministic Node tests cover contact response, locality, boundary conditions, bounded displacement, large frame deltas, damping/recovery, invalid input, reset, and repeatability.
- Stiffness, damping, and neighbor coupling can be adjusted using the UI sliders.
- The maximum displacement readout is in **arbitrary scene units**, not millimetres or a measured material property.
- The reset control removes visual practice markings and returns the membrane to its rest configuration.

This is a small **mass-spring membrane approximation**, not finite-element analysis. The parameter values are visual defaults, not literature-derived measurements for human skin, fat, fascia, or muscle.

### Anatomy reference

- The existing anatomy-atlas iframe remains available for inspecting named anatomical structures.
- A separate optional external body mesh is loaded on demand from [UMRAM-Bilkent/supine-human-model](https://github.com/UMRAM-Bilkent/supine-human-model), whose repository states that its model is released under CC0 1.0: [source README](https://github.com/UMRAM-Bilkent/supine-human-model/blob/main/README.md).
- The mesh is a single static body-surface object. It does not include selectable organs, bones, vessel layers, or surgical collision geometry. The app does not copy the binary mesh into this repository.
- The BodyParts3D/Z-Anatomy-based viewer has separate upstream terms, including ShareAlike and other restrictions. Its assets are embedded by reference and should not be copied or redistributed without checking the relevant notices.

### Collision and anatomy proxy layer

- The new dependency-free `components/anatomy_collision_engine.js` provides point-to-plane contact, point-to-sphere proxy contact, penetration depth, and a contact normal.
- The scene displays two translucent labelled proxy volumes and reports whether a probe point overlaps a proxy.
- Collision helpers are covered by Node regression tests for surface contact, non-contact, finite contact normals, deepest-proxy selection, and invalid inputs.
- These are deliberately simple geometric proxies. Their labels are placeholders for interaction testing, not claims that the rendered objects match real vessels or organs. They are not a full instrument-vs-triangle collision system and do not provide force feedback.
- During pointer movement, the UI now checks the straight segment between consecutive pointer samples with `deepestSweptProxyContact`, so a fast drag can register a proxy crossing even when both sampled endpoints are outside the proxy.
- Swept checks approximate a point moving along a segment; they do not model the full instrument shaft, continuous rigid-body motion, triangle-mesh collisions, penetration dynamics, or force feedback. Contact labels remain schematic and must not be interpreted as anatomical injury prediction.

### Current interactions

- Camera orbit and zoom.
- Selectable Explore, Probe, Incision, and Suture practice modes.
- Raycast contact on the synthetic training surface.
- Local surface depression and damped recovery.
- Visual incision traces and point-to-point visual stitches.
- Surface-layer toggling, optional body-reference view, counter readouts, and reset.

The incision marks do **not** split the mesh. Stitches do **not** measure tissue purchase, tension, or knot security. The static body mesh is a reference view and is not connected to the spring membrane.

## Development checks

Run from the repository root:

```bash
node --test tests/anatomy_collision_engine.test.js
node --test tests/tissue_physics_engine.test.js
python -m unittest discover -s tests -p 'test_tissue_interaction_lab.py' -v
python -m py_compile pages/3_Tissue_Interaction_Lab.py
```

The GitHub Actions workflow `.github/workflows/tissue-lab-ci.yml` runs collision and physics regression suites, simulator smoke tests, Python compilation, and inline JavaScript syntax validation.

The Node tests check geometric collision and numerical invariants for these simplified models; they do not prove biomechanical accuracy. Source smoke tests and syntax checks do not validate visual output, anatomical correctness, or clinical training value. The simulator still needs live-browser testing.

## Recommended engineering sequence

1. Select a single region and source a legally compatible mesh set with separate labelled structures, explicit units, landmarks, collision proxies, and attribution.
2. Add a documented transform from anatomical meshes to the existing scene; test scale and landmark alignment.
3. Prototype collision handling between the instrument tip and a deformable surface.
4. Evaluate a volumetric physics engine such as [SOFA](https://github.com/sofa-framework/sofa) for volumetric deformation. SOFA is a research-grade C++ framework and is **not currently integrated**; embedding it would need a separately built native/service layer and a tested interface.
5. Treat cutting, tearing, bleeding, suturing mechanics, and haptics as separate systems, each requiring tests and material parameters.
6. Validate with qualified anatomy and surgical-simulation reviewers before describing the result as realistic or clinically useful.

## Safety boundary

This prototype is for software exploration and general medical education. It is not intended for procedural instruction, patient treatment, or surgical credentialing. Do not infer safe operative technique from its score counters or visual feedback.
