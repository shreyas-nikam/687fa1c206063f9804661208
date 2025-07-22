id: 687fa1c206063f9804661208_documentation
summary: Module 6 Lab2 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Crypto Operational Loss Mitigation Simulator: A Streamlit Codelab

## 1. Introduction and Application Overview
Duration: 00:05:00

Welcome to the Crypto Operational Loss Mitigation Simulator Codelab! In this lab, you will gain a comprehensive understanding of a Streamlit application designed to simulate and analyze operational loss events within a hypothetical cryptocurrency exchange environment.

This application is crucial for anyone interested in risk management, particularly in the volatile and rapidly evolving cryptocurrency sector. It provides an interactive platform to:
*   Simulate various operational loss events using different statistical distributions.
*   Analyze the financial impact of these losses.
*   Evaluate the effectiveness of insurance-like mitigation strategies, such as self-insurance funds or traditional excess-of-loss policies.

<aside class="positive">
<b>Why is this important?</b> Operational risk is a significant concern for financial institutions, including crypto exchanges. Understanding and mitigating these risks can prevent substantial financial losses and enhance institutional resilience. This simulator provides a practical tool to explore these concepts.
</aside>

The core concepts explained and demonstrated in this application include:
*   **Loss Severity Distributions**: Modeling the size of losses using Lognormal, Pareto, and Exponential distributions.
*   **Mitigation Policies**: Understanding the role of `Deductible` and `Cover` in reducing net losses.
*   **Transferred vs. Retained Loss**: Differentiating between losses covered by a policy and those borne by the entity.
*   **Aggregate Risk**: Calculating total financial impact over multiple events.

At a high level, the application is structured using Streamlit's modular page system. The `app.py` file acts as the main entry point, handling the sidebar navigation to different functionalities:

```python
# app.py
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we will explore the Crypto Operational Loss Mitigation Simulator.
This application provides an interactive platform for simulating operational loss events within a hypothetical cryptocurrency exchange environment. Its primary objective is to demonstrate and analyze the financial impact of different insurance-like mitigation strategies, such as self-insurance funds or traditional excess-of-loss policies.

formulae, explanations, tables, etc.
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Simulator", "Explanation", "About"])
if page == "Simulator":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Explanation":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "About":
    from application_pages.page3 import run_page3
    run_page3()
# Your code ends
```
As you can see, `app.py` uses `st.sidebar.selectbox` to allow users to navigate between three distinct pages:
*   **Simulator**: Handled by `application_pages/page1.py`, where the core simulation and visualization logic resides.
*   **Explanation**: Handled by `application_pages/page2.py`, providing theoretical background and formulae.
*   **About**: Handled by `application_pages/page3.py`, containing information about the lab and its contributors.

## 2. Setting Up Your Development Environment
Duration: 00:03:00

Before running the application, you need to set up your Python environment and install the necessary libraries.

### Prerequisites

*   Python 3.7+ installed on your system.
*   `pip` (Python package installer) for managing dependencies.

### Installation Steps

1.  **Create a Project Directory**:
    Create a new directory for your project and navigate into it.

    ```bash
    mkdir crypto_loss_simulator
    cd crypto_loss_simulator
    ```

2.  **Create `application_pages` Directory**:
    The application's structure requires an `application_pages` subdirectory.

    ```bash
    mkdir application_pages
    ```

3.  **Create `app.py`**:
    Create a file named `app.py` in the root of your project directory and paste the content provided in the Introduction step.

4.  **Create `page1.py`, `page2.py`, `page3.py`**:
    Create these three files inside the `application_pages` directory and populate them with the respective code provided in the problem description.

    For `application_pages/page1.py`:
    <button>
      [Download page1.py content](https://raw.githubusercontent.com/streamlit/docs/main/docs/knowledge-base/tutorials/create-a-streamlit-app.md) - *Note: This is a placeholder link. You should copy the content directly from the problem description.*
    </button>
    For `application_pages/page2.py`:
    <button>
      [Download page2.py content](https://raw.githubusercontent.com/streamlit/docs/main/docs/knowledge-base/tutorials/create-a-streamlit-app.md) - *Note: This is a placeholder link. You should copy the content directly from the problem description.*
    </button>
    For `application_pages/page3.py`:
    <button>
      [Download page3.py content](https://raw.githubusercontent.com/streamlit/docs/main/docs/knowledge-base/tutorials/create-a-streamlit-app.md) - *Note: This is a placeholder link. You should copy the content directly from the problem description.*
    </button>

    **Important**: Ensure you copy the *entire* content for each file from the problem description, especially for `page1.py` as it contains multiple functions.

5.  **Install Dependencies**:
    The application relies on `streamlit`, `pandas`, `numpy`, `plotly`, and `matplotlib`. Install them using pip:

    ```bash
    pip install streamlit pandas numpy plotly matplotlib
    ```

6.  **Run the Application**:
    Once all files are in place and dependencies are installed, you can run the Streamlit application from your project's root directory:

    ```bash
    streamlit run app.py
    ```
    This command will open the application in your default web browser, usually at `http://localhost:8501`.

## 3. Exploring the Simulator (Page 1: `page1.py`)
Duration: 00:15:00

The `page1.py` file is the heart of the simulator. It contains all the logic for simulating loss events, calculating payouts, and generating interactive visualizations.

### 3.1. Overview of `page1.py`

The `run_page1()` function orchestrates the entire simulation process within this page. It sets up the Streamlit UI elements (sidebar inputs, main content display) and calls helper functions for the core calculations and plotting.

Here's a simplified flow of operations within `page1.py`:

1.  **User Input**: Retrieve simulation parameters (number of events, distribution type, distribution parameters, deductible, cover) from the Streamlit sidebar.
2.  **Simulation**: Generate a DataFrame of `gross_loss` events based on user-selected distribution.
3.  **Calculation**: Compute `transferred_loss` (payout) and `retained_loss` for each event.
4.  **Aggregation**: Calculate total `gross_loss`, `transferred_loss`, and `retained_loss` over all simulated events.
5.  **Visualization**: Generate and display various plots to illustrate the simulation results and the impact of the mitigation strategy.
6.  **Summary**: Present aggregated financial metrics.

### 3.2. Loss Simulation Function: `simulate_loss_events`

This function is responsible for generating random gross loss values based on the chosen statistical distribution and its parameters.

```python
# From application_pages/page1.py
def simulate_loss_events(num_events, distribution_type, **params):
    """Generates gross loss values based on a specified distribution."""
    if distribution_type == 'Lognormal':
        # ... Lognormal calculation ...
        gross_loss = np.random.lognormal(mean=mu, sigma=sigma, size=num_events)
    elif distribution_type == 'Pareto':
        # ... Pareto calculation ...
        gross_loss = (np.random.pareto(alpha, num_events) + 1) * xm
    elif distribution_type == 'Exponential':
        # ... Exponential calculation ...
        gross_loss = np.random.exponential(scale=1/lambda_, size=num_events)
    # ...
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), size=num_events)),
        'gross_loss': gross_loss
    })
    return df
```
*   **`num_events`**: The total number of operational loss incidents to simulate.
*   **`distribution_type`**: Can be 'Lognormal', 'Pareto', or 'Exponential'. Each has different characteristics suitable for modeling loss severities.
*   **`params`**: A dictionary containing the specific parameters for the chosen distribution (e.g., `mu`, `sigma` for Lognormal; `xm`, `alpha` for Pareto; `lambda_` for Exponential).
*   **Output**: A Pandas DataFrame containing `timestamp` (randomly assigned) and `gross_loss` for each simulated event.

### 3.3. Payout and Retained Loss Calculations

These functions apply the mitigation policy logic to each simulated gross loss.

#### `calculate_payout` (Transferred Loss)

This function models the amount covered by an insurance-like policy (or self-insurance fund).

```python
# From application_pages/page1.py
def calculate_payout(gross_loss_series, deductible, cover):
    """Calculates the transferred loss (payout)."""
    payout = (gross_loss_series - deductible).clip(lower=0)
    payout = payout.clip(upper=cover)
    return payout
```
The formula implemented here is:
$$ L_{d,c}(X_i) = \min(\max(X_i - d, 0), c) $$
Where:
*   $X_i$ is the `gross_loss` for event $i$.
*   $d$ is the `deductible`.
*   $c$ is the `cover` (maximum payout).

This means the payout is:
1.  The `gross_loss` minus the `deductible`, but not less than 0 (i.e., no negative payout if loss is less than deductible).
2.  Capped at the `cover` amount.

#### `calculate_retained_loss`

This function determines the portion of the loss that the entity still has to bear after the payout.

```python
# From application_pages/page1.py
def calculate_retained_loss(gross_loss_series, payout_series):
    """Calculates the retained loss by subtracting the payout from the gross loss."""
    return gross_loss_series - payout_series
```
The retained loss is simply the `gross_loss` minus the `transferred_loss` (payout).

### 3.4. Aggregating Losses: `aggregate_losses`

After calculating individual event losses, this function sums them up to provide a total overview.

```python
# From application_pages/page1.py
def aggregate_losses(dataframe):
    """Calculates aggregated losses from the DataFrame."""
    gross_loss = dataframe['gross_loss'].sum()
    transferred_loss = dataframe['transferred_loss'].sum()
    retained_loss = dataframe['retained_loss'].sum()

    return {
        'gross_loss': float(gross_loss),
        'transferred_loss': float(transferred_loss),
        'retained_loss': float(retained_loss)
    }
```
This function returns a dictionary containing the sum of gross, transferred, and retained losses over all simulated events.

### 3.5. Visualizations

`page1.py` includes several plotting functions to visually represent the simulation results. These plots use `plotly` for interactive graphs and `matplotlib` for static plots.

#### `plot_payout_function`

```python
# From application_pages/page1.py
def plot_payout_function(deductible, cover):
    """Generates an interactive Plotly plot visualizing the payout function."""
    gross_loss_range = np.linspace(0, deductible + cover + 2000000, 500)
    payout = np.minimum(np.maximum(gross_loss_range - deductible, 0), cover)
    retained_loss = gross_loss_range - payout
    # ... Plotly figure creation ...
    return fig
```
This plot shows how the payout and retained loss change with varying gross loss amounts, based on the set deductible and cover. It's crucial for understanding the policy's mechanics.

#### `plot_cumulative_losses`

```python
# From application_pages/page1.py
def plot_cumulative_losses(dataframe):
    """Generates a trend plot showing the cumulative gross and net losses."""
    cumulative_gross_loss = dataframe['gross_loss'].cumsum()
    cumulative_retained_loss = dataframe['retained_loss'].cumsum()
    # ... Matplotlib figure creation ...
    return fig
```
This trend plot illustrates the cumulative sum of gross and retained losses over time (or event order). It visually demonstrates the effectiveness of the mitigation strategy in reducing the overall financial burden.

#### `plot_relationship`

```python
# From application_pages/page1.py
def plot_relationship(dataframe):
    """Generates a scatter plot of gross loss vs. transferred loss."""
    # ... Matplotlib figure creation ...
    ax.scatter(dataframe['gross_loss'], dataframe['transferred_loss'], alpha=0.6, color='#2ca02c')
    # ...
    return fig
```
A scatter plot showing each individual `gross_loss` event against its corresponding `transferred_loss`. This plot clearly highlights the impact of the deductible (no payout below deductible) and the cover (payout capping).

#### `plot_aggregated_comparison`

```python
# From application_pages/page1.py
def plot_aggregated_comparison(aggregated_data):
    """Generates a bar chart comparing losses."""
    # ... Matplotlib figure creation ...
    ax.bar(df['Loss Category'], df['Total Amount'], color=colors)
    # ...
    return fig
```
A bar chart comparing the total gross loss, total transferred loss, and total retained loss. This provides a clear, concise summary of the simulation's overall financial outcome.

### 3.6. Streamlit UI Integration (`run_page1` function)

The `run_page1` function ties all these components together.

```python
# From application_pages/page1.py
def run_page1():
    st.header("Crypto Operational Loss Mitigation Simulator")
    # ... introductory markdown ...

    #  Sidebar for Controls 
    st.sidebar.header("Simulation Parameters")
    num_events = st.sidebar.slider("Number of Events", min_value=100, max_value=5000, value=1000, step=100)
    distribution_type = st.sidebar.selectbox("Loss Severity Distribution Type",
                                             options=['Lognormal', 'Pareto', 'Exponential'])
    # ... Conditional parameter inputs based on distribution_type ...

    st.sidebar.divider()
    st.sidebar.header("Mitigation Policy Parameters")
    deductible = st.sidebar.number_input("Deductible (d)", value=1000000.0, min_value=1000.0, max_value=10000000.0, step=100000.0)
    cover = st.sidebar.number_input("Cover (c)", value=5000000.0, min_value=1000.0, max_value=10000000.0, step=100000.0)

    #  Simulation and Calculation Logic 
    try:
        simulated_losses_df = simulate_loss_events(num_events, distribution_type, **distribution_params)
        simulated_losses_df['transferred_loss'] = calculate_payout(simulated_losses_df['gross_loss'], deductible, cover)
        simulated_losses_df['retained_loss'] = calculate_retained_loss(simulated_losses_df['gross_loss'], simulated_losses_df['transferred_loss'])
        aggregated_loss_data = aggregate_losses(simulated_losses_df)

        st.subheader("Simulated Loss Data Overview")
        st.dataframe(simulated_losses_df.head())
        # ... Display descriptive statistics ...

        st.divider()

        st.subheader("Payout Function Visualization")
        payout_fig = plot_payout_function(deductible, cover)
        st.plotly_chart(payout_fig, use_container_width=True)

        # ... Display other plots (cumulative, relationship, aggregated comparison) ...

        st.subheader("Aggregated Financial Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Gross Loss", value=f"\${aggregated_loss_data['gross_loss']:,.2f}")
        # ... Display other metrics ...

    except Exception as e:
        st.error(f"An error occurred: {e}")
```
This section demonstrates how Streamlit widgets like `st.slider`, `st.selectbox`, and `st.number_input` are used to capture user inputs, which then drive the simulation logic. The results are displayed using `st.dataframe`, `st.plotly_chart`, `st.pyplot`, and `st.metric`. Error handling is also included to gracefully manage potential issues with parameter inputs.

## 4. Understanding the Concepts (Page 2: `page2.py`)
Duration: 00:07:00

The `page2.py` file serves as a comprehensive reference for the theoretical concepts and mathematical formulae used in the simulator. It's designed to help users grasp the underlying principles of operational risk modeling and mitigation.

```python
# application_pages/page2.py
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
```

This page uses Streamlit's `st.header` and `st.markdown` to display rich text, including mathematical formulas rendered using LaTeX syntax (enclosed in `$$...$$`). This ensures that complex financial and statistical concepts are presented clearly and accurately.

<aside class="positive">
This page is essential for developers and users alike. For developers, it provides a quick reference to the mathematical models implemented. For users, it offers the necessary theoretical background to interpret the simulation results effectively.
</aside>

## 5. About the Application (Page 3: `page3.py`)
Duration: 00:01:00

The `page3.py` file provides general information about the application, its purpose, contributors, and any relevant references.

```python
# application_pages/page3.py
import streamlit as st

def run_page3():
    st.header("About This Lab")
    st.markdown("""
    This Streamlit application was created as part of the "Module 6 Lab2" assignment. It provides an interactive tool for simulating operational loss events and analyzing the effectiveness of different mitigation strategies in a cryptocurrency exchange environment.

    ### Contributors
    *   [Your Name]
    *   [Another Contributor's Name]

    ### Contact
    For questions or feedback, please contact: [Your Email]

    ### References
    *   PRMIA Operational Risk Manager Handbook [7], [8]
    """)
```
This page serves as a standard "About Us" section, giving credit to the creators and providing contact information for feedback or inquiries. It also lists references, which are vital for academic or professional applications to ensure transparency and allow users to delve deeper into the subject matter.

## 6. Running the Application and Experimenting
Duration: 00:05:00

Now that you understand the different components, let's interact with the application.

1.  **Start the Application**: If you haven't already, run the application from your terminal:

    ```bash
    streamlit run app.py
    ```

2.  **Navigate to the Simulator**: By default, the application should load the "Simulator" page. If not, use the sidebar dropdown menu under "Navigation" to select "Simulator".

3.  **Experiment with Simulation Parameters**:
    *   **Number of Events**: Adjust the slider to see how increasing or decreasing the number of events impacts the statistical stability of the aggregated results.
    *   **Loss Severity Distribution Type**:
        *   Select "Lognormal" and vary `Mean of Log (μ)` and `Std Dev of Log (σ)`. Observe how these changes affect the typical magnitude and spread of losses. Lognormal is good for skewed data where values are always positive.
        *   Switch to "Pareto" and change `Minimum Value (xm)` and `Shape Parameter (α)`. Notice how a lower `α` value creates a "heavier tail," meaning a higher probability of very large, infrequent losses. This is characteristic of extreme events.
        *   Try "Exponential" and modify `Rate Parameter (λ)`. This distribution is often simpler and can represent constant hazard rates.
    *   **Mitigation Policy Parameters**:
        *   **Deductible (d)**: Increase the deductible. You'll see the "Total Retained Loss" increase and "Total Transferred Loss" decrease. The payout function plot will show the shift in the start of the payout.
        *   **Cover (c)**: Increase or decrease the cover. This affects the maximum payout per event. If your cover is too low, many large losses might still result in significant retained losses, as the policy caps its payout.

4.  **Observe the Visualizations**:
    *   **Payout Function Visualization**: Understand how the `deductible` and `cover` directly shape the payout curve. Losses below the deductible are fully retained. Losses between deductible and (deductible + cover) are partially transferred. Losses above (deductible + cover) are partially transferred up to the cover limit, with the rest retained.
    *   **Cumulative Losses Trend**: Pay close attention to the gap between "Cumulative Gross Loss" and "Cumulative Retained Loss". This gap represents the total benefit derived from the mitigation policy. The wider the gap, the more effective the policy.
    *   **Gross Loss vs. Transferred Loss Relationship**: This plot visually confirms the payout logic. You'll see a cluster of points near the origin (losses below deductible with zero payout), and then a linearly increasing payout up to the cover limit, after which it flattens.
    *   **Aggregated Loss Comparison**: This bar chart provides a clear summary of the overall financial impact.

5.  **Review Explanations**: Navigate to the "Explanation" page to refresh your understanding of the mathematical formulae and concepts being simulated. This is especially useful for understanding the impact of distribution parameters.

<aside class="negative">
If you encounter `TypeError` or `ValueError`, double-check the parameter values in the sidebar. Some distributions might be sensitive to very small or very large inputs, or incorrect data types.
</aside>

## 7. Conclusion and Next Steps
Duration: 00:02:00

Congratulations! You have successfully explored the Crypto Operational Loss Mitigation Simulator. You've learned how to set up the environment, understand the core simulation logic, interpret the visualizations, and grasp the underlying mathematical concepts.

This codelab provided a practical example of how Streamlit can be used to build interactive tools for complex financial modeling and risk analysis. The modular design, clear parameter controls, and comprehensive visualizations make it an effective educational and analytical tool.

### Key Takeaways:

*   Operational losses can be modeled using various statistical distributions.
*   Mitigation strategies (like excess-of-loss policies) can significantly reduce the retained financial impact.
*   Streamlit provides a powerful and easy-to-use framework for building interactive data applications in Python.

### Potential Enhancements:

*   **Frequency Modeling**: Extend the simulator to include the frequency of events (e.g., using Poisson distribution) in addition to severity, to calculate aggregate loss distributions more accurately.
*   **Cost of Mitigation**: Incorporate the "premium" or cost associated with the mitigation policy to analyze the net financial benefit.
*   **Multiple Policies**: Allow for layering of multiple policies (e.g., primary, excess layers).
*   **VaR/Expected Shortfall**: Add calculations for Value-at-Risk (VaR) and Expected Shortfall (ES) for both gross and net losses to provide more advanced risk metrics.
*   **Time Series Analysis**: Improve timestamp generation to create more realistic time series of events and allow for trend analysis.
*   **Database Integration**: Store simulation results in a database for historical analysis.

We hope this codelab has been insightful and encourages you to explore further into financial risk modeling and Streamlit application development!
