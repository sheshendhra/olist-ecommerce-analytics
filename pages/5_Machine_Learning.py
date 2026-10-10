"""
Machine Learning Page for Olist E-commerce Analytics — Sheshendra.
Evaluates Churn Prediction models without data leakage, compares against baseline,
and provides a live interactive prediction simulator.
"""

import streamlit as st
import pandas as pd
from utils.config import (
    PROJECT_TITLE, PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR, DANGER_COLOR
)
from services.data_loader import build_master_dataset
from services.ml_service import (
    train_and_evaluate_models, predict_single_customer, ML_FEATURE_COLS
)
from components.metrics import render_kpi_card
from components.charts import plot_confusion_matrix, plot_feature_importance

st.set_page_config(page_title=f"Machine Learning — {PROJECT_TITLE}", page_icon="🤖", layout="wide")

def main():
    st.title("🤖 Machine Learning: Customer Churn Prediction")
    st.markdown(
        "Statistically rigorous churn classification model predicting whether a customer will churn "
        "(never make a repeat order) based on their first-purchase experience — engineered with **zero data leakage**."
    )

    with st.spinner("Loading ML models and evaluation metrics..."):
        df_master = build_master_dataset()
        ml_results = train_and_evaluate_models(df_master)

    if "error" in ml_results:
        st.error(ml_results["error"])
        st.stop()

    # 1. Headline Model Performance
    rf_metrics = ml_results["models"].get("Random Forest (Balanced)", {})
    baseline_metrics = ml_results["models"].get("Baseline (Majority Dummy)", {})

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Overall Churn Rate", f"{ml_results['churn_rate']:.2f}%", "Single-purchase customers", color=DANGER_COLOR)
    with col2:
        render_kpi_card("Random Forest ROC-AUC", f"{rf_metrics.get('roc_auc', 0):.4f}", "vs 0.5000 Baseline", color=ACCENT_COLOR)
    with col3:
        render_kpi_card("Balanced F1 Score", f"{rf_metrics.get('f1', 0):.4f}", "Harmonic mean P & R", color=PRIMARY_COLOR)
    with col4:
        render_kpi_card("Evaluation Sample", f"{ml_results['test_size']:,}", "Stratified holdout test set", color=SECONDARY_COLOR)

    st.markdown("---")

    # 2. Methodology & Leakage Prevention Explanation
    with st.expander("📘 ML Architecture & Target Leakage Prevention Note", expanded=False):
        st.markdown("""
        ### Why Many Olist Churn Models Suffer From Target Leakage
        - **The Classic Mistake:** Many implementations define `churn = (frequency == 1)` and then feed `frequency` or `days_active` into the feature matrix. Because the model sees whether the customer placed >1 order in the features, it achieves an artificial 98%+ accuracy that is useless in real production.
        - **Our Rigorous Formulation:** We predict whether a customer will churn (never place a second order) **strictly using information available at the time of their first order**:
          1. Basket value & freight cost
          2. Delivery duration & delay flag
          3. Customer review score
          4. Payment installments
        - **Class Imbalance:** Over 96% of Olist customers are single-order buyers. A naive dummy model predicting 'churned' for everyone achieves **96.95% accuracy** but has a **0.5000 ROC-AUC** and 0% recall on repeat buyers. Our balanced Random Forest addresses this using class weights.
        """)

    # 3. Model Comparison Table
    st.markdown("### 📊 Model Comparison & Benchmark")
    comp_rows = []
    for model_name, m in ml_results["models"].items():
        comp_rows.append({
            "Model Name": model_name,
            "ROC-AUC": f"{m.get('roc_auc', 0):.4f}",
            "F1-Score": f"{m.get('f1', 0):.4f}",
            "Precision": f"{m.get('precision', 0):.4f}",
            "Recall": f"{m.get('recall', 0):.4f}",
            "Accuracy": f"{m.get('accuracy', 0):.4f}"
        })
    st.table(pd.DataFrame(comp_rows))

    # 4. Evaluation Charts: Confusion Matrix & Feature Importances
    c1, c2 = st.columns(2)
    with c1:
        if "confusion_matrix" in rf_metrics:
            fig_cm = plot_confusion_matrix(rf_metrics["confusion_matrix"])
            st.plotly_chart(fig_cm, use_container_width=True)
    with c2:
        if "feature_importances" in ml_results:
            fig_fi = plot_feature_importance(ml_results["feature_names"], ml_results["feature_importances"])
            st.plotly_chart(fig_fi, use_container_width=True)

    st.markdown("---")

    # 5. Live Interactive Customer Churn Predictor
    st.markdown("### 🔮 Live Customer Churn Risk Simulator")
    st.markdown("Test hypothetical customer profiles to evaluate predicted churn risk and receive automated retention playbooks:")

    with st.form("churn_prediction_form"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            first_val = st.number_input("First Order Value (R$)", min_value=10.0, max_value=5000.0, value=120.0, step=10.0)
            freight_val = st.number_input("Freight Charges (R$)", min_value=0.0, max_value=500.0, value=18.0, step=2.0)
        with fc2:
            deliv_days = st.slider("Delivery Duration (Days)", min_value=1.0, max_value=60.0, value=11.0, step=1.0)
            is_late_flag = st.selectbox("Arrived Late?", options=[0, 1], format_func=lambda x: "Yes (Late)" if x == 1 else "No (On-Time)")
        with fc3:
            review_input = st.slider("Customer Review Rating (1-5 ⭐)", min_value=1.0, max_value=5.0, value=4.0, step=1.0)
            installments_input = st.slider("Payment Installments", min_value=1, max_value=24, value=2)

        submit_btn = st.form_submit_button("⚡ Predict Customer Churn Risk")

    if submit_btn:
        inputs = {
            'first_order_value': first_val,
            'first_order_freight': freight_val,
            'item_count': 1,
            'payment_installments': installments_input,
            'delivery_days': deliv_days,
            'is_late': is_late_flag,
            'review_score': review_input
        }
        pred = predict_single_customer(inputs)

        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 12px; padding: 20px; border-left: 5px solid {pred.get('badge_color', '#4F46E5')}; margin-top: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #F8FAFC;">Prediction: <span style="color: {pred.get('badge_color', '#4F46E5')};">{pred['churn_risk']}</span></h3>
                <span style="font-size: 1.2rem; font-weight: 700; color: #E2E8F0;">Churn Probability: {pred['churn_probability']*100:.1f}%</span>
            </div>
            <p style="margin: 10px 0 0 0; color: #CBD5E1; font-size: 0.95rem;">
                <b>Recommended Retention Action:</b> {pred['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
