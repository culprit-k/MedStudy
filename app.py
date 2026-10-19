import json
import os
import random
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "questions.json"
VISUAL_FILE = ROOT / "data" / "visual_questions.json"

st.set_page_config(
    page_title="MedStudy — Medical Learning Studio",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

QUESTIONS = load_json(DATA_FILE)
VISUAL_QUESTIONS = load_json(VISUAL_FILE)
SUBJECTS = list(QUESTIONS)
ALL_CARDS = [{"subject": subject, **item} for subject, items in QUESTIONS.items() for item in items]
ALL_CARDS += [{"subject": item["subject"], **item} for item in VISUAL_QUESTIONS]

def init_state():
    defaults = {
        "navigation": "Home", "answered": [], "bookmarks": [], "quiz_ids": [],
        "quiz_index": 0, "quiz_feedback": {}, "flashcard_index": 0,
        "tutor_messages": [], "profile_level": "MBBS — Core concepts",
        "profile_goal": "Exam preparation", "profile_style": "Explain simply, then go deeper",
        "daily_goal": 15, "visual_index": 0, "case_revealed": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#14263d; --muted:#6b7b90; --teal:#087f8c; --line:#e2eaf2; }
.stApp { background: linear-gradient(180deg,#f5f8fc 0%,#f8fafc 40%,#f3f7fa 100%); color:var(--ink); }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
h1,h2,h3 { font-family:'Manrope',sans-serif; letter-spacing:-.035em; color:var(--ink); }
[data-testid="stSidebar"] { background: #101f33; border-right:1px solid #263950; }
[data-testid="stSidebar"] * { color:#eef6ff; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .35rem .2rem; }
[data-testid="stSidebar"] hr { border-color:#30445a; }
.hero { padding:2.25rem 2.3rem; border-radius:26px; background:radial-gradient(circle at 85% 10%,#2c9ba0 0,transparent 28%),linear-gradient(120deg,#10233b,#164f61 72%,#087f8c); color:white; margin-bottom:1.2rem; box-shadow:0 18px 45px #0d34421a; }
.hero h1 { color:white; font-size:clamp(2rem,4vw,3.25rem); line-height:1.08; margin:0 0 .8rem; }
.hero p { color:#d7f3f1; font-size:1.05rem; max-width:760px; margin-bottom:1.2rem; }
.eyebrow { text-transform:uppercase; letter-spacing:.14em; font-size:.72rem; font-weight:800; color:#8ee4dd; margin-bottom:.7rem; }
.panel { background:white; border:1px solid var(--line); border-radius:20px; padding:1.15rem 1.25rem; box-shadow:0 8px 25px #172d4210; margin-bottom:.8rem; }
.pill { display:inline-block; background:#e8f7f6; color:#08717b; border-radius:999px; padding:.28rem .65rem; font-size:.76rem; font-weight:700; margin-right:.3rem; }
.muted { color:var(--muted); font-size:.9rem; }
div[data-testid="stMetric"] { background:white; border:1px solid var(--line); border-radius:17px; padding:1rem; box-shadow:0 6px 20px #172d4208; }
div.stButton > button { border-radius:12px; font-weight:700; min-height:2.65rem; }
.stButton > button[kind="primary"] { background:linear-gradient(100deg,#087f8c,#176b80); border:0; }
[data-testid="stExpander"] { background:white; border:1px solid var(--line); border-radius:14px; }
[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#0d9298,#62c6b6); }
div[data-testid="stChatMessage"] { background:white; border:1px solid var(--line); border-radius:16px; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

def jump(page):
    st.session_state.navigation = page

def find_question(qid):
    return next((item for item in ALL_CARDS if item["id"] == qid), None)

def show_image(relative_path):
    """Render local SVGs from their markup so Streamlit can display them reliably."""
    image_path = ROOT / relative_path
    if image_path.suffix.lower() == ".svg":
        st.image(image_path.read_text(encoding="utf-8"), use_container_width=True)
    else:
        st.image(str(image_path), use_container_width=True)

def record_answer(item, correct, chosen):
    st.session_state.answered.append({
        "id": item["id"], "subject": item["subject"], "correct": bool(correct),
        "chosen": chosen,
    })

attempts = len(st.session_state.answered)
correct_total = sum(int(x["correct"]) for x in st.session_state.answered)
accuracy = round(correct_total * 100 / attempts) if attempts else 0
mastered_subjects = len({x["subject"] for x in st.session_state.answered if x["correct"]})
total_questions = len(ALL_CARDS)

with st.sidebar:
    st.markdown("# 🩺 MedStudy")
    st.caption("MEDICAL LEARNING STUDIO")
    st.markdown("---")
    page = st.radio(
        "YOUR WORKSPACE",
        ["Home", "Learning Library", "Whole-Body Organ Simulator", "Anatomy Lab", "Physiology Lab", "Histology Lab", "Pathology Lab", "Microbiology Lab", "Biochemistry Lab", "Pharmacology Lab", "Radiology Lab", "ECG Lab", "Simulation Center", "Exam Arena", "Visual Lab", "Clinical Cases", "OSCE Studio", "Research & EBM", "Teacher AI", "Flashcards", "Bookmarks", "Progress & Goals"],
        key="navigation",
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("**Your learning profile**")
    st.caption(st.session_state.profile_level)
    st.caption(f"Goal: {st.session_state.profile_goal}")
    st.progress(min(attempts / max(st.session_state.daily_goal, 1), 1.0))
    st.caption(f"{attempts}/{st.session_state.daily_goal} questions attempted this session")
    st.markdown("---")
    st.caption("Study companion only · not for diagnosis or treatment decisions")

if page == "Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Your personal medical learning space</div>
      <h1>Learn medicine.<br>Think like a clinician.</h1>
      <p>Move beyond memorisation with image-based anatomy, clinical reasoning cases, exam-level questions, and a tutor that adapts to your goals.</p>
      <span class="pill">MBBS</span><span class="pill">Postgraduate revision</span><span class="pill">Research-minded learning</span>
    </div>
    """, unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Learning topics", len(SUBJECTS))
    m2.metric("Question bank", total_questions)
    m3.metric("Attempted", attempts)
    m4.metric("Accuracy", f"{accuracy}%")
    st.markdown("## Choose your next session")
    cards = [
        ("🧠","Learning library","Build strong foundations, then review mechanisms and clinical correlations.","Learning Library"),
        ("🩻","Visual lab","Interpret anatomy illustrations and image-led questions.","Visual Lab"),
        ("🫀","Anatomy lab","Explore cardiovascular, renal, nervous and respiratory structures with clinical links.","Anatomy Lab"),
        ("🧪","Physiology lab","Run interactive experiments in cardiovascular, respiratory, renal and nerve physiology.","Physiology Lab"),
        ("🧍","Whole-body organ simulator","Adjust organ-system variables and explore simplified whole-body responses.","Whole-Body Organ Simulator"),
        ("🔬","Histology lab","Study tissue architecture, cell identification and microscopic patterns.","Histology Lab"),
        ("🧫","Pathology lab","Explore mechanisms, gross patterns, blood films and case-based morphology.","Pathology Lab"),
        ("🦠","Microbiology lab","Practise organism identification, staining, culture and diagnostic reasoning.","Microbiology Lab"),
        ("⚗️","Biochemistry lab","Interpret enzymes, metabolism, electrolytes and clinical laboratory panels.","Biochemistry Lab"),
        ("💊","Pharmacology lab","Explore dose-response, receptors, kinetics, interactions and adverse effects.","Pharmacology Lab"),
        ("🩻","Radiology lab","Practise a systematic approach to imaging and anatomy orientation.","Radiology Lab"),
        ("💓","ECG lab","Learn ECG waves, intervals, rhythm interpretation and common patterns.","ECG Lab"),
        ("🧬","Simulation center","Use safe, fictional patient data to practise integrated clinical reasoning.","Simulation Center"),
        ("🩺","Clinical reasoning","Work through structured cases and explain your differential.","Clinical Cases"),
        ("👩‍⚕️","OSCE studio","Practise structured history, examination, and communication.","OSCE Studio"),
        ("📊","Research & EBM","Explore PICO, study design, diagnostic tests, and critical appraisal.","Research & EBM"),
        ("👩‍🏫","Personal teacher","Ask for a lesson, a Socratic hint, or a revision plan.","Teacher AI"),
    ]
    cols = st.columns(2)
    for i,(icon,title,desc,target) in enumerate(cards):
        with cols[i%2]:
            st.markdown(f'<div class="panel"><div style="font-size:1.8rem">{icon}</div><h3>{title}</h3><p class="muted">{desc}</p></div>', unsafe_allow_html=True)
            st.button(f"Open {title} →", key=f"home_{target}", use_container_width=True, on_click=jump, args=(target,))
    st.markdown("## Keep your momentum")
    left,right = st.columns([1.4,1])
    with left:
        st.markdown('<div class="panel"><h3>Suggested study loop</h3><p>① Learn one concept → ② test recall → ③ apply it to a case → ④ explain it in your own words.</p><p class="muted">Short active-recall sessions are more useful than rereading alone.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Session snapshot</h3><p><b>'+str(correct_total)+'</b> correct responses</p><p><b>'+str(len(st.session_state.bookmarks))+'</b> saved questions</p><p><b>'+str(mastered_subjects)+'</b> subjects with a correct answer</p></div>', unsafe_allow_html=True)

elif page == "Learning Library":
    st.title("📚 Learning library")
    st.caption("Start with the core idea, then use the explanation to connect mechanism to clinical relevance.")
    subject = st.selectbox("Subject", SUBJECTS)
    level = st.select_slider("Learning depth", options=["Foundation", "MBBS exam", "Clinical integration", "Postgraduate / research"], value=st.session_state.profile_level.split(" — ")[0] if st.session_state.profile_level.split(" — ")[0] in ["Foundation","MBBS exam","Clinical integration","Postgraduate / research"] else "MBBS exam")
    st.session_state.profile_level = level
    search = st.text_input("Search within this subject", placeholder="e.g. inflammation, nephron, receptor…")
    items = QUESTIONS[subject]
    if search:
        items = [q for q in items if search.lower() in (q["question"]+" "+q["explanation"]).lower()]
    st.caption(f"{len(items)} items · {subject}")
    for i,item in enumerate(items,1):
        with st.expander(f"{i:02d}  ·  {item['question']}"):
            st.markdown("**Options**")
            for option in item["options"]:
                st.write("• "+option)
            st.success("Correct answer: "+item["answer"])
            st.write(item["explanation"])
            if level in ["Clinical integration","Postgraduate / research"]:
                st.info("Higher-level prompt: What mechanism explains this finding, and which alternative explanation would you exclude?")
            if st.button("☆ Save to bookmarks", key=f"libsave_{item['id']}"):
                if item["id"] not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(item["id"])
                st.toast("Saved to your revision list")

elif page == "Exam Arena":
    st.title("🏁 Exam arena")
    st.caption("Active recall with instant feedback. Choose your focus, attempt the question, then review the reasoning.")
    c1,c2,c3=st.columns(3)
    with c1:
        quiz_subject=st.selectbox("Question pool",["All subjects"]+SUBJECTS,key="arena_subject")
    with c2:
        quiz_size=st.selectbox("Session length",[5,10,15,20],key="arena_size")
    with c3:
        quiz_mode=st.selectbox("Practice style",["Standard MCQ","Mechanism challenge","Clinical integration"],key="arena_mode")
    if st.button("Start / restart exam",type="primary",use_container_width=True):
        pool=ALL_CARDS if quiz_subject=="All subjects" else [q for q in ALL_CARDS if q["subject"]==quiz_subject]
        if quiz_mode=="Clinical integration":
            pool=[q for q in pool if q["subject"]=="Clinical reasoning"] or pool
        chosen=random.sample(pool,k=min(quiz_size,len(pool)))
        st.session_state.quiz_ids=[q["id"] for q in chosen]
        st.session_state.quiz_index=0
        st.session_state.quiz_feedback={}
        st.rerun()
    ids=st.session_state.quiz_ids
    if not ids:
        st.markdown('<div class="panel"><h3>Ready when you are</h3><p>Pick a subject and session length, then start. Treat every explanation as a mini-review.</p></div>',unsafe_allow_html=True)
    elif st.session_state.quiz_index>=len(ids):
        answers=list(st.session_state.quiz_feedback.values())
        score=sum(1 for x in answers if x["correct"])
        st.balloons()
        st.success("Session complete — review your errors before starting another round.")
        a,b,c=st.columns(3)
        a.metric("Score",f"{score}/{len(answers)}")
        b.metric("Accuracy",f"{round(100*score/max(len(answers),1))}%")
        c.metric("Questions reviewed",len(answers))
        misses=[x for x in answers if not x["correct"]]
        if misses:
            st.markdown("### Review missed questions")
            for missed in misses:
                item=find_question(missed["id"])
                if item:
                    with st.expander(item["question"]):
                        st.write("Your answer: "+missed["chosen"])
                        st.success("Correct answer: "+item["answer"])
                        st.write(item["explanation"])
    else:
        qid=ids[st.session_state.quiz_index]
        item=find_question(qid)
        if item:
            st.progress(st.session_state.quiz_index/len(ids))
            st.caption(f"QUESTION {st.session_state.quiz_index+1} OF {len(ids)} · {item['subject']} · {quiz_mode}")
            if item.get("image"):
                show_image(item["image"])
            st.markdown(f'<div class="panel"><h3>{item["question"]}</h3></div>',unsafe_allow_html=True)
            feedback=st.session_state.quiz_feedback.get(qid)
            if feedback:
                st.write("Your answer: "+feedback["chosen"])
                if feedback["correct"]: st.success("Correct.")
                else: st.error("Correct answer: "+item["answer"])
                st.write(item["explanation"])
                if st.button("Next question →",type="primary",use_container_width=True):
                    st.session_state.quiz_index+=1; st.rerun()
            else:
                choice=st.radio("Select one answer",item["options"],key=f"arena_choice_{qid}")
                if st.button("Submit answer",type="primary",use_container_width=True):
                    is_correct=choice==item["answer"]
                    st.session_state.quiz_feedback[qid]={"id":qid,"chosen":choice,"correct":is_correct}
                    record_answer(item,is_correct,choice)
                    st.rerun()
                if st.button("Bookmark this question",key=f"arena_bookmark_{qid}"):
                    if qid not in st.session_state.bookmarks: st.session_state.bookmarks.append(qid)
                    st.toast("Saved to revision list")

elif page == "Anatomy Lab":
    st.title("🫀 Anatomy Lab")
    st.caption("Explore systems, select structures, connect gross anatomy to physiology, and test your understanding.")
    systems = {
        "Cardiovascular": {
            "image":"assets/heart.svg",
            "structures":{
                "Heart":("Four-chambered muscular pump","Right atrium receives systemic venous blood; right ventricle pumps it to the pulmonary circulation. Left atrium receives oxygenated pulmonary venous blood; left ventricle ejects into the aorta.","Clinical link: left ventricular dysfunction can cause pulmonary congestion; right ventricular dysfunction can cause systemic venous congestion."),
                "Coronary circulation":("Arterial supply of the myocardium","The right and left coronary arteries arise from the ascending aorta. Coronary perfusion, especially of the left ventricle, occurs predominantly during diastole.","Clinical link: coronary occlusion can cause myocardial ischaemia and infarction."),
                "Conduction system":("Specialised cardiac excitation pathway","The SA node normally initiates impulses; conduction proceeds through the AV node, His bundle, bundle branches and Purkinje network.","Clinical link: conduction blocks alter the relationship between atrial and ventricular activity.")
            }},
        "Renal": {
            "image":"assets/nephron.svg",
            "structures":{
                "Nephron":("Functional unit of the kidney","Glomerular filtration is followed by selective tubular reabsorption and secretion. The proximal tubule reabsorbs most filtered sodium and water; the loop of Henle contributes to the medullary osmotic gradient.","Clinical link: tubular injury may impair electrolyte handling even when filtration is relatively preserved."),
                "Glomerulus":("Capillary filtration apparatus","Fenestrated endothelium, glomerular basement membrane and podocyte slit diaphragms contribute to selective filtration.","Clinical link: damage to the filtration barrier can produce haematuria and/or proteinuria."),
                "Juxtaglomerular apparatus":("Renal pressure and salt-sensing region","Macula densa cells sense tubular NaCl delivery; granular cells release renin in response to appropriate signals.","Clinical link: renin initiates the renin–angiotensin–aldosterone system.")
            }},
        "Nervous": {
            "image":"assets/neuron.svg",
            "structures":{
                "Neuron":("Excitable information-processing cell","Dendrites receive signals, the soma integrates them, the axon conducts action potentials and synaptic terminals communicate with target cells.","Clinical link: demyelination can slow or block saltatory conduction."),
                "Myelin":("Electrical insulation around selected axons","Myelin increases conduction velocity by allowing action potentials to regenerate at nodes of Ranvier.","Clinical link: central and peripheral demyelinating disorders affect different myelin-forming cells."),
                "Synapse":("Junction for cell-to-cell signalling","Chemical synapses convert presynaptic electrical activity into neurotransmitter release and postsynaptic responses.","Clinical link: many medicines alter neurotransmitter synthesis, release, receptors or reuptake.")
            }},
        "Respiratory": {
            "image":"assets/alveoli.svg",
            "structures":{
                "Alveolar interface":("Thin barrier for gas exchange","Oxygen and carbon dioxide diffuse down partial-pressure gradients across the alveolar–capillary interface; effective exchange depends on area, thickness and ventilation–perfusion matching.","Clinical link: oedema or fibrosis increases diffusion distance; pulmonary embolism disrupts perfusion."),
                "Type I pneumocytes":("Thin alveolar epithelial cells","These cells cover most of the alveolar surface and provide a short diffusion path.","Clinical link: injury to the alveolar epithelium can compromise gas exchange."),
                "Type II pneumocytes":("Surfactant-producing epithelial cells","They secrete pulmonary surfactant and can proliferate to help restore alveolar epithelium after injury.","Clinical link: surfactant deficiency increases alveolar surface tension.")
            }}
    }
    system_name = st.selectbox("Choose a system", list(systems.keys()), key="anatomy_system")
    system = systems[system_name]
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        show_image(system["image"])
        st.markdown("#### Structure explorer")
        structure_name = st.radio("Select a structure", list(system["structures"].keys()), key=f"anatomy_structure_{system_name}")
        st.caption("Teaching schematics are simplified and not to scale.")
    with right:
        title, explanation, clinical = system["structures"][structure_name]
        st.markdown(f"### {structure_name}")
        st.markdown(f"**{title}**")
        st.write(explanation)
        st.info(clinical)
        st.markdown("#### Quick actions")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Explain clinically", use_container_width=True):
                st.session_state.navigation = "Teacher AI"
                st.session_state.tutor_prefill = f"Explain {structure_name} in the {system_name.lower()} system with clinical correlations, mechanisms, and exam traps."
                st.rerun()
        with c2:
            if st.button("Quiz me on this", type="primary", use_container_width=True):
                st.session_state.anatomy_quiz_structure = structure_name
                st.session_state.anatomy_quiz_system = system_name
        if st.session_state.get("anatomy_quiz_structure") == structure_name and st.session_state.get("anatomy_quiz_system") == system_name:
            quiz_items = {
                "Heart":("Which chamber ejects blood into the systemic circulation?","Left ventricle"),
                "Coronary circulation":("When does most left ventricular coronary perfusion occur?","During diastole"),
                "Conduction system":("What is the usual primary pacemaker of the heart?","SA node"),
                "Nephron":("Which two processes follow glomerular filtration to modify tubular fluid?","Reabsorption and secretion"),
                "Glomerulus":("Name one component of the glomerular filtration barrier.","Glomerular basement membrane"),
                "Juxtaglomerular apparatus":("Which enzyme is released by granular cells?","Renin"),
                "Neuron":("Which neuronal region commonly conducts action potentials away from the soma?","Axon"),
                "Myelin":("What is the effect of myelin on conduction velocity?","It increases conduction velocity"),
                "Synapse":("What chemical messenger is released at a typical chemical synapse?","Neurotransmitter"),
                "Alveolar interface":("Name one factor that reduces diffusion across the alveolar-capillary membrane.","Increased membrane thickness / reduced surface area"),
                "Type I pneumocytes":("What is the main gas-exchange role of type I pneumocytes?","Provide a thin diffusion surface"),
                "Type II pneumocytes":("What important substance do type II pneumocytes produce?","Surfactant")
            }
            question, answer = quiz_items[structure_name]
            st.markdown(f"**Recall check:** {question}")
            if st.button("Reveal answer", key=f"reveal_{system_name}_{structure_name}"):
                st.success(answer)
    st.markdown("---")
    st.markdown("### Course pathway")
    chapters = [
        ("1","Orientation & anatomical language","Foundations"),
        ("2","Cardiovascular system","Core concepts"),
        ("3","Respiratory system","Structure–function"),
        ("4","Renal system","Filtration and regulation"),
        ("5","Nervous system","Neuroanatomy"),
        ("6","Integrated clinical anatomy","Clinical application")
    ]
    cols = st.columns(3)
    for i,(num,name,detail) in enumerate(chapters):
        with cols[i%3]:
            with st.container(border=True):
                st.caption(f"CHAPTER {num}")
                st.markdown(f"**{name}**")
                st.caption(detail)
                if st.button("Open chapter", key=f"anatomy_chapter_{num}", use_container_width=True):
                    st.session_state.anatomy_system = {"2":"Cardiovascular","3":"Respiratory","4":"Renal","5":"Nervous"}.get(num, system_name)
                    st.rerun()
    st.caption("Next pathway suggestion: revise a structure, answer its recall check, then practise related questions in Exam Arena. Content is educational and should be checked against trusted anatomy resources.")

elif page == "Whole-Body Organ Simulator":
    st.title("🧍 Whole-Body Organ Simulator")
    st.caption("An educational sandbox for exploring how organ systems interact. All outputs are simplified teaching models, not predictions for real people.")
    st.warning("Simulation only: these equations are illustrative, not physiologically complete or clinically validated. Do not enter real patient data or use the outputs for diagnosis, treatment, or medication decisions.")
    organ_groups = {
        "Heart & circulation": {
            "organ":"Heart","icon":"💓","description":"Explore how heart rate, stroke volume and vascular resistance interact in a simplified circulation model.",
            "controls":[("Heart rate (beats/min)",40,180,75),("Stroke volume (mL/beat)",30,130,70),("Systemic vascular resistance (relative units)",0.5,2.0,1.0)],
            "model":"cardio"
        },
        "Lungs & ventilation": {
            "organ":"Lungs","icon":"🫁","description":"Explore minute ventilation and a simplified carbon dioxide trend.",
            "controls":[("Respiratory rate (breaths/min)",6,40,14),("Tidal volume (mL)",200,900,500),("Dead-space volume (mL)",50,300,150)],
            "model":"resp"
        },
        "Kidneys & fluid balance": {
            "organ":"Kidneys","icon":"🫘","description":"Explore conceptual relationships among filtration, urine output and fluid balance.",
            "controls":[("Filtration index (% of reference)",10,140,100),("Daily fluid intake (L)",0.5,5.0,2.0),("Daily fluid loss outside urine (L)",0.2,3.0,0.8)],
            "model":"renal"
        },
        "Liver & metabolism": {
            "organ":"Liver","icon":"🟤","description":"Explore a conceptual hepatic processing index and its effect on a fictional metabolism score.",
            "controls":[("Hepatic function index (%)",10,120,100),("Nutrient load (relative units)",0,10,5),("Medication burden (relative units)",0,10,2)],
            "model":"liver"
        },
        "Pancreas & glucose": {
            "organ":"Pancreas","icon":"🧬","description":"Explore how a simplified insulin-effect parameter changes a fictional glucose trend.",
            "controls":[("Glucose input (relative units)",0,12,5),("Insulin effect (%)",0,150,100),("Activity level (relative units)",0,10,4)],
            "model":"glucose"
        },
        "Brain & nervous system": {
            "organ":"Brain / nerves","icon":"🧠","description":"Explore a conceptual signal transmission index as myelination and synaptic efficiency vary.",
            "controls":[("Myelination index (%)",0,100,90),("Synaptic efficiency (%)",10,120,85),("Signal load (relative units)",1,10,5)],
            "model":"neuro"
        },
        "Gastrointestinal system": {
            "organ":"GI tract","icon":"🫃","description":"Explore simplified transit and absorption concepts.",
            "controls":[("Motility index (%)",10,180,100),("Absorption efficiency (%)",10,100,85),("Nutrient load (relative units)",1,10,5)],
            "model":"gi"
        },
        "Endocrine / thyroid": {
            "organ":"Thyroid axis","icon":"🦋","description":"Explore a conceptual metabolic activity index; real endocrine feedback is more complex.",
            "controls":[("Thyroid hormone activity index (%)",10,180,100),("Energy demand (relative units)",1,10,5),("Stress signal (relative units)",0,10,3)],
            "model":"endo"
        },
        "Blood & oxygen transport": {
            "organ":"Blood","icon":"🩸","description":"Explore oxygen-carrying capacity concepts using haemoglobin and saturation sliders.",
            "controls":[("Haemoglobin (g/dL)",4.0,20.0,14.0),("Oxygen saturation (%)",50,100,98),("Cardiac output (L/min)",2.0,10.0,5.0)],
            "model":"blood"
        },
        "Immune / inflammation": {
            "organ":"Immune system","icon":"🛡️","description":"Explore a fictional inflammation-response index, illustrating how immune activation can affect systemic demand.",
            "controls":[("Immune activation index (%)",0,200,30),("Tissue injury index (%)",0,100,10),("Recovery support index (%)",0,100,70)],
            "model":"immune"
        },
        "Skin & temperature": {
            "organ":"Skin / thermoregulation","icon":"🌡️","description":"Explore conceptual thermoregulation inputs and heat-loss balance.",
            "controls":[("Ambient temperature (°C)",-5,40,22),("Activity heat production (relative units)",0,10,4),("Skin blood-flow index (%)",10,150,80)],
            "model":"skin"
        },
        "Reproductive system": {
            "organ":"Reproductive system","icon":"🧬","description":"Explore a conceptual hormone-cycle signal. This does not model fertility or predict individual outcomes.",
            "controls":[("Hormone signal A (relative units)",0,10,5),("Hormone signal B (relative units)",0,10,5),("Cycle phase (teaching index)",1,4,2)],
            "model":"repro"
        }
    }
    organ_name = st.selectbox("Choose an organ system", list(organ_groups.keys()), key="wholebody_organ")
    cfg = organ_groups[organ_name]
    st.markdown(f"### {cfg['icon']} {cfg['organ']}")
    st.write(cfg["description"])
    left, right = st.columns([1,1], gap="large")
    values = []
    with left:
        st.markdown("#### Simulation controls")
        for label, lo, hi, default in cfg["controls"]:
            if isinstance(lo, int) and isinstance(hi, int):
                value = st.slider(label, lo, hi, default, key=f"wholebody_{cfg['model']}_{label}")
            else:
                value = st.slider(label, float(lo), float(hi), float(default), key=f"wholebody_{cfg['model']}_{label}")
            values.append(value)
    a,b,c = values
    if cfg["model"] == "cardio":
        cardiac_output = a*b/1000
        pressure_index = cardiac_output*c
        metrics = [("Cardiac output",f"{cardiac_output:.1f} L/min"),("Relative pressure index",f"{pressure_index:.1f}"),("Heart rate",f"{a} bpm")]
        chart = {"Heart rate":[a,a+5,a+10,a+15],"Cardiac output (L/min)":[round(cardiac_output,1),round(cardiac_output*1.04,1),round(cardiac_output*1.08,1),round(cardiac_output*1.12,1)]}
        note = "Cardiac output = heart rate × stroke volume. The pressure index is illustrative; real blood pressure depends on complex haemodynamics."
    elif cfg["model"] == "resp":
        minute_vent = a*b/1000
        alveolar = a*max(b-c,0)/1000
        co2_index = 40*5/max(alveolar,0.1)
        metrics = [("Minute ventilation",f"{minute_vent:.1f} L/min"),("Alveolar ventilation",f"{alveolar:.1f} L/min"),("Illustrative CO₂ index",f"{co2_index:.1f}")]
        chart = {"Respiratory rate":[max(6,a-3),a,a+3,a+6],"Alveolar ventilation (L/min)":[round(max(0,(a-3)*max(b-c,0)/1000),1),round(alveolar,1),round((a+3)*max(b-c,0)/1000,1),round((a+6)*max(b-c,0)/1000,1)]}
        note = "The inverse CO₂ relationship assumes constant CO₂ production and idealised steady state. Real gas exchange depends on perfusion, metabolism and lung disease."
    elif cfg["model"] == "renal":
        net = b-(c+1.2)
        metrics = [("Filtration index",f"{a}%"),("Illustrative net fluid balance",f"{net:+.1f} L/day"),("Model urine trend", "Lower" if a<60 else ("Reference range" if a<=120 else "Higher filtration index"))]
        chart = {"Filtration index (%)":[max(10,a-30),max(10,a-15),a,min(140,a+15)],"Net fluid balance (L/day)":[round(net-0.6,1),round(net-0.3,1),round(net,1),round(net+0.3,1)]}
        note = "This is not a kidney-function estimator. Actual GFR requires appropriate clinical assessment and validated methods; fluid balance depends on many inputs."
    elif cfg["model"] == "liver":
        score = max(0, a - 2*b - c)
        metrics = [("Hepatic function index",f"{a}%"),("Fictional processing score",f"{score:.0f}"),("Relative load",f"{b+c} units")]
        chart = {"Function index (%)":[max(10,a-30),max(10,a-15),a,min(120,a+10)],"Fictional processing score":[max(0,score-10),max(0,score-5),score,score+3]}
        note = "There is no single liver-function score represented here. Real hepatic assessment uses history, examination, laboratory patterns and sometimes imaging or other tests."
    elif cfg["model"] == "glucose":
        trend = max(0, 100 + 8*a - 0.45*b - 3*c)
        metrics = [("Fictional glucose trend index",f"{trend:.0f}"),("Insulin-effect input",f"{b}%"),("Activity input",f"{c} units")]
        chart = {"Glucose trend index":[trend+10,trend+5,trend, max(0,trend-5)],"Insulin effect (%)":[max(0,b-30),max(0,b-15),b,min(150,b+15)]}
        note = "This is not a blood glucose prediction. Real glucose regulation depends on pancreatic secretion, sensitivity, meals, counter-regulatory hormones and many other factors."
    elif cfg["model"] == "neuro":
        signal = a*b/100
        metrics = [("Signal transmission index",f"{signal:.0f}/100"),("Signal load",f"{c} units"),("Conceptual efficiency","Higher" if signal>65 else "Reduced")]
        chart = {"Myelination (%)":[max(0,a-30),max(0,a-15),a,min(100,a+5)],"Transmission index":[round(max(0,a-30)*b/100),round(max(0,a-15)*b/100),round(signal),round(min(100,a+5)*b/100)]}
        note = "Neural signalling is far more complex than a single index; this slider illustrates only the conceptual contribution of myelin and synaptic function."
    elif cfg["model"] == "gi":
        absorption = b * min(1.2, max(0.2, a/100))
        metrics = [("Conceptual absorption index",f"{absorption:.0f}"),("Motility index",f"{a}%"),("Nutrient load",f"{c} units")]
        chart = {"Motility index (%)":[max(10,a-30),max(10,a-15),a,min(180,a+15)],"Absorption index":[round(absorption*0.7,1),round(absorption*0.85,1),round(absorption,1),round(absorption*1.05,1)]}
        note = "Motility and absorption vary by organ segment, nutrient, neural and hormonal regulation, and disease. This is a conceptual illustration only."
    elif cfg["model"] == "endo":
        score = a - 2*c + b
        metrics = [("Metabolic activity index",f"{score:.0f}"),("Hormone activity input",f"{a}%"),("Stress signal",f"{c} units")]
        chart = {"Hormone activity (%)":[max(10,a-30),max(10,a-15),a,min(180,a+15)],"Metabolic activity index":[score-10,score-5,score,score+5]}
        note = "The hypothalamic–pituitary–thyroid axis uses feedback loops; this model does not represent hormone concentrations or diagnose thyroid disorders."
    elif cfg["model"] == "blood":
        oxygen_capacity = 1.34*a*b/100
        delivery = oxygen_capacity*c
        metrics = [("Estimated O₂ capacity component",f"{oxygen_capacity:.1f} mL O₂/dL"),("Conceptual delivery index",f"{delivery:.1f}"),("Haemoglobin",f"{a:.1f} g/dL")]
        chart = {"Haemoglobin (g/dL)":[max(4,a-3),max(4,a-1.5),a,min(20,a+1)],"O₂ capacity component":[round(1.34*max(4,a-3)*b/100,1),round(1.34*max(4,a-1.5)*b/100,1),round(oxygen_capacity,1),round(1.34*min(20,a+1)*b/100,1)]}
        note = "The haemoglobin-bound oxygen component is approximate and excludes dissolved oxygen; oxygen delivery also depends on cardiac output and tissue extraction."
    elif cfg["model"] == "immune":
        score = max(0,a + 0.7*b - 0.5*c)
        metrics = [("Fictional inflammation index",f"{score:.0f}"),("Tissue injury input",f"{b}%"),("Recovery support",f"{c}%")]
        chart = {"Immune activation (%)":[max(0,a-30),max(0,a-15),a,min(200,a+15)],"Fictional inflammation index":[max(0,score-15),max(0,score-7),score,score+5]}
        note = "Inflammation is a coordinated biological response, not a single numerical score. This toy model is not a sepsis or immune-risk calculator."
    elif cfg["model"] == "skin":
        heat = c/100*max(1,35-a) + b
        metrics = [("Conceptual heat-balance index",f"{heat:.1f}"),("Ambient temperature",f"{a} °C"),("Skin blood-flow input",f"{c}%")]
        chart = {"Ambient temperature (°C)":[max(-5,a-6),max(-5,a-3),a,min(40,a+3)],"Heat-balance index":[round(heat+4,1),round(heat+2,1),round(heat,1),round(heat-1,1)]}
        note = "Thermoregulation includes hypothalamic control, sweating, vasomotor changes, behaviour and environmental factors. This is not a core-temperature prediction."
    else:
        score = max(0,10-abs(a-b)-abs(c-2))
        metrics = [("Fictional synchrony index",f"{score:.0f}/10"),("Signal A",f"{a} units"),("Signal B",f"{b} units")]
        chart = {"Signal A":[max(0,a-2),max(0,a-1),a,min(10,a+1)],"Signal B":[max(0,b-2),max(0,b-1),b,min(10,b+1)]}
        note = "Reproductive physiology depends on age, anatomy, endocrine feedback, timing and individual variation. This toy score has no fertility or diagnostic meaning."
    with right:
        st.markdown("#### Live model output")
        metric_cols = st.columns(2)
        for i,(label,value) in enumerate(metrics):
            metric_cols[i%2].metric(label,value)
        st.markdown("#### Response curve")
        st.line_chart(chart)
        st.info(note)
    st.markdown("### Organ-to-organ connections")
    connections = {
        "Heart & circulation":"The heart supplies blood flow to the lungs, kidneys, brain, liver and other tissues; vascular resistance and circulating volume influence pressure.",
        "Lungs & ventilation":"Lungs exchange gases with blood; ventilation and perfusion must be matched for efficient oxygen uptake and carbon dioxide removal.",
        "Kidneys & fluid balance":"Kidneys regulate water, electrolytes, acid–base balance and contribute to blood-pressure control through volume handling and hormonal pathways.",
        "Liver & metabolism":"The liver processes nutrients, synthesises proteins, metabolises many substances and contributes to glucose homeostasis.",
        "Pancreas & glucose":"Insulin and glucagon coordinate with liver, muscle and adipose tissue to regulate circulating glucose.",
        "Brain & nervous system":"Autonomic and endocrine signals coordinate heart rate, breathing, temperature, digestion and many homeostatic responses.",
        "Gastrointestinal system":"Digestion and absorption provide nutrients and fluid for metabolism and influence endocrine and immune signalling.",
        "Endocrine / thyroid":"Hormones coordinate metabolic activity and interact with cardiovascular, nervous, reproductive and other systems.",
        "Blood & oxygen transport":"Blood transports oxygen, carbon dioxide, nutrients, hormones and immune components between organs.",
        "Immune / inflammation":"Immune signalling interacts with circulation, liver acute-phase responses, bone marrow and thermoregulation.",
        "Skin & temperature":"Skin blood flow and sweating help exchange heat with the environment; the brain coordinates thermoregulatory responses.",
        "Reproductive system":"Reproductive function interacts with hypothalamic, pituitary, gonadal and other endocrine pathways."
    }
    st.write(connections[organ_name])
    st.markdown("### Suggested practical sequence")
    st.write("1. Record the baseline settings.  2. Change one variable at a time.  3. Observe the output curve.  4. Explain the mechanism.  5. Identify at least one limitation of the model.  6. Compare the concept with a trusted physiology text.")
    if st.button("Ask Teacher AI to explain these results", type="primary", key="wholebody_explain"):
        st.session_state.tutor_prefill = f"Explain the physiology of {cfg['organ']} and its connections to other organ systems. Explain these illustrative simulation outputs: {metrics}. State the model limitations and give MBBS-level retrieval questions."
        st.session_state.navigation = "Teacher AI"
        st.rerun()

elif page in ["Physiology Lab", "Histology Lab", "Pathology Lab", "Microbiology Lab", "Biochemistry Lab", "Pharmacology Lab", "Radiology Lab", "ECG Lab", "Simulation Center"]:
    lab_configs = {
      "Physiology Lab": {
        "icon":"🧪","subtitle":"Virtual experiments: change a variable, observe the response, and explain the mechanism.",
        "experiments":{
          "Cardiovascular response to exercise":("Heart rate (beats/min)",40,180,90,"As workload rises, sympathetic drive generally increases heart rate and contractility. Actual responses vary with fitness, medications, temperature and disease."),
          "Ventilation and carbon dioxide":("Alveolar ventilation (L/min)",2,12,5,"For a constant CO₂ production rate, increasing alveolar ventilation lowers arterial CO₂; reducing ventilation raises it. This is a simplified teaching model."),
          "Renal clearance explorer":("Urine concentration factor",1,5,3,"Urine concentration depends on the medullary osmotic gradient, tubular function, and ADH. A single slider cannot represent the full renal physiology.")
        }},
      "Histology Lab": {
        "icon":"🔬","subtitle":"Virtual microscopy and tissue identification practice. Schematic descriptions are educational, not diagnostic slides.",
        "experiments":{
          "Cardiac muscle":("Identify the key feature",["Striations with branching fibres and intercalated discs","Parallel non-striated spindle-shaped cells","Chondrocytes in lacunae"],0,"Cardiac muscle has striations, branching cells, central nuclei and intercalated discs that support coordinated contraction."),
          "Kidney cortex":("Identify the key feature",["Glomeruli and convoluted tubules","Alveoli and thin septa","Hepatic lobules with central veins"],0,"The renal cortex contains glomeruli and proximal/distal convoluted tubules. The medulla lacks renal corpuscles."),
          "Respiratory epithelium":("Choose the typical conducting-airway lining",["Pseudostratified ciliated columnar epithelium with goblet cells","Simple squamous epithelium throughout","Transitional epithelium"],0,"Much of the conducting airway is lined by pseudostratified ciliated columnar epithelium; the alveoli are predominantly lined by thin type I pneumocytes.")
        }},
      "Pathology Lab": {
        "icon":"🧫","subtitle":"Practise morphological pattern recognition and connect findings to mechanisms.",
        "experiments":{
          "Cell injury pattern":("Which finding is most consistent with reversible cell injury?",["Cellular swelling and fatty change","Complete membrane rupture with karyolysis","Caseous necrosis"],0,"Cellular swelling and fatty change can occur in reversible injury. Severe irreversible injury may cause membrane disruption and nuclear changes."),
          "Inflammation pattern":("Which cell predominates early in many acute bacterial infections?",["Neutrophil","Plasma cell","Eosinophil"],0,"Neutrophils commonly predominate early in acute bacterial inflammation, although patterns depend on cause, site and timing."),
          "Thrombus vs postmortem clot":("Which feature supports an antemortem thrombus?",["Attachment to vessel wall and lines of Zahn when present","Uniform jelly-like clot without attachment","Presence only after death"],0,"Antemortem thrombi may attach to the vessel wall and show laminations (lines of Zahn), especially in flowing blood. Morphology must be interpreted in context.")
        }},
      "Microbiology Lab": {
        "icon":"🦠","subtitle":"Virtual bench exercises in staining, culture logic and diagnostic test selection. No real specimens are involved.",
        "experiments":{
          "Gram stain reasoning":("A Gram-positive organism typically appears:",["Purple due to retention of crystal violet–iodine complex","Pink because it loses crystal violet","Green due to acid-fast stain"],0,"Gram-positive bacteria retain the crystal violet–iodine complex after decolorisation and appear purple."),
          "Acid-fast staining":("Why can Mycobacterium retain carbol fuchsin?",["Lipid-rich, mycolic-acid-containing cell envelope","A bacterial nucleus","Absence of a cell wall"],0,"The mycolic-acid-rich envelope contributes to acid-fastness. Staining results need appropriate controls and clinical interpretation."),
          "Diagnostic test choice":("For suspected bloodstream infection, which sample is commonly collected before antibiotics when feasible?",["Blood cultures using appropriate sets and technique","A swab of intact skin only","A urine dipstick alone"],0,"Blood cultures are collected with aseptic technique and adequate volume before antibiotics when this does not dangerously delay urgent treatment.")
        }},
      "Biochemistry Lab": {
        "icon":"⚗️","subtitle":"Interpret simplified laboratory scenarios and explore biochemical mechanisms.",
        "experiments":{
          "Enzyme interpretation":("A markedly increased ALT most directly suggests injury involving:",["Hepatocytes (interpreted with the full panel and context)","Red cells only","Bone mineral exclusively"],0,"ALT is associated with hepatocellular injury, but magnitude and pattern must be interpreted alongside AST, ALP, bilirubin, history and other findings."),
          "Acid-base basics":("A low pH with elevated PaCO₂ most directly indicates:",["Primary respiratory acidosis (check compensation and context)","Primary respiratory alkalosis","Isolated metabolic alkalosis"],0,"A low pH and raised PaCO₂ support respiratory acidosis; assess bicarbonate, compensation, timing and mixed disorders."),
          "Glucose regulation":("Which hormone generally lowers blood glucose by promoting uptake and storage?",["Insulin","Glucagon","Cortisol"],0,"Insulin promotes glucose uptake in insulin-sensitive tissues and supports glycogen, lipid and protein synthesis.")
        }},
      "Pharmacology Lab": {
        "icon":"💊","subtitle":"Explore pharmacodynamics and pharmacokinetics using simplified teaching models.",
        "experiments":{
          "Dose-response":("Increasing agonist concentration usually increases response until:",["A maximal effect is approached","All receptors disappear immediately","The drug becomes an antagonist by definition"],0,"A graded dose-response curve rises toward an Emax. Potency and efficacy are distinct; curves depend on system and experimental conditions."),
          "Half-life":("After approximately five half-lives, the fraction remaining after a single dose is about:",["3%","50%","25%"],0,"After five half-lives, about 1/32 (3.1%) remains under first-order elimination assumptions."),
          "Receptor antagonism":("A reversible competitive antagonist commonly causes which effect on an agonist curve?",["Rightward shift that can often be overcome by more agonist","A guaranteed increase in Emax","Irreversible destruction of all receptors"],0,"A reversible competitive antagonist often shifts the agonist curve rightward without reducing Emax if sufficient agonist can be given.")
        }},
      "Radiology Lab": {
        "icon":"🩻","subtitle":"Imaging interpretation framework: verify modality, orientation, anatomy and image quality before interpretation.",
        "experiments":{
          "Chest X-ray sequence":("Which is a sensible first step when reviewing a chest radiograph?",["Confirm patient, projection, orientation and image quality","Immediately name a diagnosis without checking the image","Ignore rotation and inspiration"],0,"A systematic review starts with identity/context, projection, rotation, inspiration, exposure and then proceeds through structures."),
          "CT density":("On a typical non-contrast CT, which structure is usually higher attenuation?",["Cortical bone","Air in the lung","Fat"],0,"Cortical bone is usually high attenuation, air is very low attenuation, and fat is lower attenuation than soft tissue. Windowing matters."),
          "Ultrasound principle":("Most diagnostic ultrasound images are formed from:",["Reflected sound waves at tissue interfaces","Ionising radiation absorption","Magnetic resonance signals"],0,"Ultrasound forms images from returning echoes; operator technique and acoustic windows strongly affect image quality.")
        }},
      "ECG Lab": {
        "icon":"💓","subtitle":"Learn a systematic ECG approach. Educational examples only; not for real-time diagnosis or emergency triage.",
        "experiments":{
          "ECG intervals":("The PR interval represents conduction from:",["Atrial depolarisation onset to ventricular depolarisation onset","Start to end of ventricular repolarisation","Only ventricular depolarisation"],0,"The PR interval extends from the beginning of the P wave to the beginning of the QRS complex, reflecting atrial-to-ventricular conduction."),
          "Rate estimation":("For a regular rhythm on standard 25 mm/s ECG paper, the 300 rule estimates rate using:",["300 divided by the number of large squares between R waves","Large squares multiplied by 10","PR interval divided by QT"],0,"For a regular rhythm, rate ≈ 300 divided by large squares between successive R waves; confirm with the full tracing."),
          "ST elevation":("ST elevation in contiguous leads may indicate:",["Acute myocardial injury among other causes; urgent clinical context matters","A diagnosis that can be made from one isolated lead in every case","Always normal repolarisation"],0,"ST elevation requires assessment of lead distribution, symptoms, reciprocal changes, mimics and urgent clinical context. Never use this teaching tool to assess a real emergency.")
        }},
      "Simulation Center": {
        "icon":"🧬","subtitle":"A fictional case simulator for structured reasoning. Never enter real patient identifiers or use this for clinical decisions.",
        "experiments":{
          "Fever and tachycardia":("Which additional information is most useful to assess severity?",["Mental status, blood pressure, respiratory status, perfusion and clinical context","Only the patient's favourite food","A single temperature value without context"],0,"Severity assessment uses the whole clinical picture, including haemodynamics, breathing, mental status, perfusion, history and relevant investigations."),
          "Dyspnoea framework":("Which first-pass approach is most appropriate for a fictional acute dyspnoea case?",["Assess immediate stability and organise airway, breathing, circulation before focused history","Start with a detailed remote family tree","Assume anxiety before checking danger signs"],0,"Clinical teaching prioritises immediate stability and ABC assessment, then focused history, examination and investigations. Real acute symptoms require professional assessment."),
          "Evidence and uncertainty":("When findings do not fit one diagnosis, the safest reasoning habit is to:",["Reassess data quality, keep a differential, and seek appropriate supervision","Force every finding into the first hypothesis","Ignore contradictory evidence"],0,"Good reasoning tests hypotheses against all findings, acknowledges uncertainty and seeks supervision when needed.")
        }}
    }
    cfg = lab_configs[page]
    st.title(f"{cfg['icon']} {page}")
    st.caption(cfg["subtitle"])
    topic = st.selectbox("Choose a virtual practical", list(cfg["experiments"].keys()), key=f"lab_topic_{page}")
    if page == "Physiology Lab":
        label, minimum, maximum, default, explanation = cfg["experiments"][topic]
        options, correct_index = [], 0
    else:
        label, options, correct_index, explanation = cfg["experiments"][topic]
    st.markdown('<div class="panel"><div class="eyebrow">VIRTUAL PRACTICAL</div><h3>'+topic+'</h3><p class="muted">Read the prompt, choose your answer, submit it, then review the mechanism.</p></div>',unsafe_allow_html=True)
    if page == "Physiology Lab":
        st.markdown("### Experiment controls")
        value_label, minimum, maximum, default, mechanism = cfg["experiments"][topic]
        value = st.slider(value_label, minimum, maximum, default, key=f"phys_slider_{topic}")
        if topic == "Cardiovascular response to exercise":
            response = max(40, min(210, round(55 + 0.85 * value)))
            st.metric("Illustrative response estimate", f"{response} beats/min", help="Toy relationship for learning only; not a physiological prediction for an individual.")
            st.caption("Model: a deliberately simplified trend illustrating that heart rate usually rises with workload.")
        elif topic == "Ventilation and carbon dioxide":
            co2 = round(40 * 5 / value, 1)
            st.metric("Illustrative PaCO₂ trend", f"{co2} mmHg", help="Simplified inverse relationship assuming constant CO₂ production and idealised steady state.")
            st.caption("Teaching relationship only: PaCO₂ is approximately proportional to CO₂ production divided by alveolar ventilation.")
        else:
            st.metric("Selected concentration factor", f"{value}×")
            st.caption("The slider is a conceptual control, not a prediction of a person's urine osmolality.")
        st.info(mechanism)
    elif page == "Histology Lab":
        st.markdown("### Microscopy concept card")
        st.markdown(f"**What to look for:** {explanation}")
        st.caption("This version uses text-based virtual microscopy prompts; licensed high-resolution slide collections can be integrated in a later content pass.")
    elif page == "Radiology Lab":
        st.markdown("### Image-reading checklist")
        st.write("1. Confirm modality, patient/context and orientation.  2. Assess image quality.  3. Review anatomy systematically.  4. Describe findings before forming an impression.  5. State limitations and uncertainty.")
        st.warning("This lab currently teaches interpretation workflow and modality principles; it does not contain a validated radiology image library.")
    elif page == "ECG Lab":
        st.markdown("### ECG systematic approach")
        st.write("Rate → rhythm → axis → intervals (PR, QRS, QT) → P waves → QRS morphology → ST segments/T waves → comparison with prior ECG and clinical context.")
        st.warning("Do not use educational examples to interpret symptoms or delay emergency care.")
    elif page == "Microbiology Lab":
        st.markdown("### Bench workflow")
        st.write("Clinical question → appropriate specimen → correct collection and transport → microscopy/stain → culture or validated assay → organism identification → susceptibility interpretation → clinical correlation.")
    elif page == "Pharmacology Lab":
        st.markdown("### Model assumptions")
        st.write("All examples are simplified. Real dosing depends on indication, age, organ function, interactions, formulation, pregnancy status and local guidance. Do not use this module to select or change a patient's medication.")
    else:
        st.markdown("### Practical interpretation")
        st.write("Use the mechanism, pattern, limitations and clinical context together. Avoid interpreting any isolated result as a diagnosis.")
    st.markdown("### Knowledge check")
    response = st.radio(label, options, key=f"lab_answer_{page}_{topic}")
    if st.button("Submit practical", type="primary", key=f"lab_submit_{page}_{topic}"):
        ok = options.index(response) == correct_index
        st.session_state[f"lab_result_{page}_{topic}"] = {"ok":ok,"answer":response}
        record_answer({"id":f"{page}:{topic}","subject":page},ok,response)
    result = st.session_state.get(f"lab_result_{page}_{topic}")
    if result:
        if result["ok"]:
            st.success("Correct — good reasoning.")
        else:
            st.error(f"Not quite. Best answer: {options[correct_index]}")
        st.write(explanation)
        st.caption("Educational simulation only. Content should be checked against current textbooks, laboratory standards and qualified faculty.")
    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Ask teacher to explain", key=f"lab_teacher_{page}", use_container_width=True):
            st.session_state.tutor_prefill = f"Teach me {topic} from {page} at {st.session_state.profile_level}, with mechanisms, clinical relevance and exam traps."
            st.session_state.navigation = "Teacher AI"
            st.rerun()
    with c2:
        if st.button("Open exam arena", key=f"lab_exam_{page}", use_container_width=True):
            st.session_state.navigation = "Exam Arena"
            st.rerun()
    with c3:
        if st.button("View progress", key=f"lab_progress_{page}", use_container_width=True):
            st.session_state.navigation = "Progress & Goals"
            st.rerun()

elif page == "Visual Lab":
    st.title("🩻 Visual lab")
    st.markdown("Study a diagram first, then answer the question. These are schematic teaching illustrations, not diagnostic images.")
    if not VISUAL_QUESTIONS:
        st.info("Visual questions are being prepared.")
    else:
        if "visual_order" not in st.session_state or len(st.session_state.visual_order) != len(VISUAL_QUESTIONS):
            st.session_state.visual_order = list(range(len(VISUAL_QUESTIONS)))
        order = st.session_state.visual_order
        index = st.session_state.visual_index % len(order)
        item = VISUAL_QUESTIONS[order[index]]
        st.progress((index+1)/len(order))
        st.caption(f"IMAGE CHALLENGE {index+1} / {len(order)}  ·  {item['subject']}  ·  {item.get('level','MBBS')}")
        a,b = st.columns([1.05,1])
        with a:
            show_image(item["image"])
            st.caption(item.get("image_caption","Schematic illustration for learning."))
        with b:
            st.markdown(f"### {item['question']}")
            response = st.radio("Choose the best answer", item["options"], key=f"visual_{item['id']}")
            if item["id"] not in st.session_state.get("visual_answered", []):
                if st.button("Check interpretation", type="primary", key=f"visual_check_{item['id']}"):
                    st.session_state.setdefault("visual_feedback", {})[item["id"]] = {"choice":response,"correct":response==item["answer"]}
                    if "visual_answered" not in st.session_state:
                        st.session_state.visual_answered=[]
                    st.session_state.visual_answered.append(item["id"])
                    record_answer(item,response==item["answer"],response)
                    st.rerun()
            feedback = st.session_state.get("visual_feedback",{}).get(item["id"])
            if feedback:
                if feedback["correct"]:
                    st.success("Correct interpretation.")
                else:
                    st.error("Not quite. Best answer: "+item["answer"])
                st.write(item["explanation"])
                st.markdown("**Clinical / exam pearl**")
                st.info(item.get("pearl","Connect the structure with its function and clinical relevance."))
            if st.button("Bookmark image question", key=f"visual_save_{item['id']}"):
                if item["id"] not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(item["id"])
                st.toast("Saved")
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("← Previous image", use_container_width=True):
                st.session_state.visual_index=(index-1)%len(order); st.rerun()
        with c2:
            if st.button("Shuffle images", use_container_width=True):
                random.shuffle(st.session_state.visual_order); st.session_state.visual_index=0; st.rerun()
        with c3:
            if st.button("Next image →", type="primary", use_container_width=True):
                st.session_state.visual_index=(index+1)%len(order); st.rerun()

elif page == "Clinical Cases":
    st.title("🩺 Clinical reasoning cases")
    st.caption("Use a structured approach: identify the problem → explain the physiology/pathology → select the next best reasoning step.")
    cases = [
        {"title":"Case 01 · Microcytic anaemia","level":"MBBS / clinical","stem":"A 22-year-old student reports fatigue. Hb is low, MCV is 68 fL, ferritin is reduced, and total iron-binding capacity is increased. There is no acute bleeding.","question":"Which mechanism best explains the laboratory pattern?","options":["Impaired haem synthesis due to iron depletion","Failure of intrinsic-factor secretion","Accelerated globin-chain synthesis","Reduced erythropoietin due to renal failure"],"answer":"Impaired haem synthesis due to iron depletion","explanation":"Low ferritin indicates depleted iron stores. Iron deficiency limits haem synthesis, producing microcytosis and hypochromia; TIBC is often increased. Clinical evaluation should identify the cause, including blood loss or inadequate intake/absorption.","pearl":"Interpret MCV together with ferritin and the clinical context; no single result replaces evaluation of the underlying cause."},
        {"title":"Case 02 · Acute coronary syndrome","level":"MBBS / postgraduate revision","stem":"A patient presents with central chest pressure and diaphoresis. ECG shows new ST-segment elevation in contiguous leads. The patient is haemodynamically stable while the team initiates urgent assessment.","question":"Which process is most directly responsible for myocardial injury during sustained coronary occlusion?","options":["Prolonged oxygen supply–demand mismatch causing ATP depletion and cell injury","Increased mitochondrial ATP production","Selective activation of collagen synthesis only","Isolated reduction in plasma albumin"],"answer":"Prolonged oxygen supply–demand mismatch causing ATP depletion and cell injury","explanation":"Sustained ischaemia impairs oxidative phosphorylation, depletes ATP, disrupts ion homeostasis, and can lead to irreversible myocyte injury. This is an educational case: real suspected ACS requires emergency services and time-critical guideline-based care.","pearl":"Separate the mechanism of injury from the emergency management pathway; do not use a study app to triage a real patient."},
        {"title":"Case 03 · Nephrotic syndrome","level":"Pathophysiology","stem":"A patient has generalised oedema, heavy proteinuria, and reduced serum albumin. Renal biopsy findings are being correlated with the clinical picture.","question":"Which change contributes directly to oedema in this presentation?","options":["Reduced plasma oncotic pressure from albumin loss","Increased plasma oncotic pressure","Reduced capillary hydrostatic pressure in all tissues","Increased lymphatic drainage beyond capacity"],"answer":"Reduced plasma oncotic pressure from albumin loss","explanation":"Urinary albumin loss lowers plasma colloid oncotic pressure and favours movement of fluid into interstitial spaces. Renal sodium retention can also contribute; oedema mechanisms are often multifactorial.","pearl":"Use Starling forces, sodium balance, and the underlying renal lesion together rather than memorising a single cause."},
        {"title":"Case 04 · Antibiotic-associated diarrhoea","level":"Microbiology / pharmacology","stem":"An adult develops watery diarrhoea after a course of broad-spectrum antibiotics. There is abdominal discomfort and concern for toxin-mediated colitis.","question":"Which organism should be considered in the differential diagnosis?","options":["Clostridioides difficile","Mycobacterium leprae","Neisseria meningitidis","Treponema pallidum"],"answer":"Clostridioides difficile","explanation":"Antibiotic exposure can disrupt colonisation resistance and permit C. difficile toxin-mediated disease. Diagnosis depends on appropriate stool testing and clinical context; not every post-antibiotic diarrhoea is C. difficile.","pearl":"Understand pre-test probability and testing algorithms; a positive molecular test may require interpretation alongside symptoms."}
    ]
    selected = st.selectbox("Choose a case", [c["title"] for c in cases])
    case = next(c for c in cases if c["title"]==selected)
    st.markdown(f'<div class="panel"><span class="pill">{case["level"]}</span><h3>Clinical vignette</h3><p>{case["stem"]}</p></div>',unsafe_allow_html=True)
    st.markdown("### Your reasoning")
    choice = st.radio(case["question"],case["options"],key="case_"+selected)
    reveal_key = "reveal_"+selected
    if st.button("Submit reasoning",type="primary"):
        st.session_state[reveal_key]=choice
        record_answer({"id":selected,"subject":"Clinical reasoning"},choice==case["answer"],choice)
    if reveal_key in st.session_state:
        if st.session_state[reveal_key]==case["answer"]:
            st.success("Best answer.")
        else:
            st.error("Best answer: "+case["answer"])
        st.write(case["explanation"])
        st.info("Exam pearl: "+case["pearl"])
        st.markdown("**Stretch question:** What additional finding would strengthen or weaken your leading explanation?")
        st.text_area("Write a one-sentence rationale (optional)",key="rationale_"+selected,placeholder="I chose this because…")

elif page == "OSCE Studio":
    st.title("👩‍⚕️ OSCE studio")
    st.caption("Practise a structured approach. These are educational checklists, not a substitute for supervised clinical skills training.")
    station = st.selectbox("Choose a station",["Focused history: chest discomfort","Respiratory examination: verbalised sequence","Communication: explaining a new investigation"])
    stations = {
      "Focused history: chest discomfort":{"time":"6 minutes","aim":"Explore symptoms, associated features, risk factors, and red flags in a systematic, patient-centred way.","steps":[("Introduction","Hand hygiene, introduce yourself, confirm identity, obtain consent."),("Presenting symptom","Clarify onset, site, character, radiation, associated symptoms, timing, exacerbating/relieving factors, and severity."),("Associated symptoms","Ask about dyspnoea, sweating, nausea, palpitations, syncope, fever, and relevant associated features."),("Relevant background","Ask about cardiovascular risk factors, past history, medications, allergies, family history, and social history."),("Red flags and summary","Identify instability or emergency warning signs, summarise back to the patient, ask what they are most concerned about, and explain next steps.")],"pitfall":"Do not assume all chest pain is cardiac or use a study checklist to triage a real person. Acute severe chest pain or associated collapse/breathlessness needs emergency assessment."},
      "Respiratory examination: verbalised sequence":{"time":"7 minutes","aim":"Describe a safe, systematic respiratory examination and connect signs to physiology.","steps":[("Preparation","Hand hygiene, introduce yourself, confirm identity, explain, gain consent, position appropriately, and expose only as needed."),("General inspection","Assess work of breathing, ability to speak, respiratory rate, oxygen delivery, cyanosis, and relevant devices."),("Hands and face","Look for peripheral signs and assess the trachea and relevant head/neck findings when appropriate."),("Chest examination","Inspect chest shape and movement; palpate expansion and tracheal position; percuss systematically; auscultate comparable zones."),("Completion","Thank the patient, ensure comfort and privacy, state further examinations or investigations you would consider, and summarise findings.")],"pitfall":"A real examination requires consent, supervision when learning, appropriate infection control, and escalation for clinical instability."},
      "Communication: explaining a new investigation":{"time":"5 minutes","aim":"Explain purpose, practical steps, likely benefits, limitations, and patient questions in plain language.","steps":[("Establish understanding","Ask what the patient has already been told and what they would like to know."),("Explain clearly","Use plain language to describe why the test is being offered and what will happen."),("Benefits and limitations","Discuss likely benefits, discomforts or risks, alternatives, and uncertainty without promising a result."),("Check understanding","Use teach-back: ask the patient to explain in their own words what they understand."),("Shared decision and close","Invite questions, check preferences and consent, and explain how and when results will be communicated.")],"pitfall":"Do not pressure a patient or present uncertain findings as a guaranteed diagnosis."}
    }
    st.markdown(f'<div class="panel"><span class="pill">{stations[station]["time"]}</span><h3>Station objective</h3><p>{stations[station]["aim"]}</p></div>',unsafe_allow_html=True)
    st.markdown("### Candidate checklist")
    checked=[]
    for i,(title,desc) in enumerate(stations[station]["steps"]):
        if st.checkbox(f"{i+1}. {title} — {desc}",key=f"osce_{station}_{i}"):
            checked.append(title)
    score=round(100*len(checked)/len(stations[station]["steps"]))
    st.progress(score/100)
    st.metric("Self-check completion",f"{score}%")
    st.info("Safety / communication pearl: "+stations[station]["pitfall"])
    reflection=st.text_area("Examiner reflection",placeholder="What did I do well? What would I improve on the next attempt?",key="osce_reflection_"+station)
    if st.button("Save reflection for this session",key="osce_save_"+station):
        st.session_state.setdefault("osce_reflections",{})[station]={"score":score,"reflection":reflection}
        st.toast("Reflection saved for this session")
    with st.expander("View previous reflections"):
        st.write(st.session_state.get("osce_reflections",{}))

elif page == "Research & EBM":
    st.title("📊 Research methods & evidence-based medicine")
    st.caption("A starter workspace for clinical research literacy. Results are teaching calculations, not a substitute for statistical review.")
    tab1,tab2,tab3,tab4=st.tabs(["PICO builder","Study design","Diagnostic tests","Critical appraisal"])
    with tab1:
        st.markdown("### Turn a clinical uncertainty into a searchable question")
        population=st.text_input("P · Population / problem",placeholder="Adults with newly diagnosed hypertension")
        intervention=st.text_input("I · Intervention / exposure",placeholder="Home blood-pressure monitoring")
        comparison=st.text_input("C · Comparison",placeholder="Usual clinic follow-up")
        outcome=st.text_input("O · Outcome",placeholder="Change in systolic blood pressure at 6 months")
        if st.button("Build PICO question",type="primary"):
            st.session_state["pico_question"]=f"In {population or '[population]'}, does {intervention or '[intervention/exposure]'} compared with {comparison or '[comparison]'} improve or change {outcome or '[outcome]'}?"
        if st.session_state.get("pico_question"):
            st.success(st.session_state["pico_question"])
            st.caption("Next: define eligibility criteria, select databases, and plan search terms before choosing a study design.")
    with tab2:
        st.markdown("### Match the question to a design")
        kind=st.selectbox("What are you trying to learn?",["Effect of an intervention","Association between exposure and outcome","Prevalence of a condition","Diagnostic accuracy","Rare adverse effect","Patient experience or meaning"])
        design={
          "Effect of an intervention":("Randomised controlled trial, when ethical and feasible","Random allocation helps balance confounding; assess allocation concealment, blinding where possible, attrition, and intention-to-treat analysis."),
          "Association between exposure and outcome":("Cohort or case-control study","Choose cohort for incidence and temporal follow-up; case-control can be efficient for rare outcomes. Address confounding and selection bias."),
          "Prevalence of a condition":("Cross-sectional study with representative sampling","Sampling frame, non-response, case definition, and confidence intervals are central."),
          "Diagnostic accuracy":("Prospective or well-designed diagnostic accuracy study","Compare index test with an appropriate reference standard; consider spectrum, verification, and incorporation bias."),
          "Rare adverse effect":("Often case-control, registry, or pharmacovigilance approaches","Randomised trials may be underpowered for rare harms; assess confounding, reporting bias, and denominator quality."),
          "Patient experience or meaning":("Qualitative interviews, focus groups, or ethnographic approaches","Assess sampling rationale, reflexivity, analytic transparency, and whether interpretations are grounded in data.")
        }[kind]
        st.markdown(f'<div class="panel"><h3>Possible design: {design[0]}</h3><p>{design[1]}</p></div>',unsafe_allow_html=True)
        st.caption("No single design is automatically best; feasibility, ethics, causal aims, and available data matter.")
    with tab3:
        st.markdown("### Diagnostic-test calculator")
        st.caption("Enter counts from a 2×2 table. Use integer counts from a defined reference standard.")
        c1,c2=st.columns(2)
        with c1:
            tp=st.number_input("True positives (TP)",min_value=0,value=80,step=1)
            fn=st.number_input("False negatives (FN)",min_value=0,value=20,step=1)
        with c2:
            fp=st.number_input("False positives (FP)",min_value=0,value=15,step=1)
            tn=st.number_input("True negatives (TN)",min_value=0,value=85,step=1)
        sensitivity=100*tp/(tp+fn) if tp+fn else None
        specificity=100*tn/(tn+fp) if tn+fp else None
        ppv=100*tp/(tp+fp) if tp+fp else None
        npv=100*tn/(tn+fn) if tn+fn else None
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Sensitivity",f"{sensitivity:.1f}%" if sensitivity is not None else "N/A")
        m2.metric("Specificity",f"{specificity:.1f}%" if specificity is not None else "N/A")
        m3.metric("PPV",f"{ppv:.1f}%" if ppv is not None else "N/A")
        m4.metric("NPV",f"{npv:.1f}%" if npv is not None else "N/A")
        st.info("Positive and negative predictive values depend on prevalence in the tested population. These calculations do not validate the test or its reference standard.")
    with tab4:
        st.markdown("### Critical-appraisal checklist")
        prompts=["Is the research question focused and clinically relevant?","Was the design appropriate to the question?","Were participants selected in a way that limits selection bias?","Were exposure, intervention, and outcomes measured reliably?","Were important confounders addressed?","Are effect estimates reported with confidence intervals?","Are benefits, harms, and absolute effects considered?","Do the findings apply to the population I care for?","Are funding and conflicts of interest disclosed?"]
        checked=[st.checkbox(p,key="ebm_"+p) for p in prompts]
        st.progress(sum(checked)/len(prompts))
        st.caption(f"{sum(checked)} of {len(prompts)} appraisal prompts considered.")
        st.text_area("Paper notes",placeholder="Study design, sample, primary outcome, effect estimate, key bias, applicability…",key="ebm_notes")
    st.markdown("---")
    st.markdown("**Research integrity:** do not invent data, fabricate citations, upload identifiable patient records, or treat statistical association as proof of causation. Verify methods and conclusions against the original paper.")

elif page == "Teacher AI":
    st.title("👩‍🏫 Your personal medical teacher")
    st.caption("Choose your level and learning style. Ask for a concept lesson, Socratic hints, exam questions, or feedback on your reasoning.")
    with st.expander("Personalise your tutor",expanded=not bool(st.session_state.tutor_messages)):
        a,b=st.columns(2)
        with a:
            st.session_state.profile_level=st.selectbox("Study level",["Foundation","MBBS — Core concepts","MBBS — Exam depth","Clinical integration","Postgraduate / research"],index=["Foundation","MBBS — Core concepts","MBBS — Exam depth","Clinical integration","Postgraduate / research"].index(st.session_state.profile_level) if st.session_state.profile_level in ["Foundation","MBBS — Core concepts","MBBS — Exam depth","Clinical integration","Postgraduate / research"] else 1)
            st.session_state.profile_goal=st.selectbox("Main goal",["Exam preparation","Understand mechanisms","Clinical reasoning","Research / deeper reading"])
        with b:
            st.session_state.profile_style=st.selectbox("Teaching style",["Explain simply, then go deeper","Socratic: ask me questions","High-yield exam revision","Case-based teaching"])
            tutor_subject=st.selectbox("Focus subject",SUBJECTS)
    for msg in st.session_state.tutor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt=st.chat_input("Ask your teacher: e.g. Explain B12 absorption step by step")
    if prompt:
        st.session_state.tutor_messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        system_prompt = f"You are MedStudy Teacher, a supportive medical educator. Learner level: {st.session_state.profile_level}. Goal: {st.session_state.profile_goal}. Style: {st.session_state.profile_style}. Focus: {tutor_subject}. Teach accurately with clear headings, mechanisms, clinical correlations, and 2 retrieval questions. Distinguish established facts from uncertainty. Do not diagnose real users or replace medical care. If asked about a real emergency, direct them to emergency services. Keep educational answers appropriate to level."
        api_key = os.environ.get("OPENAI_API_KEY")
        try:
            if not api_key:
                api_key = st.secrets.get("OPENAI_API_KEY", None)
        except Exception:
            api_key = api_key
        answer = None
        if api_key:
            try:
                from openai import OpenAI
                client=OpenAI(api_key=api_key)
                recent=[{"role":m["role"],"content":m["content"]} for m in st.session_state.tutor_messages[-10:]]
                response=client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":system_prompt}]+recent,temperature=0.35)
                answer=response.choices[0].message.content
            except Exception as exc:
                answer=f"The AI service could not respond ({type(exc).__name__}). Check the API key and account access. Meanwhile, use the guided prompts below."
        if not answer:
            topic=prompt.strip().lower()
            known = {
                "b12":("Vitamin B12 absorption — a stepwise map","Dietary B12 is released from food proteins by gastric acid and pepsin, binds haptocorrin, is released by pancreatic proteases in the duodenum, then binds intrinsic factor from parietal cells. The B12–intrinsic-factor complex is absorbed in the terminal ileum. Deficiency can impair DNA synthesis and methylmalonyl-CoA metabolism, producing megaloblastic anaemia and potentially neurological injury.","Why can B12 deficiency cause neurological signs while folate deficiency usually does not?"),
                "inflammation":("Acute inflammation — the sequence","Recognition of injury/infection activates resident cells and mediators. Vasodilation increases blood flow; increased vascular permeability allows protein-rich exudate; leukocytes marginate, roll, adhere, transmigrate, and chemotax. Neutrophils commonly dominate early, with macrophages becoming important later.","How do histamine and leukotrienes differ in their effects on vessels?"),
                "anemia":("Approach to anaemia","Start with haemoglobin and red-cell indices (especially MCV), then reticulocyte response and targeted studies. Microcytosis suggests iron deficiency, thalassaemia, or chronic inflammation; macrocytosis raises B12/folate deficiency, alcohol, liver disease, drugs, and marrow causes. Interpret ferritin in context of inflammation.","What does a high reticulocyte count suggest about marrow response?"),
                "cardiac":("Myocardial ischaemia and injury","Reduced coronary perfusion limits oxygen delivery and oxidative phosphorylation. ATP depletion impairs ion pumps, increases intracellular sodium and calcium, and promotes cellular swelling and injury. Persistent severe ischaemia can progress to irreversible injury; biomarkers and ECG findings must be interpreted in clinical context.","Why is subendocardium particularly vulnerable to ischaemia?")
            }
            hit=next((v for k,v in known.items() if k in topic),None)
            if hit:
                answer=f"## {hit[0]}\n\n{hit[1]}\n\n**Check your understanding:** {hit[2]}\n\n**Personalised next step:** Based on your goal ({st.session_state.profile_goal}), explain the mechanism aloud, then answer the check question without looking."
            else:
                answer=f"## Let's learn this together\n\n**Your level:** {st.session_state.profile_level}  \n**Your goal:** {st.session_state.profile_goal}  \n**Your style:** {st.session_state.profile_style}\n\nI can build a lesson around **{prompt}**. Start by identifying: (1) the key definition, (2) the underlying mechanism, (3) one clinical or laboratory correlation, and (4) a common exam trap.\n\n**Socratic first step:** What do you already know about this topic, and which part is confusing?\n\n*For full open-ended AI responses, add an OPENAI_API_KEY in Streamlit Cloud → App settings → Secrets. The guided tutor works without a key.*"
        st.session_state.tutor_messages.append({"role":"assistant","content":answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
    c1,c2=st.columns(2)
    with c1:
        if st.button("Give me an exam question",use_container_width=True):
            st.session_state.tutor_messages.append({"role":"assistant","content":f"**Retrieval practice ({tutor_subject}):** Without checking notes, explain one core mechanism from {tutor_subject} in 3 steps. Then name one clinical correlation and one common misconception."})
            st.rerun()
    with c2:
        if st.button("Clear teacher conversation",use_container_width=True):
            st.session_state.tutor_messages=[]; st.rerun()
    st.info("Medical education only. AI-generated explanations can be incomplete or wrong; verify high-stakes facts with current textbooks, guidelines, and faculty.")

elif page == "Flashcards":
    st.title("🧠 Active-recall cards")
    subject=st.selectbox("Subject filter",["All subjects"]+SUBJECTS,key="flash_filter")
    cards=ALL_CARDS if subject=="All subjects" else [q for q in ALL_CARDS if q["subject"]==subject]
    if cards:
        index=st.session_state.flashcard_index%len(cards); item=cards[index]
        st.caption(f"CARD {index+1} OF {len(cards)} · {item['subject']}")
        if item.get("image"):
            show_image(item["image"])
        st.markdown(f'<div class="hero"><div class="eyebrow">Recall before reveal</div><h1 style="font-size:1.8rem">{item["question"]}</h1><p>Say the answer aloud before opening the explanation.</p></div>',unsafe_allow_html=True)
        with st.expander("Reveal answer and explanation"):
            st.success(item["answer"]); st.write(item["explanation"])
        x,y,z=st.columns(3)
        with x:
            if st.button("← Previous",use_container_width=True): st.session_state.flashcard_index=(index-1)%len(cards); st.rerun()
        with y:
            if st.button("☆ Bookmark",use_container_width=True):
                if item["id"] not in st.session_state.bookmarks: st.session_state.bookmarks.append(item["id"])
                st.toast("Saved")
        with z:
            if st.button("Next card →",type="primary",use_container_width=True): st.session_state.flashcard_index=(index+1)%len(cards); st.rerun()

elif page == "Bookmarks":
    st.title("⭐ Your revision list")
    saved=[find_question(qid) for qid in st.session_state.bookmarks]
    saved=[q for q in saved if q]
    if not saved: st.info("Your saved list is empty. Save useful questions from the library, visual lab, or flashcards.")
    else:
        st.caption(f"{len(saved)} saved items")
        for item in saved:
            with st.expander(f"{item['subject']} · {item['question']}"):
                if item.get("image"): show_image(item["image"])
                st.success(item["answer"]); st.write(item["explanation"])
                if st.button("Remove from list",key=f"remove_{item['id']}"):
                    st.session_state.bookmarks.remove(item["id"]); st.rerun()

elif page == "Progress & Goals":
    st.title("📈 Progress & study goals")
    a,b,c,d=st.columns(4)
    a.metric("Attempted",attempts); b.metric("Correct",correct_total); c.metric("Accuracy",f"{accuracy}%"); d.metric("Subjects touched",len({x["subject"] for x in st.session_state.answered}))
    st.markdown("### Set your daily practice target")
    st.session_state.daily_goal=st.slider("Questions per study session",5,60,int(st.session_state.daily_goal),5)
    st.progress(min(attempts/max(st.session_state.daily_goal,1),1.0))
    st.caption(f"{min(attempts,st.session_state.daily_goal)} / {st.session_state.daily_goal} questions toward your session target")
    if st.session_state.answered:
        per_subject={}
        for entry in st.session_state.answered:
            stats=per_subject.setdefault(entry["subject"],{"attempted":0,"correct":0})
            stats["attempted"]+=1; stats["correct"]+=int(entry["correct"])
        st.markdown("### Attempts by subject")
        st.bar_chart({key:value["attempted"] for key,value in per_subject.items()})
        st.markdown("### Accuracy by subject (%)")
        st.bar_chart({key:round(100*value["correct"]/value["attempted"]) for key,value in per_subject.items()})
        weakest=sorted(per_subject.items(),key=lambda pair:pair[1]["correct"]/pair[1]["attempted"])[0]
        st.info(f"Suggested focus: {weakest[0]}. Review the explanation for missed questions, then retry using active recall.")
    else:
        st.info("Your charts will appear after you answer questions in the Visual Lab or Clinical Cases.")
    st.caption("Progress is currently session-based; it may reset when your session ends. No patient data should be entered.")
    if st.checkbox("I understand this clears my current session"):
        if st.button("Reset session progress",type="secondary"):
            for key in ["answered","quiz_feedback","quiz_ids","quiz_index","visual_answered","visual_feedback"]:
                st.session_state[key]=[] if key in ["answered","quiz_ids","visual_answered"] else {}
            st.session_state.quiz_index=0; st.rerun()

st.markdown("---")
st.markdown('<p class="muted">MedStudy is an educational learning project, not a clinical decision-support system. Confirm medical content with trusted textbooks, current guidance, and qualified teachers.</p>',unsafe_allow_html=True)
