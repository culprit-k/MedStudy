# 🩺 MedStudy — Medical Learning Studio

MedStudy is an interactive medical learning project built for medical students who want to move from basic recall toward mechanism-based understanding and clinical reasoning. It uses Streamlit, a JSON question bank, and GitHub Actions; it does not require a database or a trained ML model.

> **Educational use only.** This is not a diagnostic or treatment tool. Clinical vignettes are for learning and must not be used to make real patient-care decisions. Verify information with current textbooks, guidelines, and qualified faculty.

## What is included

- **Learning library:** 90 starter MCQs across anatomy, physiology, biochemistry, pathology, microbiology, and pharmacology, with explanations and adjustable learning depth.
- **Visual lab:** original heart, nephron, neuron, alveolar-interface, and ECG teaching schematics with image-based questions and clinical/exam pearls.
- **Medical Image Library:** searchable image catalogue across 30 medical subjects, live Wikimedia Commons previews, original source pages, creator credits, per-file licence metadata, session-saved references, and curated collection links.
- **Tissue Interaction Lab:** a separate 3D educational prototype with a static external body-surface reference, a generated deformable surface using an adjustable damped mass-spring approximation, visual probe/incision/suture interactions, and automated unit, syntax, and headless-browser smoke checks. The mesh parameters are illustrative, not calibrated human biomechanics; this is not a realistic or clinically validated surgical simulator. See [technical documentation](docs/TISSUE_INTERACTION_LAB.md).
- **Hands-on Skills Lab:** a touch-controlled Three.js learning sandbox with camera-orientation, instrument-targeting, suture-anchor alignment and instrument-recognition stations. Its renal anatomy station now renders one standalone procedural kidney with external-surface and cutaway views, schematic cortex, medulla/pyramids, calyces, pelvis, ureter, and vessel teaching layers, plus touch rotation/zoom, layer toggles, structure descriptions, and a visual target drill. The internal geometry is simplified rather than segmented from a validated specimen, so the model is not a precisely registered anatomical dissection and has not been clinically validated; the target drill is not a surgical competency assessment. The kidney scene no longer depends on a remote organ-mesh CDN. See [kidney anatomy technical notes](docs/KIDNEY_ANATOMY_LAB.md).
- **Surgery Simulator:** four fictional surgical/operative training cases (appendectomy, laparoscopic cholecystectomy, wound-assessment/closure decisions, and hip-fracture theatre safety), with staged decisions, anatomy orientation, explanations, scores, missed-answer review, restart controls, and links to the detailed 3D anatomy atlas. This is a safety-focused educational simulation, not a surgical procedural guide or credentialing tool. It also includes a 10-stage end-to-end operating-room workflow from pre-operative checks through team briefing, anaesthesia handoff, positioning, sterile-field/equipment checks, intraoperative uncertainty, deterioration response, sign-out, recovery handover and postoperative review.
- **Virtual Hospital:** immersive teaching workspace with an animated conceptual organ map, fictional bedside-monitor values, structured patient-assessment scenarios, operating-theatre safety workflow, virtual microbiology test interpretation, and fictional diagnostic laboratory panels.
- **Immersive visual scenes:** animated fictional bedside monitor/organ map, illustrated operating-theatre environment, and microscopy bench with clearly labelled teaching-only visual specimens.
- **Detailed 3D Anatomy Atlas:** embeds the externally hosted Z-Anatomy-derived browser atlas, with thousands of individually selectable structures, touch rotation, pinch zoom, isolate/hide/transparent controls and anatomical detail panels. Requires internet access. The upstream atlas has mixed CC BY-SA and non-commercial model licence terms; the atlas is externally hosted and not copied into this repository.
- **Image reuse safeguards:** every online image links to its source and licence details; users must verify file-specific reuse terms before redistribution or publication.
- **Clinical cases:** structured case vignettes with explanations and stretch prompts.
- **Exam arena:** configurable mixed-question sessions, immediate feedback, score summaries, and missed-question review.
- **OSCE studio:** self-checklists for focused history, respiratory examination, and patient communication.
- **Research & EBM:** PICO builder, study-design guide, diagnostic-test calculator, and critical-appraisal checklist.
- **Personal teacher:** adapts tone and level to the learner's goal; guided tutor prompts work without an API key.
- **Optional AI tutor:** configure an OpenAI API key in Streamlit Community Cloud Secrets as `OPENAI_API_KEY = "your-key"` to enable open-ended AI responses. API usage may incur charges. Never commit keys to GitHub.
- **Active-recall flashcards, bookmarks, and progress charts.**
- **Android test wrapper:** a lightweight APK shell for opening the deployed Streamlit app on Android. Build and install instructions are in [android/README.md](android/README.md); GitHub Actions builds a downloadable debug APK.
- **Automated checks** through GitHub Actions, including question/data integrity, page-navigation wiring, syntax, and an actual Streamlit startup/health smoke test. Tissue Lab also has numerical regression tests and a headless Chromium interaction smoke test.

The question bank is a growing educational starter set, not a comprehensive MBBS, postgraduate, or PhD curriculum. Advanced learning depth changes the style of prompts, but it does not replace validated specialist-level content or research supervision. The current question set is deliberately a foundation for expansion and should be faculty-reviewed before formal exam use.

## Deploy publicly

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
2. Create an app from repository `culprit-k/MedStudy`, branch `main`, main file `app.py`.
3. Deploy and open the generated `.streamlit.app` URL.
4. Optional: to enable AI responses, open app settings → Secrets and add `OPENAI_API_KEY = "your-key"`. Do not put the key in source code or commit it to GitHub.

A public repository is not automatically a live website: the first deployment requires the repository owner to authorize the service and press Deploy. See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Run locally

Requires Python 3.10+.

```bash
git clone https://github.com/culprit-k/MedStudy.git
cd MedStudy
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
streamlit run app.py
```

## Android APK

The Android project is in [android/](android/). The APK is a WebView wrapper; it requires a deployed HTTPS Streamlit URL and internet access, and it is not an offline/native rewrite of the Python app.

Open the [Android APK workflow](https://github.com/culprit-k/MedStudy/actions/workflows/android-apk.yml), select a successful run, and download the `MedStudy-Android-debug-APK` artifact. The artifact contains `app-debug.apk` and is retained for 14 days. Detailed instructions: [android/README.md](android/README.md).

## Add questions

- Core questions: `data/questions.json`
- Image-led questions: `data/visual_questions.json`
- Original schematic illustrations: `assets/*.svg`

Every question should have a unique ID, question, options, answer matching one option, and an explanatory rationale. Visual questions also specify an image path. Cite reliable educational sources when expanding the bank, respect image licences, and never upload identifiable patient information.

## Current limitations

- Progress and bookmarks are stored in the active Streamlit session and may reset.
- The starter question bank is small; it must be expanded and faculty-reviewed before claiming comprehensive exam coverage.
- Visuals are original schematic teaching diagrams, not radiology, histopathology, or diagnostic-grade clinical images.
- Surgery Simulator cases use fictional patients and high-level safety/decision questions; they do not teach hands-on surgical technique and are not a substitute for simulation-lab training or direct supervision.
- The detailed 3D atlas is a third-party project hosted at https://nqwrc.github.io/3d-anatomy/ and documented at https://github.com/nqwrc/3d-anatomy. Its model set includes non-commercial components; review upstream attribution and licence terms before redistribution or commercial use. It is for education, not clinical use.
- AI tutor output can be inaccurate. An API key is optional and usage may incur charges.
- No licence has been added yet; public visibility does not automatically grant reuse rights.
- The Android wrapper does not include or host the Streamlit backend and cannot work until a public HTTPS app URL is configured.

## Virtual Hospital data

Fictional training scenarios, organ-system notes, microbiology interpretation stations, OR safety checklists, and diagnostic panels live in `data/hospital_training.json`. All values are educational examples, not clinical decision support.
