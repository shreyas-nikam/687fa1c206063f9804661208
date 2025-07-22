import pytest
import numpy as np
from definition_c21c93652f364a58b848103e4de9f80e import calculate_percentile_risk

@pytest.mark.parametrize("losses_array, percentile, expected", [
    ([1, 2, 3, 4, 5], 50, 3.0),
    ([1, 2, 3, 4, 5], 90, 4.6),
    ([1, 2, 3, 4, 5], 100, 5.0),
    ([1, 1, 1, 1, 1], 50, 1.0),
    ([], 50, ValueError)
])
def test_calculate_percentile_risk(losses_array, percentile, expected):
    if losses_array:
        assert np.isclose(calculate_percentile_risk(losses_array, percentile), expected)
    else:
        with pytest.raises(ValueError):
            calculate_percentile_risk(losses_array, percentile)
