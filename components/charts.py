"""
Interactive Plotly visualization components for Olist E-commerce Analytics.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.config import (
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, WARNING_COLOR,
    DANGER_COLOR, PLOTLY_TEMPLATE
)

def plot_monthly_sales_trend(monthly_df: pd.DataFrame) -> go.Figure:
    """Creates a dual-axis chart for Monthly Revenue and Order Count."""
    if monthly_df.empty:
        return go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Revenue Bar Chart
    fig.add_trace(
        go.Bar(
            x=monthly_df['month'],
            y=monthly_df['revenue'],
            name="Revenue (R$)",
            marker_color=PRIMARY_COLOR,
            opacity=0.85,
            hovertemplate="<b>Month:</b> %{x}<br><b>Revenue:</b> R$ %{y:,.2f}<extra></extra>"
        ),
        secondary_y=False
    )

    # 3-Month Moving Average
    fig.add_trace(
        go.Scatter(
            x=monthly_df['month'],
            y=monthly_df['ma_3m'],
            name="3-Month Moving Avg",
            line=dict(color=ACCENT_COLOR, width=2.5, dash="dash"),
            hovertemplate="<b>3M Moving Avg:</b> R$ %{y:,.2f}<extra></extra>"
        ),
        secondary_y=False
    )

    # Orders Line Chart
    fig.add_trace(
        go.Scatter(
            x=monthly_df['month'],
            y=monthly_df['orders'],
            name="Total Orders",
            line=dict(color=SECONDARY_COLOR, width=3),
            marker=dict(size=6),
            hovertemplate="<b>Orders:</b> %{y:,}<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="<b>Monthly Revenue Trend & Order Volume</b>",
        template=PLOTLY_TEMPLATE,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=420
    )
    fig.update_yaxes(title_text="Revenue (R$)", secondary_y=False, tickformat=",.0f")
    fig.update_yaxes(title_text="Orders Count", secondary_y=True, showgrid=False)
    return fig

def plot_category_revenue(category_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart for Top Product Categories by Revenue."""
    if category_df.empty:
        return go.Figure()

    df_top = category_df.head(top_n).sort_values('revenue', ascending=True)

    fig = px.bar(
        df_top,
        x='revenue',
        y='category_name',
        orientation='h',
        color='revenue',
        color_continuous_scale='Blues',
        text='revenue',
        title=f"<b>Top {top_n} Product Categories by Revenue</b>",
        labels={'revenue': 'Total Revenue (R$)', 'category_name': 'Category'},
        template=PLOTLY_TEMPLATE
    )

    fig.update_traces(
        texttemplate="R$ %{x:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: R$ %{x:,.2f}<br>Share: %{customdata[0]:.1f}%<extra></extra>",
        customdata=df_top[['revenue_share_pct']].values
    )
    fig.update_layout(
        coloraxis_showscale=False,
        height=420,
        margin=dict(l=10, r=60, t=50, b=30)
    )
    return fig

def plot_pareto_analysis(category_df: pd.DataFrame) -> go.Figure:
    """Pareto 80/20 chart showing category revenue bars with cumulative % line."""
    if category_df.empty:
        return go.Figure()

    df_pareto = category_df.head(20).copy()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=df_pareto['category_name'],
            y=df_pareto['revenue'],
            name="Category Revenue",
            marker_color=PRIMARY_COLOR,
            opacity=0.85
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df_pareto['category_name'],
            y=df_pareto['cumulative_share_pct'],
            name="Cumulative Share %",
            line=dict(color=DANGER_COLOR, width=2.5),
            marker=dict(size=6)
        ),
        secondary_y=True
    )

    # 80% Threshold reference line
    fig.add_hline(y=80, line_dash="dot", line_color=WARNING_COLOR, secondary_y=True,
                  annotation_text="80% Revenue Cutoff", annotation_position="top left")

    fig.update_layout(
        title="<b>Pareto Analysis (80/20 Rule) — Top 20 Categories</b>",
        template=PLOTLY_TEMPLATE,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=440,
        xaxis_tickangle=-45
    )
    fig.update_yaxes(title_text="Revenue (R$)", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative %", secondary_y=True, range=[0, 105])
    return fig

def plot_state_sales(state_df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Bar chart for Revenue by Customer State."""
    if state_df.empty:
        return go.Figure()

    df_top = state_df.head(top_n)

    fig = px.bar(
        df_top,
        x='customer_state',
        y='revenue',
        color='revenue',
        color_continuous_scale='Purples',
        text='revenue',
        title=f"<b>Top {top_n} Customer States by Revenue</b>",
        labels={'revenue': 'Total Revenue (R$)', 'customer_state': 'State Code'},
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(
        texttemplate="R$ %{y:,.0f}",
        textposition="outside",
        hovertemplate="<b>State:</b> %{x}<br>Revenue: R$ %{y:,.2f}<br>Share: %{customdata[0]:.1f}%<extra></extra>",
        customdata=df_top[['revenue_share_pct']].values
    )
    fig.update_layout(
        coloraxis_showscale=False,
        height=400,
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig

def plot_rfm_segments(rfm_df: pd.DataFrame) -> go.Figure:
    """Treemap chart showing customer segment distribution and total spend."""
    if rfm_df.empty or 'segment' not in rfm_df.columns:
        return go.Figure()

    seg_summary = rfm_df.groupby('segment').agg(
        customers=('customer_unique_id', 'count'),
        total_revenue=('monetary', 'sum'),
        avg_clv=('clv_estimate', 'mean')
    ).reset_index()

    fig = px.treemap(
        seg_summary,
        path=['segment'],
        values='customers',
        color='total_revenue',
        color_continuous_scale='Viridis',
        title="<b>RFM Customer Segment Distribution (Size: Customers, Color: Revenue)</b>",
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Customers: %{value:,}<br>Total Revenue: R$ %{color:,.2f}<extra></extra>"
    )
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10))
    return fig

def plot_delivery_delay_distribution(delivered_df: pd.DataFrame) -> go.Figure:
    """Histogram of delivery delays (positive = late, negative = early)."""
    if delivered_df.empty or 'delay_days' not in delivered_df.columns:
        return go.Figure()

    delays = delivered_df['delay_days'].dropna().clip(lower=-25, upper=25)

    fig = px.histogram(
        delays,
        x='delay_days',
        nbins=50,
        color_discrete_sequence=[PRIMARY_COLOR],
        title="<b>Distribution of Delivery Performance vs Estimated Date</b>",
        labels={'delay_days': 'Days Difference (Negative = Early, Positive = Late)'},
        template=PLOTLY_TEMPLATE
    )
    fig.add_vline(x=0, line_dash="dash", line_color=DANGER_COLOR,
                  annotation_text="Estimated Delivery Date (0)", annotation_position="top right")
    fig.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=30))
    return fig

def plot_delivery_vs_review(score_dict: dict) -> go.Figure:
    """Bar chart showing customer review score for on-time vs late delivery."""
    if not score_dict:
        return go.Figure()

    df_score = pd.DataFrame([
        {"status": k, "score": v, "color": ACCENT_COLOR if "On-Time" in k else DANGER_COLOR}
        for k, v in score_dict.items()
    ])

    fig = px.bar(
        df_score,
        x='status',
        y='score',
        color='status',
        color_discrete_map={k: ACCENT_COLOR if "On-Time" in k else DANGER_COLOR for k in score_dict.keys()},
        text='score',
        title="<b>Impact of Delivery Punctuality on Review Rating</b>",
        labels={'status': 'Delivery Status', 'score': 'Average Review Score (1-5)'},
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(texttemplate="%{y:.2f} ⭐", textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 5.5], height=380)
    return fig

def plot_confusion_matrix(cm_matrix: list) -> go.Figure:
    """Confusion matrix heatmap for ML evaluation."""
    labels = ["Repeat Customer (0)", "Churned Customer (1)"]
    fig = px.imshow(
        cm_matrix,
        x=labels,
        y=labels,
        labels=dict(x="Predicted Class", y="Actual True Class", color="Count"),
        color_continuous_scale="Blues",
        text_auto=True,
        title="<b>Test Set Confusion Matrix (Class-Weighted Random Forest)</b>",
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(height=380, margin=dict(l=30, r=30, t=40, b=30))
    return fig

def plot_feature_importance(features: list, importances: list) -> go.Figure:
    """Feature importance horizontal bar chart."""
    df_fi = pd.DataFrame({"feature": features, "importance": importances}).sort_values('importance', ascending=True)
    fig = px.bar(
        df_fi,
        x='importance',
        y='feature',
        orientation='h',
        color='importance',
        color_continuous_scale='Teal',
        title="<b>Churn Prediction Feature Importances</b>",
        labels={'importance': 'Gini Importance', 'feature': 'Feature Name'},
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(coloraxis_showscale=False, height=360, margin=dict(l=10, r=20, t=40, b=20))
    return fig
