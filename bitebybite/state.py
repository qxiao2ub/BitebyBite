"""Session-state helpers for the Streamlit prototype."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any

import streamlit as st

from .constants import (
    DEFAULT_ACCOUNT,
    DEFAULT_CARE_TEAM,
    DEFAULT_CHILD,
    DEFAULT_MEALS,
    DEFAULT_NUTRIENTS,
    DEFAULT_SUBSTITUTIONS,
)


def initialize_state() -> None:
    """Populate all state used by the app without overwriting user changes."""
    defaults: dict[str, Any] = {
        "authenticated": False,
        "auth_mode": "Sign in",
        "profile_created": True,
        "current_page": "Home",
        "account": deepcopy(DEFAULT_ACCOUNT),
        "child": deepcopy(DEFAULT_CHILD),
        "meals": deepcopy(DEFAULT_MEALS),
        "nutrients": deepcopy(DEFAULT_NUTRIENTS),
        "care_team": deepcopy(DEFAULT_CARE_TEAM),
        "substitutions": deepcopy(DEFAULT_SUBSTITUTIONS),
        "selected_meal_id": "lunch",
        "onboarding_date": date(2020, 3, 15),
        "demo_mode": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_demo_account() -> None:
    """Reset the session to the pre-populated demonstration account."""
    st.session_state.account = deepcopy(DEFAULT_ACCOUNT)
    st.session_state.child = deepcopy(DEFAULT_CHILD)
    st.session_state.meals = deepcopy(DEFAULT_MEALS)
    st.session_state.nutrients = deepcopy(DEFAULT_NUTRIENTS)
    st.session_state.care_team = deepcopy(DEFAULT_CARE_TEAM)
    st.session_state.substitutions = deepcopy(DEFAULT_SUBSTITUTIONS)
    st.session_state.authenticated = True
    st.session_state.profile_created = True
    st.session_state.current_page = "Home"
    st.session_state.selected_meal_id = "lunch"
    st.session_state.demo_mode = True


def sign_out() -> None:
    """Return to the sign-in screen while retaining no sensitive form fields."""
    st.session_state.authenticated = False
    st.session_state.auth_mode = "Sign in"
    st.session_state.current_page = "Home"


def go_to(page: str) -> None:
    """Navigate to a main view."""
    st.session_state.current_page = page


def meal_by_id(meal_id: str) -> dict[str, Any] | None:
    """Return a mutable meal record from session state."""
    for meal in st.session_state.meals:
        if meal["id"] == meal_id:
            return meal
    return None
