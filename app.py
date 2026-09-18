"""Streamlit Cloud entry point for Bite by Bite.

Author: Sidra Almoghrabi
"""

from __future__ import annotations

import streamlit as st

from bitebybite.constants import APP_NAME
from bitebybite.state import initialize_state
from bitebybite.ui import LOGO_PATH, inject_css
from bitebybite.views import render_auth, render_child_onboarding, render_main_app

st.set_page_config(
    page_title=f"{APP_NAME} | Pediatric Meal Tracker",
    page_icon=str(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Bite by Bite — Pediatric Meal Tracker. Author: Sidra Almoghrabi.",
    },
)

initialize_state()
inject_css()

if not st.session_state.authenticated:
    render_auth()
elif not st.session_state.profile_created:
    render_child_onboarding()
else:
    render_main_app()
