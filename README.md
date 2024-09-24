
<img width="665" alt="Screenshot 2024-09-11 at 10 00 28 AM" src="https://github.com/user-attachments/assets/065d73dd-c3ae-4dcc-94ab-e29e6e7d0f93">

# **Spectrometer Project**

Welcome to the **Spectrometer Project**, a Flask-based web application designed for running a spectrum plot on a Raspberry Pi. The app provides real-time visualizations using **Matplotlib** and is containerized for easy deployment using **Docker**.

![Flask](https://img.shields.io/badge/Flask-v2.0-blue)
![Docker](https://img.shields.io/badge/Docker-ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## **Features**

- 🖥 **Web-based UI** built using Flask and Bootstrap.
- 📊 **Real-time spectrum plotting** using Matplotlib.
- 🌐 **Responsive Design** for various screen sizes.
- 🚢 **Dockerized** for easy installation and deployment.
- 🔧 **Compatible with Raspberry Pi** for hardware integration.

---

## **Project Setup**

### **Prerequisites**

Before running the project, make sure you have the following installed:

- **Python 3.x**
- **Flask**
- **Matplotlib**
- **Bootstrap 5.3.0-alpha1**
- **Docker** (if you plan to use the containerized version)

## **Docker Setup**

```Dockerfile
# Use a lightweight Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]
```

This Dockerfile sets up a lightweight container for running a Flask web application using Python 3.9. Key steps:

1. **Base Image**: Uses `python:3.9-slim` for a minimal Python environment.
2. **Working Directory**: Sets `/app` as the working directory inside the container.
3. **Dependencies**: Copies `requirements.txt` and installs dependencies using `pip`.
4. **App Files**: Copies all app files into the container.
5. **Environment Variables**: Sets `FLASK_APP=app.py` and configures Flask to run on `0.0.0.0`, making the app accessible externally.
6. **Port Exposure**: Exposes port 5000 for the Flask app.
7. **Run App**: Uses `flask run` to start the application.

For a pre-built image, visit the Docker Hub link:  
[https://hub.docker.com/r/sanchithaudana/flask-app](https://hub.docker.com/r/sanchithaudana/flask-app).

<img width="1440" alt="Screenshot 2024-09-24 at 9 10 10 AM" src="https://github.com/user-attachments/assets/0cbd4f22-67b5-442f-a430-28374ca2617f">

