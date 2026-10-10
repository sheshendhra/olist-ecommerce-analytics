"""
Tests for services/ml_service.py.
"""
import pytest
from services.data_loader import build_master_dataset
from services.ml_service import (
    build_ml_dataset, load_trained_model, predict_single_customer
)

def test_build_ml_dataset():
    df = build_master_dataset()
    features, X, y = build_ml_dataset(df.head(5000))
    assert not X.empty
    assert len(y) == len(X)
    assert X.isna().sum().sum() == 0
    assert "frequency" not in X.columns, "Leakage check: frequency must not be in X"
    assert "days_active" not in X.columns, "Leakage check: days_active must not be in X"

def test_load_trained_model():
    model, scaler = load_trained_model()
    assert model is not None
    assert scaler is not None

def test_predict_single_customer():
    inputs = {
        'first_order_value': 150.0,
        'first_order_freight': 20.0,
        'item_count': 1,
        'payment_installments': 2,
        'delivery_days': 10.0,
        'is_late': 0,
        'review_score': 5.0
    }
    pred = predict_single_customer(inputs)
    assert "churn_probability" in pred
    assert 0.0 <= pred["churn_probability"] <= 1.0
    assert "churn_risk" in pred
    assert pred["churn_risk"] in ["High Risk", "Medium Risk", "Low Risk"]
    assert "recommendation" in pred
