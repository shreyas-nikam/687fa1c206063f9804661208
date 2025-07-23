import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# --- 4.2. Simulating Operational Loss Events ---
def simulate_loss_events(num_events, distribution_type, **params):
    """Generates gross loss values based on a specified distribution."""
    if distribution_type == 'Lognormal':
        try:
            mu = params['mu']
            sigma = params['sigma']
            gross_loss = np.random.lognormal(mean=mu, sigma=sigma, size=num_events)
        except KeyError as e:
            raise ValueError(f"Missing parameter for Lognormal: {e}")
        except TypeError:
            raise TypeError("Invalid parameter type for Lognormal.")
    elif distribution_type == 'Pareto':
        try:
            xm = params['xm']
            alpha = params['alpha']
            gross_loss = (np.random.pareto(alpha, num_events) + 1) * xm
        except KeyError as e:
            raise ValueError(f"Missing parameter for Pareto: {e}")
        except TypeError:
            raise TypeError("Invalid parameter type for Pareto.")
    elif distribution_type == 'Exponential':
        try:
            lambda_ = params['lambda_'] # Renamed to lambda_ to avoid keyword conflict
            gross_loss = np.random.exponential(scale=1/lambda_, size=num_events)
        except KeyError as e:
            raise ValueError(f"Missing parameter for Exponential: {e}")
        except TypeError:
            raise TypeError("Invalid parameter type for Exponential.")
    else:
        raise ValueError("Invalid distribution type.")

    df = pd.DataFrame({
        'timestamp': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), size=num_events)),
        'gross_loss': gross_loss
    })
    return df

# --- 4.3. Calculating Payout (Transferred Loss) ---
def calculate_payout(gross_loss_series, deductible, cover):
    """Calculates the transferred loss (payout)."""
    payout = (gross_loss_series - deductible).clip(lower=0)
    payout = payout.clip(upper=cover)
    return payout

# --- 4.4. Calculating Retained Loss ---
def calculate_retained_loss(gross_loss_series, payout_series):
    """Calculates the retained loss by subtracting the payout from the gross loss."""
    return gross_loss_series - payout_series

# --- 4.5. Aggregating Losses ---
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

# --- 4.6. Visualizing the Payout Function ---
def plot_payout_function(deductible, cover):
    """Generates an interactive Plotly plot visualizing the payout function."""
    gross_loss_range = np.linspace(0, deductible + cover + 2000000, 500) # Extended range for better visualization
    payout = np.minimum(np.maximum(gross_loss_range - deductible, 0), cover)
    retained_loss = gross_loss_range - payout

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=gross_loss_range, y=payout, mode='lines', name='Payout'))
    fig.add_trace(go.Scatter(x=gross_loss_range, y=retained_loss, mode='lines', name='Retained Loss'))
    fig.update_layout(
        title='Payout Function',
        xaxis_title='Gross Loss ($)',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        font=dict(size=12)
    )
    return fig # Return figure object for Streamlit

# --- 4.7. Visualizing Cumulative Losses (Trend Plot) ---
def plot_cumulative_losses(dataframe):
    """Generates a trend plot showing the cumulative gross and net losses."""
    cumulative_gross_loss = dataframe['gross_loss'].cumsum()
    cumulative_retained_loss = dataframe['retained_loss'].cumsum()

    fig, ax = plt.subplots(figsize=(10, 6)) # Use subplots for Streamlit
    ax.plot(cumulative_gross_loss, label='Cumulative Gross Loss', color='#1f77b4') # Color-blind friendly
    ax.plot(cumulative_retained_loss, label='Cumulative Retained Loss', color='#ff7f0e') # Color-blind friendly

    ax.set_xlabel('Event Number', fontsize=12)
    ax.set_ylabel('Cumulative Loss ($)', fontsize=12)
    ax.set_title('Cumulative Gross and Retained Losses Over Events', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    return fig # Return figure object for Streamlit

# --- 4.8. Visualizing the Relationship between Gross Loss and Transferred Loss ---
def plot_relationship(dataframe):
    """Generates a scatter plot of gross loss vs. transferred loss."""
    if not {'gross_loss', 'transferred_loss'}.issubset(dataframe.columns):
        st.warning("DataFrame must contain 'gross_loss' and 'transferred_loss' columns for relationship plot.")
        return None
    if not pd.api.types.is_numeric_dtype(dataframe['gross_loss']) or not pd.api.types.is_numeric_dtype(dataframe['transferred_loss']):
        st.warning("Columns 'gross_loss' and 'transferred_loss' must be numeric for relationship plot.")
        return None
    if dataframe.empty:
        st.warning("No data to plot for Gross Loss vs. Transferred Loss.")
        return None

    fig, ax = plt.subplots(figsize=(8, 6)) # Use subplots for Streamlit
    ax.scatter(dataframe['gross_loss'], dataframe['transferred_loss'], alpha=0.6, color='#2ca02c') # Color-blind friendly
    ax.set_xlabel('Gross Loss ($)', fontsize=12)
    ax.set_ylabel('Transferred Loss (Payout) ($)', fontsize=12)
    ax.set_title('Relationship between Gross Loss and Transferred Loss', fontsize=14)
    ax.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    return fig # Return figure object for Streamlit

# --- 4.9. Visualizing Aggregated Loss Comparison ---
def plot_aggregated_comparison(aggregated_data):
    """Generates a bar chart comparing losses."""
    if not aggregated_data:
        st.warning("No aggregated data to plot.")
        return None

    if isinstance(aggregated_data, dict):
        df = pd.DataFrame({'Loss Category': list(aggregated_data.keys()),
                           'Total Amount': list(aggregated_data.values())})
    elif isinstance(aggregated_data, pd.DataFrame):
        df = aggregated_data.copy()
    else:
        st.warning("Input data for aggregated comparison must be a dictionary or DataFrame.")
        return None

    fig, ax = plt.subplots(figsize=(8, 6)) # Use subplots for Streamlit
    # Color-blind friendly palette
    colors = ['#d62728', '#17becf', '#7f7f7f'] # Red, Cyan, Grey
    ax.bar(df['Loss Category'], df['Total Amount'], color=colors)
    ax.set_xlabel('Loss Category', fontsize=12)
    ax.set_ylabel('Total Amount ($)', fontsize=12)
    ax.set_title('Aggregated Loss Comparison', fontsize=14)
    fig.tight_layout()
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    return fig # Return figure object for Streamlit


def run_page1():
    st.markdown("""
    This interactive simulator allows you to model operational loss events within a hypothetical cryptocurrency exchange and analyze the impact of different insurance-like mitigation strategies.
    """)
    
    # Add explanation section at the top
    with st.expander("Concepts and Formulae Explanation", expanded=False):
        st.markdown(r"""
        ### Loss Severity Distributions
        The simulator uses different statistical distributions to model the severity of operational loss events:

        *   **Lognormal Distribution**: Often used to model phenomena that are positively skewed, such as insurance losses.
            *   **Formula**: $$ f(x | \mu, \sigma) = \frac{1}{x\sigma\sqrt{2\pi}} e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}} $$
            *   **Parameters**: `mu` (μ): Mean of the logarithm; `sigma` (σ): Standard deviation of the logarithm

        *   **Pareto Distribution**: Characterized by a heavy tail, often used to model extreme events.
            *   **Formula**: $$ f(x | x_m, \alpha) = \frac{\alpha x_m^\alpha}{x^{\alpha+1}} \quad \text{for } x \ge x_m $$
            *   **Parameters**: `xm` ($x_m$): Minimum possible value; `alpha` (α): Shape parameter

        *   **Exponential Distribution**: Often used to model the time until an event occurs.
            *   **Formula**: $$ f(x | \lambda) = \lambda e^{-\lambda x} \quad \text{for } x \ge 0 $$
            *   **Parameter**: `lambda` (λ): Rate parameter

        ### Mitigation Policy
        The simulator uses a mitigation policy with:
        *   **Deductible (d)**: Amount of loss the insured must bear before the policy pays out
        *   **Cover (c)**: Maximum amount the policy will pay out per loss event

        **Payout Function**: $$ L_{d,c}(X_i) = \min(\max(X_i - d, 0), c) $$
        **Retained Loss**: $$ \text{Retained Loss} = \text{Gross Loss} - \text{Payout} $$
        **Aggregate Net Risk**: $$ S_{net} = \sum_{i=1}^{N} (X_i - L_{d,c}(X_i)) $$
        """)
    
    st.divider()

    # --- Sidebar for Controls ---
    st.sidebar.header("Simulation Parameters")
    num_events = st.sidebar.slider("Number of Events", min_value=100, max_value=5000, value=1000, step=100)
    st.sidebar.info("Determines the number of simulated operational loss events.")

    distribution_type = st.sidebar.selectbox("Loss Severity Distribution Type",
                                             options=['Lognormal', 'Pareto', 'Exponential'])
    st.sidebar.info("Select the statistical distribution for loss severity.")

    distribution_params = {}
    if distribution_type == 'Lognormal':
        st.sidebar.subheader("Lognormal Distribution Parameters")
        distribution_params['mu'] = st.sidebar.number_input("Mean of Log (μ)", value=8.0, min_value=0.1, max_value=20.0, step=0.1)
        distribution_params['sigma'] = st.sidebar.number_input("Std Dev of Log (σ)", value=1.0, min_value=0.1, max_value=5.0, step=0.1)
        st.sidebar.info("Used for modeling positively skewed phenomena like insurance losses")
    elif distribution_type == 'Pareto':
        st.sidebar.subheader("Pareto Distribution Parameters")
        distribution_params['xm'] = st.sidebar.number_input("Minimum Value (xm)", value=10000.0, min_value=100.0, max_value=1000000.0, step=1000.0)
        distribution_params['alpha'] = st.sidebar.number_input("Shape Parameter (α)", value=2.0, min_value=0.1, max_value=10.0, step=0.1)
        st.sidebar.info("Heavy-tailed distribution for modeling extreme events")
    elif distribution_type == 'Exponential':
        st.sidebar.subheader("Exponential Distribution Parameters")
        distribution_params['lambda_'] = st.sidebar.number_input("Rate Parameter (λ)", value=0.0001, format="%.5f", min_value=0.00001, max_value=0.1, step=0.00001)
        st.sidebar.info("Models time between events or event frequencies")

    st.sidebar.divider()
    st.sidebar.header("Mitigation Policy Parameters")
    deductible = st.sidebar.number_input("Deductible (d)", value=1000000.0, min_value=1000.0, max_value=10000000.0, step=100000.0)
    st.sidebar.info("The amount of loss the insured must bear before the policy pays out per event.")
    cover = st.sidebar.number_input("Cover (c)", value=5000000.0, min_value=1000.0, max_value=10000000.0, step=100000.0)
    st.sidebar.info("The maximum amount the policy will pay out per loss event.")


    # --- Simulation and Calculation Logic ---
    try:
        simulated_losses_df = simulate_loss_events(num_events, distribution_type, **distribution_params)
        simulated_losses_df['transferred_loss'] = calculate_payout(simulated_losses_df['gross_loss'], deductible, cover)
        simulated_losses_df['retained_loss'] = calculate_retained_loss(simulated_losses_df['gross_loss'], simulated_losses_df['transferred_loss'])
        aggregated_loss_data = aggregate_losses(simulated_losses_df)

        st.subheader("Simulated Loss Data Overview")
        st.markdown("Here's a preview of the simulated loss events and their characteristics:")
        st.dataframe(simulated_losses_df.head())
        st.subheader("Descriptive Statistics of Gross Losses")
        st.write(simulated_losses_df['gross_loss'].describe())

        st.divider()

        st.subheader("Payout Function Visualization")
        st.markdown(r"""
        The payout function $L_{d,c}(X_i)$ illustrates how much of each individual loss event $X_i$ is covered by the mitigation policy, given a deductible $d$ and cover $c$.
        The formula is: $$ L_{d,c}(X_i) = \min(\max(X_i - d, 0), c) $$
        """)
        payout_fig = plot_payout_function(deductible, cover)
        st.plotly_chart(payout_fig, use_container_width=True)

        st.divider()

        st.subheader("Cumulative Losses Trend")
        st.markdown(r"""
        This plot shows the cumulative sum of gross losses and retained losses over the simulated events.
        It highlights the effectiveness of the mitigation strategy in reducing the cumulative financial impact.
        """)
        cumulative_fig = plot_cumulative_losses(simulated_losses_df)
        st.pyplot(cumulative_fig, use_container_width=True)

        st.divider()

        st.subheader("Gross Loss vs. Transferred Loss Relationship")
        st.markdown(r"""
        This scatter plot visualizes the relationship between the original gross loss and the amount transferred (payout) for each event.
        You can observe how the deductible and cover limit affect the payout for different loss magnitudes.
        """)
        relationship_fig = plot_relationship(simulated_losses_df)
        if relationship_fig: # Only display if figure was successfully created
            st.pyplot(relationship_fig, use_container_width=True)


        st.divider()

        st.subheader("Aggregated Loss Comparison")
        st.markdown(r"""
        This bar chart provides an aggregated view of total gross, transferred, and retained losses over all simulated events.
        The aggregate net risk, $S_{net}$, after mitigation is calculated as:
        $$ S_{net} = \sum_{i=1}^{N} X_i - \sum_{i=1}^{N} L_{d,c}(X_i) $$
        This is equivalent to summing the individual retained losses:
        $$ S_{net} = \sum_{i=1}^{N} (X_i - L_{d,c}(X_i)) = \sum_{i=1}^{N} \text{Retained Loss}_i $$
        """)
        aggregated_fig = plot_aggregated_comparison(aggregated_loss_data)
        if aggregated_fig: # Only display if figure was successfully created
            st.pyplot(aggregated_fig, use_container_width=True)

        st.divider()

        st.subheader("Aggregated Financial Summary")
        st.markdown("A summary of the total financial impact:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Gross Loss", value=f"${aggregated_loss_data['gross_loss']:,.2f}")
        with col2:
            st.metric(label="Total Transferred Loss (Payout)", value=f"${aggregated_loss_data['transferred_loss']:,.2f}")
        with col3:
            st.metric(label="Total Retained Loss", value=f"${aggregated_loss_data['retained_loss']:,.2f}")

    except ValueError as e:
        st.error(f"Configuration Error: {e}")
    except TypeError as e:
        st.error(f"Type Error: {e}. Please check parameter inputs.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

