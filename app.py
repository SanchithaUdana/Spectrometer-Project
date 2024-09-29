from flask import *
import plotly.graph_objs as go
import numpy as np
from urllib.parse import quote
import matplotlib.pyplot as plt
import io
import random
import random
import time

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


@app.route('/absorbanceParameters')
def absorbanceParameters():
    return render_template('absorbanceParameters.html')


@app.route('/reflectanceParameters')
def reflectanceParameters():
    return render_template('reflectanceParameters.html')


@app.route('/transmissionParameters')
def transmissionParameters():
    return render_template('transmissionParameters.html')


@app.route('/blankReference')
def blankReference():
    return render_template('blankReferance.html')


@app.route('/darkReference')
def darkReference():
    return render_template('darkReferance.html')


@app.route('/calibratePlot')
def calibratePlot():
    return render_template('calibratePlot.html')


#####################
#  Python functions #
#####################

# Function to simulate updating plot data
# Route to serve the live-updating chart image
# Route to generate the plot dynamically
@app.route('/plot-data')
def plot_data():
    # Example sensor data: Replace with actual sensor data retrieval
    x = [595, 595, 596, 596, 595, 596, 597, 595, 595, 596, 596, 595, 596, 593, 595, 596, 595, 596, 597, 594, 595, 596,
         591, 595, 597, 593, 595, 595, 594, 595, 598, 593, 595, 596, 595, 595, 597, 593, 593, 598, 598, 594, 609, 608,
         598, 595, 600, 593, 593, 596, 591, 595, 595, 595, 595, 595, 595, 595, 593, 594, 595, 595, 595, 595, 595, 600,
         593, 593, 602, 594, 595, 605, 597, 595, 600, 590, 590, 593, 594, 591, 595, 593, 594, 596, 595, 593, 595, 595,
         595, 595, 595, 594, 595, 596, 583, 591, 600, 590, 595, 595, 593, 595, 600, 593, 595, 600, 591, 596, 598, 593,
         594, 595, 594, 596, 596, 591, 593, 596, 596, 596, 598, 598, 595, 594, 597, 595, 591, 600, 595, 593, 595, 595,
         595, 595, 591, 595, 595, 595, 595, 595, 595, 595, 594, 600, 595, 593, 600, 593, 594, 597, 593, 596, 595, 591,
         598, 600, 595, 596, 600, 591, 597, 595, 591, 595, 595, 594
         ]
    y = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
         0.3, 0.3, 0.5, 1.3, 1.5, 2.3, 2.5, 3.3, 3.5, 1.3, 1.5, 2.3, 2.5, 3.3, 3.5, 4.3, 4.5, 2.3, 2.5, 3.3, 3.5, 4.3,
         4.5, 5.3, 5.5, 3.3, 3.5, 4.3, 4.5, 5.3, 5.5, 6.3, 6.5, 4.3, 4.5, 5.3, 5.5, 6.3, 6.5, 7.3, 7.5, 5.3, 5.5, 6.3,
         6.5, 7.3, 7.5, 8.3, 8.5, 6.3, 6.5, 7.3, 7.5, 8.3, 8.5, 9.3, 9.5, 7.3, 7.5, 8.3, 8.5, 9.3, 9.5, 10.3, 10.5, 8.3,
         8.5, 9.3, 9.5, 10.3, 10.5, 11.3, 11.5, 9.3, 9.5, 10.3, 10.5, 11.3, 11.5, 12.3, 12.5, 10.3, 10.5, 11.3, 11.5,
         12.3, 12.5, 13.3, 13.5, 11.3, 11.5, 12.3, 12.5, 13.3, 13.5, 14.3, 14.5, 12.3, 12.5, 13.3, 13.5, 14.3, 14.5,
         15.3, 15.5, 13.3, 13.5, 14.3, 14.5, 15.3, 15.5, 16.3, 16.5, 14.3, 14.5, 15.3, 15.5, 16.3, 16.5, 17.3, 17.5,
         15.3, 15.5, 16.3, 16.5, 17.3, 17.5, 18.3, 18.5, 16.3, 16.5, 17.3, 17.5, 18.3, 18.5, 19.3, 19.5, 17.3, 17.5,
         18.3, 18.5, 19.3, 19.5, 20.3
         ]

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sensor Data'))
    fig.update_layout(
        xaxis_title="waves",
        yaxis_title="Absorbance",
        height=320,  # Set height to fit 480x320 resolution
        width=480
    )

    # Define the custom configuration for the toolbar
    config = {
        'displaylogo': False,  # Remove the Plotly logo
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage'
                                   ],  # Remove unwanted buttons
        # 'modeBarButtonsToAdd': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d', 'select2d',
        #                         ],  # Add custom buttons
    }

    # Convert plotly figure to JSON
    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


###################
#  Main Function  #
###################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
