"""
Tests for utils/validation.py.
"""
from datetime import date
import pandas as pd
from utils.validation import validate_dataframe, validate_date_range, validate_rfm_input

def test_validate_dataframe():
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    valid, err = validate_dataframe(df, ["col1", "col2"])
    assert valid is True
    assert err is None

    valid, err = validate_dataframe(df, ["col1", "col3"])
    assert valid is False
    assert "col3" in err

def test_validate_date_range():
    valid, err = validate_date_range(date(2018, 1, 1), date(2018, 12, 31))
    assert valid is True

    valid, err = validate_date_range(date(2018, 12, 31), date(2018, 1, 1))
    assert valid is False

def test_validate_rfm_input():
    valid, err = validate_rfm_input(30.0, 2, 250.0)
    assert valid is True

    valid, err = validate_rfm_input(-5.0, 1, 100.0)
    assert valid is False
