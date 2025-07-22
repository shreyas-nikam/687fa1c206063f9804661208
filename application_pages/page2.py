
import streamlit as st

def run_page2():
    st.header("Explanation of Concepts and Formulae")
    st.markdown("""
    This page provides detailed explanations of the concepts and formulae used in the Crypto Operational Loss Mitigation Simulator.

    ### Loss Severity Distributions
    The simulator uses different statistical distributions to model the severity of operational loss events. The distributions available are:

    *   **Lognormal Distribution**: This distribution is often used to model phenomena that are positively skewed, such as insurance losses.
        *   **Formula**: The probability density function is given by:
            $$ f(x | \mu, \sigma) = \frac{1}{x\sigma\sqrt{2\pi}} e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}} $$
        *   **Parameters**:
            *   `mu` (μ): Mean of the logarithm of the variable.
            *   `sigma` (σ): Standard deviation of the logarithm of the variable.

    *   **Pareto Distribution**: This distribution is characterized by a heavy tail and is often used to model extreme events.
        *   **Formula**: Its probability density function (Type I) is:
            $$ f(x | x_m, \alpha) = \frac{\alpha x_m^\alpha}{x^{\alpha+1}} \quad \text{for } x \ge x_m $$
        *   **Parameters**:
            *   `xm` ($x_m$): Minimum possible value of the variable.
            *   `alpha` (α): Shape parameter.

    *   **Exponential Distribution**: This distribution is often used to model the time until an event occurs.
        *   **Formula**: Its probability density function is:
            $$ f(x | \lambda) = \lambda e^{-\lambda x} \quad \text{for } x \ge 0 $$
        *   **Parameter**:
            *   `lambda` (λ): Rate parameter.

    ### Mitigation Policy
    The simulator allows you to define a mitigation policy with the following parameters:

    *   **Deductible (d)**: The amount of loss the insured must bear before the policy pays out.
    *   **Cover (c)**: The maximum amount the policy will pay out per loss event.

    The payout function, $L_{d,c}(X_i)$, is defined as:
    $$ L_{d,c}(X_i) = \min(\max(X_i - d, 0), c) $$
    where $X_i$ is the gross loss for event $i$.

    The retained loss is calculated as:
    $$ \text{Retained Loss} = \text{Gross Loss} - \text{Payout} $$

    The aggregate net risk, $S_{net}$, after mitigation is calculated as:
    $$ S_{net} = \sum_{i=1}^{N} X_i - \sum_{i=1}^{N} L_{d,c}(X_i) $$
    This is equivalent to summing the individual retained losses:
    $$ S_{net} = \sum_{i=1}^{N} (X_i - L_{d,c}(X_i)) = \sum_{i=1}^{N} \text{Retained Loss}_i $$
    """)
