#!/bin/bash

# Secure Question Paper Encryption System - Startup Script

echo "Starting Secure Question Paper Encryption System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if they're not installed
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p uploads stego_images keys encrypted hash payload_zip

echo "Starting Flask application on http://0.0.0.0:5000"
echo "Press Ctrl+C to stop the server"

# Start the Flask application
python app.py