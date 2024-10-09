from matplotlib.colors import Normalize

import whitedata
import darkdata
import numpy as np
import plotly.graph_objects as go

# Convert the list to NumPy arrays for easier calculations
raw = np.array(referanceData.raw)
white = np.array(referanceData.whiteData)
dark = np.array(referanceData.darkData)

# Small constant to avoid division by zero
epsilon = 1e-10

# Calculate the denominator and replace zeros with epsilon
denominator = white - dark
denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number

# Calibrate the data
calibrated = (raw - dark) / denominator

# Mask NaN values as 0
calibrated = np.where(np.isnan(calibrated), 0, calibrated)

norm = Normalize(vmin=min(calibrated), vmax=max(calibrated))

# Create a plot using Plotly
fig = go.Figure()

# Add a line trace for the calibrated data
fig.add_trace(go.Scatter(
    x=np.arange(len(calibrated)),  # x-axis as the index
    y=norm(calibrated),                  # y-axis as the calibrated values
    mode='markers',          # Use lines and markers
    marker=dict(symbol='cross', color='blue'),  # Marker settings
    line=dict(color='blue'),
))

# Customize the layout
fig.update_layout(
    xaxis_title='Index',
    yaxis_title='Calibrated Value',
    showlegend=False,  # No legend is needed for a single plot
    plot_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    width=480,
    height=320
)

# Show the plot
fig.show()
