"""
Tests for services/data_loader.py.
"""
import pytest
import pandas as pd
from services.data_loader import build_master_dataset, load_raw_tables

def test_load_raw_tables():
    tables = load_raw_tables()
    assert isinstance(tables, dict)
    assert "orders" in tables
    assert "items" in tables
    assert not tables["orders"].empty
    assert not tables["items"].empty

def test_build_master_dataset():
    df = build_master_dataset()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[0] > 10000
    
    # Required columns
    expected_cols = [
        'order_id', 'order_purchase_timestamp', 'customer_unique_id',
        'category_name', 'price', 'freight_value', 'order_item_total',
        'delivery_days', 'is_late', 'customer_state'
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"

    # Valid data types
    assert pd.api.types.is_datetime64_any_dtype(df['order_purchase_timestamp'])
    assert df['order_item_total'].sum() > 0
