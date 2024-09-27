#!/bin/bash

# Update and upgrade the system packages
sudo apt update && sudo apt upgrade -y

# Install Git, Python 3, pip, and venv if not already installed
sudo apt install git python3 python3-pip python3-venv -y

sudo apt update -y
sudo apt install libatlas-base-dev -y
    
# Clone your GitHub repository into the home directory
cd ~
git clone https://github.com/SanchithaUdana/Spectrometer-Project.git

# Navigate to the cloned project directory
cd Spectrometer-Project

# Set up a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables for Flask
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0

# Optionally, set Flask environment to development for debugging
# export FLASK_ENV=development

# Run the Flask app
flask run --host=0.0.0.0 --port=5000
s