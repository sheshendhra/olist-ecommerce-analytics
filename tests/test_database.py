"""
Tests for services/database.py.
"""
import pytest
from services.database import execute_query, CURATED_SQL_QUERIES

def test_database_connection_and_basic_query():
    df, err = execute_query("SELECT COUNT(*) AS total_rows FROM olist;")
    assert err is None
    assert df is not None
    assert df.iloc[0]['total_rows'] > 0

def test_curated_queries_syntax():
    # Test execution of first 3 curated queries
    for q in CURATED_SQL_QUERIES[:3]:
        df, err = execute_query(q["sql"])
        assert err is None, f"Query failed: {q['id']} with error: {err}"
        assert df is not None
        assert not df.empty
