"""
Olist E-commerce Analytics — Sheshendra
Primary Application Entry Point and Executive Overview Dashboard.
"""

import streamlit as st
import pandas as pd
from utils.config import (
    PROJECT_TITLE, PROJECT_SUBTITLE, AUTHOR_NAME, ORIGINAL_ATTRIBUTION,
    format_currency, format_number, format_percentage,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR
)
from services.data_loader import build_master_dataset
from services.analytics import compute_executive_kpis, get_monthly_sales_trend
from components.metrics import render_kpi_card
from components.charts import plot_monthly_sales_trend
from components.filters import render_sidebar_filters

# Configure Streamlit page layout
st.set_page_config(
    page_title=PROJECT_TITLE,
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished portfolio look
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 24px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: #312E81;
        color: #C7D2FE;
        margin-right: 8px;
    }
    .badge-author {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: #064E3B;
        color: #A7F3D0;
    }
    .insight-card {
        background: #1E293B;
        border-radius: 8px;
        padding: 16px;
        border-left: 3px solid #4F46E5;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header Banner
    st.markdown(f'<div class="main-header">🛒 {PROJECT_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div>
        <span class="badge-pill">Brazilian E-Commerce Dataset</span>
        <span class="badge-pill">98K+ Orders Analyzed</span>
        <span class="badge-author">Project Lead: {AUTHOR_NAME}</span>
    </div>
    <div class="sub-header">{PROJECT_SUBTITLE}</div>
    """, unsafe_allow_html=True)

    # Load master data
    with st.spinner("Loading analytical data..."):
        df_master = build_master_dataset()

    if df_master.empty:
        st.error("⚠️ Master dataset could not be loaded. Please ensure data files exist in the `data/` directory or run `python scripts/download_data.py`.")
        st.stop()

    # Apply Sidebar Filters
    df_filtered = render_sidebar_filters(df_master)

    # Compute Executive KPIs
    kpis = compute_executive_kpis(df_filtered)

    st.markdown("### 📊 Executive Overview & Key Business Metrics")
    
    # Primary KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(
            label="Total Gross Revenue",
            value=format_currency(kpis.get("total_sales", 0)),
            subtext=f"Items: {format_currency(kpis.get('total_items_price', 0))}",
            delta="+ Items & Freight",
            color=PRIMARY_COLOR
        )
    with col2:
        render_kpi_card(
            label="Total Orders Placed",
            value=format_number(kpis.get("total_orders", 0)),
            subtext=f"Delivered: {format_percentage(kpis.get('delivered_pct', 0))}",
            color=SECONDARY_COLOR
        )
    with col3:
        render_kpi_card(
            label="Average Order Value (AOV)",
            value=format_currency(kpis.get("aov", 0)),
            subtext="Revenue per order",
            color=ACCENT_COLOR
        )
    with col4:
        render_kpi_card(
            label="Unique Customers",
            value=format_number(kpis.get("total_customers", 0)),
            subtext=f"Sellers: {format_number(kpis.get('total_sellers', 0))}",
            color=WARNING_COLOR
        )

    # Secondary KPI Row (Logistics & Customer Experience)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            label="On-Time Delivery Rate",
            value=format_percentage(kpis.get("ontime_pct", 0)),
            subtext="Delivered before deadline",
            color=ACCENT_COLOR if kpis.get("ontime_pct", 0) > 90 else WARNING_COLOR
        )
    with c2:
        render_kpi_card(
            label="Avg Delivery Time",
            value=f"{kpis.get('avg_delivery_days', 0):.1f} Days",
            subtext="Order purchase to customer door",
            color=SECONDARY_COLOR
        )
    with c3:
        render_kpi_card(
            label="Total Freight Charges",
            value=format_currency(kpis.get("total_freight", 0)),
            subtext=f"{kpis.get('total_freight', 0)/max(kpis.get('total_sales', 1), 1)*100:.1f}% of total sales",
            color=WARNING_COLOR
        )
    with c4:
        render_kpi_card(
            label="Customer Rating Score",
            value=f"{kpis.get('avg_review_score', 0):.2f} / 5.0 ⭐",
            subtext="Average review satisfaction",
            color=PRIMARY_COLOR
        )

    st.markdown("---")

    # Interactive Monthly Sales Trend Chart
    st.markdown("### 📈 Monthly Revenue & Order Velocity")
    monthly_sales = get_monthly_sales_trend(df_filtered)
    if not monthly_sales.empty:
        fig_monthly = plot_monthly_sales_trend(monthly_sales)
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("No sales data available for the selected filters.")

    # Strategic Business Insights Section
    st.markdown("### 💡 Strategic Business Takeaways")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown("""
        <div class="insight-card">
            <h4 style="color: #818CF8; margin: 0 0 6px 0;">🚀 Consistent Revenue Scaling</h4>
            <p style="font-size: 0.9rem; color: #CBD5E1; margin: 0;">
                Platform revenue scaled aggressively from <b>R$ 136K</b> in January 2017 to over <b>R$ 890K</b> in May 2018 (over 6x growth), propelled by category diversification and customer acquisition.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with i2:
        st.markdown("""
        <div class="insight-card">
            <h4 style="color: #34D399; margin: 0 0 6px 0;">📦 High On-Time Fulfillment</h4>
            <p style="font-size: 0.9rem; color: #CBD5E1; margin: 0;">
                Over <b>92% of delivered shipments</b> arrived on or before the estimated delivery promise date, keeping customer satisfaction healthy with an average rating of <b>4.08 / 5.0</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with i3:
        st.markdown("""
        <div class="insight-card">
            <h4 style="color: #FBBF24; margin: 0 0 6px 0;">⚠️ Single-Order Churn Exposure</h4>
            <p style="font-size: 0.9rem; color: #CBD5E1; margin: 0;">
                Approximately <b>96.9% of customers</b> made only a single purchase during this period. Implementing automated retention workflows and loyalty incentives represents the single biggest revenue expansion lever.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Footer Attribution
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
        f"<b>{PROJECT_TITLE}</b> · Lead Analyst: <b>{AUTHOR_NAME}</b><br>"
        f"{ORIGINAL_ATTRIBUTION}</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
