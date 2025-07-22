import pytest
import pandas as pd
import numpy as np
from definition_51e93c56439b409a90daf532fb87461d import simulate_loss_events

@pytest.mark.parametrize("num_events, distribution_type, params, expected_columns", [
    (10, 'Lognormal', {'mu': 5, 'sigma': 0.5}, ['timestamp', 'gross_loss']),
    (5, 'Pareto', {'xm': 500, 'alpha': 2.0}, ['timestamp', 'gross_loss']),
    (0, 'Exponential', {'lambda': 0.01}, ['timestamp', 'gross_loss']),
])
def test_simulate_loss_events_basic(num_events, distribution_type, params, expected_columns):
    df = simulate_loss_events(num_events, distribution_type, **params)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == expected_columns
    if num_events > 0:
        assert len(df) == num_events

@pytest.mark.parametrize("num_events, distribution_type, params", [
    (10, 'InvalidDistribution', {}),
])
def test_simulate_loss_events_invalid_distribution(num_events, distribution_type, params):
    with pytest.raises(ValueError):
        simulate_loss_events(num_events, distribution_type, **params)

@pytest.mark.parametrize("num_events, distribution_type, params", [
    (10, 'Lognormal', {'mu': 'a', 'sigma': 0.5}),
    (5, 'Pareto', {'xm': 500, 'alpha': 'b'}),
])
def test_simulate_loss_events_invalid_params(num_events, distribution_type, params):
    with pytest.raises(TypeError):
        simulate_loss_events(num_events, distribution_type, **params)

def test_simulate_loss_events_gross_loss_values():
    num_events = 5
    distribution_type = 'Exponential'
    params = {'lambda': 0.1}
    df = simulate_loss_events(num_events, distribution_type, **params)
    assert all(df['gross_loss'] >= 0)

def test_simulate_loss_events_timestamp_dtype():
    num_events = 5
    distribution_type = 'Lognormal'
    params = {'mu': 5, 'sigma': 0.5}
    df = simulate_loss_events(num_events, distribution_type, **params)
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])

