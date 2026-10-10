# 🛒 Olist E-commerce Analytics — Sheshendra

> **End-to-End E-Commerce Data Analytics, Logistics Intelligence & Machine Learning Platform**  
> Analyzing 98,666 real Brazilian marketplace orders, revenue performance, delivery punctuality, RFM customer segmentation, and churn risk.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sheshendra-olist-analytics.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/sheshendhra/olist-ecommerce-analytics)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML%20Churn%20Model-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQL-Analytical%20Engine-003B57?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passed-brightgreen)](https://github.com/sheshendhra/olist-ecommerce-analytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> 🚀 **Live Application:** [https://sheshendra-olist-analytics.streamlit.app/](https://sheshendra-olist-analytics.streamlit.app/)  
> 📂 **GitHub Repository:** [https://github.com/sheshendhra/olist-ecommerce-analytics](https://github.com/sheshendhra/olist-ecommerce-analytics)

---

## 📌 Project Overview

**Olist** is the largest department store marketplace in Brazilian e-commerce, connecting small merchants from across Brazil to major sales channels. This project delivers an executive intelligence suite, interactive SQL exploratory console, and machine learning decision tool based on the official Olist Brazilian E-Commerce dataset.

- **Author & Maintainer:** **Sheshendra** ([GitHub: @sheshendhra](https://github.com/sheshendhra) | [Email](mailto:sheshendra09@gmail.com))
- **Live Deployment:** [sheshendra-olist-analytics.streamlit.app](https://sheshendra-olist-analytics.streamlit.app/)
- **Original Source Attribution:** This project builds on an existing open-source analytics project and has been adapted and enhanced. See the repository's license and applicable third-party notices.
- **Dataset:** [Olist Brazilian E-Commerce Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## 🎯 Business Problems Solved

1. **Executive Revenue Intelligence:** What is the true gross revenue across 98K+ orders, and which months fueled the 6.5x scaling between Jan 2017 and May 2018?
2. **Category & Product Economics:** Which categories generate top revenue, and does the 80/20 Pareto principle apply to product catalog performance?
3. **Logistics & Delivery Punctuality:** How do actual transit times compare against promised delivery deadlines across Brazil's 27 states, and how severely do delivery delays degrade review scores?
4. **Customer Retention & RFM Segmentation:** What percentage of customers return for repeat purchases, and how can we segment customers into actionable cohorts (Champions, Loyal, At Risk, Lost)?
5. **Predictive Churn Risk:** Can first-purchase fulfillment experience (delivery days, freight ratio, review rating) predict whether a customer will churn before they lapse?

---

## 📊 Key Verified Metrics (Olist Dataset)

| Metric | Validated Value | Business Context |
|---|---|---|
| **Total Gross Sales** | **R$ 15,843,553** | Includes R$ 13.49M item prices + R$ 2.35M freight charges |
| **Total Orders** | **98,666** | Delivered order rate: 97.02% |
| **Unique Customers** | **95,420** | Over 96.9% single-purchase customers |
| **Average Order Value (AOV)** | **R$ 160.58** | Average spend per customer transaction |
| **On-Time Delivery Rate** | **92.2%** | Shipments delivered on or before deadline |
| **Average Delivery Duration** | **12.5 Days** | Average door-to-door transit time across all states |
| **Average Customer Rating** | **4.08 / 5.0 ⭐** | 4.14 ⭐ for on-time vs 2.27 ⭐ for late deliveries |
| **Top Product Category** | `beleza_saude` | Health & Beauty (R$ 1.45M sales, 8,646 orders) |
| **Top Customer State** | `SP` (São Paulo) | Accounts for 37.5% of total gross platform revenue |

---

## 🖥️ Application Pages & Features

The platform is organized into 8 interactive multi-page dashboards:

| Page | Features & Capabilities |
|---|---|
| **Executive Overview (`app.py`)** | Hero KPI metric cards, gross sales vs shipping costs, monthly revenue trend chart, quick navigation |
| **1. Sales Analytics** | Monthly revenue trends, AOV progression, MoM growth rates, revenue distribution by Brazilian state |
| **2. Product & Seller Analytics** | Top category ranking, cumulative Pareto 80/20 curve, top seller leaderboards, volume vs revenue matrices |
| **3. Customer Analytics** | Single-purchase vs repeat buyer analysis, RFM segmentation (Recency, Frequency, Monetary), cohort retention |
| **4. Delivery Analytics** | State transit time comparison, promised vs actual delivery variance, rating degradation vs delay correlation |
| **5. Machine Learning** | Zero-leakage Random Forest churn model benchmark, confusion matrix, feature importance, live what-if churn simulator |
| **6. SQL Insights Console** | In-memory SQLite analytics engine, 10 business SQL questions with CTEs and Window Functions (`LAG`, `DENSE_RANK`), live custom SQL query runner |
| **7. BI Dashboards & Excel** | Preserved Microsoft Power BI dashboard showcase and downloadable multi-tab Excel model (`Olist_Ecommerce_Analytics.xlsx`) |
| **8. About Project** | Full system documentation, architecture overview, dataset lineage, and maintainer profile |

---

## 🏗️ System Architecture

```
                               ┌─────────────────────────────┐
                               │   Kaggle / Olist CSV Data   │
                               │  (8 Interconnected Tables)  │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │     Python & Pandas ETL     │
                               │  - Clean nulls & datetimes  │
                               │  - Join orders/items/custs  │
                               │  - Parquet Caching (20.6MB) │
                               └──────────────┬──────────────┘
                                              │
                   ┌──────────────────────────┼──────────────────────────┐
                   ▼                          ▼                          ▼
     ┌──────────────────────────┐┌──────────────────────────┐┌──────────────────────────┐
     │   Analytical Services    ││   SQL & Database Engine  ││    Scikit-learn ML       │
     │  - Executive KPIs        ││  - In-memory SQLite DB   ││  - First-order features │
     │  - Sales & MoM Growth    ││  - Optional PostgreSQL   ││  - Class-balanced RF    │
     │  - Pareto 80/20 analysis ││  - 10 Business Queries   ││  - ROC-AUC / F1 metrics │
     │  - RFM Segmentation      ││  - Window LAG, RANK, CTE ││  - Live Simulator       │
     └─────────────┬────────────┘└────────────┬─────────────┘└────────────┬─────────────┘
                   │                          │                           │
                   └──────────────────────────┼───────────────────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │    Streamlit Web Platform   │
                               │   - Multi-Page Navigation   │
                               │   - Global Sidebar Filters  │
                               │   - Interactive Plotly Visuals│
                               │   - CSV Data Export         │
                               └─────────────────────────────┘
```

---

## 🗂️ Project Structure

```
olist-ecommerce-analytics/
├── app.py                          # Primary Streamlit entry point (Executive Overview)
├── pages/
│   ├── 1_Sales_Analytics.py        # Monthly trends, AOV, MoM growth, state distribution
│   ├── 2_Product_Seller_Analytics.py # Category revenue, Pareto 80/20, seller performance
│   ├── 3_Customer_Analytics.py     # Customer retention, RFM segmentation, CLV analysis
│   ├── 4_Delivery_Analytics.py     # Delivery duration, delay rates, review score correlation
│   ├── 5_Machine_Learning.py       # Churn classification, confusion matrix, live simulator
│   ├── 6_SQL_Insights.py           # Curated business queries, custom SQL console, schema
│   ├── 7_BI_Dashboards.py          # Power BI report views and Excel pivot table showcase
│   └── 8_About_Project.py          # Project background, Sheshendra profile, attribution
├── components/
│   ├── charts.py                   # Reusable Plotly chart builders
│   ├── filters.py                  # Global sidebar filters & CSV exporter
│   └── metrics.py                  # Custom styled KPI metric cards
├── services/
│   ├── data_loader.py              # ETL pipeline & parquet cache loader
│   ├── analytics.py                # Sales, category, delivery, and RFM calculations
│   ├── database.py                 # SQLite engine & curated SQL questions
│   └── ml_service.py               # Leakage-free churn model training & inference
├── utils/
│   ├── config.py                   # Branding, color themes, and formatting helpers
│   └── validation.py               # Input and schema validation utilities
├── scripts/
│   ├── download_data.py            # Automated dataset download from public repository
│   ├── build_cache.py              # Generates the fast analytical parquet cache
│   └── train_model.py              # Trains and serializes the Random Forest model
├── sql/
│   ├── postgres_data_load.sql      # PostgreSQL DDL and \copy import script
│   └── Sql_Questions.ipynb         # Jupyter notebook containing analytical queries
├── tests/
│   ├── test_data_loader.py         # ETL and dataset tests
│   ├── test_analytics.py           # KPIs and calculation tests
│   ├── test_database.py            # SQL query execution tests
│   ├── test_ml_service.py          # Model training, leakage checks & prediction tests
│   └── test_validation.py          # Input validation tests
├── models/
│   ├── churn_model.joblib          # Trained Random Forest classifier
│   └── scaler.joblib               # StandardScaler preprocessing artifact
├── data/
│   └── olist_master.parquet        # High-speed pre-joined analytical cache (20.6MB)
├── .streamlit/
│   └── config.toml                 # Streamlit UI configuration
├── Olist_Ecommerce_Analytics.xlsx  # Preserved Excel workbook (KPIs, RFM, Monthly)
├── Powerbi_dashboard/              # Preserved Power BI screenshots & views
├── MsExcel_Dashboard/              # Preserved Excel pivot table screenshots
├── requirements.txt                # Production Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
└── README.md                       # Comprehensive portfolio documentation
```

---

## 🤖 Machine Learning: Churn Prediction

### Target Formulation & Leakage Elimination
- **Original Pitfall:** In typical implementations, churn was defined as `frequency == 1` while feeding `frequency` or `days_active` directly into the feature matrix, creating 98%+ artificial target leakage.
- **Our Leakage-Free Approach:** We predict whether a customer will fail to make a repeat purchase using **strictly first-purchase behavioral data**:
  - `first_order_value` (Price + Freight)
  - `first_order_freight` (Shipping charge)
  - `item_count` (Items in basket)
  - `payment_installments` (Installments chosen)
  - `delivery_days` (Carrier transit duration)
  - `is_late` (Delivery past deadline flag)
  - `review_score` (Customer satisfaction rating)

### Model Evaluation Benchmark (Stratified Holdout Test Set)

| Model | ROC-AUC | F1-Score | Precision | Recall | Balanced Accuracy |
|---|---|---|---|---|---|
| **Majority Baseline Dummy** | 0.5000 | 0.9845 | 0.9695 | 1.0000 | 50.00% |
| **Logistic Regression (Balanced)** | 0.5703 | 0.7617 | 0.9753 | 0.6248 | 62.09% |
| **Random Forest (Balanced)** ⭐ | **0.5748** | **0.7962** | **0.9744** | **0.6731** | **66.59%** |

---

## ⚡ Local Setup & Execution Instructions

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/sheshendhra/olist-ecommerce-analytics.git
cd olist-ecommerce-analytics
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Build Dataset Cache & Train Model (Optional)
The pre-built Parquet cache (`data/olist_master.parquet`) and trained model artifacts (`models/`) are already included in the repository. If you ever need to rebuild from raw CSVs:
```bash
# Downloads the 8 core Olist tables from public repository (~1 minute)
python scripts/download_data.py

# Generates the high-speed analytical parquet cache (~10 seconds)
python scripts/build_cache.py

# Trains and serializes the Random Forest churn model (~2 seconds)
python scripts/train_model.py
```

### 5. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing

Run the complete 16-test suite using pytest:
```bash
python -m pytest -v
```

**Verified Test Results (16/16 Passed):**
```
tests/test_analytics.py::test_compute_executive_kpis PASSED              [  6%]
tests/test_analytics.py::test_get_monthly_sales_trend PASSED             [ 12%]
tests/test_analytics.py::test_get_category_performance PASSED            [ 18%]
tests/test_analytics.py::test_get_state_performance PASSED               [ 25%]
tests/test_analytics.py::test_compute_rfm_segmentation PASSED            [ 31%]
tests/test_analytics.py::test_compute_delivery_analytics PASSED          [ 37%]
tests/test_data_loader.py::test_load_raw_tables PASSED                   [ 43%]
tests/test_data_loader.py::test_build_master_dataset PASSED              [ 50%]
tests/test_database.py::test_database_connection_and_basic_query PASSED  [ 56%]
tests/test_database.py::test_curated_queries_syntax PASSED               [ 62%]
tests/test_ml_service.py::test_build_ml_dataset PASSED                   [ 68%]
tests/test_ml_service.py::test_load_trained_model PASSED                 [ 75%]
tests/test_ml_service.py::test_predict_single_customer PASSED            [ 81%]
tests/test_validation.py::test_validate_dataframe PASSED                 [ 87%]
tests/test_validation.py::test_validate_date_range PASSED                [ 93%]
tests/test_validation.py::test_validate_rfm_input PASSED                 [100%]

============================= 16 passed in 12.80s =============================
```

---

## ☁️ Deployment Instructions

The application is deployed on **Streamlit Community Cloud**:
- **Live URL:** [https://sheshendra-olist-analytics.streamlit.app/](https://sheshendra-olist-analytics.streamlit.app/)
- **Repository:** `sheshendhra/olist-ecommerce-analytics`
- **Branch:** `main`
- **Main file path:** `app.py`

### Deployment Characteristics:
- **No external database required:** Operates using the high-performance local Parquet cache and in-memory SQLite analytics engine.
- **Zero credential risk:** No hardcoded secrets, database passwords, or environment variables needed for production operation.
- **Multi-page routing:** Automatically detected from the `pages/` directory by Streamlit.

---

## 👤 Maintainer & Attribution

- **Project Owner:** **Sheshendra**
  - GitHub: [@sheshendhra](https://github.com/sheshendhra)
  - Email: [sheshendra09@gmail.com](mailto:sheshendra09@gmail.com)
  - Live Demo: [sheshendra-olist-analytics.streamlit.app](https://sheshendra-olist-analytics.streamlit.app/)
- **Original Source Attribution:** This project builds on an existing open-source analytics project and has been adapted and enhanced. See the repository's license and applicable third-party notices.
- **Dataset Rights:** The dataset is public domain under CC BY-NC-SA 4.0, provided by Olist and André Sionek on Kaggle.

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).
