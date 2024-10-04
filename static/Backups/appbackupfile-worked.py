from flask import Flask, render_template, jsonify
import plotly.graph_objs as go
import numpy as np
import serial
import time
from matplotlib.colors import Normalize

app = Flask(__name__)


#######################
#  Arduino Connection #
#######################

class ArduinoConnector:
    def __init__(self):
        self.ser = None
        self.baudrate_var = "230400"  # Set default baud rate

    def connect_to_arduino(self):
        selected_baudrate = self.baudrate_var
        connectPort = '/dev/ttyUSB0'  # Replace this with your logic to find Arduino port
        if selected_baudrate:
            if connectPort != 'None':
                try:
                    self.ser = serial.Serial(connectPort, baudrate=int(selected_baudrate), timeout=1)
                    print(f'Connected to {connectPort}')
                    return "Connected"
                except Exception as e:
                    print(f'Connection failed: {str(e)}')
                    return f'Connection failed: {str(e)}'
            else:
                return 'Connection Issue'
        else:
            return 'Please select baudrate'

    def read_data(self):
        data_list = []
        while True:
            line = self.ser.readline().decode().strip()
            if not line:
                continue
            elif line == 's':
                continue
            elif line == 'f':
                break
            else:
                data_list.append(int(line))

        if data_list:
            data_list.pop()

        return data_list

    def send_request(self):
        self.ser.write(b'r')

    def read_data_from_arduino(self):
        try:
            self.send_request()  # Send a request to Arduino

            # Add a short delay to allow the Arduino time to respond
            time.sleep(0.5)

            # Try reading the data
            data = self.read_data()

            # Check if data is received
            if data:
                print("Received Data List:", data)
                print("Length of Data List:", len(data))
                return data
            else:
                print("No data received from Arduino.")
                return []
        except Exception as e:
            print(f"Error while reading from Arduino: {e}")
            return []


arduino = ArduinoConnector()


@app.route('/connect')
def connect():
    result = arduino.connect_to_arduino()
    return jsonify({"message": result})


@app.route('/read-data')
def read_data():
    if arduino.ser is None:
        return jsonify({"error": "Arduino not connected"}), 400

    try:
        data = arduino.read_data_from_arduino()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    # Get real-time data from Arduino
    data = arduino.read_data_from_arduino()

    if not data:
        return jsonify({"error": "No data available"}), 500

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(data))  # Simulate wavelength range

    norm = Normalize(vmin=min(data), vmax=max(data))
    y = norm(data)

    # y = np.array(data)  # Use Arduino data as y-values (intensity)
    # Normalize the y-values (optional, depending on your use case)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', line=dict(dash='dot'), name='Sensor Data 1'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Reflectance",
        xaxis=dict(range=[300, 900]),  # x axis
        yaxis=dict(range=[0, 1]),  # y axis
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
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Sensor Data 3'))
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
