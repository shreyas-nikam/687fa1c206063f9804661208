import pytest
import numpy as np
from definition_d84d5551eb7c49f5a393a2dc42d4f94f import simulate_loss_events

@pytest.mark.parametrize("N, mu, sigma, expected_shape", [
    (100, 0, 1, (100,)),  # Basic test with N=100
    (0, 0, 1, (0,)),    # Edge case: N=0
    (1, 5, 2, (1,)),      # Single event
])
def test_simulate_loss_events_shape(N, mu, sigma, expected_shape):
    result = simulate_loss_events(N, mu, sigma)
    assert result.shape == expected_shape

@pytest.mark.parametrize("N, mu, sigma", [
    (100, 0, 1),  # Basic test with N=100
    (1, 5, 2),      # Single event
])
def test_simulate_loss_events_type(N, mu, sigma):
    result = simulate_loss_events(N, mu, sigma)
    assert isinstance(result, np.ndarray)

def test_simulate_loss_events_sigma_zero():
    with pytest.raises(ValueError):
        simulate_loss_events(100, 0, 0) #sigma cannot be zero for lognorm

def test_simulate_loss_events_negative_N():
    with pytest.raises(ValueError):
        simulate_loss_events(-1, 0, 1) #N cannot be negative

def test_simulate_loss_events_non_numeric_input():
    with pytest.raises(TypeError):
        simulate_loss_events("abc", 0, 1) #N must be numeric
