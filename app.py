from flask import Flask, render_template, jsonify
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__)

################
#  DB Connection (if needed in the future)  #
################


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
    return render_template('spectrum.html')  # Corrected to a distinct template if needed


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


@app.route('/absorbanceParameters')
def absorbanceParameters():
    return render_template('absorbanceParameters.html')


@app.route('/reflectanceParameters')
def reflectanceParameters():
    return render_template('reflectanceParameters.html')


@app.route('/transmissionParameters')
def transmissionParameters():
    return render_template('transmissionParameters.html')


@app.route('/whiteReference')
def whiteReference():
    return render_template('whiteReference.html')  # Corrected the spelling


@app.route('/darkReference')
def darkReference():
    return render_template('darkReference.html')  # Corrected the spelling


@app.route('/calibratePlot')
def calibratePlot():
    return render_template('calibratePlot.html')


#####################
#  Plot Data Routes #
#####################

@app.route('/plot-data')
def plot_data():
    # Generate random dataset
    y = np.random.random(2088)
    x = np.linspace(300, 900, 100)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 1'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance ( White )",
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


@app.route('/plot-data2')
def plot_data2():
    # Generate random dataset
    y = np.random.random(2088)
    x = np.linspace(300, 900, 100)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 2'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance ( White )",
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
    # Generate random dataset
    y = np.random.random(2088)
    x = np.linspace(300, 900, 100)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 3'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance ( White )",
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
