from flask import Flask, render_template, redirect, url_for, Response, jsonify
import matplotlib.pyplot as plt
import io
import random
import numpy as np
import random
import time

app = Flask(__name__)

# Global variables to simulate live data for the chart
x_data = []
y_data = []


def generate_live_data():
    global x_data, y_data
    if len(x_data) >= 20:  # Keep last 20 data points for better view
        x_data.pop(0)
        y_data.pop(0)

    # Simulate live data (random sine wave)
    new_x = x_data[-1] + 1 if x_data else 0
    new_y = np.sin(new_x) + random.uniform(-0.5, 0.5)  # Adding some random noise
    x_data.append(new_x)
    y_data.append(new_y)


# Function to generate a live chart using matplotlib
def generate_plot():
    plt.figure(figsize=(5, 3))
    plt.plot(x_data, y_data, color='blue')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Live Updating Chart')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img


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


@app.route('/spectrumDefault')
def spectrumDefault():
    return render_template('absorbance.html')


# Function to simulate updating plot data
# Route to serve the live-updating chart image
# Route to generate the plot dynamically
@app.route('/plot.png')
def plot_png():
    # Update live data
    generate_live_data()

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data, color='blue', marker='o')

    ax.set_title("Live Updating Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")

    # Save plot to a BytesIO object
    png_output = io.BytesIO()
    plt.savefig(png_output, format='png', dpi=80)  # Adjust DPI for resolution
    png_output.seek(0)
    plt.close(fig)

    return Response(png_output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
