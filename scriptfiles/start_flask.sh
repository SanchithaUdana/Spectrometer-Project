#!/bin/bash

# Navigate to the project directory
cd ~/Spectrometer-Project

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run the installation script first."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Check if the Flask app is already running
FLASK_PID=$(pgrep -f "flask run")

if [ -n "$FLASK_PID" ]; then
    echo "Flask app is already running with PID: $FLASK_PID. Stopping it now..."
    kill -9 $FLASK_PID
    echo "Flask app stopped successfully."
fi

# Set environment variables for Flask
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0

# Optionally, set Flask environment to development for debugging
# export FLASK_ENV=development

# Start the Flask app
echo "Starting the Flask app..."
flask run --host=0.0.0.0 --port=5000 &

# Get the PID of the new Flask process
NEW_FLASK_PID=$!
echo "Flask app started successfully with PID: $NEW_FLASK_PID."

# Deactivate the virtual environment
deactivate
