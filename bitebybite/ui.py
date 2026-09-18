"""Reusable visual components and styling for Bite by Bite."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from .constants import APP_NAME, APP_SUBTITLE, AUTHOR

ROOT_DIR = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT_DIR / "assets" / "bitebybite_light_logo.png"


def inject_css() -> None:
    """Apply a responsive visual system inspired by the original mobile mockups."""
    st.markdown(
        """
        <style>
        :root {
            --bbb-green: #1E3F2D;
            --bbb-green-2: #2D6045;
            --bbb-cream: #F9F8F4;
            --bbb-card: #FFFFFF;
            --bbb-border: #E7E2D7;
            --bbb-muted: #6B6B6B;
            --bbb-soft-green: #E5EEDC;
            --bbb-mint: #CFE6BE;
            --bbb-orange: #D97706;
            --bbb-red: #B91C1C;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
        }

        .stApp {
            background: var(--bbb-cream);
            color: #172019;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #EEF3E8;
            border-right: 1px solid #DCE5D4;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.25rem;
        }

        div[data-testid="stForm"],
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.96);
            border-color: var(--bbb-border) !important;
            border-radius: 18px;
            box-shadow: 0 7px 22px rgba(30, 63, 45, 0.05);
        }

        .stButton > button,
        .stDownloadButton > button,
        button[kind="primary"] {
            border-radius: 999px !important;
            font-weight: 700 !important;
            min-height: 2.65rem;
        }

        button[kind="primary"] {
            background: var(--bbb-green) !important;
            border-color: var(--bbb-green) !important;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stDateInput input,
        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        .bbb-brand-title {
            margin: 0;
            color: var(--bbb-green);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.05;
        }

        .bbb-subtitle {
            color: var(--bbb-muted);
            font-weight: 700;
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .bbb-kicker {
            color: var(--bbb-green-2);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .bbb-muted {
            color: var(--bbb-muted);
        }

        .bbb-card {
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid var(--bbb-border);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 7px 22px rgba(30, 63, 45, 0.05);
            margin-bottom: 0.75rem;
        }

        .bbb-card h3, .bbb-card h4, .bbb-card p {
            margin-top: 0;
        }

        .bbb-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.22rem 0.58rem;
            font-size: 0.74rem;
            font-weight: 800;
            line-height: 1.2;
            white-space: nowrap;
        }

        .bbb-badge.success { background: #DDF3D8; color: #1F6B37; }
        .bbb-badge.warning { background: #FFF0C7; color: #9A5A00; }
        .bbb-badge.danger  { background: #FDE2E2; color: #9B1C1C; }
        .bbb-badge.info    { background: #E2ECFA; color: #265B96; }
        .bbb-badge.neutral { background: #ECECE8; color: #53534F; }

        .bbb-avatar {
            width: 42px;
            height: 42px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: var(--bbb-soft-green);
            color: var(--bbb-green);
            font-weight: 800;
            border: 1px solid #CBDABF;
        }

        .bbb-progress-ring {
            --progress: 144deg;
            width: 118px;
            height: 118px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            background: conic-gradient(var(--bbb-green) var(--progress), #E8E7DE 0deg);
            margin: 0.3rem auto 0.8rem auto;
        }

        .bbb-progress-ring::before {
            content: "";
            width: 88px;
            height: 88px;
            border-radius: 50%;
            background: white;
            position: absolute;
        }

        .bbb-progress-ring-inner {
            z-index: 1;
            text-align: center;
            color: var(--bbb-green);
            font-weight: 800;
            line-height: 1.05;
        }

        .bbb-progress-ring-inner strong {
            display: block;
            font-size: 1.55rem;
        }

        .bbb-progress-ring-inner span {
            font-size: 0.67rem;
            color: var(--bbb-muted);
            letter-spacing: 0.06em;
        }

        .bbb-footer {
            text-align: center;
            color: var(--bbb-muted);
            font-size: 0.78rem;
            padding-top: 2.2rem;
        }

        .bbb-nav-label {
            color: var(--bbb-green);
            font-weight: 800;
            font-size: 0.84rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin: 0.75rem 0 0.45rem 0;
        }

        .bbb-divider {
            height: 1px;
            background: #E6E2D8;
            margin: 0.75rem 0;
        }

        @media (max-width: 720px) {
            .block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
            .bbb-card {
                padding: 0.9rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_centered_brand() -> None:
    """Render the landing-page brand treatment."""
    left, center, right = st.columns([1, 1.35, 1])
    with center:
        st.image(str(LOGO_PATH), width=125)
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:-0.55rem; margin-bottom:1.25rem;">
            <h1 class="bbb-brand-title" style="font-size:2.25rem;">{APP_NAME}</h1>
            <div class="bbb-subtitle">{APP_SUBTITLE}</div>
            <div style="margin-top:.45rem; color:#54705F; font-size:.82rem;">
                Created by <strong>{AUTHOR}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_app_header() -> None:
    """Render a compact, responsive in-app header."""
    logo_col, title_col, status_col = st.columns([0.55, 5.4, 1.2], vertical_alignment="center")
    with logo_col:
        st.image(str(LOGO_PATH), width=52)
    with title_col:
        st.markdown(
            f"""
            <h2 class="bbb-brand-title" style="font-size:1.42rem;">{APP_NAME}</h2>
            <div class="bbb-subtitle">{APP_SUBTITLE}</div>
            """,
            unsafe_allow_html=True,
        )
    with status_col:
        st.markdown(
            '<div style="text-align:right;"><span class="bbb-badge success">● Session active</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown('<div class="bbb-divider"></div>', unsafe_allow_html=True)


def badge(text: str, variant: str = "neutral") -> str:
    """Return safe badge markup."""
    safe_variant = variant if variant in {"success", "warning", "danger", "info", "neutral"} else "neutral"
    return f'<span class="bbb-badge {safe_variant}">{html.escape(text)}</span>'


def progress_ring(completed: int, total: int) -> None:
    """Render a circular completion indicator."""
    total = max(total, 1)
    completed = min(max(completed, 0), total)
    degrees = round((completed / total) * 360)
    st.markdown(
        f"""
        <div class="bbb-progress-ring" style="--progress:{degrees}deg; position:relative;">
            <div class="bbb-progress-ring-inner">
                <strong>{completed} / {total}</strong>
                <span>LOGGED</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render authorship and prototype disclaimer."""
    st.markdown(
        f"""
        <div class="bbb-footer">
            <strong>{APP_NAME}</strong> &middot; Author: <strong>{AUTHOR}</strong><br>
            Educational prototype only. It does not provide medical diagnosis or replace a clinician.
        </div>
        """,
        unsafe_allow_html=True,
    )
