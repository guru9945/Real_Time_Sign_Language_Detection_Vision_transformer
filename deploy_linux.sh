#!/bin/bash
# Quick Deploy Script for Linux/Mac
# Automates the setup process

echo "================================"
echo "Sign Language Detection Deploy"
echo "================================"
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
python3 --version || { echo "Python 3 not found. Please install Python 3.8+"; exit 1; }
echo "✓ Python OK"
echo ""

# Install requirements
echo "[2/5] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo ""

# Create necessary directories
echo "[3/5] Setting up directories..."
mkdir -p logs
mkdir -p data
mkdir -p outputs
echo "✓ Directories created"
echo ""

# Check for model files
echo "[4/5] Verifying model files..."
if [ -f "model/keypoint_classifier/keypoint_classifier_vit.tflite" ]; then
    echo "✓ TFLite model found"
else
    echo "✗ Model file not found!"
    echo "  Expected: model/keypoint_classifier/keypoint_classifier_vit.tflite"
    exit 1
fi

if [ -f "model/keypoint_classifier/keypoint_classifier_label.csv" ]; then
    echo "✓ Label file found"
else
    echo "✗ Label file not found!"
    exit 1
fi
echo ""

# Run application
echo "[5/5] Starting application..."
echo ""
echo "Choose deployment option:"
echo "1) Desktop GUI (Recommended for testing)"
echo "2) Web Server (For local network)"
echo "3) CLI Mode (Command line)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting GUI application..."
        python3 gui_app.py
        ;;
    2)
        echo "Starting Flask web server..."
        echo "Access at: http://localhost:5000"
        python3 web_app.py
        ;;
    3)
        echo "Starting CLI mode..."
        python3 cli_wrapper.py
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
