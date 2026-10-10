"""
Delivery & Logistics Analytics Page for Olist E-commerce Analytics — Sheshendra.
Analyzes carrier delivery durations, estimated vs actual delivery dates, late rates,
and their direct correlation with customer review ratings.
"""

import streamlit as st
import pandas as pd
from utils.config import (
    PROJECT_TITLE, format_currency, format_number, format_percentage,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR, DANGER_COLOR
)
from services.data_loader import build_master_dataset
from services.analytics import compute_delivery_analytics
from components.metrics import render_kpi_card
from components.charts import plot_delivery_delay_distribution, plot_delivery_vs_review
from components.filters import render_sidebar_filters

st.set_page_config(page_title=f"Delivery Analytics — {PROJECT_TITLE}", page_icon="🚚", layout="wide")

def main():
    st.title("🚚 Delivery & Logistics Performance")
    st.markdown("Fulfillment speed, on-time delivery rates, regional shipping delays, and satisfaction impact.")

    with st.spinner("Analyzing fulfillment and logistics data..."):
        df_master = build_master_dataset()

    if df_master.empty:
        st.error("No data available.")
        st.stop()

    df_filtered = render_sidebar_filters(df_master)

    delivery_metrics = compute_delivery_analytics(df_filtered)
    if not delivery_metrics:
        st.info("No delivery records available for the chosen filters.")
        st.stop()

    # 1. Headline Logistics KPIs
    avg_actual = delivery_metrics["avg_actual_days"]
    avg_estimated = delivery_metrics["avg_estimated_days"]
    ontime_pct = delivery_metrics["ontime_pct"]
    late_pct = delivery_metrics["late_pct"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Avg Actual Delivery", f"{avg_actual:.1f} Days", "Door-to-door duration", color=PRIMARY_COLOR)
    with col2:
        render_kpi_card("Avg Estimated Promise", f"{avg_estimated:.1f} Days", "Target commitment date", color=SECONDARY_COLOR)
    with col3:
        render_kpi_card("On-Time Delivery Rate", format_percentage(ontime_pct), "Arrived before deadline", color=ACCENT_COLOR if ontime_pct >= 90 else WARNING_COLOR)
    with col4:
        render_kpi_card("Late Delivery Rate", format_percentage(late_pct), f"Avg late: {delivery_metrics['avg_delay_when_late']:.1f}d", color=DANGER_COLOR if late_pct > 8 else WARNING_COLOR)

    st.markdown("---")

    # 2. Charts: Punctuality vs Review Rating & Delay Distribution
    c1, c2 = st.columns(2)
    with c1:
        fig_score = plot_delivery_vs_review(delivery_metrics["score_by_status"])
        st.plotly_chart(fig_score, use_container_width=True)
    with c2:
        fig_dist = plot_delivery_delay_distribution(df_filtered)
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")

    # 3. State Delivery Comparison
    st.markdown("### 🗺️ State Fulfillment Speed & Delay Ranking")
    state_df = delivery_metrics["state_delivery"]
    if not state_df.empty:
        st.dataframe(
            state_df.style.format({
                'avg_delivery_days': "{:.1f} days",
                'avg_estimated_days': "{:.1f} days",
                'late_pct': "{:.1f}%",
                'total_delivered': "{:,}"
            }),
            use_container_width=True
        )
        st.info("💡 **Logistics Insight:** Remote northern and northeastern states (e.g. AP, RR, AM, PA) experience significantly longer transit times (>20 days) and higher late rates compared to southeastern states (SP, RJ, MG: 8-12 days).")

if __name__ == "__main__":
    main()
