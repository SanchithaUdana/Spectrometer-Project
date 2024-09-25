from flask import Flask, render_template, redirect, url_for, Response, jsonify
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import io
import random
import numpy as np
import random
import time

import plotly.graph_objs as go

app = Flask(__name__)

# Global variables to simulate live data for the chart
x_data = []
y_data = []


################
#  UI Routing  #
################

@app.route('/')
def splash():
    return render_template('statSegments/splash.html')


@app.route('/navigate_to_index')
def navigate_to_index():
    return render_template('index.html')


@app.route('/analyze')
def analyze():
    return render_template('analyze.html')


# Route for Directories page
@app.route('/directories')
def directories():
    return render_template('directories.html')


# Route for Spectrum page
@app.route('/spectrum')
def spectrum():
    return render_template('analyze.html')


# Route for Models page
@app.route('/models')
def models():
    return render_template('models.html')


# Route for Activity Log page
@app.route('/activity-log')
def activity_log():
    return render_template('activity_log.html')


# Route for Settings page
@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/appType')
def appType():
    return render_template('appType.html')


@app.route('/absorbance')
def absorbance():
    return render_template('absorbance.html')


@app.route('/reflectance')
def reflectance():
    return render_template('reflectance.html')


@app.route('/transmission')
def transmission():
    return render_template('transmission.html')


#####################
#  Python functions #
#####################

# Function to simulate updating plot data
# Route to serve the live-updating chart image
# Route to generate the plot dynamically
@app.route('/plot-data')
def plot_data():
    # Example sensor data: Replace with actual sensor data retrieval
    x = np.linspace(0, 2048, 2048)
    y = np.random.random(2048)

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sensor Data'))
    fig.update_layout(
        xaxis_title="Pixel",
        yaxis_title="Value",
        height=320,  # Set height to fit 480x320 resolution
        width=480,
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                        "fromcurrent": True, "mode": "immediate"}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [None, {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate"}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]
    )

    # Convert plotly figure to JSON
    graphJSON = fig.to_json()
    return jsonify(graphJSON)


###################
#  Main Function  #
###################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
