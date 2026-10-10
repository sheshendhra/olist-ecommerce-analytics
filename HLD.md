# HLD.md — High Level Design
# Olist E-commerce Analytics — Sheshendra
# Brazilian E-Commerce Intelligence Platform

---

## 1. What Is This Document?

HLD = High Level Design.
This document explains the BIG PICTURE of how the project works.
No code. No numbers. Just architecture — boxes and arrows.

Anyone reading this should understand:
- What the system does
- How data flows from raw files to final output
- Which tools are used at each stage and why

---

## 2. System Architecture — Big Picture

```
+--------------------------------------------------+
|              DATA SOURCE LAYER                   |
|  Kaggle — 9 raw CSV files (Olist Dataset)        |
+--------------------------------------------------+
                        |
                        | (download + load)
                        v
+--------------------------------------------------+
|              DATA ENGINEERING LAYER              |
|  Tool: Python + Pandas                           |
|                                                  |
|  - Load all 9 tables into memory                 |
|  - Fix data types (datetime parsing)             |
|  - Handle nulls and duplicates                   |
|  - Merge all 9 tables into 1 master dataframe    |
|  - Engineer new business features                |
|                                                  |
|  Output: df.csv (master merged file)             |
+--------------------------------------------------+
                        |
                        | (clean master data)
                        v
+--------------------------------------------------+
|              ANALYSIS LAYER                      |
|  Tool: Python + Pandas (7 Pipelines)             |
|                                                  |
|  Pipeline 2 → Build summary tables               |
|    monthly_performance_summary.csv               |
|    category_performance_summary.csv              |
|    state_performance_summary.csv                 |
|    segment_summary.csv (RFM)                     |
|    clv_summary.csv                               |
|    churn_features.csv                            |
|    pareto (80/20 analysis)                       |
+--------------------------------------------------+
                        |
           +------------+------------+
           |            |            |
           v            v            v
+------------------+ +----------+ +-----------------+
| VISUALIZATION    | | SQL      | | ML LAYER        |
| LAYER            | | LAYER    | |                 |
|                  | |          | | Tool: Sklearn   |
| Pipeline 3,4,5   | | Tool:    | |                 |
| Matplotlib       | | PostgreSQL| | - Logistic Reg  |
| (static charts)  | |          | | - Decision Tree |
|                  | | 60       | | - Random Forest |
| Pipeline 6,7     | | questions| |                 |
| Plotly           | | basic to | | Output:         |
| (interactive)    | | advanced | | churn_prob      |
|                  | |          | | churn_risk      |
+------------------+ +----------+ +-----------------+
           |            |            |
           v            v            v
+--------------------------------------------------+
|              REPORTING LAYER                     |
|                                                  |
|  Excel     → Pivot tables + slicers + KPIs       |
|  Power BI  → Interactive business dashboard      |
|  Streamlit → Live churn prediction web app       |
|  HTML/CSS  → Portfolio website                   |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|              DEPLOYMENT LAYER                    |
|                                                  |
|  GitHub        → Code + notebooks + SQL          |
|  GitHub Pages  → Portfolio website               |
|  Streamlit Cloud → Live ML model                 |
+--------------------------------------------------+
```

---

## 3. Data Flow — Step by Step

```
STEP 1: Raw CSV files arrive
        9 files, different shapes, different columns

STEP 2: Load into Pandas
        Each table becomes a DataFrame

STEP 3: Clean each table
        Fix dates → handle nulls → remove duplicates

STEP 4: Merge all 9 tables
        Join on: order_id, customer_id, product_id, seller_id
        Result: 1 big master dataframe (df.csv)

STEP 5: Feature engineering
        Create revenue, profit, margin, delay, RFM columns

STEP 6: Build summary tables
        Group by month / category / state / customer

STEP 7: Run analysis
        EDA → Cohort → 80/20 → RFM → CLV

STEP 8: Generate charts
        Static (Matplotlib) + Interactive (Plotly)

STEP 9: SQL analysis
        60 questions on raw tables in PostgreSQL

STEP 10: Excel reporting
         Pivot tables + slicers on summary data

STEP 11: Power BI dashboard
         Connect all 9 tables, build KPI dashboard

STEP 12: Train ML model
         churn_features → 3 models → best model → save

STEP 13: Deploy
         GitHub + Streamlit + Portfolio page
```

---

## 4. Components Overview

### Component 1 — Data Engineering
- **What it does:** Takes raw messy data, makes it clean and usable
- **Input:** 9 raw CSV files
- **Output:** 1 clean master dataframe (df.csv)
- **Tool:** Python + Pandas

### Component 2 — Analysis Engine
- **What it does:** Runs 7 pipelines to extract business insights
- **Input:** df.csv (master dataframe)
- **Output:** 7 summary CSV files
- **Tool:** Python + Pandas + NumPy

### Component 3 — Visualization Engine
- **What it does:** Turns numbers into charts business users can understand
- **Input:** Summary CSV files
- **Output:** Static charts + interactive dashboard
- **Tool:** Matplotlib + Seaborn + Plotly

### Component 4 — SQL Engine
- **What it does:** Answers 60 business questions using pure SQL
- **Input:** 9 raw tables loaded into PostgreSQL
- **Output:** Query results + insights
- **Tool:** PostgreSQL

### Component 5 — ML Engine
- **What it does:** Predicts which customers will churn
- **Input:** churn_features.csv (RFM + behavioral features)
- **Output:** churn_probability + churn_risk label per customer
- **Tool:** Scikit-learn (3 models trained and compared)

### Component 6 — Reporting Layer
- **What it does:** Makes insights presentable to business stakeholders
- **Input:** Summary data + ML predictions
- **Output:** Excel report + Power BI dashboard + Portfolio page
- **Tool:** Excel, Power BI, HTML/CSS, Streamlit

---

## 5. Tech Choices — Why Each Tool

| Tool | Why Chosen |
|------|-----------|
| Python + Pandas | Industry standard for data work. Handles 100K+ rows easily |
| Matplotlib | Full control over chart styling. Used in every data job |
| Plotly | Interactive charts that business users can explore |
| PostgreSQL | Most common SQL database in data analyst job descriptions |
| Scikit-learn | Simple API, all 3 models use same interface for easy comparison |
| Excel | Business users live in Excel. Shows practical business skill |
| Power BI | Most used BI tool in India. High demand in job market |
| Streamlit | Fastest way to deploy ML model as a web app in Python |
| GitHub | Every employer checks GitHub. Shows code quality and consistency |

---

## 6. Key Design Decisions

**Decision 1 — Merge all 9 tables into 1 master file**
Why: Easier to run all analysis from one source of truth.
Trade-off: Large file size but manageable for 100K rows.

**Decision 2 — Build 7 separate pipelines**
Why: Each pipeline has one job. Easy to debug, easy to re-run.
Trade-off: More functions to manage.

**Decision 3 — Save summary CSVs as output files**
Why: Portfolio website and Streamlit app can load pre-computed data fast.
Trade-off: Data is static (not real-time).

**Decision 4 — Train 3 ML models and compare**
Why: Shows model selection thinking, not just "I ran one model."
Trade-off: More time to build, but much stronger for resume.

**Decision 5 — Use RFM for customer segmentation**
Why: RFM is the most widely used customer segmentation method in e-commerce.
Trade-off: Simplified CLV (frequency × monetary) not full predictive CLV.

---

## 7. Project Stages

```
Stage 0 — Foundation
  Folder structure, README, HLD, LLD, Git setup

Stage 1 — Data
  Download Olist, load 9 tables, clean, merge, engineer features

Stage 2 — Analysis
  Run 7 pipelines, build all summary tables, EDA complete

Stage 3 — Visualization
  Static charts (Matplotlib), interactive charts (Plotly)

Stage 4 — Reporting
  Excel pivot tables, SQL 60 questions, Power BI dashboard

Stage 5 — Machine Learning
  Train 3 models, compare, select best, save model

Stage 6 — Deploy
  GitHub push, Streamlit cloud, Portfolio page live
```

---

*HLD.md — High Level Design*

*Read LLD.md for detailed per-feature design*