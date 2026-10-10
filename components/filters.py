"""
Sidebar filters and interactive controls for Olist E-commerce Analytics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders sidebar filters for date range, category, state, and status.
    Returns filtered DataFrame.
    """
    st.sidebar.markdown("### 🔍 Global Filters")

    if df.empty:
        return df

    filtered_df = df.copy()

    # 1. Date Range Filter
    if 'order_purchase_timestamp' in filtered_df.columns:
        min_date = filtered_df['order_purchase_timestamp'].min().date()
        max_date = filtered_df['order_purchase_timestamp'].max().date()

        date_range = st.sidebar.date_input(
            "📅 Order Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter orders by customer purchase date"
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_dt, end_dt = date_range
            filtered_df = filtered_df[
                (filtered_df['order_purchase_timestamp'].dt.date >= start_dt) &
                (filtered_df['order_purchase_timestamp'].dt.date <= end_dt)
            ]

    # 2. Product Category Filter
    if 'category_name' in filtered_df.columns:
        categories = sorted([c for c in filtered_df['category_name'].dropna().unique() if c != 'unknown'])
        selected_categories = st.sidebar.multiselect(
            "🏷️ Product Categories",
            options=categories,
            default=[],
            placeholder="All Categories",
            help="Leave empty to include all categories"
        )
        if selected_categories:
            filtered_df = filtered_df[filtered_df['category_name'].isin(selected_categories)]

    # 3. Customer State Filter
    if 'customer_state' in filtered_df.columns:
        states = sorted(filtered_df['customer_state'].dropna().unique().tolist())
        selected_states = st.sidebar.multiselect(
            "📍 Customer States",
            options=states,
            default=[],
            placeholder="All States (SP, RJ, MG...)",
            help="Leave empty to include all states"
        )
        if selected_states:
            filtered_df = filtered_df[filtered_df['customer_state'].isin(selected_states)]

    # 4. Order Status Filter
    if 'order_status' in filtered_df.columns:
        statuses = sorted(filtered_df['order_status'].dropna().unique().tolist())
        selected_status = st.sidebar.selectbox(
            "📦 Order Status",
            options=["All Statuses"] + statuses,
            index=0 if "delivered" not in statuses else statuses.index("delivered") + 1,
            help="Filter by order lifecycle status"
        )
        if selected_status != "All Statuses":
            filtered_df = filtered_df[filtered_df['order_status'] == selected_status]

    # Quick summary of filtered records
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Orders:** `{filtered_df['order_id'].nunique():,}`")
    st.sidebar.markdown(f"**Filtered Line Items:** `{len(filtered_df):,}`")

    # CSV Download in sidebar
    csv_data = filtered_df[['order_id', 'order_purchase_timestamp', 'customer_state', 'category_name', 'price', 'freight_value', 'order_status']].head(1000).to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Download Sample CSV",
        data=csv_data,
        file_name="olist_filtered_sample.csv",
        mime="text/csv",
        help="Export up to 1,000 rows of currently filtered data"
    )

    return filtered_df
