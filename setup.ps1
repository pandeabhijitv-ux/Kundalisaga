# AstroKnowledge Setup Script
# Run this script to set up your environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AstroKnowledge Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host $pythonVersion -ForegroundColor Green

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully!" -ForegroundColor Green

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies." -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies installed successfully!" -ForegroundColor Green

# Create .env file
Write-Host ""
Write-Host "Creating .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ".env file created from .env.example" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Yellow
}

# Create data directories
Write-Host ""
Write-Host "Creating data directories..." -ForegroundColor Yellow
$directories = @(
    "data\books",
    "data\vector_db",
    "data\user_data\profiles",
    "data\user_data\charts",
    "data\user_data\history",
    "logs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    }
}

# Check Ollama
Write-Host ""
Write-Host "Checking Ollama installation..." -ForegroundColor Yellow
$ollamaCheck = ollama --version 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Ollama is installed: $ollamaCheck" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Checking for llama3.2 model..." -ForegroundColor Yellow
    $ollamaList = ollama list 2>&1
    
    if ($ollamaList -match "llama3.2") {
        Write-Host "llama3.2 model found!" -ForegroundColor Green
    } else {
        Write-Host "llama3.2 model not found. Pulling model..." -ForegroundColor Yellow
        Write-Host "This may take several minutes (model is ~2GB)..." -ForegroundColor Yellow
        ollama pull llama3.2
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "llama3.2 model installed successfully!" -ForegroundColor Green
        } else {
            Write-Host "Failed to pull llama3.2 model. You can do this later with: ollama pull llama3.2" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Ollama not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Ollama from: https://ollama.ai" -ForegroundColor Yellow
    Write-Host "After installation, run: ollama pull llama3.2" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Make sure Ollama is running" -ForegroundColor White
Write-Host "2. Place your astrology books in: data\books\" -ForegroundColor White
Write-Host "3. Run the application:" -ForegroundColor White
Write-Host "   streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Yellow
Write-Host ""
