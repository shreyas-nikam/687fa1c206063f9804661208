import pytest
from definition_202d7066256f4298b043c1d8778c29c2 import plot_payout_function

@pytest.mark.parametrize("deductible, cover", [
    (1000, 5000),
    (0, 1000),
    (2000, 2000),
    (500, 0),
    (-100, 500), #Deductible can't be negative
])
def test_plot_payout_function(deductible, cover):
    # This test case primarily checks if the function runs without errors.
    # Ideally, we'd assert properties of the plot itself, but that's difficult
    # without inspecting the underlying plotting library's data structures.
    try:
        plot_payout_function(deductible, cover)
    except Exception as e:
        pytest.fail(f"plot_payout_function raised an exception: {e}")
