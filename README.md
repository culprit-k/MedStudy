# 🩺 MedStudy — Medical Learning Studio

MedStudy is an interactive medical learning project built for medical students who want to move from basic recall toward mechanism-based understanding and clinical reasoning. It uses Streamlit, a JSON question bank, and GitHub Actions; it does not require a database or a trained ML model.

> **Educational use only.** This is not a diagnostic or treatment tool. Clinical vignettes are for learning and must not be used to make real patient-care decisions. Verify information with current textbooks, guidelines, and qualified faculty.

## What is included

- **Learning library:** 120 starter MCQs (20 each in anatomy, physiology, biochemistry, pathology, microbiology, and pharmacology), with explanations and adjustable learning depth.
- **Visual lab:** original heart, nephron, neuron, alveolar-interface, and ECG teaching schematics with image-based questions and clinical/exam pearls.
- **Medical Image Library:** searchable image catalogue across 30 medical subjects, live Wikimedia Commons previews, original source pages, creator credits, per-file licence metadata, session-saved references, and curated collection links.
- **Image Quiz:** a focused quiz workflow that searches real medical images from Wikimedia Commons, shows available creator/licence/source metadata, and generates image-grounded MCQs through the optional vision-capable AI service. Without an API key it falls back to the curated question bank and labels that fallback clearly.





- **Image reuse safeguards:** every online image links to its source and licence details; users must verify file-specific reuse terms before redistribution or publication.
- **Clinical cases:** structured case vignettes with explanations and stretch prompts.
- **Exam arena:** configurable mixed-question sessions, immediate feedback, score summaries, and missed-question review.
- **OSCE studio:** self-checklists for focused history, respiratory examination, and patient communication.
- **Research & EBM:** PICO builder, study-design guide, diagnostic-test calculator, and critical-appraisal checklist.
- **Personal teacher:** adapts to learner stage, syllabus/exam, preferred language, weak subjects, pace, goal, teaching style, personal context and recent incorrect answers. Guided prompts work without an API key; full generative tutoring and vision-based image questions require `OPENAI_API_KEY` in Streamlit Community Cloud Secrets.
- **Optional AI tutor:** configure an OpenAI API key in Streamlit Community Cloud Secrets as `OPENAI_API_KEY = "your-key"` to enable open-ended AI responses. API usage may incur charges. Never commit keys to GitHub.
- **Active-recall flashcards, bookmarks, and progress charts.**
- **Android test wrapper:** a lightweight APK shell for opening the deployed Streamlit app on Android. Build and install instructions are in [android/README.md](android/README.md); GitHub Actions builds a downloadable debug APK.
- **Automated checks** through GitHub Actions, including question/data integrity, navigation wiring, Python syntax, application startup/health, and browser smoke checks for archived prototype code.

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

- The active learning experience is focused on questions, sourced medical images, revision, clinical cases, and the personal teacher. Heavy 3D and simulator prototypes are not part of the main navigation.
- Progress, bookmarks, and the learner profile are currently session-based and may reset when the session ends.
- The question bank contains 120 starter MCQs. It should be expanded and faculty-reviewed before being treated as comprehensive exam coverage.
- Some local teaching illustrations are schematic diagrams, not diagnostic-grade radiology or histopathology images. Online images display source and licence metadata when available; confirm the individual file's terms before reuse.
- AI-generated answers and image questions can be inaccurate. Full generative tutoring requires an `OPENAI_API_KEY`; API usage may incur charges.
- The Android wrapper is a WebView shell and does not host the Streamlit backend. It requires a real deployed HTTPS app URL and internet access.
- No production release or clinical validation is claimed. MedStudy is an educational project, not a diagnostic or treatment tool.
