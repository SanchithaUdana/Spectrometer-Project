from flask import Flask, render_template, jsonify
import plotly.graph_objs as go
import numpy as np
import mysql.connector

app = Flask(__name__)


################
#  DB Connection (if needed in the future)  #
################
def get_activity_logs():
    # Update these values to match your MySQL/WAMP server settings
    db = mysql.connector.connect(
        host="localhost",  # Or your server IP if remote
        user="root",  # Replace with your MySQL username
        password="root",  # Replace with your MySQL password (WAMP default is empty)
        database="spectro"  # Replace with your MySQL database name
    )

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT action, description, timestamp FROM activity_logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    db.close()
    return logs


@app.route('/activity-log')
def activity_log():
    logs = get_activity_logs()
    return render_template('activityLog.html', activity_logs=logs)


################
#  UI Routing  #
################

@app.route('/')
def splash():
    return render_template('statSegments/splash.html')


@app.route('/navigate_to_index')
def navigate_to_index():
    return render_template('index.html')


# Route for Directories page
# @app.route('/directories')
# def directories():
#     return render_template('directories.html')


# Route for Spectrum page
@app.route('/spectrum')
def spectrum():
    return render_template('spectrum.html')  # Corrected to a distinct template if needed


# Route for Models page
@app.route('/models')
def models():
    return render_template('models.html')


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
    return render_template('whiteReferance.html')  # Corrected the spelling


@app.route('/darkReference')
def darkReference():
    return render_template('darkReference.html')  # Corrected the spelling


@app.route('/calibratePlot')
def calibratePlot():
    return render_template('calibratePlot.html')


@app.route('/activityLog')
def activityLog():
    return render_template('activityLog.html')

@app.route('/logView')
def logView():
    return render_template('logView.html')


#####################
#  Plot Data Routes #
#####################

@app.route('/plot-data')
def plot_data():
    # Generate random dataset
    x = np.linspace(300, 900, 2048)

    wavelengths = np.linspace(300, 800, 2048)
    intensity = (
            np.exp(-((wavelengths - 450) / 50) ** 2)  # First peak around 450nm
            + 0.5 * np.exp(-((wavelengths - 600) / 70) ** 2)  # Second peak around 600nm
    )

    intensity = intensity / np.max(intensity)

    y = intensity

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
        yaxis_title="Absorbance ( Dark )",
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


# New route for the third plot with different data
@app.route('/plot-data4')
def plot_data4():
    # Generate random dataset
    y = np.random.random(2088)
    x = np.linspace(300, 900, 100)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 3'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance ( White & Dark )",
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
@app.route('/plot-data5')
def plot_data5():
    # Generate random dataset
    y = np.random.random(2088)
    x = np.linspace(300, 900, 100)

    # Create Plotly figure
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
