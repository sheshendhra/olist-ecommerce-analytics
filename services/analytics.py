"""
Analytics calculation service for Olist E-commerce Analytics.
Computes business KPIs, sales trends, category performance, seller metrics,
RFM segmentation, customer lifetime value, and logistics performance.
"""

import pandas as pd
import numpy as np

def compute_executive_kpis(df: pd.DataFrame) -> dict:
    """Computes headline KPIs from filtered or unfiltered master data."""
    if df.empty:
        return {}

    # Unique orders dataframe to prevent duplicate counting of order-level attributes
    order_grain = df.drop_duplicates(subset=['order_id'])

    total_orders = int(order_grain['order_id'].nunique())
    total_sales = float(df['order_item_total'].sum())
    total_items_price = float(df['price'].sum())
    total_freight = float(df['freight_value'].sum())
    aov = float(total_sales / total_orders) if total_orders > 0 else 0.0

    total_customers = int(df['customer_unique_id'].nunique()) if 'customer_unique_id' in df.columns else 0
    total_products = int(df['product_id'].nunique()) if 'product_id' in df.columns else 0
    total_sellers = int(df['seller_id'].nunique()) if 'seller_id' in df.columns else 0

    # Delivery & Review metrics
    delivered_orders = order_grain[order_grain['order_status'] == 'delivered']
    delivered_pct = (len(delivered_orders) / total_orders * 100.0) if total_orders > 0 else 0.0

    valid_deliv = delivered_orders[delivered_orders['delivery_days'].notna() & (delivered_orders['delivery_days'] >= 0)]
    avg_delivery_days = float(valid_deliv['delivery_days'].mean()) if not valid_deliv.empty else 0.0

    valid_delays = delivered_orders[delivered_orders['delay_days'].notna()]
    ontime_pct = float((valid_delays['delay_days'] <= 0).mean() * 100.0) if not valid_delays.empty else 0.0

    avg_review = float(order_grain['review_score'].dropna().mean()) if 'review_score' in order_grain.columns else 0.0

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "total_items_price": total_items_price,
        "total_freight": total_freight,
        "aov": aov,
        "total_customers": total_customers,
        "total_products": total_products,
        "total_sellers": total_sellers,
        "delivered_pct": delivered_pct,
        "ontime_pct": ontime_pct,
        "avg_delivery_days": avg_delivery_days,
        "avg_review_score": avg_review
    }

def get_monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Computes monthly sales, order volume, AOV, and MoM growth."""
    if df.empty or 'order_purchase_timestamp' not in df.columns:
        return pd.DataFrame()

    df_valid = df.dropna(subset=['order_purchase_timestamp']).copy()
    df_valid['month_period'] = df_valid['order_purchase_timestamp'].dt.to_period('M')

    monthly = df_valid.groupby('month_period').agg(
        revenue=('order_item_total', 'sum'),
        items_revenue=('price', 'sum'),
        freight=('freight_value', 'sum'),
        orders=('order_id', 'nunique'),
        customers=('customer_unique_id', 'nunique')
    ).reset_index()

    monthly['month'] = monthly['month_period'].astype(str)
    monthly['aov'] = monthly['revenue'] / monthly['orders']
    monthly['mom_growth_pct'] = monthly['revenue'].pct_change() * 100.0
    monthly['ma_3m'] = monthly['revenue'].rolling(window=3, min_periods=1).mean()

    # Sort chronologically
    monthly = monthly.sort_values('month')
    return monthly

def get_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Computes sales, orders, AOV, and revenue share per product category."""
    if df.empty or 'category_name' not in df.columns:
        return pd.DataFrame()

    cat = df.groupby('category_name').agg(
        revenue=('order_item_total', 'sum'),
        items_price=('price', 'sum'),
        freight=('freight_value', 'sum'),
        orders=('order_id', 'nunique'),
        items_sold=('order_item_id', 'count'),
        avg_price=('price', 'mean'),
        avg_freight=('freight_value', 'mean')
    ).reset_index()

    total_rev = cat['revenue'].sum()
    cat['revenue_share_pct'] = (cat['revenue'] / total_rev * 100.0) if total_rev > 0 else 0.0
    cat = cat.sort_values('revenue', ascending=False).reset_index(drop=True)
    cat['cumulative_share_pct'] = cat['revenue_share_pct'].cumsum()
    return cat

def get_state_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Computes customer state distribution, revenue, and order volume."""
    if df.empty or 'customer_state' not in df.columns:
        return pd.DataFrame()

    states = df.groupby('customer_state').agg(
        revenue=('order_item_total', 'sum'),
        orders=('order_id', 'nunique'),
        customers=('customer_unique_id', 'nunique'),
        avg_freight=('freight_value', 'mean')
    ).reset_index()

    total_rev = states['revenue'].sum()
    states['revenue_share_pct'] = (states['revenue'] / total_rev * 100.0) if total_rev > 0 else 0.0
    states = states.sort_values('revenue', ascending=False).reset_index(drop=True)
    return states

def get_seller_performance(df: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
    """Computes seller volume, revenue, freight ratio, and review score."""
    if df.empty or 'seller_id' not in df.columns:
        return pd.DataFrame()

    sellers = df.groupby('seller_id').agg(
        revenue=('order_item_total', 'sum'),
        orders=('order_id', 'nunique'),
        items_sold=('order_item_id', 'count'),
        seller_state=('seller_state', lambda x: x.iloc[0] if not x.empty else 'unknown'),
        avg_freight=('freight_value', 'mean'),
        avg_review=('review_score', 'mean')
    ).reset_index()

    sellers['freight_ratio_pct'] = (sellers['avg_freight'] / (sellers['revenue'] / sellers['items_sold']) * 100.0).fillna(0)
    sellers = sellers.sort_values('revenue', ascending=False).head(top_n).reset_index(drop=True)
    return sellers

def compute_rfm_segmentation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes genuine RFM (Recency, Frequency, Monetary) metrics and segments
    at the unique customer level (customer_unique_id).
    """
    if df.empty or 'customer_unique_id' not in df.columns or 'order_purchase_timestamp' not in df.columns:
        return pd.DataFrame()

    snapshot_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('customer_unique_id').agg(
        recency=('order_purchase_timestamp', lambda x: (snapshot_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('order_item_total', 'sum'),
        first_purchase=('order_purchase_timestamp', 'min'),
        last_purchase=('order_purchase_timestamp', 'max'),
        total_items=('order_item_id', 'count'),
        avg_review=('review_score', 'mean')
    ).reset_index()

    # Score R, F, M
    # For Recency: lower days = higher score (1 to 5)
    r_bins = [-1, 90, 180, 270, 365, np.inf]
    rfm['r_score'] = pd.cut(rfm['recency'], bins=r_bins, labels=[5, 4, 3, 2, 1]).astype(int)

    # For Frequency: in Olist >96% of customers have 1 order
    def score_frequency(f):
        if f >= 4:
            return 5
        elif f == 3:
            return 4
        elif f == 2:
            return 3
        else:
            return 1
    rfm['f_score'] = rfm['frequency'].apply(score_frequency)

    # For Monetary: quintiles based on revenue
    m_quantiles = rfm['monetary'].quantile([0.2, 0.4, 0.6, 0.8]).tolist()
    m_bins = [-np.inf] + m_quantiles + [np.inf]
    rfm['m_score'] = pd.cut(rfm['monetary'], bins=m_bins, labels=[1, 2, 3, 4, 5], duplicates='drop').astype(int)

    # Segment Assignment
    def assign_segment(row):
        r, f, m = row['r_score'], row['f_score'], row['m_score']
        if r >= 4 and f >= 3:
            return 'Champions'
        elif f >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f == 1 and m >= 4:
            return 'Promising / High Value'
        elif r >= 4 and f == 1:
            return 'Recent Customers'
        elif r == 3:
            return 'Need Attention'
        elif r <= 2 and f >= 2:
            return 'At Risk'
        elif r <= 2 and f == 1:
            return 'Lost / Inactive'
        else:
            return 'Regular'

    rfm['segment'] = rfm.apply(assign_segment, axis=1)

    # Estimated Customer Lifetime Value (CLV)
    # Simple CLV = Monetary * (1 + (Frequency - 1)*0.2)
    rfm['clv_estimate'] = rfm['monetary'] * (1.0 + (rfm['frequency'] - 1) * 0.25)

    return rfm

def compute_delivery_analytics(df: pd.DataFrame) -> dict:
    """Computes comprehensive delivery and logistics metrics."""
    if df.empty:
        return {}

    order_grain = df.drop_duplicates(subset=['order_id']).copy()
    delivered = order_grain[order_grain['order_status'] == 'delivered'].copy()

    # Valid delivery days
    valid_deliv = delivered[delivered['delivery_days'].notna() & (delivered['delivery_days'] >= 0)]

    avg_actual = float(valid_deliv['delivery_days'].mean()) if not valid_deliv.empty else 0.0
    median_actual = float(valid_deliv['delivery_days'].median()) if not valid_deliv.empty else 0.0
    avg_estimated = float(delivered['estimated_delivery_days'].dropna().mean()) if not delivered.empty else 0.0

    late_orders = delivered[delivered['delay_days'] > 0]
    ontime_orders = delivered[delivered['delay_days'] <= 0]
    late_pct = (len(late_orders) / len(delivered) * 100.0) if len(delivered) > 0 else 0.0
    avg_delay_when_late = float(late_orders['delay_days'].mean()) if not late_orders.empty else 0.0

    # Delivery performance by state
    state_delivery = delivered.groupby('customer_state').agg(
        avg_delivery_days=('delivery_days', 'mean'),
        avg_estimated_days=('estimated_delivery_days', 'mean'),
        late_rate=('is_late', 'mean'),
        total_delivered=('order_id', 'count')
    ).reset_index()
    state_delivery['late_pct'] = state_delivery['late_rate'] * 100.0
    state_delivery = state_delivery.sort_values('avg_delivery_days', ascending=False)

    # Delay vs review score correlation
    delay_review = delivered.dropna(subset=['delay_days', 'review_score']).copy()
    delay_review['delivery_status'] = np.where(delay_review['delay_days'] > 0, 'Late Delivery', 'On-Time Delivery')
    score_by_status = delay_review.groupby('delivery_status')['review_score'].mean().to_dict()

    return {
        "avg_actual_days": avg_actual,
        "median_actual_days": median_actual,
        "avg_estimated_days": avg_estimated,
        "late_pct": late_pct,
        "ontime_pct": 100.0 - late_pct,
        "avg_delay_when_late": avg_delay_when_late,
        "state_delivery": state_delivery,
        "score_by_status": score_by_status
    }
