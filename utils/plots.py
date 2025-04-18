import plotly.graph_objects as go
import streamlit as st

def plot_time_series(data, y=-0.2):
    """
    Plots a time series chart with legend positioned below the graph.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing time series data (index should be datetime)
    y : float, optional
        Vertical position of the legend (negative values place it below chart)
        Default is -0.2 (slightly below the chart)
    """
    # Create Plotly figure
    fig = go.Figure()

    # Add a line plot for each column
    for col in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[col],
                mode='lines',
                name=col
            )
        )

    # Configure layout with legend below
    fig.update_layout(
        legend=dict(
            orientation="h",    # Horizontal layout
            yanchor="top",     # Anchor point
            y=y,               # Vertical position (negative = below)
            xanchor="center",   # Horizontal anchor
            x=0.5              # Center position
        ),
        margin=dict(b=50)      # Add bottom margin to prevent cutoff
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Example usage:
# plot_time_series(your_dataframe, y=-0.25)