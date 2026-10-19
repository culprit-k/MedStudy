"""Advanced interactive 3D surgical simulation learning page for MedStudy.

Educational prototype only; not a clinical simulator or surgical guide.
"""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="MedStudy · Advanced Surgical Lab", page_icon="🩺", layout="wide")
st.markdown("""
<style>
.stApp {background: radial-gradient(circle at 12% 0%, #123143 0, transparent 32%), #07111b;}
.block-container {max-width: 1500px; padding-top: 1.4rem;}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="background:linear-gradient(120deg,#071827,#15384b 60%,#087f8c);border:1px solid #2b6271;border-radius:22px;padding:22px;color:#effcff;margin-bottom:14px">
<div style="font-size:11px;letter-spacing:2px;color:#89e8df;font-weight:800">MEDSTUDY · ADVANCED SIMULATION</div>
<h1 style="color:white;margin:.45rem 0">Advanced 3D Surgical Simulation Lab</h1>
<p style="color:#ccebed;margin:0">Explore a 3D operative field, select schematic anatomy, practise camera orientation and target acquisition, and progress through structured safety checkpoints.</p>
</div>
""", unsafe_allow_html=True)
st.warning("EDUCATIONAL PROTOTYPE ONLY. This is not a validated surgical simulator. It does not model realistic tissue mechanics, cutting, suturing, bleeding, haptics or patient-specific anatomy, and cannot establish surgical competence.")
sim_path = ROOT / "components" / "advanced_surgical_lab.html"
if sim_path.exists():
    components.html(sim_path.read_text(encoding="utf-8"), height=1040, scrolling=True)
else:
    st.error("The simulation component file is missing. Check the repository's components folder.")
st.caption("Use alongside faculty-supervised simulation, current anatomy references, and approved institutional teaching.")
