# LLD.md — Low Level Design
# Olist E-commerce Analytics — Sheshendra
# Brazilian E-Commerce Intelligence Platform

---

## 1. What Is This Document?

LLD = Low Level Design.
This document explains HOW each part was built in detail.
- Which functions exist and what they do
- Which columns are used for each analysis
- What the input and output of every step is
- How the ML model was designed

---

## 2. Data Engineering — Detailed Design

### 2.1 Table Join Design

All 9 tables are joined using these keys:

```
olist_orders
    |-- order_id ---------> olist_order_items
    |-- order_id ---------> olist_order_payments
    |-- order_id ---------> olist_order_reviews
    |-- customer_id ------> olist_customers
                                |
olist_order_items
    |-- product_id -------> olist_products
    |-- seller_id ---------> olist_sellers
                                |
olist_products
    |-- product_category_name -> product_category_name_translation

olist_customers / olist_sellers
    |-- zip_code_prefix --> olist_geolocation
```

Final result: 1 master dataframe with all columns from all 9 tables.

---

### 2.2 Cleaning Functions

| Function | What It Does | Input | Output |
|----------|-------------|-------|--------|
| load_data() | Loads df.csv into memory | file path | DataFrame |
| fix_datetime_cols() | Parses 5 date columns to datetime type | raw df | df with proper dates |
| clean_nulls() | Drops rows missing critical cols, fills medians for dimensions | dirty df | clean df |
| add_financial_features() | Creates revenue, cost, profit, margin, freight_ratio | clean df | df + new columns |
| add_delivery_features() | Creates delivery_delay_days, is_late | clean df | df + delay columns |
| add_time_features() | Creates purchase_month, purchase_year, purchase_hour | clean df | df + time columns |

---

### 2.3 Engineered Features — Detailed Formulas

| Feature | Formula | Data Type | Purpose |
|---------|---------|-----------|---------|
| revenue | price + freight_value | float | Total order value |
| cost | price × 0.80 | float | Estimated cost (80% of price) |
| profit | revenue − cost | float | Order-level profit |
| margin_% | (profit / revenue) × 100 | float | Profitability % |
| freight_ratio | freight_value / revenue | float | Shipping cost as % of revenue |
| delivery_delay_days | actual_delivered − estimated_delivery | int | Positive = late, negative = early |
| is_late | 1 if delay > 0 else 0 | binary | Late delivery flag |
| purchase_month | truncate(purchase_timestamp, 'month') | date | For monthly grouping |
| purchase_year | year(purchase_timestamp) | int | For yearly grouping |

---

## 3. Analysis Pipelines — Detailed Design

### Pipeline 1 — Data Load + Clean
```
Input  : raw df.csv path
Steps  : load → fix_datetime → clean_nulls → add_financial → add_delivery → add_time
Output : clean master df in memory
```

### Pipeline 2 — Build Summary Tables
```
Input  : clean master df

build_monthly_summary()
  Group by: purchase_month
  Aggregations: sum(revenue), sum(profit), nunique(order_id),
                nunique(customer_id), mean(delay), sum(is_late)
  Calculated: profit_margin_%, AOV, MoM_growth_%, Revenue_3M_MA,
              YoY_growth_%, late_order_rate_%
  Output: monthly_performance_summary.csv

build_category_summary()
  Group by: product_category_name
  Aggregations: sum(revenue), sum(profit), nunique(order_id),
                mean(price), mean(delay)
  Calculated: profit_margin_%, avg_order_value, freight_ratio_avg, late_rate_%
  Output: category_performance_summary.csv

build_state_summary()
  Group by: customer_state
  Aggregations: sum(revenue), sum(profit), nunique(order_id),
                nunique(customer_id), mean(delay)
  Calculated: profit_margin_%, AOV, freight_ratio, late_rate_%
  Output: state_performance_summary.csv

build_rfm_table()
  Per customer:
    Recency  = days since last purchase (from max date in dataset)
    Frequency = count of orders
    Monetary  = sum of revenue
  Segments assigned by rules:
    Champions    : Recency < 90,  Frequency >= 3
    Loyal        : Recency < 180, Frequency >= 2
    At Risk      : Recency > 180, Frequency >= 2
    New Customers: Frequency = 1, Recency < 90
    Lost         : everything else
  Output: segment_summary.csv

build_clv_table()
  Per customer:
    CLV = Monetary × Frequency
  Output: clv_summary.csv

build_churn_features()
  Per customer:
    churned = 1 if frequency = 1 (never reordered), else 0
    Features: recency, frequency, monetary, avg_profit,
              avg_freight, avg_price, total_items,
              avg_installments, days_active
  Output: churn_features.csv

build_pareto_table()
  Sort products by revenue descending
  Calculate cumulative revenue %
  Flag products where cumulative % <= 80
  Output: pareto analysis in memory
```

---

### Pipeline 3 — Static Performance Charts (Matplotlib)
```
p3_revenue_profit_trend()
  Chart type : Dual-axis line chart
  X-axis     : purchase_month
  Y-axis 1   : total_revenue (blue line)
  Y-axis 2   : total_profit (green line)
  Purpose    : Show revenue and profit trend over 2 years
```

### Pipeline 4 — Static Product & Regional Charts (Matplotlib)
```
p4_top_categories()
  Chart type : Horizontal bar chart (2 charts side by side)
  Left chart : Top 10 categories by revenue
  Right chart: Top 10 categories by profit
  Purpose    : Show which categories matter most

p4_state_map()
  Chart type : Bar chart
  X-axis     : customer_state
  Y-axis     : total_revenue
  Purpose    : Show geographic revenue distribution
```

### Pipeline 5 — Customer Intelligence Charts (Matplotlib)
```
p5_rfm_distribution()
  Chart type : Pie chart + bar chart side by side
  Left       : Customer count per segment (pie)
  Right      : Revenue per segment (bar)
  Purpose    : Show customer quality distribution

p5_pareto_chart()
  Chart type : Bar + line combo (Pareto/80-20 chart)
  Bars       : Revenue per product (sorted descending)
  Line       : Cumulative revenue %
  Purpose    : Show 80/20 rule visually
```

### Pipeline 6 — Interactive Charts (Plotly)
```
p6_interactive_revenue()
  Type   : Area chart with secondary Y axis
  X      : purchase_month
  Y1     : total_revenue (filled area)
  Y2     : total_orders (line)
  Feature: Hover shows exact values, zoom, pan

p6_interactive_categories()
  Type   : Interactive horizontal bar chart
  X      : total_revenue
  Y      : category name
  Feature: Hover, sort, filter
```

### Pipeline 7 — Executive KPI Dashboard (Plotly)
```
KPI Cards row:
  Total Revenue | Total Profit | Total Orders | Customers | Avg Margin

Charts below:
  - Revenue trend line
  - Top categories bar
  - State revenue bar
  - Customer segments donut

Purpose: Single screen summary — what a CEO/manager wants to see
```

---

## 4. SQL Analysis — Question Categories Using PostGrey And MYSQl WorkBench BOth

60 questions organized from basic to advanced:

| Level | Questions | Topics |
|-------|-----------|--------|
| Basic (1–15) | 15 | SELECT, WHERE, ORDER BY, LIMIT, COUNT, SUM |
| Intermediate (16–35) | 20 | GROUP BY, HAVING, JOIN (2-3 tables), subqueries |
| Advanced (36–60) | 25 | CTEs, window functions, RANK, DENSE_RANK, LAG, LEAD, running totals, YoY growth, cohort SQL |

Sample questions:
- Q1: Total revenue by state
- Q15: Top 10 sellers by order count
- Q30: Monthly revenue with 3-month moving average
- Q45: Customer RFM using window functions
- Q55: Year-over-year revenue growth per category
- Q60: Cohort retention table using SQL only

---

## 5. Machine Learning — Detailed Design

### 5.1 Problem Definition
```
Type    : Binary Classification
Target  : churned (1 = churned, 0 = active)
Definition of churn: customer with only 1 order (no repeat purchase)
```

### 5.2 Features Used
```
Feature           | Type    | Why It Matters
------------------|---------|----------------------------------
recency           | int     | How recently did they buy?
frequency         | int     | How often do they buy?
monetary          | float   | How much do they spend?
avg_profit        | float   | Are they profitable customers?
avg_freight       | float   | Do they buy heavy/expensive items?
avg_price         | float   | What price range do they buy?
total_items       | int     | How many items per order?
avg_installments  | float   | Do they pay in installments?
days_active       | int     | How long have they been a customer?
```

### 5.3 Model Designs

**Model 1 — Logistic Regression**
```
Type        : Linear binary classifier
How it works: Finds a line (decision boundary) to separate churned vs not
Good for    : Baseline comparison, highly interpretable
Weakness    : Cannot capture non-linear patterns
```

**Model 2 — Decision Tree**
```
Type        : Tree-based classifier
How it works: Splits data on feature thresholds (e.g. recency > 180?)
Good for    : Interpretable, shows decision rules clearly
Weakness    : Tends to overfit on training data
```

**Model 3 — Random Forest (SELECTED)**
```
Type        : Ensemble of many decision trees
How it works: Builds 100+ trees, each on random subset of data + features
              Final prediction = majority vote of all trees
Good for    : Handles non-linear patterns, resistant to overfitting
Why selected: Highest accuracy + best F1 score across all 3 models
Output      : churn_probability (0.0 to 1.0) per customer
```

### 5.4 Output Design

```
churn_probability >= 0.7  → churn_risk = "High Risk"
churn_probability 0.4–0.7 → churn_risk = "Medium Risk"
churn_probability < 0.4   → churn_risk = "Low Risk"
```

### 5.5 Model Evaluation Metrics

| Metric | What It Measures | Why It Matters Here |
|--------|-----------------|---------------------|
| Accuracy | % of correct predictions | Overall performance |
| Precision | Of predicted churners, how many actually churned | Avoid false alarms |
| Recall | Of actual churners, how many did we catch | Missing churners is costly |
| F1 Score | Balance of precision and recall | Best single metric for imbalanced data |

---

## 6. Streamlit App — Design

```
Page Title: Olist Customer Churn Predictor

Input fields (user fills in):
  - Recency (days since last order)
  - Frequency (number of orders)
  - Monetary (total spend in R$)
  - Average Price (R$)
  - Average Freight (R$)
  - Total Items
  - Average Installments
  - Days Active

On button click:
  - Load saved Random Forest model (churn_model.pkl)
  - Run prediction on input
  - Show: Churn Probability % + Risk Label (High/Medium/Low)
  - Show: What this means for the business
```

---

## 7. Page — Design

```
Section 1 — Hero
  Name, title, one-line project description

Section 2 — The Problem
  What business problem Olist was facing

Section 3 — EDA + Key Charts
  KPI numbers, revenue trend, top categories, 80/20 chart

Section 4 — Customer Analysis
  RFM segments, CLV, cohort chart

Section 5 — SQL Work
  Show 3 example queries (basic, intermediate, advanced)

Section 6 — Power BI Dashboard
  Screenshot + short explanation

Section 7 — ML Churn Prediction
  Model comparison table, best model result

Section 8 — Live Model
  Embedded Streamlit app OR link to it

Section 9 — GitHub Links + Skills
  Repo links, tech stack 
```

---

*LLD.md — Low Level Design*
*For big picture architecture see HLD.md*