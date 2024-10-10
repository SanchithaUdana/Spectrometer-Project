import time
import numpy as np
import plotly.graph_objs as go
import serial
from flask import Flask, render_template, jsonify, make_response
from matplotlib.colors import Normalize

import whitedata
import darkdata
import calData

app = Flask(__name__)


#######################
#  Arduino Connection #
#######################

class ArduinoConnector:
    def __init__(self):
        self.ser = None
        self.baudrate_var = "230400"  # Set default baud rate
        # self.connect_to_arduino()
        # self.read_data_from_arduino()

    def connect_to_arduino(self):
        selected_baudrate = self.baudrate_var
        connectPort = 'COM3'  # Replace this with your logic to find Arduino port
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


#######################################
# Reflectance Plot Analyzing  Routing #
#######################################

@app.route('/connect')
def connect():
    # global freeze_plot01
    # freeze_plot01 = False  # Reset the freeze flag when play is pressed
    # Attempt to connect to Arduino
    connection_result = arduino.connect_to_arduino()
    flag = 'True'  # Set the flag to False if connection failed
    return render_template('reflectanceToAnalyze.html', flag=flag)


@app.route('/pauseData')
def pauseData():
    # global freeze_plot01
    # freeze_plot01 = True  # Set this flag to True to indicate the plot should be frozen
    return make_response('', 204)


@app.route('/stopData')
def stopData():
    flag = 'False'
    return render_template('reflectanceToAnalyze.html', flag=flag)


@app.route('/read-data')
def read_data():
    if arduino.ser is None:
        return jsonify({"error": "Arduino not connected"}), 400

    try:
        data = arduino.read_data_from_arduino()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


###########################
# Plot Analyzing  Routing #
###########################
@app.route('/analyze')
def analyze():
    # Connect to the Arduino
    connection_result = arduino.connect_to_arduino()

    if connection_result:
        # Read raw data from Arduino
        # Get real-time data from Arduino
        data = arduino.read_data_from_arduino()

        # Convert the list to NumPy arrays for easier calculations
        raw = np.array(data)
        white = np.array(whitedata.whiteData)
        dark = np.array(darkdata.darkData)

        # Avoid division by zero by adding a very small number (epsilon) where the denominator is zero
        # Small constant to avoid division by zero
        epsilon = 1e-10
        denominator = white - dark
        denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number
        calibrated = (raw - dark) / denominator

        # mask the NAN values as 0
        calibratedData = np.where(np.isnan(calibrated), 0, calibrated)
        # Replace inf values with 0
        calibratedData = np.where(np.isinf(calibratedData), 0, calibratedData)

        calibratedData = np.abs(calibratedData)

        # Save the data in calData.py file
        save_calData_to_py(calibratedData)

        return render_template('saveAndModel.html')
    else:
        return jsonify({'message': 'Failed to connect to Arduino'}), 500
    # return render_template('darkReference.html')


# Function to save darkData as a Python variable in darkdata.py
def save_calData_to_py(data):
    # convert the numpy data array to simple list
    data_list = data.tolist()
    with open('calData.py', 'w') as f:
        f.write(f"calData = {data_list}")


################################
# Reflectance Raw Plot Routing #
################################

@app.route('/connectRaw')
def connectRaw():
    # global freeze_plot01
    # freeze_plot01 = False  # Reset the freeze flag when play is pressed
    # Attempt to connect to Arduino
    connection_result = arduino.connect_to_arduino()
    flag1 = 'True'  # Set the flag to False if connection failed
    return render_template('absorbance.html', flag1=flag1)


@app.route('/pauseDataRaw')
def pauseDataRaw():
    # global freeze_plot01
    # freeze_plot01 = True  # Set this flag to True to indicate the plot should be frozen
    return make_response('', 204)


@app.route('/stopDataRaw')
def stopDataRaw():
    flag1 = 'False'
    return render_template('absorbance.html', flag1=flag1)


@app.route('/readDataRaw')
def readDataRaw():
    if arduino.ser is None:
        return jsonify({"error": "Arduino not connected"}), 400

    try:
        data = arduino.read_data_from_arduino()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


###############################
# Dark Reference Plot Routing #
###############################

@app.route('/connectDark')
def connectDark():
    # global freeze_plot
    # freeze_plot = False  # Reset the freeze flag when play is pressed
    # Attempt to connect to Arduino
    connection_result = arduino.connect_to_arduino()
    flag2 = 'True'  # Set the flag to False if connection failed
    return render_template('darkReference.html', flag2=flag2)


@app.route('/pauseDataDark')
def pauseDataDark():
    # global freeze_plot
    # freeze_plot = True  # Set this flag to True to indicate the plot should be frozen
    return jsonify({'message': 'Data stream paused'})


@app.route('/stopDataDark')
def stopDataDark():
    flag = 'False'
    return render_template('darkReference.html', flag=flag)


@app.route('/recDark')
def recDark():
    # Connect to the Arduino
    connection_result = arduino.connect_to_arduino()

    if connection_result:
        # Read raw data from Arduino
        dataDark = arduino.read_data_from_arduino()

        # Save the data in darkdata.py file
        save_dark_data_to_py(dataDark)

        return render_template('darkReference.html')
    else:
        return jsonify({'message': 'Failed to connect to Arduino'}), 500
    # return render_template('darkReference.html')


# Function to save darkData as a Python variable in darkdata.py
def save_dark_data_to_py(data):
    with open('darkdata.py', 'w') as f:
        f.write(f"darkData = {data}")


################################
# White Reference Plot Routing #
################################

@app.route('/connectWhite')
def connectWhite():
    # global freeze_plot
    freeze_plot = False  # Reset the freeze flag when play is pressed
    # Attempt to connect to Arduino
    connection_result = arduino.connect_to_arduino()
    flag3 = 'True'  # Set the flag to False if connection failed
    return render_template('whiteReferance.html', flag3=flag3)


@app.route('/pauseDataWhite')
def pauseDataWhite():
    # global freeze_plot
    freeze_plot = True  # Set this flag to True to indicate the plot should be frozen
    return jsonify({'message': 'Data stream paused'})


@app.route('/stopDataWhite')
def stopDataWhite():
    flag = 'False'
    return render_template('whiteReferance.html', flag=flag)


@app.route('/recWhite')
def recWhite():
    # Connect to the Arduino
    connection_result = arduino.connect_to_arduino()

    if connection_result:
        # Read raw data from Arduino
        data = arduino.read_data_from_arduino()

        # Save the data in whiteData.py file
        save_white_data_to_py(data)

        return render_template('whiteReferance.html')
    else:
        return jsonify({'message': 'Failed to connect to Arduino'}), 500
    # return render_template('darkReference.html')


# Function to save darkData as a Python variable in darkdata.py
def save_white_data_to_py(data):
    with open('whitedata.py', 'w') as f:
        f.write(f"whiteData = {data}")


#############################################
#  DB Connection (if needed in the future)  #
#############################################


################
#  UI Routing  #
################

@app.route('/')
def splash():
    return render_template('statSegments/splash.html')


@app.route('/navigate_to_index')
def navigate_to_index():
    return render_template('index.html')


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


@app.route('/reflectanceAnalyzing')
def reflectanceAnalyzing():
    return render_template('reflectanceToAnalyze.html')


@app.route('/activityLog')
def activityLog():
    return render_template('activityLog.html')


@app.route('/logView')
def logView():
    return render_template('logView.html')


###################################################################
#                       Plot Routing Start                        #
###################################################################

###############################
#  Reflectance Analyze Routes #
###############################

# freeze_plot = False  # Global flag to manage plot freeze
# frozen_graph = None


@app.route('/plot-data')
def plot_data():
    # global freeze_plot, frozen_graph
    # # If the plot is frozen, return the last plot data
    # config = {
    #     'displaylogo': False,
    #     'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
    #                                'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
    #                                'resetScale2d',
    #                                'select2d', 'toggleSpikelines', 'toImage']
    # }

    # If freeze_plot is True, return the last frozen graph
    # if freeze_plot:
    #     # Check if the frozen graph has been set before
    #     if frozen_graph:
    #         return jsonify({'figure': frozen_graph, 'config': config})
    #     else:
    #         # Return a placeholder message if no graph has been frozen yet
    #         return jsonify({'message': 'No graph data to display (graph has not been frozen yet).'})

    # Get real-time data from Arduino
    data = arduino.read_data_from_arduino()

    # Convert the list to NumPy arrays for easier calculations
    raw = np.array(data)
    white = np.array(whitedata.whiteData)
    dark = np.array(darkdata.darkData)

    # Avoid division by zero by adding a very small number (epsilon) where the denominator is zero
    # Small constant to avoid division by zero
    epsilon = 1e-10
    denominator = white - dark

    denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number
    calibrated = (raw - dark) / denominator

    # mask the NAN values as 0
    calibratedData = np.where(np.isnan(calibrated), 0, calibrated)

    # Replace inf values with 0
    calibratedData = np.where(np.isinf(calibratedData), 0, calibratedData)

    denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number

    calibratedData = np.abs(calibratedData)

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    # x = np.linspace(300, 900, len(calibrated))  # Simulate wavelength range

    # norm = Normalize(vmin=min(calibrated), vmax=max(calibrated))

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(len(calibratedData)),  # x-axis as the index
        y=calibratedData,
        mode='markers',
        marker=dict(size=3)  # Adjust the size (6 is smaller than default)
    ))

    fig.update_layout(
        xaxis_title="Wavelength (nm)",
        yaxis_title="Reflectance (%)",
        xaxis=dict(autorange=True),  # x axis
        yaxis=dict(autorange=True),  # y axis
        height=320,
        width=480,
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                   'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    # frozen_graph = fig.to_json()  # Update the last frozen graph

    return jsonify({'figure': fig.to_json(), 'config': config})


#########################
# Dark Reference Routes #
#########################

@app.route('/plot-data2')
def plot_data2():
    # Get real-time data from Arduino
    darkData = arduino.read_data_from_arduino()

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(darkData))  # Simulate wavelength range
    norm = Normalize(vmin=min(darkData), vmax=max(darkData))
    y = norm(darkData)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,  # x-axis as the index
        y=1 - y,
        mode='markers',
        marker=dict(size=3)  # Adjust the size (6 is smaller than default)
    ))

    fig.update_layout(
        xaxis_title="Wavelength (nm)",
        yaxis_title="Reflectance (%)",
        xaxis=dict(range=[300, 900]),  # x axis
        yaxis=dict(range=[0, 1.2]),  # y axis
        height=320,
        width=480,
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                   'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    # frozen_graph = fig.to_json()  # Update the last frozen graph
    return jsonify({'figure': fig.to_json(), 'config': config})


#########################
# White Reference Routes #
#########################

@app.route('/plot-data3')
def plot_data3():
    # Get real-time data from Arduino
    whiteData = arduino.read_data_from_arduino()

    # Save darkData to a Python file
    # save_dark_data_to_py(darkData)

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(whiteData))  # Simulate wavelength range
    norm = Normalize(vmin=min(whiteData), vmax=max(whiteData))
    y = norm(whiteData)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,  # x-axis as the index
        y=1 - y,
        mode='markers',
        marker=dict(size=3)  # Adjust the size (6 is smaller than default)
    ))

    fig.update_layout(
        xaxis_title="Wavelength (nm)",
        yaxis_title="Reflectance (%)",
        xaxis=dict(range=[300, 900]),  # x axis
        yaxis=dict(range=[0, 1.2]),  # y axis
        height=320,
        width=480,
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                   'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    # frozen_graph = fig.to_json()  # Update the last frozen graph
    return jsonify({'figure': fig.to_json(), 'config': config})


########################
# Reference Raw Routes #
########################

@app.route('/plot-data4')
def plot_data4():
    # Get real-time data from Arduino
    rawData = arduino.read_data_from_arduino()

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(rawData))  # Simulate wavelength range
    norm = Normalize(vmin=min(rawData), vmax=max(rawData))
    y = norm(rawData)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,  # x-axis as the index
        y=1 - y,
        mode='markers',
        marker=dict(size=3)  # Adjust the size (6 is smaller than default)
    ))

    fig.update_layout(
        xaxis_title="Wavelength (nm)",
        yaxis_title="Reflectance (%)",
        xaxis=dict(range=[300, 900]),  # x axis
        yaxis=dict(range=[0, 1.2]),  # y axis
        height=320,
        width=480,
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                   'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    # frozen_graph = fig.to_json()  # Update the last frozen graph
    return jsonify({'figure': fig.to_json(), 'config': config})


###################
#  Main Function  #
###################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
