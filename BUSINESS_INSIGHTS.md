# BUSINESS_INSIGHTS.md
# Olist E-Commerce — Business Problems, Root Causes & Revenue Strategy
# Based on Real Data Analysis | Sheshendra

---

## HOW TO USE THIS FILE

This file answers 3 questions every interviewer or CEO will ask:

1. What problems is this business facing?
2. Why are these problems happening?
3. What should the business DO to fix them and grow revenue?

Every insight below is based on real data from this project.

---

---

# PART 1 — WHAT IS HAPPENING RIGHT NOW

## Business Snapshot (Real Numbers)

| Metric | Value |
|--------|-------|
| Total Revenue (2016–2018) | R$16,110,492 |
| Total Profit | R$5,061,907 |
| Average Profit Margin | 32.3% |
| Total Orders | 96,454 |
| Total Customers | 93,335 |
| Champions (best customers) | 141 only |
| Lost Customers | 45,822 (49% of all customers) |
| High Churn Risk Customers | 90,535 out of 93,335 |

**One line summary:**
Olist is growing in revenue but sitting on a ticking time bomb —
97% of customers are at high risk of never coming back.

---

---

# PART 2 — THE 6 REAL BUSINESS PROBLEMS

---

## PROBLEM 1 — Massive Customer Churn Crisis

### What the data shows:
| Segment | Customers | Churn Rate |
|---------|-----------|-----------|
| Champions | 141 | 0% |
| Loyal | 1,408 | 0% |
| At Risk | 672 | 0% (but about to churn) |
| Lost | 45,822 | **98.74%** |
| New Customers | 45,292 | **100%** |

- 90,535 out of 93,335 customers are High Risk
- Only 237 customers are Low Risk
- 49% of all customers are already Lost
- New customers (45,292) are churning at 100% — they buy once and never return

### Why this is happening:
- No retention strategy exists — customers buy once and disappear
- No loyalty program, no follow-up, no re-engagement campaign
- New customer acquisition is strong but retention is broken
- Average frequency of Lost customers = 1.01 (barely one order ever)

### Business Impact:
- Acquiring a new customer costs 5x more than retaining one
- Olist is spending on acquisition and getting zero repeat value
- Champions (141 customers) have CLV of R$2,174 vs Lost (R$174)
- That is 12.5x more value per loyal customer

### What to do:
```
ACTION 1: Email reactivation campaign for 672 At Risk customers
  → Offer 10–15% discount to bring them back before they go Lost
  → Priority: Do this first. These customers still have some loyalty.

ACTION 2: Onboarding sequence for New Customers
  → After first order: send thank you + recommendation email
  → Day 7: send related products based on first purchase
  → Day 30: send loyalty reward if they reorder

ACTION 3: Champions retention program
  → These 141 customers generate R$2,174 avg CLV
  → Give them VIP status, early access, exclusive offers
  → Losing even 20 champions = R$43,000 CLV lost

ACTION 4: Build subscription / loyalty model
  → Customers who subscribe (monthly box, etc.) have forced frequency
  → Converts one-time buyers into recurring revenue
```

---

## PROBLEM 2 — Heavy Dependence on São Paulo (SP)

### What the data shows:
| State | Revenue | % of Total |
|-------|---------|-----------|
| SP | R$6,041,602 | 37.5% |
| RJ | R$2,158,351 | 13.4% |
| MG | R$1,882,714 | 11.7% |
| ALL other 24 states | R$6,027,825 | 37.4% |

- SP alone = 37.5% of total revenue
- Top 3 states = 62.6% of revenue
- Bottom 5 states combined = R$132,508 (less than 1%)

### Why this is happening:
- Olist started in São Paulo — brand awareness is concentrated there
- Logistics infrastructure is stronger in SE Brazil
- Marketing spend is likely concentrated in SP/RJ/MG

### Business Impact:
- If SP has any economic shock, 37% of revenue is at risk
- Over-dependence on one region = business vulnerability
- Huge untapped market in the other 24 states

### What to do:
```
ACTION 1: Identify high-potential underperforming states
  → RS (R$903K), PR (R$809K) — already decent, can grow with marketing
  → SC, BA, GO — mid tier, good logistics, worth targeting

ACTION 2: Freight subsidy for expansion states
  → North/Northeast states have high freight ratio (0.20–0.22)
  → Subsidize freight for first 3 orders to acquire customers cheaply
  → Once habit is formed, remove subsidy gradually

ACTION 3: Regional seller recruitment
  → Recruit sellers from underserved states (AM, RO, AC, AP)
  → Local sellers = lower freight costs = better margins in those states

ACTION 4: Regional marketing campaigns
  → Target RS and PR first — lower freight ratio, good margins
  → These are the most profitable expansion opportunities
```

---

## PROBLEM 3 — Low Margin Categories Dragging Profitability

### What the data shows:
**Highest margin categories:**
| Category | Revenue | Margin |
|----------|---------|--------|
| moveis_decoracao | R$922K | 35.34% |
| utilidades_domesticas | R$798K | 35.09% |
| ferramentas_jardim | R$593K | 33.67% |
| cama_mesa_banho | R$1.29M | 33.28% |

**Lowest margin categories (problem areas):**
| Category | Revenue | Margin | Issue |
|----------|---------|--------|-------|
| pcs (computers) | R$248K | 23.34% | Too low — freight low but product margin thin |
| portateis_casa | R$50K | 24.39% | Very low margin |
| telefonia_fixa | R$60K | 26.07% | Declining product category |
| relogios_presentes | R$1.31M | 26.20% | **HIGH revenue but LOW margin — biggest risk** |

### The critical insight:
`relogios_presentes` (watches & gifts) is the 2nd highest revenue category
at R$1.31M but has only 26.20% margin — well below the 32.3% average.
This category is pulling down overall profitability significantly.

### What to do:
```
ACTION 1: Price optimization for relogios_presentes
  → It generates R$1.31M revenue — a 3% margin improvement = R$39,000 extra profit
  → Test 5–8% price increase on mid-range watches
  → Bundle watches with gifts to increase AOV and justify higher price

ACTION 2: Promote high-margin categories actively
  → moveis_decoracao (35.34%) and utilidades_domesticas (35.09%)
  → More marketing spend on these = same revenue, more profit
  → Feature them in homepage, email campaigns, promotions

ACTION 3: Review low-revenue + low-margin categories
  → telefonia_fixa (R$60K, 26% margin) — consider removing
  → portateis_casa (R$50K, 24% margin) — too small, too thin
  → These categories take operational effort for minimal return
```

---

## PROBLEM 4 — Revenue is Growing But Plateau is Starting

### What the data shows:
```
2017-01: R$136K   (start of growth)
2017-05: R$610K   (strong growth)
2017-11: R$1.19M  (peak — festive season)
2018-01: R$1.12M  (post-festive dip)
2018-03: R$1.17M  (recovery)
2018-04: R$1.17M  (flat — +0.26% MoM)
2018-05: R$1.17M  (flat — -0.06% MoM)
2018-06: R$1.06M  (declining — -9.18% MoM)
2018-07: R$1.06M  (flat — +0.01% MoM)
2018-08: R$1.02M  (declining — -4.07% MoM)
```

- Strong growth through 2017 (+107% MoM in Feb 2017)
- November 2017 = R$1.19M peak (Black Friday / festive season)
- From April 2018 onwards: 5 consecutive months of flat or negative growth
- Business has hit a growth ceiling

### Why this is happening:
- Customer base is not expanding (new customers churn immediately)
- No repeat purchases to sustain revenue base
- Seasonal spike (Nov 2017) not sustained — no loyalty mechanism
- Revenue is event-driven, not relationship-driven

### What to do:
```
ACTION 1: Convert Black Friday buyers into loyal customers
  → Nov 2017 spike = R$1.19M from one-time buyers
  → Follow-up campaign in Dec/Jan with personalized recommendations
  → Goal: convert even 10% of Nov buyers = 4,700 loyal customers

ACTION 2: Introduce subscription revenue
  → Monthly essentials box from top categories (cama_mesa_banho, beleza_saude)
  → Even R$99/month × 1,000 subscribers = R$1.19M/year guaranteed

ACTION 3: Upsell and cross-sell to existing customers
  → Champions (141 customers) buy 3.55 orders avg
  → Loyal (1,408 customers) buy 2.0 orders avg
  → Target these with higher-value product recommendations
  → Increasing their AOV by 10% = meaningful revenue without new customers
```

---

## PROBLEM 5 — High Late Delivery Rate in Key States

### What the data shows:
| State | Late Rate | Revenue |
|-------|-----------|---------|
| RJ | **13.97%** | R$2.15M |
| RR | 12.20% | R$9K |
| SP | 5.18% | R$6.04M |
| MG | 5.10% | R$1.88M |
| AM | 3.45% | R$28K |

- RJ has 13.97% late delivery rate — nearly 1 in 7 orders is late
- RJ is 2nd biggest state by revenue (R$2.15M)
- Late deliveries = bad reviews = lower ratings = fewer future orders

### Why this is happening:
- RJ has complex logistics (geography, traffic, multiple carriers)
- Possible carrier issues specific to Rio de Janeiro
- Sellers shipping from SP to RJ face longer transit times

### Business Impact:
- Late orders damage review scores
- Lower reviews = lower product ranking = fewer new orders
- RJ customers who get late orders have high churn probability

### What to do:
```
ACTION 1: Audit carriers serving RJ specifically
  → Identify which carriers cause most delays in RJ
  → Switch primary carrier or add backup carrier for RJ

ACTION 2: Set up local warehouse / fulfillment in RJ
  → Stock top 50 products in RJ fulfillment center
  → Reduces transit time from 3–5 days to 1–2 days

ACTION 3: Proactive communication for at-risk deliveries
  → If delivery is predicted late → send SMS/email to customer immediately
  → Offer small discount on next order as apology
  → This reduces negative reviews even when delivery is late
```

---

## PROBLEM 6 — Business Revenue Concentrated in Top 20% Products (80/20 Risk)

### What the data shows:
- 80/20 rule confirmed: top 20% of products generate ~80% of revenue
- Heavy concentration in beleza_saude and relogios_presentes
- If any top category faces supply issues or price competition → big revenue impact

### What to do:
```
ACTION 1: Diversify top product catalog
  → Actively recruit sellers in mid-tier categories
  → Goal: spread revenue across 10+ categories (currently 2–3 dominate)

ACTION 2: Protect top category supply chain
  → For beleza_saude (top revenue): have 3+ seller options per product
  → Single seller dependency = supply risk

ACTION 3: Grow second-tier categories
  → cool_stuff (R$719K, 29.47% margin) — potential to become top 5
  → automotivo (R$696K, 30.74% margin) — growing market in Brazil
  → Targeted seller recruitment + promotions in these categories
```

---

---

# PART 3 — REVENUE GROWTH STRATEGY

## How to Increase Revenue — 3 Levels

### Level 1 — Quick Wins (0–3 months)

| Action | Expected Impact | Effort |
|--------|----------------|--------|
| Reactivate 672 At Risk customers with 10% discount | R$150K–200K saved CLV | Low |
| Price optimization on relogios_presentes (+3% margin) | R$39K extra profit | Low |
| Onboarding email for all new customers | 5–10% conversion to repeat | Low |
| Reduce late deliveries in RJ | Protect R$2.15M revenue base | Medium |

### Level 2 — Medium Term (3–6 months)

| Action | Expected Impact | Effort |
|--------|----------------|--------|
| Champions VIP program for 141 top customers | Protect R$306K CLV base | Medium |
| Expand marketing to RS and PR states | R$200K–400K new revenue | Medium |
| Promote high-margin categories (moveis, utilidades) | +1–2% overall margin | Medium |
| Upsell cross-sell to Loyal segment (1,408 customers) | R$100K–200K incremental | Medium |

### Level 3 — Long Term (6–12 months)

| Action | Expected Impact | Effort |
|--------|----------------|--------|
| Subscription / loyalty model | Predictable recurring revenue | High |
| Regional fulfillment center in RJ | Fix late delivery, protect R$2.15M | High |
| Diversify product categories | Reduce 80/20 concentration risk | High |
| Convert Black Friday spike to loyal base | Sustainable growth past plateau | High |

---

---

# PART 4 — GOLDEN ANSWER FRAMEWORK

## How to answer ANY business question in an interview

Use this structure for every answer:

```
1. BUSINESS CONTEXT    → What was the situation?
2. METRIC DEFINITION   → What did I measure and how?
3. ANALYSIS METHOD     → How did I find the insight?
4. INSIGHT FOUND       → What did the data actually show?
5. BUSINESS IMPACT     → What does this mean in money / risk?
6. RECOMMENDED ACTION  → What should the business do?
```

---

## Example — If interviewer asks: "What was your biggest finding?"

```
1. CONTEXT:
   Olist had strong revenue growth through 2017 but started plateauing in 2018.

2. METRIC:
   I tracked MoM growth rate and customer segment churn rates.

3. METHOD:
   RFM segmentation on 93,335 customers revealed segment health.
   Monthly trend analysis showed growth trajectory.

4. INSIGHT:
   97% of customers (90,535) are High Risk for churn.
   New customers (45,292) are churning at 100% — buying once, never returning.
   Revenue plateau from April 2018 is directly caused by zero retention.

5. IMPACT:
   Without retention fix, revenue will decline further as acquisition costs rise.
   Lost segment alone holds R$7.77M revenue but at 98.74% churn.
   Champions (141 customers) have 12.5x higher CLV than Lost customers.

6. ACTION:
   Priority 1 — Reactivate At Risk (672 customers) before they become Lost.
   Priority 2 — Build onboarding sequence for New Customers.
   Priority 3 — VIP program for Champions to protect highest CLV base.
```

---

## Example — If interviewer asks: "Where would you focus to increase revenue?"

```
1. The fastest revenue lever is retention, not acquisition.
2. Increasing repeat purchase rate from 1% to even 5% across 93K customers
   would add thousands of new orders at zero acquisition cost.
3. Second lever: margin improvement on relogios_presentes.
   R$1.31M category at only 26% margin — 3% improvement = R$39K pure profit.
4. Third lever: geographic expansion to RS and PR.
   Both states have strong margins (32%+) and existing customer bases.
   Low-cost expansion with high return potential.
```

---

---

# PART 5 — KEY NUMBERS TO MEMORIZE FOR INTERVIEWS

```
Total Revenue          : R$16,110,492
Total Profit           : R$5,061,907
Avg Profit Margin      : 32.3%
Total Orders           : 96,454
Total Customers        : 93,335
Date Range             : Oct 2016 – Aug 2018 (22 months)

Top State              : SP — R$6,041,602 (37.5% of revenue)
Top Category           : beleza_saude — R$1,456,027
Worst Margin Category  : pcs (computers) — 23.34%
Best Margin Category   : moveis_decoracao — 35.34%

Champions              : 141 customers | Avg CLV R$2,174
Loyal                  : 1,408 customers | Avg CLV R$608
At Risk                : 672 customers | Avg CLV R$696
Lost                   : 45,822 customers | 98.74% churn
New Customers          : 45,292 customers | 100% churn

High Risk Churn        : 90,535 customers (97% of all)
Low Risk               : 237 customers only

Worst Late Delivery    : RJ — 13.97% late rate
Best On-Time State     : AM — 3.45% late rate

Peak Revenue Month     : Nov 2017 — R$1,194,739 (Black Friday)
Growth Plateau Start   : April 2018 (MoM +0.26%, then flat/negative)
```

---

*BUSINESS_INSIGHTS.md — Built from real Olist data analysis*
*Use this file to prepare for interviews and to guide portfolio storytelling*