import pytest
import pandas as pd
from definition_13224653d83a4e95931fd02638aa8735 import calculate_payout

@pytest.fixture
def sample_series():
    return pd.Series([100, 200, 300, 400, 500])

def test_calculate_payout_no_deductible_full_cover(sample_series):
    result = calculate_payout(sample_series, deductible=0, cover=1000)
    expected = pd.Series([100, 200, 300, 400, 500])
    pd.testing.assert_series_equal(result, expected)

def test_calculate_payout_with_deductible(sample_series):
    result = calculate_payout(sample_series, deductible=150, cover=1000)
    expected = pd.Series([0, 50, 150, 250, 350])
    pd.testing.assert_series_equal(result, expected)

def test_calculate_payout_with_cover(sample_series):
    result = calculate_payout(sample_series, deductible=0, cover=350)
    expected = pd.Series([100, 200, 300, 350, 350])
    pd.testing.assert_series_equal(result, expected)

def test_calculate_payout_deductible_greater_than_all_losses(sample_series):
    result = calculate_payout(sample_series, deductible=600, cover=1000)
    expected = pd.Series([0, 0, 0, 0, 0])
    pd.testing.assert_series_equal(result, expected)

def test_calculate_payout_mixed_deductible_and_cover(sample_series):
    result = calculate_payout(sample_series, deductible=100, cover=200)
    expected = pd.Series([0, 100, 200, 200, 200])
    pd.testing.assert_series_equal(result, expected)
