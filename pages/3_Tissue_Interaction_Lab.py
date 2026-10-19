"""Layered tissue interaction lab for MedStudy.

Educational browser prototype only; not a validated surgical simulator.
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(
    page_title="MedStudy · Tissue Interaction Lab",
    page_icon="🩺",
    layout="wide",
)
st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(circle at 12% 0%, #123143 0, transparent 32%), #07111b; }
    .block-container { max-width: 1600px; padding-top: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="background:linear-gradient(120deg,#071827,#15384b 60%,#087f8c);
    border:1px solid #2b6271;border-radius:22px;padding:22px;color:#effcff;margin-bottom:14px">
    <div style="font-size:11px;letter-spacing:2px;color:#89e8df;font-weight:800">
    MEDSTUDY · TISSUE INTERACTION</div>
    <h1 style="color:white;margin:.45rem 0">Layered Tissue Interaction Lab</h1>
    <p style="color:#ccebed;margin:0">An interactive 3D training surface with selectable modes,
    visible tissue layers, simulated incision traces, probe-contact markers, and visual closure stitches.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.warning(
    "Important limitation: this is a browser-based educational prototype, not a realistic or "
    "validated surgical simulator. Tissue appearance and interactions are approximations. It "
    "does not provide validated anatomical geometry, physical tissue deformation, cutting "
    "mechanics, bleeding, haptics, or clinical skill assessment. It must not be used to train "
    "or perform real procedures without qualified supervision."
)
sim_path = ROOT / "components" / "realistic_tissue_interaction_lab.html"
if sim_path.exists():
    components.html(sim_path.read_text(encoding="utf-8"), height=790, scrolling=True)
else:
    st.error("The tissue interaction component is missing from the components directory.")
st.caption(
    "Next engineering milestone for higher fidelity: integrate properly licensed anatomical "
    "meshes, then implement and validate a deformable-tissue physics model and instrument collision."
)
