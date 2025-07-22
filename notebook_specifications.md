
# Technical Specification: Jupyter Notebook for Insurance Mitigation Impact Analyzer

## 1. Notebook Overview

This Jupyter Notebook provides an interactive laboratory environment for understanding and quantifying the impact of insurance mitigation on operational risk capital for financial institutions. It models how different insurance policy terms, specifically deductibles and cover limits, affect the transfer of operational losses and the subsequent reduction in net aggregate risk and capital requirements. The concepts and methodologies are aligned with the PRMIA Operational Risk Manager Handbook [1].

### 1.1 Learning Goals

Upon completion of this lab, users will be able to:
-   Understand the key insights related to insurance mitigation for operational risk as outlined in relevant industry handbooks [1].
-   Identify and apply the qualifying criteria and haircuts for insurance policies to be eligible for capital relief.
-   Analyze the effect of policy parameters such as deductible ($d$) and cover limit ($c$) on the allocation of losses between the insured and the insurer.
-   Quantify the capital relief achieved by insurance policies against operational risks, considering factors like insurer claims-paying ability.
-   Visually interpret the payout function of an excess of loss insurance policy and its implications for risk transfer.

### 1.2 Expected Outcomes

The user will interact with a Jupyter Notebook that:
-   Allows for dynamic input of synthetic excess of loss insurance policy parameters and operational loss simulation characteristics.
-   Generates a series of synthetic operational loss events.
-   Calculates and visualizes the transferred and retained portions of individual loss events based on the defined policy.
-   Computes the net aggregate risk after the application of insurance mitigation.
-   Estimates the operational risk capital relief, accounting for the insurer's default probability.
-   Presents key results through interactive plots and summary statistics, demonstrating the practical application of theoretical concepts.

## 2. Mathematical and Theoretical Foundations

This section outlines the core mathematical models and theoretical concepts essential for understanding the insurance mitigation impact analyzer.

### 2.1 Operational Risk and Insurance as a Hedge

Operational risk refers to the risk of loss resulting from inadequate or failed internal processes, people and systems, or from external events. Insurance can serve as a financial hedge against such risks, akin to an option where the insurer reimburses the insured upon policy trigger. Due to the non-standardized nature of insurance policies, regulatory frameworks introduce qualifying criteria and "haircuts" to assess their effectiveness as capital substitutes [1, Chapter 7, page 225].

### 2.2 Excess of Loss Insurance Policies

The notebook focuses on "excess of loss" policies, which are characterized by:
-   **Deductible ($d$)**: The initial amount of each loss that the insured entity must bear before the insurance policy begins to pay out.
-   **Cover Limit ($c$)**: The maximum amount the insurer will pay for any single loss event, once the deductible has been exceeded.

### 2.3 Payout Function of an Excess of Loss Policy ($L_{d,c}$)

For an individual operational loss event $X_i$, the amount of loss transferred to the insurer (the payout from the policy) is given by the operator $L_{d,c}(X_i)$. This function captures the mechanics of the deductible and the cover limit:

$$L_{d,c}(X_i) = \min(\max(X_i - d, 0), c)$$

Where:
-   $\max(X_i - d, 0)$ ensures that no payment is made if the loss $X_i$ is less than or equal to the deductible $d$.
-   $\min(\dots, c)$ caps the insurer's payment at the specified cover limit $c$.

The retained loss by the insured for an event $X_i$ is then simply $X_i - L_{d,c}(X_i)$. This relationship will be visualized to demonstrate the mechanics of risk transfer [1, Figure 2, page 231].

### 2.4 Net Aggregate Risk Calculation ($S_{net}$)

The total (gross) operational risk for a period is represented by the sum of individual loss events: $S_{gross} = \sum_{i=1}^{N} X_i$.
After the impact of insurance, the net aggregate risk ($S_{net}$) is computed as the sum of gross losses minus the sum of all transferred losses over $N$ events:

$$S_{net} = \sum_{i=1}^{N} X_i - \sum_{i=1}^{N} L_{d,c}(X_i)$$

This formula quantifies the reduction in total aggregate risk due to the insurance policy [1, Chapter 7, "Modeling Insurance Policies", page 230].

### 2.5 Capital Relief Estimation and Insurer Default Risk

Capital relief is estimated based on the reduction in unexpected loss (UL) after insurance. However, this relief must be adjusted for the risk of insurer default. The PRMIA Handbook introduces the concepts of Expected Loss (EL) and Unexpected Loss (UL) due to the insurer's default [1, Chapter 7, "Claims Paying Ability", page 229].

-   **Expected Loss (EL) due to insurer default**:
    $$EL_{default} = PD_A \cdot L$$
    Where $PD_A$ is the default probability of the insurer (e.g., based on an A-rating), and $L$ is the insured limit (total maximum potential payout across all covered events, or total insured sum). For simplicity in this lab, $L$ can be considered as the total maximum aggregate payout, which for a single policy with cover $c$ and $N$ events, could be $N \cdot c$ if all events hit the cover, or more realistically, the sum of $L_{d,c}(X_i)$ up to a policy aggregate limit. For the purpose of the lab, $L$ represents the total potential insured amount.
-   **Unexpected Loss (UL) due to insurer default**:
    $$UL_{default} = 3 \cdot \sigma_{default}$$
    The handbook provides an illustrative example where $\sigma_{default}$ is related to $PD_A$ and $L$, leading to $UL_{default} = 3 \cdot PD_A \cdot (1 - PD_A) \cdot L$. For simplicity in this lab, we will use this approximation for the unexpected loss from insurer default.

The effective capital relief is then calculated as the reduction in unexpected loss from the gross portfolio to the net portfolio, adjusted downwards by these default-related losses.
We will estimate Unexpected Loss (UL) for the gross and net portfolios using a high percentile (e.g., 99.9th percentile) of the aggregate loss distributions.
$$UL_{gross} = \text{Percentile}(S_{gross}, 99.9\%)$$
$$UL_{net} = \text{Percentile}(S_{net}, 99.9\%)$$
The nominal capital relief is then $UL_{gross} - UL_{net}$.
The final Capital Relief is therefore:
$$\text{Capital Relief} = (UL_{gross} - UL_{net}) - (EL_{default} + UL_{default})$$

It is important to note that actual regulatory capital relief may be subject to additional haircuts (e.g., residual term, cancellation, coverage mismatches), and an overall capital relief cap (e.g., not exceeding 20% of gross capital), which are acknowledged but not explicitly modeled in the core calculations for this initial lab [1, Table 4, page 230].

## 3. Code Requirements

### 3.1 Expected Libraries

The notebook will utilize the following open-source Python libraries:
-   `numpy`: Essential for numerical operations, array manipulation, and efficient generation of random numbers for simulations.
-   `pandas`: For structured data handling, especially for managing simulated loss events and derived metrics in DataFrames.
-   `scipy.stats`: To provide statistical distributions (e.g., `lognorm` or `pareto`) for simulating loss severity, given their common application in operational risk modeling.
-   `matplotlib.pyplot`: For creating static visualizations, serving as a fallback for interactive plots.
-   `seaborn`: To enhance the aesthetics and statistical plots (e.g., histograms, density plots).
-   `ipywidgets`: Crucial for creating interactive user input controls (sliders, text boxes) within the Jupyter environment, enabling dynamic analysis.
-   `plotly.graph_objects`: For generating interactive and visually appealing plots (e.g., payout function, distribution comparisons). This will be the primary visualization library.

### 3.2 Input/Output Expectations

#### 3.2.1 User Inputs (via `ipywidgets`)
The following parameters will be controllable by the user:
-   **Simulation Parameters:**
    -   `Number of Loss Events (N)`: Integer, controlling the number of individual operational loss events to simulate (e.g., range 1,000 to 100,000).
    -   `Loss Severity Mean (mu)`: Float, representing the mean of the chosen loss severity distribution (e.g., Log-Normal's underlying normal distribution mean).
    -   `Loss Severity Standard Deviation (sigma)`: Float, representing the standard deviation of the chosen loss severity distribution.
-   **Insurance Policy Parameters:**
    -   `Deductible (d)`: Float, the amount of loss retained by the insured per event.
    -   `Cover Limit (c)`: Float, the maximum amount the insurer pays per event.
    -   `Insurer's Default Probability (PD_A)`: Float, representing the likelihood of insurer default (e.g., 0.001 for A-rated).
    -   `Total Insured Limit (L)`: Float, the total maximum amount that could be insured by the policy. This will be used in the $EL_{default}$ and $UL_{default}$ calculations.

#### 3.2.2 Notebook Outputs
The notebook will display the following:
-   **Descriptive Statistics**: Summary statistics (mean, std, min, max, percentiles) for gross loss events, transferred losses, and retained losses.
-   **Aggregate Risk Figures**:
    -   Gross Aggregate Risk ($S_{gross}$)
    -   Net Aggregate Risk ($S_{net}$)
    -   Total Transferred Risk ($\sum L_{d,c}(X_i)$)
-   **Capital Relief Components**:
    -   Unexpected Loss (UL) for Gross Aggregate Risk.
    -   Unexpected Loss (UL) for Net Aggregate Risk.
    -   Nominal Capital Relief (reduction in UL without default adjustment).
    -   Expected Loss (EL) due to insurer default.
    -   Unexpected Loss (UL) due to insurer default.
    -   Final Estimated Capital Relief.

### 3.3 Algorithms or Functions to be Implemented (without code)

-   **`simulate_loss_events(N, mu, sigma)`**:
    -   **Purpose**: Generates a specified number of synthetic operational loss events.
    -   **Inputs**: `N` (number of events), `mu` (mean of underlying normal for Log-Normal distribution), `sigma` (standard deviation of underlying normal for Log-Normal distribution).
    -   **Process**: Uses `scipy.stats.lognorm` (or similar) to draw `N` random samples representing individual loss severities.
    -   **Output**: A `numpy` array of simulated gross loss events ($X_i$).

-   **`calculate_payout_and_retained_loss(loss_events, d, c)`**:
    -   **Purpose**: Applies the excess of loss policy payout function to each simulated event.
    -   **Inputs**: `loss_events` (array of $X_i$), `d` (deductible), `c` (cover limit).
    -   **Process**: Vectorized application of the formula $L_{d,c}(X_i) = \min(\max(X_i - d, 0), c)$ to calculate transferred losses. Calculates retained losses as $X_i - L_{d,c}(X_i)$.
    -   **Output**: Two `numpy` arrays: `transferred_losses` and `retained_losses`.

-   **`calculate_aggregate_risks(gross_losses, transferred_losses)`**:
    -   **Purpose**: Computes the gross and net aggregate risks for the simulated portfolio.
    -   **Inputs**: `gross_losses` (array of $X_i$), `transferred_losses` (array of $L_{d,c}(X_i)$).
    -   **Process**: Sums `gross_losses` to get $S_{gross}$. Sums `transferred_losses`. Calculates $S_{net} = S_{gross} - \sum L_{d,c}(X_i)$.
    -   **Output**: Values for $S_{gross}$, $S_{net}$, and total transferred risk.

-   **`calculate_percentile_risk(losses_array, percentile)`**:
    -   **Purpose**: Calculates a specific percentile of a given loss distribution, typically used for Unexpected Loss (UL).
    -   **Inputs**: `losses_array` (array of loss values), `percentile` (e.g., 99.9).
    -   **Process**: Uses `numpy.percentile` to find the value at the specified percentile.
    -   **Output**: The percentile value.

-   **`estimate_capital_relief(UL_gross, UL_net, PD_A, L_insured)`**:
    -   **Purpose**: Calculates the final capital relief adjusted for insurer default risk.
    -   **Inputs**: `UL_gross` (Unexpected Loss of gross portfolio), `UL_net` (Unexpected Loss of net portfolio), `PD_A` (insurer default probability), `L_insured` (total insured limit for default calculation).
    -   **Process**:
        -   Calculates nominal capital relief: $UL_{gross} - UL_{net}$.
        -   Calculates $EL_{default} = PD_A \cdot L_{insured}$.
        -   Calculates $UL_{default} = 3 \cdot PD_A \cdot (1 - PD_A) \cdot L_{insured}$.
        -   Calculates final capital relief: Nominal Capital Relief - ($EL_{default} + UL_{default}$).
    -   **Output**: Values for $EL_{default}$, $UL_{default}$, Nominal Capital Relief, and Final Capital Relief.

### 3.4 Visualization Requirements

All visualizations will follow best practices for clarity, readability, and accessibility (color-blind-friendly palette, font size $\ge$ 12pt). They will include clear titles, labeled axes, and legends. Interactivity will be enabled using `plotly` or `ipywidgets` where appropriate; a static fallback will be available via `matplotlib.pyplot` saved as PNG if the interactive environment is not supported.

1.  **Payout Function Visualization (Line Plot)**
    -   **Description**: Graphically illustrates the effect of the deductible and cover limit on individual loss events.
    -   **Content**: A plot showing the original loss $X_i$ on the x-axis, and the payout (transferred loss $L_{d,c}(X_i)$) and retained loss ($X_i - L_{d,c}(X_i)$) on the y-axis.
    -   **Elements**: Three lines will be plotted:
        -   A diagonal line representing $X_i$ (total loss).
        -   A line representing $L_{d,c}(X_i)$ (transferred loss, in green).
        -   A line representing $X_i - L_{d,c}(X_i)$ (retained loss, in blue).
        -   Vertical lines or annotations will mark the deductible ($d$) and the sum of deductible and cover limit ($d+c$) on the x-axis.
    -   **Interactivity**: The plot will dynamically update as the user adjusts the `Deductible (d)` and `Cover Limit (c)` sliders.

2.  **Loss Distribution Comparison (Histogram/Density Plot)**
    -   **Description**: Compares the frequency distribution of gross operational losses with the distribution of retained losses after insurance.
    -   **Content**: Overlaid histograms or density plots of:
        -   The simulated `gross_losses`.
        -   The calculated `retained_losses`.
    -   **Elements**: Clearly distinguished colors for gross and retained distributions, labeled axes (e.g., "Loss Amount", "Frequency/Density").
    -   **Interactivity**: The plots will update dynamically as `Number of Loss Events (N)` and `Loss Severity Parameters` are adjusted.

3.  **Capital Relief Summary (Bar Chart or Table)**
    -   **Description**: A concise visual summary of the key financial impacts of insurance mitigation.
    -   **Content**: A bar chart or table displaying:
        -   UL Gross
        -   UL Net
        -   Nominal Capital Relief
        -   EL due to Insurer Default
        -   UL due to Insurer Default
        -   Final Capital Relief
    -   **Elements**: Clearly labeled bars/rows for each metric, with values annotated.
    -   **Interactivity**: Updates automatically based on all relevant input parameters (`d`, `c`, `N`, `Loss Severity Params`, `PD_A`, `L_insured`).

## 4. Additional Notes or Instructions

### 4.1 Assumptions

-   **Synthetic Data Generation**: Operational loss events will be synthetically generated using a statistical distribution (e.g., Log-Normal) for severity. Frequency of events is implicitly handled by `N` directly.
-   **Insurer Default Probability**: The $PD_A$ for the insurer is assumed to be a fixed input value for simplicity.
-   **Haircuts**: For clarity and focus, this lab primarily demonstrates the core mechanics of insurance payout and capital relief. Regulatory haircuts beyond the direct impact of insurer default (e.g., those related to policy term, cancellation, or coverage mismatches) are acknowledged but not explicitly integrated into the quantitative capital relief calculation within this notebook. This simplification allows for a clearer exposition of the primary concepts.
-   **No External Dataset Input**: The notebook will function self-contained by generating its own synthetic loss data, negating the need for external data files for its core functionality.

### 4.2 Constraints

-   **Performance**: The notebook must execute end-to-end on a mid-spec laptop (e.g., 8 GB RAM) within 5 minutes, ensuring a responsive user experience for simulations with typical event counts.
-   **Libraries**: Only open-source Python libraries available on PyPI are permitted.
-   **Documentation**: Each major step in the notebook will be accompanied by both inline code comments and a brief narrative Markdown cell explaining "what" is being done and "why" it is important, enhancing clarity for learners.

### 4.3 Customization Instructions

-   **Interactive Controls**: Learners are encouraged to use the provided sliders, dropdowns, or text inputs to modify the simulation and policy parameters. Observing the immediate impact on visualizations and calculated results is key to grasping the concepts.
-   **Scenario Analysis**: Users can rerun analyses with different combinations of deductible, cover limit, and loss distribution parameters to understand their sensitivity and impact on capital relief.
-   **Help Text**: Inline help text or tooltips will be provided for each interactive control to guide users on its purpose and valid range.

### 4.4 References

[1] PRMIA Operational Risk Manager Handbook, Updated November 2015, The Professional Risk Managers' International Association.
[2] International convergence of capital measurement and capital standards, BIS, June 2006.
[3] Recognising the risk-mitigating impact of insurance in operational risk modeling, BIS, October 2010.
