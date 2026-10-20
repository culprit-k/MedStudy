# Kidney Anatomy Skills Lab

## Purpose and safety boundary

The Hands-on Skills Lab now shows one standalone kidney instead of the earlier twin-kidney-on-a-tray model. The scene is built in the browser from original, procedurally authored geometry, so it does not depend on a third-party organ CDN and does not silently change to a different asset when a download fails.

This is an educational prototype, not a medical device, diagnostic display, operative planning tool, or validated surgical simulator.

## Current 3D scene

The kidney outer surface uses a smooth parametric mesh shaped to suggest the bean-like outline and medial hilum. The cutaway view uses a shared coordinate system for an illustrative cortex, medullary region, renal pyramids/columns, papillary targets, minor and major calyces, renal pelvis, ureter, and renal artery/vein branches. The user can switch between surface and cutaway views, hide the outer shell, toggle anatomical layers, rotate and zoom on touch screens, tap structures for explanatory text, and run a visual target-selection drill.

The prior remote asset URL pointed to a CC0 teaching model described as twin kidneys on a tray; it has been removed from the runtime. CC0 model licensing alone does not guarantee anatomical detail or make unrelated meshes line up correctly. The replacement therefore uses original geometry instead of pretending that a loosely registered overlay is a faithful dissection.

## Interaction and interpretation

- Surface view displays a single external kidney shape with a medial hilum indentation.
- Cutaway view exposes the colored cortex and medullary teaching layer.
- Renal pyramids point toward the papillae and corresponding minor-calyx markers.
- Major calyces converge toward the renal pelvis, which continues into the ureter.
- Red and blue vessel branches illustrate the renal artery and vein around the hilum.
- Layer buttons independently control the cortex, pyramids/medulla, collecting system, and vessels.
- Camera orbit, zoom, virtual-instrument movement, and target selection are visual interaction tasks only.

## Asset licensing

This version does not fetch or redistribute a third-party anatomical mesh. The procedural geometry in the component is original code; there is no external mesh licence dependency for the current scene. For future high-fidelity work, only add a downloaded mesh after the exact file's licence, redistribution rights, attribution requirements, file format, scale, topology, and anatomical scope have been confirmed. A candidate needs to depict a single kidney with useful internal segmentation—not merely a surface model or a pair of organs. Preserve source and licence records in the repository with any adopted asset.

A publicly listed [CC0 kidney-pair model](https://www.innerscene.com/tools/library/3d-parts/kidneys-pair-c78928dd) is available as an example of a permissively licensed but insufficiently scoped asset: it represents a pair, and the listing does not establish that its interior is a segmentable, validated cutaway. It is not used in this version. Higher-detail listings without a clear reusable licence should not be embedded.

## Limitations

The current anatomy is a deliberately simplified teaching illustration built from parametric shapes and curves. Although the parts share one scene coordinate system and are placed to communicate basic spatial relationships, they are not derived from a validated segmented specimen. The outlines, pyramid number/shape, calyx branching, vessel branching, scale, topology, and exact spatial relationships have not been reviewed by a qualified renal anatomist. The model is not a clinically validated anatomical reference and must not be used for diagnosis, operative planning, procedural instruction, or surgical credentialing.

The virtual instrument does not have validated mesh collision, cutting, tearing, haptics, or tissue-force modelling. The target drill measures successful selection only and is not a measure of surgical competence.

## Regression checks

From the repository root:

```bash
python -m unittest discover -s tests -p 'test_kidney_anatomy_lab.py' -v
npx playwright test --config=playwright.config.cjs
```

Automated tests check the HTML integration, anatomy-layer labels, interaction controls, and explicit limitations. Browser CI cannot verify true anatomical fidelity or guarantee rendering/performance on every iOS or Android device.

## Next high-fidelity milestone

1. Obtain a single-organ kidney asset with explicit licence metadata and separately segmented cortex, medulla, pyramids, calyces, pelvis, vessels, and ureter.
2. Confirm the anatomical landmark alignment with a qualified anatomy reviewer before describing the model as realistic or clinically representative.
3. Register the segmented parts and collision geometry to the exact same mesh coordinate system.
4. Add mesh picking and tissue-interaction physics only as separate, independently tested engineering features.
5. Test on actual iPhone and Android devices, including slow-network and offline-CDN cases.
