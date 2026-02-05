#!/bin/bash

# AstroKnowledge Setup Script for Linux/Mac
# Run this script to set up your environment

echo "========================================"
echo "  AstroKnowledge Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "ERROR: Python not found. Please install Python 3.10 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment."
    exit 1
fi

echo "Virtual environment created successfully!"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies."
    exit 1
fi

echo "Dependencies installed successfully!"

# Create .env file
echo ""
echo "Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from .env.example"
else
    echo ".env file already exists"
fi

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/books
mkdir -p data/vector_db
mkdir -p data/user_data/profiles
mkdir -p data/user_data/charts
mkdir -p data/user_data/history
mkdir -p logs

echo "Directories created successfully!"

# Check Ollama
echo ""
echo "Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    ollama --version
    echo "Ollama is installed!"
    
    echo ""
    echo "Checking for llama3.2 model..."
    if ollama list | grep -q "llama3.2"; then
        echo "llama3.2 model found!"
    else
        echo "llama3.2 model not found. Pulling model..."
        echo "This may take several minutes (model is ~2GB)..."
        ollama pull llama3.2
        
        if [ $? -eq 0 ]; then
            echo "llama3.2 model installed successfully!"
        else
            echo "Failed to pull llama3.2 model. You can do this later with: ollama pull llama3.2"
        fi
    fi
else
    echo "Ollama not found!"
    echo ""
    echo "Please install Ollama from: https://ollama.ai"
    echo "After installation, run: ollama pull llama3.2"
fi

# Summary
echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running"
echo "2. Place your astrology books in: data/books/"
echo "3. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "For more information, see README.md"
echo ""
