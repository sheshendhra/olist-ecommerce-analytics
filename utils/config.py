"""
Configuration and branding settings for Olist E-commerce Analytics — Sheshendra.
"""

PROJECT_TITLE = "Olist E-commerce Analytics — Sheshendra"
PROJECT_SUBTITLE = "Brazilian E-Commerce Intelligence, Churn Risk & Executive Decision Platform"
AUTHOR_NAME = "Sheshendra"
ORIGINAL_ATTRIBUTION = (
    "This project builds on an existing open-source analytics project and has been "
    "adapted and enhanced. See the repository's license and applicable third-party notices. "
    "Dataset: Olist Brazilian E-Commerce public dataset on Kaggle."
)
DATASET_SOURCE_URL = "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"

# Visual Theme & Colors
PRIMARY_COLOR = "#4F46E5"     # Indigo
SECONDARY_COLOR = "#06B6D4"   # Cyan
ACCENT_COLOR = "#10B981"      # Emerald Green
WARNING_COLOR = "#F59E0B"     # Amber
DANGER_COLOR = "#EF4444"      # Crimson Red
BACKGROUND_DARK = "#0F172A"   # Slate 900
SURFACE_DARK = "#1E293B"      # Slate 800
TEXT_MUTED = "#94A3B8"        # Slate 400

PLOTLY_TEMPLATE = "plotly_white"

# Currency & Metric Formatting
CURRENCY_SYMBOL = "R$"

def format_currency(val):
    if val is None or val != val:
        return f"{CURRENCY_SYMBOL} 0.00"
    return f"{CURRENCY_SYMBOL} {val:,.2f}"

def format_number(val):
    if val is None or val != val:
        return "0"
    return f"{int(val):,}" if isinstance(val, (int, float)) and val == int(val) else f"{val:,.2f}"

def format_percentage(val):
    if val is None or val != val:
        return "0.0%"
    return f"{val:.1f}%"
