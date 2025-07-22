import pytest
import numpy as np
from definition_569f37d7b8d940f08558abf288901596 import calculate_payout_and_retained_loss

@pytest.mark.parametrize("loss_events, d, c, expected_transferred, expected_retained", [
    (np.array([100, 200, 300]), 50, 100, np.array([50, 100, 100]), np.array([50, 100, 200])),
    (np.array([100, 200, 300]), 150, 50, np.array([0, 50, 50]), np.array([100, 150, 250])),
    (np.array([100, 200, 300]), 50, 200, np.array([50, 150, 200]), np.array([50, 50, 100])),
    (np.array([50, 100, 150]), 100, 50, np.array([0, 0, 50]), np.array([50, 100, 100])),
    (np.array([100]), 100, 50, np.array([0]), np.array([100])),
    (np.array([50]), 100, 50, np.array([0]), np.array([50])),
    (np.array([50]), 0, 50, np.array([50]), np.array([0])),
    (np.array([100]), 50, 0, np.array([0]), np.array([100])), #Cover Limit 0
    (np.array([100]), 100, 0, np.array([0]), np.array([100])), #Deductible = loss_event, Cover Limit 0
    (np.array([0]), 50, 50, np.array([0]), np.array([0])), #loss_event = 0
])
def test_calculate_payout_and_retained_loss(loss_events, d, c, expected_transferred, expected_retained):
    transferred_losses, retained_losses = calculate_payout_and_retained_loss(loss_events, d, c)
    assert np.allclose(transferred_losses, expected_transferred)
    assert np.allclose(retained_losses, expected_retained)
