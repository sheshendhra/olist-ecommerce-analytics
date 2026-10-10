"""
Sales Analytics Page for Olist E-commerce Analytics — Sheshendra.
Analyzes monthly trends, quarterly performance, growth rates, and regional sales.
"""

import streamlit as st
import pandas as pd
from utils.config import (
    PROJECT_TITLE, format_currency, format_number, format_percentage,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR
)
from services.data_loader import build_master_dataset
from services.analytics import get_monthly_sales_trend, get_state_performance, get_category_performance
from components.metrics import render_kpi_card
from components.charts import plot_monthly_sales_trend, plot_state_sales
from components.filters import render_sidebar_filters

st.set_page_config(page_title=f"Sales Analytics — {PROJECT_TITLE}", page_icon="📈", layout="wide")

def main():
    st.title("📈 Sales Analytics & Growth Trends")
    st.markdown("Detailed breakdown of gross revenue, order volume, average order values, and geographic performance over time.")

    with st.spinner("Loading sales data..."):
        df_master = build_master_dataset()

    if df_master.empty:
        st.error("No data available.")
        st.stop()

    df_filtered = render_sidebar_filters(df_master)

    # 1. Headline Sales Metrics
    monthly_df = get_monthly_sales_trend(df_filtered)
    total_revenue = df_filtered['order_item_total'].sum()
    total_orders = df_filtered['order_id'].nunique()
    aov = total_revenue / total_orders if total_orders > 0 else 0.0

    # Best Month calculation
    if not monthly_df.empty:
        best_month_row = monthly_df.loc[monthly_df['revenue'].idxmax()]
        best_month_str = f"{best_month_row['month']} ({format_currency(best_month_row['revenue'])})"
    else:
        best_month_str = "N/A"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Filtered Gross Sales", format_currency(total_revenue), "Items + Freight", color=PRIMARY_COLOR)
    with col2:
        render_kpi_card("Total Orders", format_number(total_orders), "Unique order IDs", color=SECONDARY_COLOR)
    with col3:
        render_kpi_card("Average Order Value (AOV)", format_currency(aov), "Revenue per order", color=ACCENT_COLOR)
    with col4:
        render_kpi_card("Peak Revenue Month", best_month_str, "Highest monthly sales", color=WARNING_COLOR)

    st.markdown("---")

    # 2. Monthly Trend Chart
    st.markdown("### 📊 Revenue & Order Volume Timeline")
    if not monthly_df.empty:
        fig_trend = plot_monthly_sales_trend(monthly_df)
        st.plotly_chart(fig_trend, use_container_width=True)

        with st.expander("🔍 View Monthly Sales Data Table"):
            st.dataframe(
                monthly_df[['month', 'revenue', 'orders', 'aov', 'mom_growth_pct', 'ma_3m']].style.format({
                    'revenue': "R$ {:,.2f}",
                    'orders': "{:,}",
                    'aov': "R$ {:,.2f}",
                    'mom_growth_pct': "{:+.1f}%",
                    'ma_3m': "R$ {:,.2f}"
                }),
                use_container_width=True
            )
    else:
        st.info("No monthly data available for the chosen filters.")

    st.markdown("---")

    # 3. Geographic Sales Analysis
    st.markdown("### 🗺️ State-Level Revenue Distribution")
    state_df = get_state_performance(df_filtered)
    if not state_df.empty:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig_state = plot_state_sales(state_df, top_n=15)
            st.plotly_chart(fig_state, use_container_width=True)
        with c2:
            st.markdown("#### Top States Summary")
            st.dataframe(
                state_df.head(10)[['customer_state', 'revenue', 'orders', 'revenue_share_pct']].style.format({
                    'revenue': "R$ {:,.2f}",
                    'orders': "{:,}",
                    'revenue_share_pct': "{:.2f}%"
                }),
                use_container_width=True
            )
            top_state = state_df.iloc[0]
            st.info(f"💡 **Key Geographic Finding:** The top state is **{top_state['customer_state']}**, generating **{format_currency(top_state['revenue'])}** ({top_state['revenue_share_pct']:.1f}% of total platform revenue).")

if __name__ == "__main__":
    main()
