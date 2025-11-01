# Cultural Context Analyzer - Setup Script for Windows
# This script sets up the entire project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cultural Context Analyzer - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version 2>&1
    Write-Host "✓ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ PostgreSQL not found or not in PATH." -ForegroundColor Yellow
    Write-Host "  Please ensure PostgreSQL is installed and running." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Backend setup
Set-Location backend

Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "✓ Backend setup complete!" -ForegroundColor Green

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "⚠ Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "  Please create backend/.env file with:" -ForegroundColor Yellow
    Write-Host "  - DATABASE_URL=postgresql://postgres:your_password@localhost:5432/cultural_context_db" -ForegroundColor Yellow
    Write-Host "  - GEMINI_API_KEY=your_gemini_api_key_here" -ForegroundColor Yellow
}

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Frontend setup
Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "✓ Frontend setup complete!" -ForegroundColor Green

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "⚠ Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "  Please create frontend/.env file with:" -ForegroundColor Yellow
    Write-Host "  - VITE_API_URL=http://localhost:8000" -ForegroundColor Yellow
}

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create the PostgreSQL database:" -ForegroundColor White
Write-Host "   psql -U postgres" -ForegroundColor Gray
Write-Host "   CREATE DATABASE cultural_context_db;" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Configure environment variables:" -ForegroundColor White
Write-Host "   - backend/.env (DATABASE_URL, GEMINI_API_KEY)" -ForegroundColor Gray
Write-Host "   - frontend/.env (VITE_API_URL)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start the backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Start the frontend (in a new terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
