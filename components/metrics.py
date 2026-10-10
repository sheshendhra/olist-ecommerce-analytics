"""
Reusable KPI metric card components with professional visual styling.
"""

import streamlit as st
from utils.config import PRIMARY_COLOR, ACCENT_COLOR, WARNING_COLOR, DANGER_COLOR

def render_kpi_card(label: str, value: str, subtext: str = "", delta: str = None, color: str = PRIMARY_COLOR):
    """Renders a modern, responsive KPI card."""
    card_html = f"""
    <div style="
        background: #1E293B;
        border-radius: 10px;
        padding: 18px 20px;
        border-left: 4px solid {color};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 12px;
    ">
        <div style="font-size: 0.82rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">
            {label}
        </div>
        <div style="font-size: 1.85rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;">
            {value}
        </div>
        <div style="font-size: 0.85rem; color: #CBD5E1; display: flex; align-items: center; gap: 6px;">
            {f'<span style="color: {ACCENT_COLOR if "+" in str(delta) else DANGER_COLOR}; font-weight: 600;">{delta}</span>' if delta else ''}
            <span>{subtext}</span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
