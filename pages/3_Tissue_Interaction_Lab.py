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
    "validated surgical simulator. The surface now uses an illustrative damped mass-spring "
    "approximation, not validated human-tissue biomechanics. It does not provide anatomically "
    "validated structures, cutting or tearing mechanics, bleeding, haptics, or clinical skill "
    "assessment. It must not be used to train or perform real procedures without qualified supervision."
)
sim_tab, anatomy_tab, roadmap_tab = st.tabs(
    ["Tissue interaction", "Anatomy reference", "Physics roadmap"]
)

with sim_tab:
    sim_path = ROOT / "components" / "realistic_tissue_interaction_lab.html"
    if sim_path.exists():
        components.html(sim_path.read_text(encoding="utf-8"), height=790, scrolling=True)
    else:
        st.error("The tissue interaction component is missing from the components directory.")

with anatomy_tab:
    st.subheader("Real 3D anatomy reference")
    st.markdown(
        "Use this linked atlas to inspect anatomical structures and spatial relationships. "
        "It is a reference viewer, not a surgically deformable model, and its assets are not "
        "automatically imported into the tissue simulator."
    )
    st.link_button("Open anatomy atlas in a new tab", "https://nqwrc.github.io/3d-anatomy/")
    st.caption(
        "The atlas documents BodyParts3D and Z-Anatomy sources. Its distributed asset set "
        "includes non-commercial components; review the upstream licence and notices before "
        "redistributing models or using them commercially."
    )
    components.iframe("https://nqwrc.github.io/3d-anatomy/", height=760, scrolling=True)

with roadmap_tab:
    st.subheader("Implementation status and remaining work")
    st.markdown(
        """
        **Implemented in this prototype**
        - External CC0 static body-surface mesh loaded on demand, with a dedicated framed body view.
        - A 55 × 39 node surface grid using a damped mass-spring approximation.
        - Adjustable spring stiffness, damping, and neighbour coupling.
        - Raycast-based surface contact, animated recovery, visible incision traces, visual stitches,
          layer toggles, counters, and reset behavior.
        - An embedded anatomy-atlas reference and a GitHub Actions smoke-test workflow.

        **Still required for a high-fidelity simulator**
        1. Import legally compatible, separately identifiable structures for one focused surgical region.
        2. Build collision meshes and align them to the body reference with documented units and landmarks.
        3. Replace the spring membrane with a validated volumetric model, such as a finite-element model,
           for tissue volumes where appropriate.
        4. Implement true geometry separation/cutting, tearing, suture purchase/tension, and tool-tissue
           collision response rather than the current visual traces.
        5. Add instrument haptics only with suitable hardware and calibration.
        6. Validate geometry, numerical stability, interaction behavior, and learning outcomes with
           qualified anatomy and surgical-simulation reviewers before making realism claims.
        """
    )
    st.markdown(
        "A research-grade candidate for future volumetric physics is "
        "[SOFA](https://github.com/sofa-framework/sofa), an open-source framework focused on "
        "interactive physics and medical simulation. SOFA is not integrated into this browser prototype; "
        "using it would require a separate native or service layer plus a tested communication interface."
    )
st.caption(
    "External body mesh source: UMRAM-Bilkent/supine-human-model, CC0 1.0. "
    "This is a static external body-surface reference, not internal anatomy and not a deformable surgical model. "
    "The mesh loads on demand from GitHub; internet access is required."
)
st.caption(
    "Current state: interactive prototype with an optional static body-surface mesh and an adjustable spring-membrane demo. "
    "No finite-element tissue physics, true cutting mechanics, calibrated tissue parameters, or clinical validation yet."
)
