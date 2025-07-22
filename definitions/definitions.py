import pandas as pd
import numpy as np

def simulate_loss_events(num_events, distribution_type, **params):
    """Generates gross loss values based on a specified distribution."""
    if distribution_type == 'Lognormal':
        try:
            mu = params['mu']
            sigma = params['sigma']
            gross_loss = np.random.lognormal(mean=mu, sigma=sigma, size=num_events)
        except KeyError as e:
            raise ValueError(f"Missing parameter: {e}")
        except TypeError:
            raise TypeError("Invalid parameter type.")
    elif distribution_type == 'Pareto':
        try:
            xm = params['xm']
            alpha = params['alpha']
            gross_loss = (np.random.pareto(alpha, num_events) + 1) * xm
        except KeyError as e:
            raise ValueError(f"Missing parameter: {e}")
        except TypeError:
            raise TypeError("Invalid parameter type.")
    elif distribution_type == 'Exponential':
        try:
            lambda_ = params['lambda']
            gross_loss = np.random.exponential(scale=1/lambda_, size=num_events)
        except KeyError as e:
            raise ValueError(f"Missing parameter: {e}")
        except TypeError:
            raise TypeError("Invalid parameter type.")
    else:
        raise ValueError("Invalid distribution type.")

    df = pd.DataFrame({
        'timestamp': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), size=num_events)),
        'gross_loss': gross_loss
    })
    return df

import pandas as pd

def calculate_payout(gross_loss_series, deductible, cover):
    """Calculates the transferred loss (payout)."""
    payout = (gross_loss_series - deductible).clip(lower=0)
    payout = payout.clip(upper=cover)
    return payout

def calculate_retained_loss(gross_loss_series, payout_series):
    """Calculates the retained loss by subtracting the payout from the gross loss."""
    return gross_loss_series - payout_series

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

import numpy as np
import plotly.graph_objects as go
from plotly.offline import iplot

def plot_payout_function(deductible, cover):
    """Generates an interactive plot visualizing the payout function."""

    gross_loss_range = np.linspace(0, deductible + cover + 2000, 500)
    payout = np.minimum(np.maximum(gross_loss_range - deductible, 0), cover)
    retained_loss = gross_loss_range - payout

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=gross_loss_range, y=payout, mode='lines', name='Payout'))
    fig.add_trace(go.Scatter(x=gross_loss_range, y=retained_loss, mode='lines', name='Retained Loss'))
    fig.update_layout(
        title='Payout Function',
        xaxis_title='Gross Loss',
        yaxis_title='Amount',
        hovermode='x unified'
    )

    iplot(fig)

import pandas as pd
import matplotlib.pyplot as plt

def plot_cumulative_losses(dataframe):
    """Generates a trend plot showing the cumulative gross and net losses."""

    cumulative_gross_loss = dataframe['gross_loss'].cumsum()
    cumulative_retained_loss = dataframe['retained_loss'].cumsum()

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_gross_loss, label='Cumulative Gross Loss')
    plt.plot(cumulative_retained_loss, label='Cumulative Retained Loss')

    plt.xlabel('Event Number')
    plt.ylabel('Cumulative Loss')
    plt.title('Cumulative Gross and Retained Losses Over Events')
    plt.legend()
    plt.grid(True)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_relationship(dataframe):
    """Generates a scatter plot of gross loss vs. transferred loss."""
    if not {'gross_loss', 'transferred_loss'}.issubset(dataframe.columns):
        raise KeyError("DataFrame must contain 'gross_loss' and 'transferred_loss' columns.")

    if not pd.api.types.is_numeric_dtype(dataframe['gross_loss']) or not pd.api.types.is_numeric_dtype(dataframe['transferred_loss']):
        raise TypeError("Columns 'gross_loss' and 'transferred_loss' must be numeric.")
    
    if dataframe.empty:
        print("DataFrame is empty, so no plot will be generated.")
        return

    plt.figure(figsize=(8, 6))
    plt.scatter(dataframe['gross_loss'], dataframe['transferred_loss'])
    plt.xlabel('Gross Loss')
    plt.ylabel('Transferred Loss (Payout)')
    plt.title('Relationship between Gross Loss and Transferred Loss')
    plt.grid(True)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_aggregated_comparison(aggregated_data):
    """Generates a bar chart comparing losses."""

    if not aggregated_data:
        raise Exception("No data to plot")

    if isinstance(aggregated_data, dict):
        df = pd.DataFrame({'Loss Category': list(aggregated_data.keys()),
                             'Total Amount': list(aggregated_data.values())})
    elif isinstance(aggregated_data, pd.DataFrame):
        df = aggregated_data.copy()
    else:
        raise TypeError("Input data must be a dictionary or DataFrame")

    plt.figure(figsize=(8, 6))
    plt.bar(df['Loss Category'], df['Total Amount'], color=['red', 'green', 'blue'])
    plt.xlabel('Loss Category')
    plt.ylabel('Total Amount')
    plt.title('Aggregated Loss Comparison')
    plt.tight_layout()
    plt.show()