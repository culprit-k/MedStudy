# 🩺 MedStudy — Medical Learning Studio

MedStudy is an interactive medical learning project built for medical students who want to move from basic recall toward mechanism-based understanding and clinical reasoning. It uses Streamlit, a JSON question bank, and GitHub Actions; it does not require a database or a trained ML model.

> **Educational use only.** This is not a diagnostic or treatment tool. Clinical vignettes are for learning and must not be used to make real patient-care decisions. Verify information with current textbooks, guidelines, and qualified faculty.

## What is included

- **Learning library:** 90 starter MCQs across anatomy, physiology, biochemistry, pathology, microbiology, and pharmacology, with explanations and adjustable learning depth.
- **Visual lab:** original heart, nephron, neuron, alveolar-interface, and ECG teaching schematics with image-based questions and clinical/exam pearls.
- **Medical Image Library:** searchable image catalogue across 30 medical subjects, live Wikimedia Commons previews, original source pages, creator credits, per-file licence metadata, session-saved references, and curated collection links.
- **Virtual Hospital:** immersive teaching workspace with an animated conceptual organ map, fictional bedside-monitor values, structured patient-assessment scenarios, operating-theatre safety workflow, virtual microbiology test interpretation, and fictional diagnostic laboratory panels.
- **Immersive visual scenes:** animated fictional bedside monitor/organ map, illustrated operating-theatre environment, and microscopy bench with clearly labelled teaching-only visual specimens.
- **Image reuse safeguards:** every online image links to its source and licence details; users must verify file-specific reuse terms before redistribution or publication.
- **Clinical cases:** structured case vignettes with explanations and stretch prompts.
- **Exam arena:** configurable mixed-question sessions, immediate feedback, score summaries, and missed-question review.
- **OSCE studio:** self-checklists for focused history, respiratory examination, and patient communication.
- **Research & EBM:** PICO builder, study-design guide, diagnostic-test calculator, and critical-appraisal checklist.
- **Personal teacher:** adapts tone and level to the learner's goal; guided tutor prompts work without an API key.
- **Optional AI tutor:** configure an OpenAI API key in Streamlit Community Cloud Secrets as `OPENAI_API_KEY = "your-key"` to enable open-ended AI responses. API usage may incur charges. Never commit keys to GitHub.
- **Active-recall flashcards, bookmarks, and progress charts.**
- **Automated checks** through GitHub Actions.

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

## Add questions

- Core questions: `data/questions.json`
- Image-led questions: `data/visual_questions.json`
- Original schematic illustrations: `assets/*.svg`

Every question should have a unique ID, question, options, answer matching one option, and an explanatory rationale. Visual questions also specify an image path. Cite reliable educational sources when expanding the bank, respect image licences, and never upload identifiable patient information.

## Current limitations

- Progress and bookmarks are stored in the active Streamlit session and may reset.
- The starter question bank is small; it must be expanded and faculty-reviewed before claiming comprehensive exam coverage.
- Visuals are original schematic teaching diagrams, not radiology, histopathology, or diagnostic-grade clinical images.
- AI tutor output can be inaccurate. An API key is optional and usage may incur charges.
- No licence has been added yet; public visibility does not automatically grant reuse rights.


## Virtual Hospital data

Fictional training scenarios, organ-system notes, microbiology interpretation stations, OR safety checklists, and diagnostic panels live in `data/hospital_training.json`. All values are educational examples, not clinical decision support.
