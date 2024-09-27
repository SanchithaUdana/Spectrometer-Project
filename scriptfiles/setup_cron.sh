#!/bin/bash

# Define the path to the start_flask.sh script
FLASK_SCRIPT_PATH="$HOME/start_flask.sh"

# Check if the start_flask.sh script exists
if [ ! -f "$FLASK_SCRIPT_PATH" ]; then
    echo "Error: $FLASK_SCRIPT_PATH not found. Please make sure the start_flask.sh script is in the home directory."
    exit 1
fi

# Make sure the start_flask.sh script is executable
chmod +x "$FLASK_SCRIPT_PATH"

# Add the start_flask.sh script to the crontab if it's not already present
(crontab -l 2>/dev/null | grep -F "$FLASK_SCRIPT_PATH") || (echo "@reboot $FLASK_SCRIPT_PATH" | crontab -)

# Verify the cron job was added
echo "Current crontab entries:"
crontab -l

echo "The Flask app will start automatically on system boot."
