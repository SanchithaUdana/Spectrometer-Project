from flask import Flask, render_template, redirect, url_for, Response
import matplotlib.pyplot as plt
import io
import random

app = Flask(__name__)

# Global variables to simulate live data for the chart
x_data = []
y_data = []


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
def index():
    return render_template('index.html')


@app.route('/navigate_to_index')
def navigate_to_index():
    return redirect(url_for('index'))


@app.route('/home')
def home():
    return render_template('home.html')


# Route to serve the live-updating chart image
@app.route('/plot.png')
def plot_png():
    global x_data, y_data
    # Simulate new data points
    x_data.append(len(x_data))
    y_data.append(random.randint(0, 100))

    img = generate_plot()
    return Response(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
