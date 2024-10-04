import plotly.graph_objects as go
import numpy as np
from matplotlib.colors import Normalize

# Initial setup for data and update_flag
data = []
update_flag = True

def update_plot():
    global data, update_flag
    if update_flag:
        send_request()  # Function to send request to get data
        new_data = read_data()  # Function to read the data
        data = new_data

        if len(data) >= 3:
            # Define the desired x-axis range for the wavelengths (300nm to 900nm)
            wavelength_range = np.linspace(300, 900, len(data))

            # Normalize the data to the range [0, 1.0]
            norm = Normalize(vmin=min(data), vmax=max(data))
            normalized_data = norm(data)

            # Create the figure using Plotly
            fig = go.Figure()

            # Add the scatter plot for the intensity vs. wavelength
            fig.add_trace(go.Scatter(
                x=wavelength_range,
                y=normalized_data,
                mode='lines+markers',
                line=dict(dash='dot'),  # Dotted line style
                name='Intensity'
            ))

            # Set the x-axis and y-axis labels
            fig.update_layout(
                title='AI-powered spectrometer spectrum graph',
                xaxis_title='Wavelength',
                yaxis_title='Intensity',
                xaxis=dict(
                    tickmode='array',
                    tickvals=np.linspace(300, 900, 7)  # Set x-axis ticks
                ),
                yaxis=dict(range=[0, 1.1]),  # Set y-axis from 0 to 1.1
                showlegend=True
            )

            # Display the plot
            fig.show()
        else:
            show_error_popup("Not enough data points for plotting.")

        # Schedule the function to be called again after a delay (e.g., 5 ms)
        root.after(5, update_plot)
