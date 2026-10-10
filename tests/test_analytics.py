"""
Tests for services/analytics.py.
"""
import pytest
import pandas as pd
from services.data_loader import build_master_dataset
from services.analytics import (
    compute_executive_kpis, get_monthly_sales_trend,
    get_category_performance, get_state_performance,
    compute_rfm_segmentation, compute_delivery_analytics
)

@pytest.fixture(scope="module")
def sample_master_df():
    df = build_master_dataset()
    return df

def test_compute_executive_kpis(sample_master_df):
    kpis = compute_executive_kpis(sample_master_df)
    assert isinstance(kpis, dict)
    assert kpis["total_orders"] > 50000
    assert kpis["total_sales"] > 10000000
    assert kpis["aov"] > 50.0
    assert 0 <= kpis["delivered_pct"] <= 100
    assert 0 <= kpis["ontime_pct"] <= 100
    assert 1.0 <= kpis["avg_review_score"] <= 5.0

def test_get_monthly_sales_trend(sample_master_df):
    monthly = get_monthly_sales_trend(sample_master_df)
    assert not monthly.empty
    assert "revenue" in monthly.columns
    assert "orders" in monthly.columns
    assert "mom_growth_pct" in monthly.columns
    assert len(monthly) >= 12

def test_get_category_performance(sample_master_df):
    cat_df = get_category_performance(sample_master_df)
    assert not cat_df.empty
    assert cat_df.iloc[0]['revenue'] >= cat_df.iloc[-1]['revenue']
    assert 0 < cat_df['cumulative_share_pct'].iloc[-1] <= 100.01

def test_get_state_performance(sample_master_df):
    state_df = get_state_performance(sample_master_df)
    assert not state_df.empty
    assert "SP" in state_df['customer_state'].values

def test_compute_rfm_segmentation(sample_master_df):
    # Test on a 10,000 row subset for speed
    subset = sample_master_df.head(10000)
    rfm = compute_rfm_segmentation(subset)
    assert not rfm.empty
    assert "segment" in rfm.columns
    assert "clv_estimate" in rfm.columns
    assert (rfm['clv_estimate'] > 0).all()

def test_compute_delivery_analytics(sample_master_df):
    delivery = compute_delivery_analytics(sample_master_df)
    assert "avg_actual_days" in delivery
    assert delivery["avg_actual_days"] > 0
    assert 0 <= delivery["late_pct"] <= 100
    assert abs(delivery["late_pct"] + delivery["ontime_pct"] - 100.0) < 0.1
