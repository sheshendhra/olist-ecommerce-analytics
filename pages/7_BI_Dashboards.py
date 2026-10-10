"""
Power BI and Excel Deliverables Showcase Page for Olist E-commerce Analytics — Sheshendra.
Preserves and documents the existing Power BI report views and Excel pivot tables.
"""

import os
import streamlit as st
from utils.config import PROJECT_TITLE

st.set_page_config(page_title=f"BI Dashboards — {PROJECT_TITLE}", page_icon="📊", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POWERBI_DIR = os.path.join(BASE_DIR, "Powerbi_dashboard")
EXCEL_DIR = os.path.join(BASE_DIR, "MsExcel_Dashboard")
EXCEL_WORKBOOK = os.path.join(BASE_DIR, "Olist_Ecommerce_Analytics.xlsx")

def main():
    st.title("📊 Business Intelligence: Power BI & Excel Deliverables")
    st.markdown(
        "Preserved reporting artifacts illustrating executive KPI cards, DAX metrics, "
        "interactive slicers, and Excel dynamic pivot models built on the Olist schema."
    )

    tab1, tab2 = st.tabs(["🟡 Microsoft Power BI Report", "🟢 Microsoft Excel Analytics Workbook"])

    # Tab 1: Power BI
    with tab1:
        st.markdown("### 🟡 Power BI Multi-Page Report Showcase")
        st.info("📌 **Note on Power BI Interactivity:** The Power BI deliverables are preserved as validated local report assets and screenshots. To explore interactively in Power BI Service or Desktop, load the dataset using the instructions below.")

        if os.path.exists(POWERBI_DIR):
            pb_images = sorted([f for f in os.listdir(POWERBI_DIR) if f.endswith(".png")])
            if pb_images:
                # Group images into a 2-column showcase
                for i in range(0, len(pb_images), 2):
                    cols = st.columns(2)
                    with cols[0]:
                        img_path = os.path.join(POWERBI_DIR, pb_images[i])
                        st.image(img_path, caption=f"Power BI Report View {i+1}", use_container_width=True)
                    if i + 1 < len(pb_images):
                        with cols[1]:
                            img_path2 = os.path.join(POWERBI_DIR, pb_images[i+1])
                            st.image(img_path2, caption=f"Power BI Report View {i+2}", use_container_width=True)
            else:
                st.warning("No Power BI screenshots found.")
        else:
            st.warning("Power BI directory not found.")

        with st.expander("🛠️ Power BI Implementation & DAX Measures Overview"):
            st.markdown("""
            - **Star Schema Design:** `olist_orders` fact table connected to `olist_customers`, `olist_items`, `olist_products`, `olist_sellers`, and `olist_order_payments` dimensions.
            - **Key DAX Measures:**
              - `Total Revenue = SUM(olist_order_items[price]) + SUM(olist_order_items[freight_value])`
              - `On-Time Delivery % = DIVIDE(CALCULATE(COUNT(olist_orders[order_id]), olist_orders[is_late] = 0), COUNT(olist_orders[order_id]))`
              - `MoM Revenue Growth = DIVIDE([Total Revenue] - CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, MONTH)), CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, MONTH)))`
            """)

    # Tab 2: Excel
    with tab2:
        st.markdown("### 🟢 Microsoft Excel Dynamic Pivot Tables & Slicers")
        st.markdown(
            "The repository includes the pre-built Excel workbook **`Olist_Ecommerce_Analytics.xlsx`** "
            "containing 3 dedicated analytical sheets: `KPI Summary`, `RFM Analysis`, and `Monthly Revenue`."
        )

        if os.path.exists(EXCEL_WORKBOOK):
            with open(EXCEL_WORKBOOK, "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="📥 Download Olist_Ecommerce_Analytics.xlsx",
                data=excel_bytes,
                file_name="Olist_Ecommerce_Analytics_Sheshendra.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        if os.path.exists(EXCEL_DIR):
            xl_images = sorted([f for f in os.listdir(EXCEL_DIR) if f.endswith(".png")])
            if xl_images:
                cols = st.columns(2)
                for idx, img_name in enumerate(xl_images):
                    with cols[idx % 2]:
                        st.image(os.path.join(EXCEL_DIR, img_name), caption=img_name.replace("-", " ").replace(".png", "").title(), use_container_width=True)

if __name__ == "__main__":
    main()
