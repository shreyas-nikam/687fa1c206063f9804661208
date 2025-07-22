import pytest
from definition_3aa83a58bf214bb3b3e5ce5be7466892 import calculate_aggregate_risks

@pytest.mark.parametrize("gross_losses, transferred_losses, expected", [
    ([100, 200, 300], [10, 20, 30], (600, 540, 60)),
    ([50, 50, 50], [0, 0, 0], (150, 150, 0)),
    ([10, 20, 30], [10, 20, 30], (60, 0, 60)),
    ([100], [50], (100, 50, 50)),
    ([], [], (0, 0, 0)),
])
def test_calculate_aggregate_risks(gross_losses, transferred_losses, expected):
    gross_risk, net_risk, transferred_risk = calculate_aggregate_risks(gross_losses, transferred_losses)
    assert gross_risk == expected[0]
    assert net_risk == expected[1]
    assert transferred_risk == expected[2]
