import pytest
from definition_d2d55d5e7d3a4f2787e36ee60b370d55 import plot_aggregated_comparison
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch

@pytest.fixture
def sample_aggregated_data_dict():
    return {'Gross': 1000, 'Transferred': 300, 'Retained': 700}

@pytest.fixture
def sample_aggregated_data_df():
    return pd.DataFrame({'Loss Category': ['Gross', 'Transferred', 'Retained'],
                         'Total Amount': [1000, 300, 700]})

@patch('matplotlib.pyplot.show')
def test_plot_aggregated_comparison_dict(mock_show, sample_aggregated_data_dict):
    plot_aggregated_comparison(sample_aggregated_data_dict)
    mock_show.assert_called_once()

@patch('matplotlib.pyplot.show')
def test_plot_aggregated_comparison_df(mock_show, sample_aggregated_data_df):
    plot_aggregated_comparison(sample_aggregated_data_df)
    mock_show.assert_called_once()

def test_plot_aggregated_comparison_empty_data():
    with pytest.raises(Exception):
        plot_aggregated_comparison({})
