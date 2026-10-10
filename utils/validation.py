"""
Input validation and data checking utilities.
"""
import pandas as pd
from typing import Tuple, Optional

def validate_dataframe(df: pd.DataFrame, required_columns: list) -> Tuple[bool, Optional[str]]:
    """Checks if the dataframe is not empty and has the required columns."""
    if df is None or df.empty:
        return False, "Dataframe is empty or not loaded."
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"
    return True, None

def validate_date_range(start_date, end_date) -> Tuple[bool, Optional[str]]:
    """Ensures start date is less than or equal to end date."""
    if start_date and end_date and start_date > end_date:
        return False, "Start date cannot be after end date."
    return True, None

def validate_rfm_input(recency_days: float, frequency: int, monetary: float) -> Tuple[bool, Optional[str]]:
    """Validates RFM raw numerical inputs for ML prediction."""
    if recency_days < 0:
        return False, "Recency (days since last purchase) cannot be negative."
    if frequency <= 0:
        return False, "Frequency (number of orders) must be at least 1."
    if monetary < 0:
        return False, "Monetary value cannot be negative."
    return True, None
