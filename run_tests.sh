#!/bin/bash

# Activate virtual environment
if [ -d "venv" ]; then
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    elif [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo "Error: Virtual environment found but activate script missing."
        exit 1
    fi
else
    echo "Error: Virtual environment 'venv' not found."
    exit 1
fi

# Run tests
echo "Running test suite..."
pytest

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Tests passed successfully!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi
