import pytest
import pandas as pd
from src.main import load_data, query_data


def test_load_data():
    """Test that load_data returns the expected DataFrame."""
    df = load_data()
    
    # Check it's a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check columns
    assert list(df.columns) == ["id", "value"]
    
    # Check data
    expected_data = {"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]}
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(df, expected_df)


def test_query_data():
    """Test that query_data correctly filters and transforms data."""
    # Create test DataFrame
    df = pd.DataFrame({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]})
    
    # Run query
    result = query_data(df)
    
    # Check it's a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Check columns (should have id, value, value2)
    assert "id" in result.columns
    assert "value" in result.columns
    assert "value2" in result.columns
    
    # Check that only values >= 20 are included
    assert all(result["value"] >= 20)
    
    # Check that value2 is value * 2
    assert all(result["value2"] == result["value"] * 2)
    
    # Check ordering (should be DESC by id)
    assert result["id"].tolist() == sorted(result["id"].tolist(), reverse=True)
    
    # Check specific results: should have rows with id 4, 3, 2 (values 40, 30, 20)
    assert len(result) == 3
    assert set(result["id"].tolist()) == {2, 3, 4}


def test_query_data_empty_result():
    """Test query_data with data that doesn't match the filter."""
    # Create DataFrame with all values < 20
    df = pd.DataFrame({"id": [1, 2], "value": [10, 15]})
    
    result = query_data(df)
    
    # Should return empty DataFrame with correct columns
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert "id" in result.columns
    assert "value" in result.columns
    assert "value2" in result.columns

