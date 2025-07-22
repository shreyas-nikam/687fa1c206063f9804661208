import pytest
import pandas as pd
from definition_7fac5ad143d24f9eb5872c4db8564af9 import calculate_retained_loss

@pytest.fixture
def sample_series():
    return pd.Series([100, 200, 300, 400, 500])

def test_calculate_retained_loss_typical(sample_series):
    payout_series = pd.Series([10, 20, 30, 40, 50])
    expected_retained_loss = pd.Series([90, 180, 270, 360, 450])
    pd.testing.assert_series_equal(calculate_retained_loss(sample_series, payout_series), expected_retained_loss)

def test_calculate_retained_loss_empty_series():
    gross_loss_series = pd.Series([])
    payout_series = pd.Series([])
    expected_retained_loss = pd.Series([])
    pd.testing.assert_series_equal(calculate_retained_loss(gross_loss_series, payout_series), expected_retained_loss)

def test_calculate_retained_loss_zero_payout(sample_series):
    payout_series = pd.Series([0, 0, 0, 0, 0])
    pd.testing.assert_series_equal(calculate_retained_loss(sample_series, payout_series), sample_series)

def test_calculate_retained_loss_full_payout(sample_series):
    pd.testing.assert_series_equal(calculate_retained_loss(sample_series, sample_series), pd.Series([0, 0, 0, 0, 0]))

def test_calculate_retained_loss_mismatched_lengths(sample_series):
    payout_series = pd.Series([10, 20, 30])
    with pytest.raises(ValueError, match="operands could not be broadcast together with shapes"):
        calculate_retained_loss(sample_series, payout_series)
