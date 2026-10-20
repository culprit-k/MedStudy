# Kidney Anatomy Skills Lab

## Purpose and safety boundary

The Hands-on Skills Lab now loads a separate kidney scene rather than a flat practice board with floating target dots. It remains an educational prototype, not a medical device, diagnostic display, or validated surgical simulator.

## 3D surface model

The component loads the **Kidney Model (Human Anatomy and Education Kit)** from [3DAssets.dev](https://3dassets.dev/assets/human-anatomy-and-education-kit-kidney-model-c48807f6). The asset listing identifies the downloadable GLB as **CC0 1.0 Universal** and describes twin bean-shaped kidneys with a hilum, ureter cords, and red/blue vessel stubs. The runtime model URL is:

`https://cdn.3dassets.dev/assets/38958/v1/model.glb`

The component loads the asset using Three.js GLTFLoader and normalizes its orientation and display scale. The model is fetched from the upstream CDN, not copied into the repository. Internet access, browser CORS, and upstream availability therefore affect loading. A procedural kidney-shaped fallback remains available if the asset or loader fails.

## Interactions

- Camera orbit/zoom and virtual instrument movement are separate modes.
- Surface visibility can be toggled.
- A schematic internal overlay shows a cortex rim, simplified renal pyramids, calyces, renal pelvis, ureter, and red/blue vessel paths.
- A two-point alignment drill checks selection order only; it does not model actual suturing.

## Important limitations

The external surface is a real 3D teaching asset, but it is a low-polygon educational model and is not a clinically validated anatomical reference. The asset represents **twin kidneys on a tray**, not a single isolated organ. The internal overlay is separate, schematic geometry and is **not registered to the mesh**. Its exact shape, scale, branching, and spatial relationships have not been anatomically validated. The scene is not suitable for diagnosis, operative planning, procedural instruction, or surgical credentialing.

The instrument has no validated mesh collision, cutting, tearing, haptics, or tissue-force model. Do not interpret target scores as surgical competence.

## Regression checks

From the repository root:

```bash
python -m unittest discover -s tests -p 'test_kidney_anatomy_lab.py' -v
npx playwright test --config=playwright.config.cjs
```

The browser test uses a deterministic mocked GLTFLoader result so that UI behavior can be checked without relying on the public asset CDN. These tests do not establish anatomical accuracy or clinical suitability.

## Remaining work for a genuinely realistic atlas

1. Replace the twin-kidney-on-tray asset with a single isolated kidney model if the station requires one organ.
2. Source segmented internal anatomy with compatible licence, units, and documented landmarks.
3. Have qualified anatomy reviewers verify the geometry, labels, and spatial relationships.
4. Register internal structures and collision geometry to the selected surface mesh.
5. Add mesh collision and tissue interaction as separate engineering tasks with independent validation.
6. Test on real iOS and Android devices; browser CI cannot guarantee device-specific performance.
