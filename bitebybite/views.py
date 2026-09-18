"""All Streamlit views for the Bite by Bite web prototype."""

from __future__ import annotations

import csv
import io
import json
from datetime import date, datetime, timedelta
from typing import Any

import streamlit as st

from .constants import (
    ALLERGY_OPTIONS,
    AMOUNT_EATEN_OPTIONS,
    APP_NAME,
    APP_SUBTITLE,
    AUTHOR,
    MEAL_NAMES,
    ROLE_DESCRIPTIONS,
)
from .state import go_to, load_demo_account, meal_by_id, sign_out
from .ui import LOGO_PATH, badge, progress_ring, render_app_header, render_centered_brand, render_footer


def _rerun_to(page: str) -> None:
    go_to(page)
    st.rerun()


def _valid_email(value: str) -> bool:
    value = value.strip()
    return "@" in value and "." in value.rsplit("@", 1)[-1]


def render_auth() -> None:
    """Sign-in and sign-up flow."""
    render_centered_brand()
    mode = st.session_state.auth_mode
    left_space, content_col, right_space = st.columns([0.7, 1.6, 0.7])
    del left_space, right_space

    with content_col:
        if mode == "Sign in":
            with st.container(border=True):
                st.markdown("## Sign In")
                st.caption("Access your child's meal tracking dashboard.")
                with st.form("sign_in_form", clear_on_submit=False):
                    email = st.text_input("Email", placeholder="Enter your email")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    submitted = st.form_submit_button("Sign in", type="primary", width="stretch")

                if submitted:
                    if not _valid_email(email):
                        st.error("Enter a valid email address.")
                    elif len(password) < 4:
                        st.error("Enter a password with at least four characters.")
                    else:
                        st.session_state.account["email"] = email.strip()
                        st.session_state.authenticated = True
                        st.session_state.profile_created = True
                        st.session_state.demo_mode = False
                        st.session_state.current_page = "Home"
                        st.rerun()

                st.markdown("<div class='bbb-divider'></div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Create account", width="stretch"):
                        st.session_state.auth_mode = "Create account"
                        st.rerun()
                with col2:
                    if st.button("Use demo account", width="stretch", type="primary"):
                        load_demo_account()
                        st.rerun()

            st.info(
                "This repository is a front-end prototype. The demo sign-in does not connect to a production identity provider."
            )

        else:
            with st.container(border=True):
                if st.button("← Back to sign in", key="back_to_sign_in"):
                    st.session_state.auth_mode = "Sign in"
                    st.rerun()

                st.markdown("## Create Your Account")
                with st.form("create_account_form", clear_on_submit=False):
                    first_col, last_col = st.columns(2)
                    with first_col:
                        first_name = st.text_input("First name", placeholder="First name")
                    with last_col:
                        last_name = st.text_input("Last name", placeholder="Last name")
                    email = st.text_input("Email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password", placeholder="Create a password")
                    confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter your password")
                    submitted = st.form_submit_button("Continue", type="primary", width="stretch")

                if submitted:
                    errors: list[str] = []
                    if not first_name.strip() or not last_name.strip():
                        errors.append("Enter both first and last name.")
                    if not _valid_email(email):
                        errors.append("Enter a valid email address.")
                    if len(password) < 6:
                        errors.append("Use a password with at least six characters.")
                    if password != confirm:
                        errors.append("The passwords do not match.")

                    if errors:
                        for message in errors:
                            st.error(message)
                    else:
                        st.session_state.account = {
                            "first_name": first_name.strip(),
                            "last_name": last_name.strip(),
                            "email": email.strip(),
                        }
                        st.session_state.authenticated = True
                        st.session_state.profile_created = False
                        st.session_state.demo_mode = False
                        st.rerun()

    render_footer()


def render_child_onboarding() -> None:
    """Collect the child's profile after account creation."""
    render_app_header()
    st.markdown("# Set up your child's profile")
    st.caption("Tell us about your child so meal tracking can be personalized.")

    with st.form("child_profile_setup"):
        first_col, last_col = st.columns(2)
        with first_col:
            first_name = st.text_input("Child's first name", placeholder="First name")
        with last_col:
            last_name = st.text_input("Child's last name", placeholder="Last name")
        date_of_birth = st.date_input(
            "Date of birth",
            value=st.session_state.onboarding_date,
            min_value=date(2005, 1, 1),
            max_value=date.today(),
        )
        dietary_information = st.text_area(
            "Dietary information",
            placeholder="Food preferences, dietary restrictions, textures, or routines",
        )
        allergies = st.multiselect("Allergies", ALLERGY_OPTIONS)
        submitted = st.form_submit_button("Create profile", type="primary", width="stretch")

    if submitted:
        if not first_name.strip() or not last_name.strip():
            st.error("Enter the child's first and last name.")
        else:
            st.session_state.child = {
                "first_name": first_name.strip(),
                "last_name": last_name.strip(),
                "date_of_birth": date_of_birth.isoformat(),
                "dietary_information": dietary_information.strip() or "No dietary information entered.",
                "allergies": allergies,
            }
            st.session_state.profile_created = True
            st.session_state.current_page = "Home"
            st.success("Profile created successfully.")
            st.rerun()

    render_footer()


def render_sidebar() -> None:
    """App navigation, account context, and author credit."""
    with st.sidebar:
        st.image(str(LOGO_PATH), width=78)
        st.markdown(f"### {APP_NAME}")
        st.caption(APP_SUBTITLE)
        st.markdown("<div class='bbb-divider'></div>", unsafe_allow_html=True)

        child = st.session_state.child
        st.markdown(
            f"**Child:** {child['first_name']} {child['last_name']}  \n"
            f"**Account:** {st.session_state.account['first_name']} {st.session_state.account['last_name']}"
        )

        st.markdown('<div class="bbb-nav-label">Navigation</div>', unsafe_allow_html=True)
        nav_items = [
            ("Home", "Home"),
            ("Meal Progress", "Meal Progress"),
            ("Care Team", "Care Team"),
            ("More", "More"),
        ]
        for label, page in nav_items:
            button_type = "primary" if st.session_state.current_page == page else "secondary"
            if st.button(label, key=f"nav_{page}", width="stretch", type=button_type):
                _rerun_to(page)

        st.markdown("<div class='bbb-divider'></div>", unsafe_allow_html=True)
        st.markdown(f"**Author**  \n{AUTHOR}")
        st.caption("Streamlit + Android dual-platform repository")
        if st.button("Sign out", width="stretch"):
            sign_out()
            st.rerun()


def render_home() -> None:
    """Dashboard matching the core mobile mockup."""
    render_app_header()
    account = st.session_state.account
    child = st.session_state.child
    meals = st.session_state.meals
    logged = sum(1 for meal in meals if meal["logged"])
    total = len(meals)
    pending = sum(1 for item in st.session_state.substitutions if item["status"] == "Pending")

    st.markdown(f"# Good morning, {account['first_name']}")
    st.caption(f"Here is {child['first_name']}'s meal activity for today.")

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Meals logged", f"{logged} / {total}")
    metric2.metric("Pending substitutions", pending)
    protein = next(item for item in st.session_state.nutrients if item["name"] == "Protein")
    metric3.metric("Weekly protein", f"{protein['actual']} {protein['unit']}", f"Target {protein['target']} {protein['unit']}")

    main_col, side_col = st.columns([1.55, 1], gap="large")
    with main_col:
        st.markdown("## Today's meals")
        for meal in meals:
            with st.container(border=True):
                title_col, status_col = st.columns([3.3, 1.2], vertical_alignment="center")
                with title_col:
                    symbol = "✓" if meal["logged"] else "○"
                    st.markdown(f"### {symbol} {meal['name']}")
                    if meal["logged"]:
                        st.caption(f"Logged at {meal['logged_at']} · {meal['food']}")
                    else:
                        st.caption(f"Scheduled {meal['scheduled']}")
                with status_col:
                    if meal["logged"]:
                        st.markdown(badge("Logged", "success"), unsafe_allow_html=True)
                    elif st.button("+ Log", key=f"home_log_{meal['id']}", width="stretch"):
                        st.session_state.selected_meal_id = meal["id"]
                        _rerun_to("Log a Meal")

        if st.button("+ Log a meal", type="primary", width="stretch"):
            st.session_state.selected_meal_id = next(
                (meal["id"] for meal in meals if not meal["logged"]), meals[0]["id"]
            )
            _rerun_to("Log a Meal")

    with side_col:
        st.markdown("## Daily completion")
        with st.container(border=True):
            progress_ring(logged, total)
            st.caption(f"{max(total - logged, 0)} meal(s) remain for today's log.")
            st.progress(logged / max(total, 1))

        st.markdown("## Substitutions")
        with st.container(border=True):
            if pending:
                item = next(item for item in st.session_state.substitutions if item["status"] == "Pending")
                st.markdown(badge(f"{pending} pending", "warning"), unsafe_allow_html=True)
                st.markdown(f"**{item['original']} → {item['replacement']}**")
                st.caption(f"Requested by {item['requested_by']}")
                if st.button("Review request", width="stretch"):
                    _rerun_to("More")
            else:
                st.success("No substitutions need review.")

        st.markdown("## Weekly overview")
        with st.container(border=True):
            for item in st.session_state.nutrients[:3]:
                variant = "success" if item["status"] == "On track" else "warning"
                st.markdown(
                    f"**{item['name']}** &nbsp; {badge(item['status'], variant)}",
                    unsafe_allow_html=True,
                )
            if st.button("View weekly summary", width="stretch"):
                _rerun_to("Meal Progress")

    render_footer()


def render_log_meal() -> None:
    """Record a meal and update the dashboard immediately."""
    render_app_header()
    if st.button("← Back to dashboard"):
        _rerun_to("Home")

    st.markdown("# Log a Meal")
    st.caption(
        f"Record what was served and what was actually eaten for {st.session_state.child['first_name']}."
    )

    meal_ids = [meal["id"] for meal in st.session_state.meals]
    meal_labels = {meal["id"]: meal["name"] for meal in st.session_state.meals}
    selected_id = st.session_state.selected_meal_id
    selected_index = meal_ids.index(selected_id) if selected_id in meal_ids else 0
    current = meal_by_id(meal_ids[selected_index])

    with st.form("log_meal_form"):
        selected_meal_id = st.selectbox(
            "Meal",
            options=meal_ids,
            index=selected_index,
            format_func=lambda value: meal_labels[value],
        )
        food = st.text_input(
            "Food",
            value=current["food"] if current else "",
            placeholder="e.g., rice, grilled chicken, cucumber",
        )
        served_amount = st.text_input("Amount served", placeholder="e.g., 1 cup")
        amount_eaten = st.radio("Amount eaten", AMOUNT_EATEN_OPTIONS, horizontal=True)
        notes = st.text_area(
            "Meal notes",
            value=current["notes"] if current else "",
            placeholder="Optional observation",
        )
        submitted = st.form_submit_button("Save meal", type="primary", width="stretch")

    if submitted:
        meal = meal_by_id(selected_meal_id)
        if meal is None:
            st.error("The selected meal could not be found.")
        elif not food.strip():
            st.error("Enter at least one food item.")
        else:
            meal["logged"] = True
            meal["logged_at"] = datetime.now().strftime("%I:%M %p").lstrip("0")
            meal["food"] = food.strip() + (f" · Served: {served_amount.strip()}" if served_amount.strip() else "")
            meal["amount_eaten"] = amount_eaten
            meal["notes"] = notes.strip()
            st.session_state.selected_meal_id = selected_meal_id
            st.success(f"{meal['name']} has been recorded.")
            st.balloons()
            if st.button("Back to dashboard", type="primary", width="stretch"):
                _rerun_to("Home")

    render_footer()


def _weekly_report_csv() -> bytes:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Nutrient", "Actual", "Target", "Unit", "Status"])
    for item in st.session_state.nutrients:
        writer.writerow([item["name"], item["actual"], item["target"], item["unit"], item["status"]])
    return buffer.getvalue().encode("utf-8")


def render_meal_progress() -> None:
    """Daily meal completion and weekly nutrient summary."""
    render_app_header()
    st.markdown("# Meal Progress")
    today_tab, weekly_tab = st.tabs(["Today's Meals", "Weekly Nutrition"])

    with today_tab:
        meals = st.session_state.meals
        logged = sum(1 for meal in meals if meal["logged"])
        ring_col, text_col = st.columns([1, 2], vertical_alignment="center")
        with ring_col:
            progress_ring(logged, len(meals))
        with text_col:
            st.markdown(f"### {date.today().strftime('%A, %B %d')}")
            st.write(
                f"{logged} of {len(meals)} planned meals are logged. "
                "Open any meal below to review details or complete the log."
            )
            st.progress(logged / max(len(meals), 1))

        for meal in meals:
            status = "Logged" if meal["logged"] else f"Scheduled {meal['scheduled']}"
            with st.expander(f"{'✓' if meal['logged'] else '○'} {meal['name']} — {status}"):
                if meal["logged"]:
                    st.write(f"**Food:** {meal['food']}")
                    st.write(f"**Amount eaten:** {meal['amount_eaten'] or 'Not specified'}")
                    if meal["notes"]:
                        st.write(f"**Notes:** {meal['notes']}")
                else:
                    st.caption("This meal has not been logged yet.")
                if st.button("Open meal form", key=f"progress_open_{meal['id']}"):
                    st.session_state.selected_meal_id = meal["id"]
                    _rerun_to("Log a Meal")

    with weekly_tab:
        week_end = date.today()
        week_start = week_end - timedelta(days=6)
        st.caption(f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}")

        for item in st.session_state.nutrients:
            with st.container(border=True):
                left, right = st.columns([3.5, 1.2], vertical_alignment="center")
                with left:
                    st.markdown(f"**{item['name']}**")
                    st.caption(
                        f"{item['actual']} {item['unit']} of {item['target']} {item['unit']} weekly target"
                    )
                    st.progress(min(item["actual"] / max(item["target"], 1), 1.0))
                with right:
                    variant = "success" if item["status"] == "On track" else "warning"
                    st.markdown(badge(item["status"], variant), unsafe_allow_html=True)

        st.success(
            "Weekly suggestion: add an iron-rich food such as lentils, beans, tofu, fortified cereal, or spinach, "
            "and pair plant-based iron with vitamin C."
        )
        st.download_button(
            "Download weekly nutrition CSV",
            data=_weekly_report_csv(),
            file_name="bite_by_bite_weekly_nutrition.csv",
            mime="text/csv",
            width="stretch",
        )

    render_footer()


def render_care_team() -> None:
    """Manage caregivers and professional connections."""
    render_app_header()
    child = st.session_state.child
    st.markdown("# Care Team")
    st.caption(f"Manage who can help care for {child['first_name']}.")

    people_tab, invite_tab, professional_tab = st.tabs(
        ["People with Access", "Invite Caregiver", "School & Healthcare"]
    )

    with people_tab:
        for person in st.session_state.care_team:
            with st.container(border=True):
                avatar_col, info_col, action_col = st.columns([0.65, 3.5, 1.25], vertical_alignment="center")
                with avatar_col:
                    st.markdown(f'<div class="bbb-avatar">{person["initials"]}</div>', unsafe_allow_html=True)
                with info_col:
                    st.markdown(f"**{person['name']}**")
                    st.caption(person["role"])
                with action_col:
                    variant = "success" if person["access"] == "Owner" else "info"
                    st.markdown(badge(person["access"], variant), unsafe_allow_html=True)
                    if person["access"] != "Owner" and st.button(
                        "Remove", key=f"remove_{person['id']}", width="stretch"
                    ):
                        st.session_state.care_team = [
                            item for item in st.session_state.care_team if item["id"] != person["id"]
                        ]
                        st.rerun()

    with invite_tab:
        st.markdown("### Invite a Caregiver")
        st.caption("Invite someone you trust to help record your child's meals.")
        with st.form("invite_caregiver_form"):
            email = st.text_input("Their email", placeholder="caregiver@example.com")
            permissions = st.multiselect(
                "Access",
                ["Log meals", "Record amount eaten", "Add meal notes", "View nutrition summary"],
                default=["Log meals", "Record amount eaten", "Add meal notes"],
            )
            submitted = st.form_submit_button("Send invitation", type="primary", width="stretch")
        if submitted:
            if not _valid_email(email):
                st.error("Enter a valid caregiver email address.")
            elif not permissions:
                st.error("Select at least one permission.")
            else:
                st.success(f"Invitation prepared for {email.strip()} with {len(permissions)} permission(s).")
                st.caption("Email delivery is simulated in this prototype.")

    with professional_tab:
        nurse_col, pediatrician_col = st.columns(2)
        with nurse_col:
            with st.container(border=True):
                st.markdown("### Connect a School Nurse")
                st.caption("The nurse must already have a verified Bite by Bite professional account.")
                with st.form("connect_nurse"):
                    nurse_email = st.text_input("School nurse's email", key="nurse_email")
                    nurse_submit = st.form_submit_button("Send connection request", width="stretch")
                if nurse_submit:
                    if _valid_email(nurse_email):
                        st.success("School nurse connection request created.")
                    else:
                        st.error("Enter a valid school nurse email address.")
        with pediatrician_col:
            with st.container(border=True):
                st.markdown("### Connect a Pediatrician")
                st.caption("Only authorized clinicians should receive detailed nutrition access.")
                with st.form("connect_pediatrician"):
                    pediatrician_email = st.text_input("Pediatrician's email", key="pediatrician_email")
                    pediatrician_submit = st.form_submit_button(
                        "Send connection request", width="stretch"
                    )
                if pediatrician_submit:
                    if _valid_email(pediatrician_email):
                        st.success("Pediatrician connection request created.")
                    else:
                        st.error("Enter a valid pediatrician email address.")

    render_footer()


def _render_profile_tab() -> None:
    child = st.session_state.child
    st.markdown("### Child Profile")
    with st.form("edit_child_profile"):
        first_col, last_col = st.columns(2)
        with first_col:
            first_name = st.text_input("First name", value=child["first_name"])
        with last_col:
            last_name = st.text_input("Last name", value=child["last_name"])
        try:
            dob_value = date.fromisoformat(child["date_of_birth"])
        except (TypeError, ValueError):
            dob_value = date(2020, 1, 1)
        dob = st.date_input("Date of birth", value=dob_value, max_value=date.today())
        dietary = st.text_area("Dietary information", value=child["dietary_information"])
        allergies = st.multiselect("Allergies", ALLERGY_OPTIONS, default=child["allergies"])
        submitted = st.form_submit_button("Save profile", type="primary", width="stretch")
    if submitted:
        if not first_name.strip() or not last_name.strip():
            st.error("First and last name are required.")
        else:
            child.update(
                {
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "date_of_birth": dob.isoformat(),
                    "dietary_information": dietary.strip(),
                    "allergies": allergies,
                }
            )
            st.success("Child profile updated.")


def _render_substitutions_tab() -> None:
    st.markdown("### Substitutions & Approvals")
    st.caption("Review substitution requests and submit new requests.")

    pending_items = [item for item in st.session_state.substitutions if item["status"] == "Pending"]
    if pending_items:
        st.markdown("#### Pending approval")
        for item in pending_items:
            with st.container(border=True):
                st.markdown(badge("Pending", "warning"), unsafe_allow_html=True)
                st.markdown(f"**{item['original']} → {item['replacement']}**")
                st.caption(f"Requested by {item['requested_by']} · {item['reason']}")
                approve_col, decline_col = st.columns(2)
                if approve_col.button("Approve", key=f"approve_{item['id']}", type="primary", width="stretch"):
                    item["status"] = "Approved"
                    st.rerun()
                if decline_col.button("Decline", key=f"decline_{item['id']}", width="stretch"):
                    item["status"] = "Declined"
                    st.rerun()
    else:
        st.success("No requests are waiting for approval.")

    st.markdown("#### New substitution request")
    with st.form("new_substitution_form"):
        meal = st.selectbox("Meal", MEAL_NAMES)
        original = st.text_input("Food being replaced", placeholder="e.g., cheese sandwich")
        replacement = st.text_input("Requested replacement", placeholder="e.g., chicken wrap")
        reason = st.text_area("Reason for the request")
        recipient = st.selectbox("Send approval request to", ["Parent / Guardian", "Pediatrician", "School nurse"])
        submitted = st.form_submit_button("Request approval", type="primary", width="stretch")
    if submitted:
        if not original.strip() or not replacement.strip():
            st.error("Enter both the original and replacement food.")
        else:
            next_id = max((item["id"] for item in st.session_state.substitutions), default=0) + 1
            st.session_state.substitutions.append(
                {
                    "id": next_id,
                    "original": original.strip(),
                    "replacement": replacement.strip(),
                    "requested_by": st.session_state.account["first_name"],
                    "reason": f"{meal}: {reason.strip() or 'No reason supplied.'} Recipient: {recipient}.",
                    "status": "Pending",
                }
            )
            st.success("Substitution request added.")
            st.rerun()

    history = [item for item in st.session_state.substitutions if item["status"] != "Pending"]
    if history:
        st.markdown("#### Recent requests")
        for item in history:
            variant = "success" if item["status"] == "Approved" else "danger"
            st.markdown(
                f"- **{item['original']} → {item['replacement']}** — {badge(item['status'], variant)}",
                unsafe_allow_html=True,
            )


def _render_privacy_tab() -> None:
    st.markdown("### Privacy & Permissions")
    st.caption("Who can access what in Bite by Bite.")
    for role, description in ROLE_DESCRIPTIONS:
        with st.container(border=True):
            st.markdown(f"**{role}**")
            st.write(description)
    st.warning(
        "This prototype stores information only in the active Streamlit session. A production system would need "
        "secure authentication, encrypted storage, audit logs, consent controls, and appropriate legal review."
    )


def _render_about_tab() -> None:
    st.markdown(f"### About {APP_NAME}")
    st.write(
        "Bite by Bite is a pediatric meal tracking concept designed to help parents, caregivers, school staff, "
        "and clinicians coordinate meal records and nutrition observations."
    )
    with st.container(border=True):
        st.markdown(f"**Author:** {AUTHOR}")
        st.markdown("**Platforms:** Streamlit web prototype and Android/Kotlin prototype")
        st.markdown("**License:** MIT")
        st.markdown("**Repository entry point for Streamlit Cloud:** `app.py`")
    export_payload: dict[str, Any] = {
        "account": st.session_state.account,
        "child": st.session_state.child,
        "meals": st.session_state.meals,
        "nutrients": st.session_state.nutrients,
        "care_team": st.session_state.care_team,
        "substitutions": st.session_state.substitutions,
    }
    st.download_button(
        "Download demo session as JSON",
        data=json.dumps(export_payload, indent=2),
        file_name="bite_by_bite_demo_session.json",
        mime="application/json",
        width="stretch",
    )


def render_more() -> None:
    """Profile, substitutions, permissions, and about page."""
    render_app_header()
    st.markdown("# More")
    profile_tab, substitution_tab, privacy_tab, about_tab = st.tabs(
        ["Child Profile", "Substitutions & Approvals", "Privacy & Permissions", "About"]
    )
    with profile_tab:
        _render_profile_tab()
    with substitution_tab:
        _render_substitutions_tab()
    with privacy_tab:
        _render_privacy_tab()
    with about_tab:
        _render_about_tab()
    render_footer()


def render_main_app() -> None:
    """Route the authenticated user to the selected view."""
    render_sidebar()
    page = st.session_state.current_page
    if page == "Home":
        render_home()
    elif page == "Meal Progress":
        render_meal_progress()
    elif page == "Care Team":
        render_care_team()
    elif page == "More":
        render_more()
    elif page == "Log a Meal":
        render_log_meal()
    else:
        st.session_state.current_page = "Home"
        render_home()
