import json
import random
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="MedStudy | MBBS Learning",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "data" / "questions.json"


@st.cache_data
def load_questions():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


QUESTIONS = load_questions()
SUBJECTS = list(QUESTIONS.keys())

if "answered" not in st.session_state:
    st.session_state.answered = []
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "quiz_question_ids" not in st.session_state:
    st.session_state.quiz_question_ids = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_feedback" not in st.session_state:
    st.session_state.quiz_feedback = {}
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0

st.markdown("""
<style>
    .stApp { background: #f5f8fc; }
    [data-testid="stSidebar"] { background: #10243a; }
    [data-testid="stSidebar"] * { color: #f4f8fc !important; }
    .hero {
        padding: 2rem 2.2rem; border-radius: 22px;
        background: linear-gradient(120deg, #10243a 0%, #176b70 100%);
        color: white; margin-bottom: 1.2rem;
    }
    .hero h1 { color: white; font-size: 2.35rem; margin-bottom: .4rem; }
    .hero p { color: #e0f2f1; font-size: 1.05rem; margin-bottom: 0; }
    .small-note { color: #526579; font-size: .9rem; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e1e9f1;
        padding: 1rem; border-radius: 14px;
    }
    .topic-card {
        background: white; padding: 1.1rem; border-radius: 15px;
        border: 1px solid #e1e9f1; min-height: 115px;
    }
</style>
""", unsafe_allow_html=True)

def jump_to_subject(subject):
    st.session_state.selected_subject = subject
    st.session_state.navigation = "Study by Subject"


if "navigation" not in st.session_state:
    st.session_state.navigation = "Dashboard"

with st.sidebar:
    st.markdown("# 🩺 MedStudy")
    st.caption("Your MBBS revision companion")
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Study by Subject", "MCQ Quiz", "Flashcards", "Bookmarks", "Progress"],
        label_visibility="visible",
        key="navigation",
    )
    st.divider()
    st.caption("Built for learning. Not for clinical decision-making.")

total_questions = sum(len(items) for items in QUESTIONS.values())
correct_count = sum(1 for item in st.session_state.answered if item["correct"])
attempt_count = len(st.session_state.answered)
accuracy = round(100 * correct_count / attempt_count) if attempt_count else 0


def all_cards():
    cards = []
    for subject, items in QUESTIONS.items():
        for item in items:
            cards.append({"subject": subject, **item})
    return cards


CARDS = all_cards()


def question_by_id(question_id):
    for item in CARDS:
        if item["id"] == question_id:
            return item
    return None


if page == "Dashboard":
    st.markdown("""
    <div class="hero">
      <h1>Learn medicine, one concept at a time.</h1>
      <p>Practice core MBBS subjects with short quizzes, quick-revision flashcards, and simple progress tracking.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b, c, d = st.columns(4)
    a.metric("Subjects", len(SUBJECTS))
    b.metric("Practice questions", total_questions)
    c.metric("Questions attempted", attempt_count)
    d.metric("Quiz accuracy", f"{accuracy}%")

    st.subheader("Explore your subjects")
    descriptions = {
        "Anatomy": "Structure and relationships of the human body",
        "Physiology": "How the body and its systems function",
        "Biochemistry": "Molecules and chemical processes of life",
        "Pathology": "Mechanisms and effects of disease",
        "Microbiology": "Microorganisms and infectious disease",
        "Pharmacology": "Medicines, mechanisms, and effects",
    }
    cols = st.columns(3)
    for index, subject in enumerate(SUBJECTS):
        with cols[index % 3]:
            st.markdown(
                f'<div class="topic-card"><h3>{subject}</h3>'
                f'<p>{descriptions.get(subject, "Review key concepts and test your knowledge.")}</p>'
                f'<b>{len(QUESTIONS[subject])} practice questions</b></div>',
                unsafe_allow_html=True,
            )
            st.button(
                f"Study {subject}", key=f"dash_{subject}", use_container_width=True,
                on_click=jump_to_subject, args=(subject,),
            )

    st.info("Tip: Read the explanation after every question, including the ones you answer correctly.")

elif page == "Study by Subject":
    st.title("📚 Study by Subject")
    default_subject = st.session_state.get("selected_subject", SUBJECTS[0])
    subject = st.selectbox("Choose a subject", SUBJECTS, index=SUBJECTS.index(default_subject) if default_subject in SUBJECTS else 0)
    st.write(f"**{len(QUESTIONS[subject])} practice questions** in {subject}")
    for number, item in enumerate(QUESTIONS[subject], start=1):
        with st.expander(f"{number}. {item['question']}"):
            for option in item["options"]:
                st.write(f"• {option}")
            st.markdown(f"**Correct answer:** {item['answer']}")
            st.write(item["explanation"])
            if st.button("Bookmark question", key=f"bookmark_subject_{item['id']}"):
                if item["id"] not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(item["id"])
                st.success("Saved to Bookmarks.")

elif page == "MCQ Quiz":
    st.title("📝 MCQ Quiz")
    st.write("Choose a subject and start a short practice session.")
    selected_subject = st.selectbox("Quiz subject", ["All subjects"] + SUBJECTS)
    quiz_length = st.selectbox("Number of questions", ["5 questions", "10 questions", "All questions"])
    if st.button("Start / restart quiz", type="primary"):
        pool = CARDS if selected_subject == "All subjects" else [
            item for item in CARDS if item["subject"] == selected_subject
        ]
        requested_count = {
            "5 questions": 5,
            "10 questions": 10,
            "All questions": len(pool),
        }[quiz_length]
        question_count = min(requested_count, len(pool))
        st.session_state.quiz_question_ids = [
            q["id"] for q in random.sample(pool, k=question_count)
        ]
        st.session_state.quiz_index = 0
        st.session_state.quiz_feedback = {}
        st.rerun()

    ids = st.session_state.quiz_question_ids
    if not ids:
        st.info("Select a subject and press **Start / restart quiz** to begin.")
    elif st.session_state.quiz_index >= len(ids):
        st.success("Quiz complete!")
        session_answers = [
            value for value in st.session_state.quiz_feedback.values()
        ]
        score = sum(1 for value in session_answers if value["correct"])
        st.metric("Session score", f"{score} / {len(session_answers)}")
        st.write("Start another quiz whenever you're ready.")
    else:
        qid = ids[st.session_state.quiz_index]
        item = question_by_id(qid)
        st.progress(st.session_state.quiz_index / len(ids))
        st.caption(f"Question {st.session_state.quiz_index + 1} of {len(ids)} · {item['subject']}")
        st.subheader(item["question"])
        existing = st.session_state.quiz_feedback.get(qid)
        if existing:
            st.info(f"Your answer: {existing['chosen']}")
            if existing["correct"]:
                st.success("Correct!")
            else:
                st.error(f"Correct answer: {item['answer']}")
            st.write(item["explanation"])
            if st.button("Next question", type="primary"):
                st.session_state.quiz_index += 1
                st.rerun()
        else:
            choice = st.radio("Choose one answer", item["options"], key=f"choice_{qid}")
            left, right = st.columns([1, 2])
            with left:
                if st.button("Check answer", type="primary"):
                    is_correct = choice == item["answer"]
                    st.session_state.quiz_feedback[qid] = {
                        "chosen": choice, "correct": is_correct
                    }
                    st.session_state.answered.append({
                        "id": qid, "subject": item["subject"], "correct": is_correct
                    })
                    st.rerun()
            with right:
                if st.button("Bookmark this question", key=f"bookmark_quiz_{qid}"):
                    if qid not in st.session_state.bookmarks:
                        st.session_state.bookmarks.append(qid)
                    st.toast("Added to bookmarks")

elif page == "Flashcards":
    st.title("🧠 Flashcards")
    subject = st.selectbox("Filter by subject", ["All subjects"] + SUBJECTS, key="flash_subject")
    cards = CARDS if subject == "All subjects" else [q for q in CARDS if q["subject"] == subject]
    if cards:
        index = st.session_state.flashcard_index % len(cards)
        item = cards[index]
        st.caption(f"{index + 1} of {len(cards)} · {item['subject']}")
        st.markdown(f"### {item['question']}")
        with st.container(border=True):
            st.markdown("**Answer**")
            st.write(item["answer"])
            st.markdown("**Explanation**")
            st.write(item["explanation"])
        previous, next_col = st.columns(2)
        with previous:
            if st.button("← Previous", use_container_width=True):
                st.session_state.flashcard_index = (index - 1) % len(cards)
                st.rerun()
        with next_col:
            if st.button("Next →", use_container_width=True, type="primary"):
                st.session_state.flashcard_index = (index + 1) % len(cards)
                st.rerun()
    else:
        st.info("No flashcards available for this selection yet.")

elif page == "Bookmarks":
    st.title("⭐ Bookmarks")
    saved = [question_by_id(qid) for qid in st.session_state.bookmarks]
    saved = [item for item in saved if item]
    if not saved:
        st.info("You haven't saved any questions yet. Bookmark a question while studying or taking a quiz.")
    else:
        st.write(f"You have saved **{len(saved)}** question(s).")
        for item in saved:
            with st.expander(f"{item['subject']}: {item['question']}"):
                st.write(f"**Answer:** {item['answer']}")
                st.write(item["explanation"])
                if st.button("Remove bookmark", key=f"remove_{item['id']}"):
                    st.session_state.bookmarks.remove(item["id"])
                    st.rerun()

elif page == "Progress":
    st.title("📊 Your Progress")
    a, b, c = st.columns(3)
    a.metric("Attempted", attempt_count)
    b.metric("Correct", correct_count)
    c.metric("Accuracy", f"{accuracy}%")
    if st.session_state.answered:
        by_subject = {}
        for item in st.session_state.answered:
            stats = by_subject.setdefault(item["subject"], {"correct": 0, "attempted": 0})
            stats["attempted"] += 1
            stats["correct"] += int(item["correct"])
        st.subheader("Attempts by subject")
        st.bar_chart({subject: stats["attempted"] for subject, stats in by_subject.items()})
        st.subheader("Correct answers by subject")
        st.bar_chart({subject: stats["correct"] for subject, stats in by_subject.items()})
    else:
        st.info("Complete a few quiz questions to see your progress here.")

    st.divider()
    st.caption("Progress is stored in this browser session and may reset when the session ends.")
    confirm_reset = st.checkbox("I want to clear this session's quiz progress")
    if st.button("Clear session progress", disabled=not confirm_reset):
        st.session_state.answered = []
        st.session_state.quiz_feedback = {}
        st.session_state.quiz_question_ids = []
        st.session_state.quiz_index = 0
        st.success("Session progress cleared.")
        st.rerun()

st.divider()
st.markdown(
    '<p class="small-note">MedStudy is an educational project. Questions are illustrative study material, '
    'not medical advice. Verify clinical facts with trusted textbooks and instructors.</p>',
    unsafe_allow_html=True,
)
