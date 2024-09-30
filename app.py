from flask import *
import plotly.graph_objs as go
import numpy as np
import json
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
    # Example sensor data for the first plot
    y = [0.986130537, 0.934567681, 0.955928545, 0.88649236, 0.974375868, 0.98904996, 0.841716833, 0.828722015,
         0.893976276, 0.832195949, 0.836127645, 0.917858404, 0.845945889, 0.992145657, 0.904151376, 0.933519638,
         0.904025549, 0.897803434, 0.885960055, 0.821355549, 0.983371006, 0.905645, 0.914920046, 0.982508633,
         0.903279402, 0.88058903, 0.922680174, 0.827214872, 0.956493765, 0.955346919, 0.932484519, 0.817502202,
         0.945659235, 0.830260061, 0.915168381, 0.850923016, 0.995457052, 0.999564292, 0.908917814, 0.922943168,
         0.881096178, 0.903347299, 0.901377787, 0.971693443, 0.936706874, 0.996383268, 0.951604933, 0.808069144,
         0.964861945, 0.945336196, 0.903372409, 0.933358442, 0.905542107, 0.877522036, 0.904303753, 0.9736246,
         0.888992392, 0.981129797, 0.915052314, 0.885935699, 0.951788622, 0.853757621, 0.968260963, 0.828673631]
    x = np.linspace(300, 900, len(y))

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sensor Data 1'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Reflectance%",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


# New route for the second plot with different data
@app.route('/plot-data2')
def plot_data2():
    # Different dataset for the second plot
    y = np.random.random(100)  # Example random data
    x = np.linspace(200, 1000, 100)

    # Create a different Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 2'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


# New route for the third plot with different data
@app.route('/plot-data3')
def plot_data3():
    # Different dataset for the second plot
    y = np.random.random(2088)  # Example random data
    x = np.linspace(300, 900, 100)

    # Create a different Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 3'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


# New route for the forth plot with different data
@app.route('/plot-data4')
def plot_data4():
    # Different dataset for the second plot
    y = np.random.random(100)  # Example random data
    x = np.linspace(300, 900, 50)

    # Create a different Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 3'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


###################
#  Main Function  #
###################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
