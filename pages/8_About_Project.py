"""
About Page for Olist E-commerce Analytics — Sheshendra.
Details project background, business problem, architecture, tech stack, and attribution.
"""

import streamlit as st
from utils.config import (
    PROJECT_TITLE, PROJECT_SUBTITLE, AUTHOR_NAME, ORIGINAL_ATTRIBUTION, DATASET_SOURCE_URL
)

st.set_page_config(page_title=f"About — {PROJECT_TITLE}", page_icon="ℹ️", layout="wide")

def main():
    st.title(f"ℹ️ About This Project")
    st.markdown(f"**{PROJECT_TITLE}** — *{PROJECT_SUBTITLE}*")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎯 Business Problem & Purpose")
        st.markdown("""
        **Olist** is a major Brazilian e-commerce marketplace connecting small merchants with customers across Brazil. 
        Between 2016 and 2018, the platform fulfilled over 98,000 orders across 27 Brazilian states. 

        This project analyzes the end-to-end transaction lifecycle to answer mission-critical business questions:
        1. **Revenue & Growth:** Where is sales growth coming from, and which months drove peak demand?
        2. **Category & Product Economics:** What are the top margin and volume categories, and does an 80/20 Pareto rule apply?
        3. **Logistics & Delivery Operations:** How does delivery punctuality vary by state, and how do shipping delays impact customer review scores?
        4. **Customer Retention & RFM Intelligence:** What percentage of customers return for a second purchase, and how should customer segments be targeted?
        5. **Predictive Churn Risk:** Can we identify high-risk first-time buyers before they permanently churn, and what interventions should be deployed?
        """)

        st.markdown("### 🏗️ Technical Architecture & Pipeline")
        st.markdown("""
        - **Data Engineering:** Python & Pandas ETL pipeline handling nulls, type conversions, datetime parsing, and normalized joins across 8 relational tables.
        - **Interactive Frontend:** Streamlit multi-page web application featuring custom KPI cards, global sidebar filters, and CSV data exports.
        - **Data Visualization:** Interactive Plotly charts (dual-axis sales trends, Pareto curves, state distributions, treemaps, and confusion matrices).
        - **SQL Analytics:** SQLite / PostgreSQL analytical query engine with CTEs, Window Functions (`LAG`, `DENSE_RANK`, `SUM OVER`), and aggregations.
        - **Machine Learning:** Scikit-learn Churn Classification pipeline with stratified train/test splitting, class balancing, baseline comparison, and zero target leakage.
        - **Business Intelligence:** Microsoft Power BI report deliverables and Excel dynamic pivot models (`Olist_Ecommerce_Analytics.xlsx`).
        """)

    with col2:
        st.markdown("### 👤 Project Owner")
        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 12px; padding: 20px; border: 1px solid #334155; margin-bottom: 16px;">
            <div style="font-size: 1.3rem; font-weight: 700; color: #F8FAFC;">{AUTHOR_NAME}</div>
            <div style="font-size: 0.9rem; color: #818CF8; margin-bottom: 12px;">Data Analyst & ML Specialist</div>
            <p style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 16px;">
                Specializing in end-to-end data analytics, machine learning pipelines, and interactive executive dashboards.
            </p>
            <div style="font-size: 0.85rem; color: #94A3B8;">
                <div>🐙 <b>GitHub:</b> <a href="https://github.com/Sheshendra" target="_blank" style="color: #60A5FA;">github.com/Sheshendra</a></div>
                <div style="margin-top: 6px;">💼 <b>LinkedIn:</b> <a href="https://linkedin.com/in/sheshendra" target="_blank" style="color: #60A5FA;">linkedin.com/in/sheshendra</a></div>
                <div style="margin-top: 6px;">✉️ <b>Email:</b> <span style="color: #94A3B8;">sheshendra@example.com</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📦 Dataset Source")
        st.markdown(f"""
        - **Source:** [Kaggle Olist Brazilian E-Commerce]({DATASET_SOURCE_URL})
        - **Scope:** 100,000 anonymized real orders from 2016 to 2018.
        - **Relational Tables:** Orders, Items, Customers, Payments, Reviews, Products, Sellers, Geolocation, Translations.
        """)

        st.markdown("### 📜 Attribution & License")
        st.markdown(f"""
        {ORIGINAL_ATTRIBUTION}
        
        Licensed under the [MIT License](https://opensource.org/licenses/MIT).
        """)

if __name__ == "__main__":
    main()
