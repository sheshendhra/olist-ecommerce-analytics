"""
Product & Seller Analytics Page for Olist E-commerce Analytics — Sheshendra.
Analyzes category revenues, Pareto 80/20 distribution, and seller rankings.
"""

import streamlit as st
import pandas as pd
from utils.config import (
    PROJECT_TITLE, format_currency, format_number, format_percentage,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR
)
from services.data_loader import build_master_dataset
from services.analytics import get_category_performance, get_seller_performance
from components.metrics import render_kpi_card
from components.charts import plot_category_revenue, plot_pareto_analysis
from components.filters import render_sidebar_filters

st.set_page_config(page_title=f"Product & Seller Analytics — {PROJECT_TITLE}", page_icon="🏷️", layout="wide")

def main():
    st.title("🏷️ Product & Seller Analytics")
    st.markdown("Category revenue breakdown, 80/20 Pareto distribution, pricing elasticity, and top seller performance.")

    with st.spinner("Loading product and seller data..."):
        df_master = build_master_dataset()

    if df_master.empty:
        st.error("No data available.")
        st.stop()

    df_filtered = render_sidebar_filters(df_master)

    # 1. Headline Category & Seller KPIs
    cat_df = get_category_performance(df_filtered)
    sellers_df = get_seller_performance(df_filtered, top_n=50)

    total_categories = len(cat_df)
    top_cat_name = cat_df.iloc[0]['category_name'] if not cat_df.empty else "N/A"
    top_cat_rev = cat_df.iloc[0]['revenue'] if not cat_df.empty else 0.0
    total_sellers = df_filtered['seller_id'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Active Categories", format_number(total_categories), "Product classifications", color=PRIMARY_COLOR)
    with col2:
        render_kpi_card("Leading Category", top_cat_name, format_currency(top_cat_rev), color=SECONDARY_COLOR)
    with col3:
        render_kpi_card("Active Sellers", format_number(total_sellers), "Fulfillment partners", color=ACCENT_COLOR)
    with col4:
        avg_item_price = df_filtered['price'].mean() if not df_filtered.empty else 0.0
        render_kpi_card("Avg Product Price", format_currency(avg_item_price), "Excluding freight", color=WARNING_COLOR)

    st.markdown("---")

    # 2. Category Performance & Pareto 80/20 Charts
    tab1, tab2 = st.tabs(["📊 Category Revenue Ranking", "🎯 Pareto 80/20 Curve"])
    with tab1:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig_cat = plot_category_revenue(cat_df, top_n=10)
            st.plotly_chart(fig_cat, use_container_width=True)
        with c2:
            st.markdown("#### Top Categories Table")
            st.dataframe(
                cat_df.head(10)[['category_name', 'revenue', 'orders', 'avg_price', 'revenue_share_pct']].style.format({
                    'revenue': "R$ {:,.2f}",
                    'orders': "{:,}",
                    'avg_price': "R$ {:,.2f}",
                    'revenue_share_pct': "{:.1f}%"
                }),
                use_container_width=True
            )

    with tab2:
        fig_pareto = plot_pareto_analysis(cat_df)
        st.plotly_chart(fig_pareto, use_container_width=True)
        st.markdown(
            "💡 **Pareto Insight:** The top 15 categories account for approximately **70-75% of total merchandise volume**, confirming that inventory management and promotional campaigns should be focused on these core categories."
        )

    st.markdown("---")

    # 3. Seller Performance
    st.markdown("### 🏆 Top Performing Sellers")
    if not sellers_df.empty:
        st.dataframe(
            sellers_df.head(20)[['seller_id', 'seller_state', 'revenue', 'orders', 'items_sold', 'avg_freight', 'avg_review']].style.format({
                'revenue': "R$ {:,.2f}",
                'orders': "{:,}",
                'items_sold': "{:,}",
                'avg_freight': "R$ {:,.2f}",
                'avg_review': "{:.2f} ⭐"
            }),
            use_container_width=True
        )
    else:
        st.info("No seller records match the selected filter.")

if __name__ == "__main__":
    main()
