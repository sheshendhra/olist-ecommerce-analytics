"""
Customer Analytics Page for Olist E-commerce Analytics — Sheshendra.
Analyzes customer retention, repeat orders, RFM segmentation, and Customer Lifetime Value (CLV).
"""

import streamlit as st
import pandas as pd
from utils.config import (
    PROJECT_TITLE, format_currency, format_number, format_percentage,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR, DANGER_COLOR
)
from services.data_loader import build_master_dataset
from services.analytics import compute_rfm_segmentation
from components.metrics import render_kpi_card
from components.charts import plot_rfm_segments
from components.filters import render_sidebar_filters

st.set_page_config(page_title=f"Customer Analytics — {PROJECT_TITLE}", page_icon="👥", layout="wide")

def main():
    st.title("👥 Customer Intelligence & RFM Segmentation")
    st.markdown("Detailed customer behavioral analysis, repeat purchase retention, RFM clustering, and Customer Lifetime Value (CLV).")

    with st.spinner("Computing customer analytics and RFM segmentation..."):
        df_master = build_master_dataset()

    if df_master.empty:
        st.error("No data available.")
        st.stop()

    df_filtered = render_sidebar_filters(df_master)

    # Compute RFM Segmentation
    rfm_df = compute_rfm_segmentation(df_filtered)

    if rfm_df.empty:
        st.info("Insufficient customer data for the selected filters.")
        st.stop()

    # 1. Headline Customer Metrics
    total_customers = len(rfm_df)
    repeat_customers = (rfm_df['frequency'] > 1).sum()
    repeat_rate = (repeat_customers / total_customers * 100.0) if total_customers > 0 else 0.0
    avg_clv = rfm_df['clv_estimate'].mean()
    champions_count = (rfm_df['segment'] == 'Champions').sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Customers", format_number(total_customers), "Unique customer profiles", color=PRIMARY_COLOR)
    with col2:
        render_kpi_card("Repeat Customers", format_number(repeat_customers), f"{repeat_rate:.2f}% Repeat Rate", color=SECONDARY_COLOR)
    with col3:
        render_kpi_card("Average CLV", format_currency(avg_clv), "Lifetime Value Estimate", color=ACCENT_COLOR)
    with col4:
        render_kpi_card("Champion VIPs", format_number(champions_count), "High frequency & spend", color=WARNING_COLOR)

    st.markdown("---")

    # 2. RFM Segment Distribution Treemap
    st.markdown("### 🗺️ RFM Customer Segment Breakdown")
    fig_rfm = plot_rfm_segments(rfm_df)
    st.plotly_chart(fig_rfm, use_container_width=True)

    # 3. RFM Summary Table
    seg_summary = rfm_df.groupby('segment').agg(
        total_customers=('customer_unique_id', 'count'),
        total_revenue=('monetary', 'sum'),
        avg_recency=('recency', 'mean'),
        avg_frequency=('frequency', 'mean'),
        avg_clv=('clv_estimate', 'mean')
    ).reset_index()

    seg_summary['customer_share_pct'] = seg_summary['total_customers'] / total_customers * 100.0
    seg_summary = seg_summary.sort_values('total_revenue', ascending=False).reset_index(drop=True)

    st.markdown("### 📋 Segment Behavioral Profiles & Action Playbooks")
    st.dataframe(
        seg_summary[['segment', 'total_customers', 'customer_share_pct', 'total_revenue', 'avg_recency', 'avg_frequency', 'avg_clv']].style.format({
            'total_customers': "{:,}",
            'customer_share_pct': "{:.1f}%",
            'total_revenue': "R$ {:,.2f}",
            'avg_recency': "{:.0f} days",
            'avg_frequency': "{:.2f}",
            'avg_clv': "R$ {:,.2f}"
        }),
        use_container_width=True
    )

    # Retention Strategy Advice
    st.markdown("### 🎯 Segment Action Recommendations")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.success("""
        **👑 Champions & Loyal**
        - Offer VIP early access to top category products.
        - Free shipping thresholds for orders over R$ 150.
        - Dedicated loyalty rewards program.
        """)
    with s2:
        st.warning("""
        **⚠️ Need Attention & At Risk**
        - Send personalized win-back discounts via email/SMS.
        - Highlight newly arrived products in their favorite category.
        - Solicit feedback on their last order experience.
        """)
    with s3:
        st.error("""
        **🚨 Lost / Inactive Customers**
        - High-discount re-engagement campaigns (e.g. 20% off next purchase).
        - Investigate if delivery delays on their first order caused dissatisfaction.
        """)

if __name__ == "__main__":
    main()
