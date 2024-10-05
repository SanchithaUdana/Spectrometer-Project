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

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Sensor Data 1',
        marker=dict(size=6)  # Adjust the size (6 is smaller than default)
    ))

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
