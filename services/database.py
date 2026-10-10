"""
Database service for SQL Insights and query execution.
Provides support for:
1. Local in-memory SQLite database populated from clean Olist tables (zero-dependency, works everywhere).
2. Managed PostgreSQL connection via DATABASE_URL or st.secrets['postgres'].
3. Curated repository of 15 advanced analytical SQL questions featuring Joins, CTEs, Window Functions, and aggregations.
"""

import os
import sqlite3
import pandas as pd
from typing import Tuple, Optional
from services.data_loader import build_master_dataset, load_raw_tables

def _safe_streamlit_cache_resource():
    try:
        import streamlit as st
        return st.cache_resource
    except Exception:
        def decorator(f):
            return f
        return decorator

@_safe_streamlit_cache_resource()
def get_sqlite_connection():
    """
    Creates an in-memory SQLite connection and loads the master dataset and raw tables
    as relational tables so queries can be run interactively.
    """
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    
    # 1. Load consolidated 'olist' table
    df_master = build_master_dataset()
    if not df_master.empty:
        # Convert datetimes to strings for SQLite compatibility
        df_sql = df_master.copy()
        for col in df_sql.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
            df_sql[col] = df_sql[col].astype(str)
        df_sql.to_sql("olist", conn, if_exists="replace", index=False)

    # 2. Also load individual raw tables if available for normalized relational queries
    raw = load_raw_tables()
    for name, df_table in raw.items():
        if not df_table.empty:
            df_table_sql = df_table.copy()
            for col in df_table_sql.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
                df_table_sql[col] = df_table_sql[col].astype(str)
            table_name = f"olist_{name}" if not name.startswith("olist_") else name
            df_table_sql.to_sql(table_name, conn, if_exists="replace", index=False)

    return conn

def execute_query(query: str, use_postgres: bool = False, pg_url: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Executes a SQL query against PostgreSQL if configured, or in-memory SQLite.
    Returns (DataFrame, error_message).
    """
    if use_postgres and pg_url:
        try:
            import psycopg2
            conn = psycopg2.connect(pg_url)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df, None
        except Exception as e:
            return None, f"PostgreSQL Error: {str(e)}"
    
    # Default: in-memory SQLite
    try:
        conn = get_sqlite_connection()
        df = pd.read_sql_query(query, conn)
        return df, None
    except Exception as e:
        return None, f"SQL Query Error: {str(e)}"

# Curated library of analytical business queries based on the project's SQL files and notebooks
CURATED_SQL_QUERIES = [
    {
        "id": "q1_exec_kpis",
        "title": "1. Executive KPIs Overview",
        "category": "Executive & Revenue",
        "question": "What is the total revenue, total freight, total orders, and average order value across all delivered orders?",
        "sql": """SELECT
    ROUND(SUM(order_item_total), 2) AS total_revenue,
    ROUND(SUM(price), 2) AS total_items_value,
    ROUND(SUM(freight_value), 2) AS total_freight,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(SUM(order_item_total) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM olist
WHERE order_status = 'delivered';"""
    },
    {
        "id": "q2_mom_growth",
        "title": "2. Monthly Revenue Trend & MoM Growth (CTE + Window LAG)",
        "category": "Sales & Growth",
        "question": "How is revenue trending month-over-month, and what is the month-over-month percentage growth?",
        "sql": """WITH monthly_sales AS (
    SELECT
        substr(order_purchase_timestamp, 1, 7) AS purchase_month,
        ROUND(SUM(order_item_total), 2) AS monthly_revenue,
        COUNT(DISTINCT order_id) AS total_orders
    FROM olist
    WHERE order_status = 'delivered' AND order_purchase_timestamp IS NOT NULL
    GROUP BY 1
)
SELECT
    purchase_month,
    monthly_revenue,
    total_orders,
    LAG(monthly_revenue, 1) OVER (ORDER BY purchase_month) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY purchase_month))
        / LAG(monthly_revenue, 1) OVER (ORDER BY purchase_month) * 100.0, 2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY purchase_month;"""
    },
    {
        "id": "q3_top_categories",
        "title": "3. Top 10 Product Categories by Revenue",
        "category": "Product Intelligence",
        "question": "Which product categories generate the highest total revenue and order volume?",
        "sql": """SELECT
    category_name,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(order_item_id) AS total_items_sold,
    ROUND(SUM(order_item_total), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS avg_item_price,
    ROUND(SUM(order_item_total) * 100.0 / (SELECT SUM(order_item_total) FROM olist WHERE order_status = 'delivered'), 2) AS revenue_share_pct
FROM olist
WHERE order_status = 'delivered' AND category_name IS NOT NULL
GROUP BY category_name
ORDER BY total_revenue DESC
LIMIT 10;"""
    },
    {
        "id": "q4_state_distribution",
        "title": "4. Geographic Distribution of Revenue by Customer State",
        "category": "Regional Analytics",
        "question": "Which customer states account for the majority of sales and orders?",
        "sql": """SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(SUM(order_item_total), 2) AS total_revenue,
    ROUND(AVG(freight_value), 2) AS avg_freight,
    ROUND(SUM(order_item_total) * 100.0 / (SELECT SUM(order_item_total) FROM olist WHERE order_status = 'delivered'), 2) AS state_revenue_pct
FROM olist
WHERE order_status = 'delivered' AND customer_state IS NOT NULL
GROUP BY customer_state
ORDER BY total_revenue DESC
LIMIT 15;"""
    },
    {
        "id": "q5_repeat_customers",
        "title": "5. Customer Repeat Purchase Behavior",
        "category": "Customer Intelligence",
        "question": "How many customers placed 1 order vs 2 or more orders, and what share of total revenue do repeat customers represent?",
        "sql": """WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(order_item_total) AS customer_revenue
    FROM olist
    WHERE customer_unique_id IS NOT NULL AND order_status = 'delivered'
    GROUP BY customer_unique_id
)
SELECT
    CASE WHEN order_count = 1 THEN '1 Order (One-Time)' ELSE '2+ Orders (Repeat)' END AS customer_type,
    COUNT(*) AS total_customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_orders), 2) AS customer_pct,
    ROUND(SUM(customer_revenue), 2) AS total_revenue,
    ROUND(SUM(customer_revenue) * 100.0 / (SELECT SUM(customer_revenue) FROM customer_orders), 2) AS revenue_pct,
    ROUND(AVG(customer_revenue), 2) AS avg_revenue_per_customer
FROM customer_orders
GROUP BY 1;"""
    },
    {
        "id": "q6_running_total",
        "title": "6. Cumulative Revenue Running Total (Window Function)",
        "category": "Financial Analytics",
        "question": "What is the cumulative running total of revenue over time across all months?",
        "sql": """WITH monthly_agg AS (
    SELECT
        substr(order_purchase_timestamp, 1, 7) AS purchase_month,
        ROUND(SUM(order_item_total), 2) AS monthly_revenue
    FROM olist
    WHERE order_status = 'delivered' AND order_purchase_timestamp IS NOT NULL
    GROUP BY 1
)
SELECT
    purchase_month,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY purchase_month), 2) AS running_total_revenue
FROM monthly_agg
ORDER BY purchase_month;"""
    },
    {
        "id": "q7_delivery_delay",
        "title": "7. Delivery Performance & Delay Analysis by State",
        "category": "Logistics & Delivery",
        "question": "Which states experience the highest average delivery duration and late delivery percentage?",
        "sql": """SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS delivered_orders,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
    ROUND(AVG(estimated_delivery_days), 1) AS avg_estimated_days,
    ROUND(SUM(CASE WHEN is_late = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT order_id), 2) AS late_order_pct
FROM olist
WHERE order_status = 'delivered' AND delivery_days IS NOT NULL
GROUP BY customer_state
HAVING COUNT(DISTINCT order_id) >= 50
ORDER BY avg_delivery_days DESC
LIMIT 10;"""
    },
    {
        "id": "q8_review_impact",
        "title": "8. Correlation Between Delivery Delays and Review Score",
        "category": "Customer Experience",
        "question": "How does on-time vs late delivery impact average customer review ratings?",
        "sql": """SELECT
    CASE WHEN is_late = 1 THEN 'Late Delivery' ELSE 'On-Time / Early' END AS delivery_timeliness,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN review_score >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS satisfied_ratings_pct,
    ROUND(SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS unsatisfied_ratings_pct
FROM olist
WHERE order_status = 'delivered' AND review_score IS NOT NULL
GROUP BY 1;"""
    },
    {
        "id": "q9_pareto_categories",
        "title": "9. Top Sellers Performance Ranking (Window DENSE_RANK)",
        "category": "Seller Intelligence",
        "question": "Who are the top 10 sellers by revenue, and what are their order counts and average reviews?",
        "sql": """WITH seller_agg AS (
    SELECT
        seller_id,
        seller_state,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(order_item_id) AS items_sold,
        ROUND(SUM(order_item_total), 2) AS total_revenue,
        ROUND(AVG(review_score), 2) AS avg_review_score
    FROM olist
    WHERE order_status = 'delivered' AND seller_id IS NOT NULL
    GROUP BY seller_id, seller_state
)
SELECT
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS seller_rank,
    seller_id,
    seller_state,
    total_orders,
    items_sold,
    total_revenue,
    avg_review_score
FROM seller_agg
LIMIT 10;"""
    },
    {
        "id": "q10_payment_distribution",
        "title": "10. Payment Method Share and Average Installments",
        "category": "Payments & Finance",
        "question": "What is the breakdown of order revenue by payment method and how many installments are typically used?",
        "sql": """SELECT
    COALESCE(primary_payment_type, 'unknown') AS payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(order_item_total), 2) AS total_revenue,
    ROUND(AVG(payment_installments_max), 1) AS avg_installments,
    ROUND(SUM(order_item_total) * 100.0 / (SELECT SUM(order_item_total) FROM olist WHERE order_status = 'delivered'), 2) AS payment_share_pct
FROM olist
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY total_revenue DESC;"""
    }
]
