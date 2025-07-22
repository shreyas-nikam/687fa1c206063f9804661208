import pytest
import pandas as pd
import matplotlib.pyplot as plt
from definition_0a70029b41d841e1b6794728ff348a63 import plot_cumulative_losses

def create_sample_dataframe():
    data = {'gross_loss': [100, 200, 150, 300, 250],
            'retained_loss': [50, 100, 75, 150, 125]}
    return pd.DataFrame(data)


def test_plot_cumulative_losses_valid_dataframe():
    dataframe = create_sample_dataframe()
    try:
        plot_cumulative_losses(dataframe)
    except Exception as e:
        pytest.fail(f"plot_cumulative_losses raised an exception: {e}")
    plt.close()


def test_plot_cumulative_losses_empty_dataframe():
    dataframe = pd.DataFrame({'gross_loss': [], 'retained_loss': []})
    try:
        plot_cumulative_losses(dataframe)
    except Exception as e:
        pytest.fail(f"plot_cumulative_losses raised an exception: {e}")
    plt.close()


def test_plot_cumulative_losses_missing_gross_loss_column():
    dataframe = pd.DataFrame({'retained_loss': [50, 100, 75]})
    with pytest.raises(KeyError) as excinfo:
        plot_cumulative_losses(dataframe)
    assert 'gross_loss' in str(excinfo.value)
    plt.close()


def test_plot_cumulative_losses_missing_retained_loss_column():
    dataframe = pd.DataFrame({'gross_loss': [100, 200, 150]})
    with pytest.raises(KeyError) as excinfo:
        plot_cumulative_losses(dataframe)
    assert 'retained_loss' in str(excinfo.value)
    plt.close()


def test_plot_cumulative_losses_non_numeric_data():
    dataframe = pd.DataFrame({'gross_loss': ['a', 'b', 'c'], 'retained_loss': ['d', 'e', 'f']})
    with pytest.raises(TypeError):
        plot_cumulative_losses(dataframe)
    plt.close()

