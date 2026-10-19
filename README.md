# 🩺 MedStudy — MBBS Learning Platform

MedStudy is a beginner-friendly medical education web app for MBBS students. It includes subject-wise practice questions, MCQ quizzes, flashcards, bookmarks, and a simple progress dashboard.

> **Educational use only:** MedStudy is not a diagnostic tool and must not be used to make patient-care decisions. Verify medical information with trusted textbooks, current guidelines, and qualified instructors.

## Features

- Six starter subjects: Anatomy, Physiology, Biochemistry, Pathology, Microbiology, and Pharmacology
- 36 multiple-choice questions with explanations
- Quiz sessions with immediate feedback and selectable quiz length
- Flashcard-style revision
- Question bookmarks
- Session-based progress summaries
- Responsive Streamlit interface
- Automated syntax and app/data tests in GitHub Actions

## Public web deployment

**Deploy MedStudy for free with Streamlit Community Cloud:**

1. Open the [Streamlit Community Cloud workspace](https://share.streamlit.io/).
2. Sign in with GitHub and authorize Streamlit to access `culprit-k/MedStudy` if asked.
3. Select **Create app**. If prompted, choose **Yup, I have an app**.
4. Enter:
   - **Repository:** `culprit-k/MedStudy`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** `medstudy-mbbs` (if available)
5. In advanced settings, use Python **3.12** (the Community Cloud default).
6. Click **Deploy** and wait for the build to finish.
7. Once it starts, open the generated `.streamlit.app` URL and test the dashboard, quizzes, flashcards, and bookmarks.

The repository is public, so the deployed app will normally be public too. If the suggested app URL is already taken, let Streamlit assign one. See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) for screenshots and troubleshooting.

> **Important:** The repository and automated checks are ready, but a live hosted URL is not created just by pushing code to GitHub. The initial deployment requires signing in to Streamlit and clicking **Deploy**. I cannot approve account permissions or click the final deployment button on your behalf from this GitHub connection.

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

Keep questions accurate, cite reliable sources when expanding the question bank, and never upload patient-identifiable information.

## Current limitations

- Progress and bookmarks are stored in the current Streamlit session and may reset when the session ends.
- The starter question bank is small and intended for demonstration and revision.
- The app does not provide diagnosis, treatment recommendations, or patient-specific medical advice.

## License

No license has been added yet. Until a license is chosen, the repository is visible publicly but reuse is not automatically granted.
