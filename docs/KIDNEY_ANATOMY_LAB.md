# Kidney Anatomy Skills Lab

## Purpose and safety boundary

The Hands-on Skills Lab now uses a real externally hosted 3D kidney surface model in place of the generic flat target board. It is still an educational prototype, not a medical device, clinically validated anatomy atlas, or surgical simulator.

## Model source and loading

The component loads the [3DAssets.dev Human Anatomy and Education Kit kidney model](https://3dassets.dev/assets/human-anatomy-and-education-kit-kidney-model-c48807f6). The source listing describes this GLB asset as **CC0 1.0**. Runtime URL:

`https://cdn.3dassets.dev/assets/38958/v1/model.glb`

The model is loaded via Three.js GLTFLoader, rotated upright, scaled to the scene, and mildly depth-compressed for a front-facing view. It is fetched at runtime rather than copied into this repository. That requires internet access, the source host to remain available, and successful browser CORS requests. If loading fails, the component displays a status message and keeps its procedural kidney-shaped fallback visible.

## Anatomy view and interactions

- Camera mode supports orbit/zoom; instrument mode supports moving a simplified virtual instrument.
- The anatomy toggle reveals a separate schematic teaching overlay for renal cortex, pyramids, calyces, renal pelvis, renal artery, renal vein, and ureter.
- The surface toggle hides/shows the external model; reset restores default view and interaction state.
- The alignment drill asks the learner to select two visual anchors in order. It measures selection order only.
- The internal overlay is **not registered to the GLB mesh**. Its positions are illustrative and do not claim to reproduce the model's actual internal structures.

## Important limitations

The external organ surface is a real 3D asset, but this is not a segmented, clinically validated kidney model. The schematic internal structures and target markers are not meshed or anatomically aligned with the external GLB. The model has not been reviewed by anatomy faculty. It should not be used for diagnosis, operative planning, or as a substitute for an approved anatomy atlas or supervised training.

The instrument does not model realistic cutting, tissue tearing, bleeding, instrument-shaft collision, haptics, or tissue force. The target drill is a basic visual-coordination task, not a suturing skill assessment.

## Regression checks

From the repository root, install the dependencies and run:

```bash
python -m unittest discover -s tests -p 'test_kidney_anatomy_lab.py' -v
npm init -y
npm install --no-save @playwright/test@1.55.0 three@0.128.0
npx playwright install chromium
npx playwright test --config=playwright.config.cjs
```

The browser suite uses a small deterministic mock GLB to test that the loader and controls work without depending on the external model CDN. This verifies integration behavior, not the real asset's anatomical accuracy or performance on every device.

## Next validation required

1. Check the actual GLB rendering on a physical iPhone and Android device.
2. Have qualified anatomy faculty inspect the external model and all labels.
3. Replace schematic internals with individually sourced/segmented structures and register them to the same coordinate system before claiming a true cutaway.
4. Retain the source and licence record if the GLB is redistributed. CC0 licensing does not establish medical accuracy.
