# Kidney Anatomy Lab — Technical Notes

## Purpose and safety boundary

The Hands-on Skills Lab now loads a standalone kidney model component rather than rendering only a flat practice board with floating target dots. It is still an educational prototype, not a surgical simulator, medical device, or validated anatomy teaching product.

## Model source

The preferred external surface model is the CC0 kidney model at [3DAssets.dev — Human Anatomy and Education Kit: Kidney Model](https://3dassets.dev/assets/human-anatomy-and-education-kit-kidney-model-c48807f6). Its source listing identifies the downloadable GLB as CC0 1.0. Runtime URL:

`https://cdn.3dassets.dev/assets/38958/v1/model.glb`

The component loads the model with Three.js GLTFLoader, rotates it upright, normalizes its height, and modestly compresses display depth for a clearer front view. The model is loaded from the source CDN rather than copied into this repository. This depends on the source URL, network access, browser CORS permissions, and the upstream host remaining available. If it fails, a procedural kidney-shaped fallback keeps the lab usable and a status message indicates the fallback state.

## Anatomy view and interactions

- The outer kidney model has orbit/zoom camera control and a separate virtual instrument control.
- The anatomy toggle reveals a schematic internal overlay for the renal cortex, renal pyramids, collecting system, renal pelvis, renal artery, renal vein, and ureter.
- The surface toggle hides/shows the organ surface; reset restores the view and interaction defaults.
- The anchor-alignment drill guides users to select two visual targets in sequence. It measures selection order only.
- Targets, tool motion, and internal-overlay landmarks are not tied to mesh triangles or a validated coordinate registration.

**Important limitation:** the external kidney mesh is a real 3D anatomical asset, but the current internal structures are a separate original schematic overlay and are not registered to the model's actual internal anatomy. It must not be presented as an anatomically accurate dissection, cutting simulator, injury predictor, or practice substitute.

## Local checks

From the repository root:

```bash
python -m unittest discover -s tests -p 'test_kidney_anatomy_lab.py' -v
npm init -y
npm install --no-save @playwright/test@1.55.0 three@0.128.0
npx playwright install chromium
npx playwright test --config=playwright.config.cjs
```

The CI browser suite uses a deterministic mock GLB to test the loader and controls without relying on the external asset host. It also verifies fallback handling in source-level checks. It does not certify the external model's anatomical accuracy or performance on every physical phone.

## Next validation required

1. Review the rendered model on an actual iPhone and an Android device.
2. Have anatomy faculty verify the surface shape and landmark labels.
3. Register any internal mesh structures to the chosen external organ surface before claiming the cutaway is anatomically aligned.
4. Keep licence/source notices with any model redistribution. CC0 asset availability does not validate the model medically.
