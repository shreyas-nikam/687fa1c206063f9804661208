import numpy as np

def simulate_loss_events(N, mu, sigma):
    """Generates synthetic operational loss events."""
    if not isinstance(N, (int, float)):
        raise TypeError("N must be numeric")
    if N < 0:
        raise ValueError("N cannot be negative")
    if sigma == 0:
        raise ValueError("sigma cannot be zero for lognorm")
    
    if N == 0:
        return np.array([])

    return np.random.lognormal(mean=mu, sigma=sigma, size=N)

import numpy as np
def calculate_payout_and_retained_loss(loss_events, d, c):
    """Calculates transferred and retained losses based on deductible and cover limit."""
    excess = np.maximum(0, loss_events - d)
    transferred_losses = np.minimum(excess, c)
    retained_losses = loss_events - transferred_losses
    return transferred_losses, retained_losses

def calculate_aggregate_risks(gross_losses, transferred_losses):
                """Computes aggregate risks."""

                S_gross = sum(gross_losses) if gross_losses else 0
                S_net = S_gross - sum(transferred_losses) if transferred_losses else S_gross
                total_transferred_risk = sum(transferred_losses) if transferred_losses else 0

                return S_gross, S_net, total_transferred_risk

import numpy as np

def calculate_percentile_risk(losses_array, percentile):
    """Calculates a specific percentile of a given loss distribution."""
    if not losses_array:
        raise ValueError("Losses array cannot be empty")
    return np.percentile(losses_array, percentile)

def estimate_capital_relief(UL_gross, UL_net, PD_A, L_insured):
    """Calculates the final capital relief adjusted for insurer default risk.

    Args:
        UL_gross: Unexpected Loss of gross portfolio.
        UL_net: Unexpected Loss of net portfolio.
        PD_A: Insurer default probability.
        L_insured: Total insured limit for default calculation.

    Returns:
        Values for EL_default, UL_default, Nominal Capital Relief, and Final Capital Relief.
    """

    EL_default = PD_A * L_insured
    UL_default = 3 * PD_A * (1 - PD_A) * L_insured
    nominal_relief = UL_gross - UL_net
    final_relief = nominal_relief - (EL_default + UL_default)

    return EL_default, UL_default, nominal_relief, final_relief