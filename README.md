# 🩺 MedStudy — MBBS Learning Platform

MedStudy is a beginner-friendly, open-source medical education web app for MBBS students. It includes subject-wise practice questions, MCQ quizzes, flashcards, bookmarks, and a simple progress dashboard.

> **Educational use only:** MedStudy is not a diagnostic tool and must not be used to make patient-care decisions. Verify medical information with trusted textbooks, current guidelines, and qualified instructors.

## Features

- Six starter subjects: Anatomy, Physiology, Biochemistry, Pathology, Microbiology, and Pharmacology
- Multiple-choice practice questions with explanations
- Quiz sessions with immediate feedback
- Flashcard-style revision
- Question bookmarks
- Session-based progress summaries
- Responsive Streamlit interface

## Run locally

Requires Python 3.10 or newer.

```bash
git clone https://github.com/culprit-k/MedStudy.git
cd MedStudy
python -m venv .venv
```

Activate the environment:

- **Windows:** `.venv\\Scripts\\activate`
- **macOS/Linux:** `source .venv/bin/activate`

Install dependencies and launch:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

1. Push the repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Create an app from this repository.
4. Set the main file path to `app.py`.

## Add questions

Edit `data/questions.json`. Each question needs a unique `id`, a `question`, an `options` list, an `answer` that exactly matches one option, and an `explanation`.

Example:

```json
{
  "id": "anat-004",
  "question": "Example question?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Option B",
  "explanation": "A short explanation of the correct answer."
}
```

Keep questions accurate, cite reliable sources when expanding the question bank, and avoid uploading patient-identifiable information.

## Current limitations

- Progress and bookmarks are stored in the current Streamlit session and may reset when the session ends.
- The starter question bank is small and intended for demonstration and revision.
- The app does not provide diagnosis, treatment recommendations, or patient-specific medical advice.

## License

No license has been added yet. Until a license is chosen, the repository is visible publicly but reuse is not automatically granted.
