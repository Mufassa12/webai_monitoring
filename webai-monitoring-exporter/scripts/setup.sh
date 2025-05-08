#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r src/requirements.txt

echo "Setup complete. Virtual environment created and packages installed."