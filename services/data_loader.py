"""
Data loading and ETL service for Olist E-commerce Analytics.
Handles loading raw CSV files, cleaning, joining, feature engineering,
and caching to ensure optimal performance.
"""

import os
import pandas as pd
import numpy as np

# Resolve base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PARQUET_CACHE = os.path.join(DATA_DIR, "olist_master.parquet")

def _safe_streamlit_cache_data():
    """Wrapper to use st.cache_data when streamlit is available and running, else no-op."""
    try:
        import streamlit as st
        return st.cache_data
    except Exception:
        def decorator(f):
            return f
        return decorator

@_safe_streamlit_cache_data()
def load_raw_tables(data_dir=DATA_DIR):
    """Loads all raw Olist CSV tables from data_dir."""
    tables = {}
    files = {
        "orders": "olist_orders_dataset.csv",
        "items": "olist_order_items_dataset.csv",
        "customers": "olist_customers_dataset.csv",
        "payments": "olist_order_payments_dataset.csv",
        "reviews": "olist_order_reviews_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "translations": "product_category_name_translation.csv"
    }
    
    for key, filename in files.items():
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            tables[key] = pd.read_csv(path)
        else:
            tables[key] = pd.DataFrame()
            
    return tables

@_safe_streamlit_cache_data()
def build_master_dataset(data_dir=DATA_DIR, use_parquet=True):
    """
    Cleans, aggregates, and joins all 8 Olist tables into a consolidated master dataframe.
    Maintains clean grains: order_item grain with order-level, customer-level, seller-level,
    and product-level metadata.
    """
    parquet_path = os.path.join(data_dir, "olist_master.parquet")
    if use_parquet and os.path.exists(parquet_path):
        try:
            df = pd.read_parquet(parquet_path)
            # Ensure datetime columns
            date_cols = [
                'order_purchase_timestamp', 'order_approved_at',
                'order_delivered_carrier_date', 'order_delivered_customer_date',
                'order_estimated_delivery_date'
            ]
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])
            return df
        except Exception:
            pass  # Fall back to rebuilding

    tables = load_raw_tables(data_dir)
    orders = tables.get("orders")
    items = tables.get("items")
    customers = tables.get("customers")
    payments = tables.get("payments")
    reviews = tables.get("reviews")
    products = tables.get("products")
    sellers = tables.get("sellers")
    translations = tables.get("translations")

    if orders.empty or items.empty:
        return pd.DataFrame()

    # 1. Parse dates in orders
    date_cols = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')

    # 2. Add delivery time & delay metrics
    orders['delivery_days'] = (
        orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
    ).dt.total_seconds() / 86400.0

    orders['estimated_delivery_days'] = (
        orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']
    ).dt.total_seconds() / 86400.0

    orders['delay_days'] = (
        orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']
    ).dt.total_seconds() / 86400.0

    orders['is_delivered'] = orders['order_status'] == 'delivered'
    orders['is_late'] = np.where(
        orders['order_delivered_customer_date'].notna() & orders['order_estimated_delivery_date'].notna(),
        (orders['delay_days'] > 0).astype(int),
        0
    )

    # 3. Aggregate payments at order level to prevent multiplication on join
    if not payments.empty:
        agg_payments = payments.groupby('order_id').agg(
            total_payment=('payment_value', 'sum'),
            payment_installments_max=('payment_installments', 'max'),
            primary_payment_type=('payment_type', lambda x: x.mode().iloc[0] if not x.empty else 'unknown')
        ).reset_index()
    else:
        agg_payments = pd.DataFrame(columns=['order_id', 'total_payment', 'payment_installments_max', 'primary_payment_type'])

    # 4. Aggregate reviews at order level
    if not reviews.empty:
        agg_reviews = reviews.groupby('order_id').agg(
            review_score=('review_score', 'mean'),
            review_count=('review_id', 'count')
        ).reset_index()
    else:
        agg_reviews = pd.DataFrame(columns=['order_id', 'review_score', 'review_count'])

    # 5. Product category translation
    if not products.empty and not translations.empty:
        products = products.merge(translations, on='product_category_name', how='left')
        products['category_name'] = products['product_category_name_english'].fillna(
            products['product_category_name'].fillna('unknown')
        )
    elif not products.empty:
        products['category_name'] = products['product_category_name'].fillna('unknown')

    # 6. Join tables: items -> orders -> customers -> products -> sellers -> payments -> reviews
    master = items.merge(orders, on='order_id', how='inner')

    if not customers.empty:
        master = master.merge(customers, on='customer_id', how='left')

    if not products.empty:
        keep_prod_cols = [c for c in ['product_id', 'category_name', 'product_weight_g', 'product_photos_qty'] if c in products.columns]
        master = master.merge(products[keep_prod_cols], on='product_id', how='left')

    if not sellers.empty:
        keep_seller_cols = [c for c in ['seller_id', 'seller_city', 'seller_state'] if c in sellers.columns]
        master = master.merge(sellers[keep_seller_cols], on='seller_id', how='left')

    if not agg_payments.empty:
        master = master.merge(agg_payments, on='order_id', how='left')

    if not agg_reviews.empty:
        master = master.merge(agg_reviews, on='order_id', how='left')

    # Financial & date helpers
    master['order_item_total'] = master['price'] + master['freight_value']
    master['year_month'] = master['order_purchase_timestamp'].dt.to_period('M').astype(str)
    master['year'] = master['order_purchase_timestamp'].dt.year

    # Save to parquet cache for future super-fast loading
    try:
        master.to_parquet(parquet_path, index=False)
    except Exception:
        pass

    return master
