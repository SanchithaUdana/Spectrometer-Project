import time
import numpy as np
import plotly.graph_objs as go
import serial
from flask import Flask, render_template, jsonify, make_response, Response, send_file, request, redirect, url_for
from matplotlib.colors import Normalize
import csv
import os

import whitedata
import darkdata
import calData
import rawData
import csvData

app = Flask(__name__)

# Create a directory to save the CSV files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
            time.sleep(0.2)

            # Try reading the data
            data = self.read_data()

            # Check if data is received
            if data:
                # print("Received Data List:", data)
                print("Length of Data List:", len(data))
                return data
            else:
                print("No data received from Arduino.")
                return []
        except Exception as e:
            print(f"Error while reading from Arduino: {e}")
            return []


arduino = ArduinoConnector()


#####################
# Data Save to CSV  #
#####################

@app.route('/save_csv', methods=['POST'])
def save_csv():
    # Save the predefined list to a CSV file
    csv_file_path = os.path.join(UPLOAD_FOLDER, 'spectrum.csv')
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        data_list = calData.calData
        for item in data_list:
            writer.writerow([item])

    # Return the CSV file as a download
    return send_file(csv_file_path, as_attachment=True)


#######################
# Data view from CSV  #
#######################

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.csv'):
        # Save the file to the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Process the CSV file
        csv_data = []
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            csv_data = [float(row[0]) for row in reader]  # Convert strings to floats

            with open('csvData.py', 'w') as o:
                o.write(f"csvData = {csv_data}")

        return render_template('view/viewCsvData.html')
    else:
        js_code = """
                                                                <script>
                                                                    alert('Invalid File Format. Try Again ! ');
                                                                    window.location.href = '/reflectanceAnalyzing';
                                                                </script>
                                                                """
        return Response(js_code, mimetype='text/html')


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
    # return render_template('saveAndModel.html')

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

        if len(raw) < 2088:
            js_code = """
                                            <script>
                                                alert('Full Data Not Captured. Try Again ! ');
                                                window.location.href = '/reflectanceAnalyzing';
                                            </script>
                                            """
            return Response(js_code, mimetype='text/html')

        # Avoid division by zero by adding a very small number (epsilon) where the denominator is zero
        # Small constant to avoid division by zero
        epsilon = 1e-10
        denominator = white - dark
        denominator[denominator == 0] = epsilon  # Replace 0 in the denominator with a small number
        calibrated = (raw - dark) / denominator

        # mask the NAN values as 0
        calibrated = np.where(np.isnan(calibrated), 0, calibrated)
        denominator[denominator == 0] = epsilon
        # Replace inf values with 0
        calibrated = np.where(np.isinf(calibrated), 0, calibrated)
        denominator[denominator == 0] = epsilon

        calibrated = np.abs(calibrated)

        if len(calibrated) < 2088:
            js_code = """
                                                        <script>
                                                            alert('Full Data Not Captured. Try Again ! ');
                                                            window.location.href = '/reflectanceAnalyzing';
                                                        </script>
                                                        """
            return Response(js_code, mimetype='text/html')

        # Save the data in calData.py file
        save_calData_to_py(calibrated)

        if len(calData.calData) < 2088:
            js_code = """
                                                        <script>
                                                            alert('Full Data Not Captured. Try Again ! ');
                                                            window.location.href = '/reflectanceAnalyzing';
                                                        </script>
                                                        """
            return Response(js_code, mimetype='text/html')

        js_code1 = """
                                    <script>
                                        alert('Data Saved !');
                                        window.location.href = '/reflectanceAnalyzing';
                                    </script>
                                    """
        return Response(js_code1, mimetype='text/html')

    else:
        js_code = """
                            <script>
                                alert('Arduino Not Connected !');
                                window.location.href = '/reflectanceAnalyzing';
                            </script>
                            """
        return Response(js_code, mimetype='text/html')


# Function to save calData as a Python variable in calData.py
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


@app.route('/recRaw')
def recRaw():
    # Connect to the Arduino
    connection_result = arduino.connect_to_arduino()

    if connection_result:
        # Read raw data from Arduino
        Data = arduino.read_data_from_arduino()

        if len(Data) < 2088:
            js_code = """
                                <script>
                                    alert('Full Data Not Captured. Try Again ! ');
                                    window.location.href = '/absorbance';
                                </script>
                                """
            return Response(js_code, mimetype='text/html')

        # Save the data in rawData.py file
        save_raw_data_to_py(Data)

        if len(darkdata.darkData) < 2088:
            js_code = """
                        <script>
                            alert('Full Data Not Captured. Try Again ! ');
                            window.location.href = '/absorbance';
                                            </script>
                                            """
            return Response(js_code, mimetype='text/html')

        js_code = """
                    <script>
                        alert('Raw Data Successfully Saved ! ');
                        window.location.href = '/absorbance';
                    </script>
                    """
        return Response(js_code, mimetype='text/html')

    else:
        js_code = """
            <script>
                alert('Arduino is Not Connected ?');
                window.location.href = '/navigate_to_index';
            </script>
            """
        return Response(js_code, mimetype='text/html')


# Function to save darkData as a Python variable in rawData.py
def save_raw_data_to_py(data):
    with open('rawData.py', 'w') as f:
        f.write(f"rawData = {data}")


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

        if len(dataDark) < 2088:
            js_codeDark = """
                                    <script>
                                        alert('Full Data Not Captured. Try Again ! ');
                                        window.location.href = '/darkReference';
                                    </script>
                                    """
            return Response(js_codeDark, mimetype='text/html')

        # Save the data in darkdata.py file
        save_dark_data_to_py(dataDark)

        if len(dataDark) < 2088:
            js_codeDark = """
                                                <script>
                                                    alert('Full Data Not Captured. Try Again ! ');
                                                    window.location.href = '/darkReference';
                                                </script>
                                                """
            return Response(js_codeDark, mimetype='text/html')

        js_code = """
                    <script>
                        alert('Dark reference Data Successfully Saved ! ');
                        window.location.href = '/darkReference';
                    </script>
                    """
        return Response(js_code, mimetype='text/html')

    else:
        js_code = """
            <script>
                alert('Arduino is Not Connected ?');
                window.location.href = '/navigate_to_index';
            </script>
            """
        return Response(js_code, mimetype='text/html')


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

        if len(data) < 2088:
            js_codeDark = """
                                    <script>
                                        alert('Full Data Not Captured. Try Again ! ');
                                        window.location.href = '/whiteReference';
                                    </script>
                                    """
            return Response(js_codeDark, mimetype='text/html')

        # Save the data in whiteData.py file
        save_white_data_to_py(data)

        if len(whitedata.whiteData) < 2088:
            js_codeDark = """
                                    <script>
                                        alert('Full Data Not Captured. Try Again ! ');
                                        window.location.href = '/whiteReference';
                                    </script>
                                    """
            return Response(js_codeDark, mimetype='text/html')

        js_code = """
                            <script>
                                alert('White reference Data Successfully Saved ! ');
                                window.location.href = '/whiteReference';
                            </script>
                            """
        return Response(js_code, mimetype='text/html')
    else:
        js_code = """
                    <script>
                        alert('Arduino is Not Connected ?');
                        window.location.href = '/navigate_to_index';
                    </script>
                    """
        return Response(js_code, mimetype='text/html')


# Function to save darkData as a Python variable in whiteData.py
def save_white_data_to_py(data):
    with open('whitedata.py', 'w') as f:
        f.write(f"whiteData = {data}")


#############################################
#  Main User Interfaces Routing Area        #
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


@app.route('/toAnalyze')
def toAnalyze():
    return render_template('reflectanceToAnalyze.html')


@app.route('/darkViewPlot')
def darkViewPlot():
    return render_template('view/viewDarkReference.html')


@app.route('/analyzeGo')
def analyzeGo():
    return render_template('saveAndModel.html')


@app.route('/rawGo')
def rawGo():
    return render_template('view/viewRawData.html')


@app.route('/viewCal')
def viewCal():
    return render_template('view/viewCalData.html')


@app.route('/whiteViewPlot')
def whiteViewPlot():
    return render_template('view/viewWhiteReference.html')


@app.route('/csvPage')
def csvPage():
    return render_template('csvSave.html')


@app.route('/viewCsv')
def viewCsv():
    return render_template('view/viewCsvData.html')


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
    calibrated = np.where(np.isnan(calibrated), 0, calibrated)
    denominator[denominator == 0] = epsilon
    # Replace inf values with 0
    calibrated = np.where(np.isinf(calibrated), 0, calibrated)
    denominator[denominator == 0] = epsilon

    calibrated = np.abs(calibrated)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(len(calibrated)),  # x-axis as the index
        y=calibrated,
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


#########################
# Dark Data Plot View   #
#########################

@app.route('/darkDataView')
def darkDataView():
    # Get real-time data from Arduino
    darkData = darkdata.darkData

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
# Raw Data Plot View   #
#########################

@app.route('/rawDataView')
def rawDataView():
    # Get real-time data from Arduino
    Data = rawData.rawData

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(Data))  # Simulate wavelength range
    norm = Normalize(vmin=min(Data), vmax=max(Data))
    y = norm(Data)

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
# Cal Data Plot View   #
#########################

@app.route('/calDataView')
def calDataView():
    # Get real-time data from Arduino
    Data = calData.calData

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(Data))  # Simulate wavelength range
    norm = Normalize(vmin=min(Data), vmax=max(Data))
    y = norm(Data)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,  # x-axis as the index
        y=y,
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
# CSV Data Plot View   #
#########################

@app.route('/csvDataView')
def csvDataView():
    # Get real-time data from Arduino
    Data = csvData.csvData

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(Data))  # Simulate wavelength range
    norm = Normalize(vmin=min(Data), vmax=max(Data))
    y = norm(Data)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,  # x-axis as the index
        y=y,
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

##########################
# White Data Plot View   #
##########################

@app.route('/whiteDataView')
def whiteDataView():
    # Get real-time data from Arduino
    Data = whitedata.whiteData

    # Generate x and y values from Arduino data
    # Assuming data corresponds to y-values (intensity) and x-values are indices
    x = np.linspace(300, 900, len(Data))  # Simulate wavelength range
    norm = Normalize(vmin=min(Data), vmax=max(Data))
    y = norm(Data)

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
