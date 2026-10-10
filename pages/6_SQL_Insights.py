"""
SQL Insights Page for Olist E-commerce Analytics — Sheshendra.
Executes live analytical SQL queries using Joins, CTEs, Window Functions, and aggregations
against the database engine.
"""

import streamlit as st
import pandas as pd
from utils.config import PROJECT_TITLE
from services.database import CURATED_SQL_QUERIES, execute_query

st.set_page_config(page_title=f"SQL Insights — {PROJECT_TITLE}", page_icon="💾", layout="wide")

def main():
    st.title("💾 SQL Analytical Queries & Business Intelligence")
    st.markdown(
        "Direct SQL engine interface executing analytical queries across **orders**, **items**, "
        "**customers**, **payments**, and **products** with CTEs, Window Functions (LAG, DENSE_RANK, SUM OVER), and aggregations."
    )

    tab1, tab2, tab3 = st.tabs([
        "📚 Curated Business Queries (Live Execution)",
        "💻 Interactive Custom SQL Console",
        "🗂️ Relational Table Schema"
    ])

    # Tab 1: Curated Queries
    with tab1:
        st.markdown("### Select an Analytical Question to Execute:")
        query_options = {q["title"]: q for q in CURATED_SQL_QUERIES}
        selected_title = st.selectbox("Choose Business Question", options=list(query_options.keys()))
        selected_q = query_options[selected_title]

        st.markdown(f"**Business Question:** *{selected_q['question']}*")
        st.markdown(f"**Category:** `{selected_q['category']}`")

        st.code(selected_q["sql"], language="sql")

        if st.button("▶️ Execute Query Live", key="btn_exec_curated"):
            with st.spinner("Executing SQL query against database engine..."):
                df_result, err = execute_query(selected_q["sql"])

            if err:
                st.error(f"Execution Error: {err}")
            elif df_result is not None:
                st.success(f"Query returned {len(df_result):,} rows successfully!")
                st.dataframe(df_result, use_container_width=True)

                # Download result as CSV
                csv_bytes = df_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Query Result as CSV",
                    data=csv_bytes,
                    file_name=f"{selected_q['id']}_result.csv",
                    mime="text/csv"
                )

    # Tab 2: Custom SQL Console
    with tab2:
        st.markdown("### 💻 Custom SQL Query Console")
        st.markdown("Write and run custom SQL queries against the `olist` analytical table or normalized tables:")

        default_query = """SELECT 
    category_name, 
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(order_item_total), 2) AS revenue
FROM olist 
WHERE order_status = 'delivered'
GROUP BY category_name 
ORDER BY revenue DESC 
LIMIT 5;"""

        user_sql = st.text_area("SQL Statement", value=default_query, height=160)

        if st.button("▶️ Run Custom Query", key="btn_exec_custom"):
            with st.spinner("Executing custom query..."):
                df_custom, err = execute_query(user_sql)

            if err:
                st.error(f"SQL Error: {err}")
            elif df_custom is not None:
                st.success(f"Executed successfully! Returned {len(df_custom):,} rows.")
                st.dataframe(df_custom, use_container_width=True)

    # Tab 3: Schema Overview
    with tab3:
        st.markdown("### 🗂️ Database Table Schema")
        st.markdown("""
        The database contains the unified analytical table `olist` and individual normalized tables:
        - `olist` (Master analytical view with orders, items, customers, products, payments, reviews)
        - `olist_orders` (`order_id`, `customer_id`, `order_status`, `order_purchase_timestamp`, `order_delivered_customer_date`...)
        - `olist_items` (`order_id`, `order_item_id`, `product_id`, `seller_id`, `price`, `freight_value`)
        - `olist_customers` (`customer_id`, `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`)
        - `olist_payments` (`order_id`, `payment_sequential`, `payment_type`, `payment_installments`, `payment_value`)
        - `olist_reviews` (`review_id`, `order_id`, `review_score`)
        - `olist_products` (`product_id`, `product_category_name`, `product_weight_g`...)
        - `olist_sellers` (`seller_id`, `seller_city`, `seller_state`)
        """)

if __name__ == "__main__":
    main()
