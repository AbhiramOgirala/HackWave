# NLP Enrichment Module Setup Script
# Run this script to install all required dependencies for the cultural context enrichment feature

Write-Host "Setting up NLP and Cultural Context Enrichment Module..." -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location -Path "$PSScriptRoot\backend"

Write-Host "[Install] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "[Download] Downloading spaCy language model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

Write-Host ""
Write-Host "[Database] Setting up Supabase tables..." -ForegroundColor Yellow
Write-Host "Please run the following SQL in your Supabase SQL Editor:" -ForegroundColor Magenta
Write-Host ""
Write-Host "File: entity_cache_migration.sql" -ForegroundColor Cyan
Write-Host ""
Get-Content -Path "entity_cache_migration.sql"
Write-Host ""

Write-Host "[Check] Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Navigate to frontend directory
Set-Location -Path "$PSScriptRoot\frontend"

Write-Host "[Install] Installing frontend dependencies (if not already installed)..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "[Check] Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Back to root
Set-Location -Path $PSScriptRoot

Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "NLP Enrichment Module Setup Complete!" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run the SQL migration in Supabase Dashboard > SQL Editor" -ForegroundColor White
Write-Host "2. Start the backend: cd backend; python main.py" -ForegroundColor White
Write-Host "3. Start the frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "New Features:" -ForegroundColor Cyan
Write-Host "* Automatic entity detection using spaCy NER" -ForegroundColor White
Write-Host "* Wikipedia/Wikidata enrichment for cultural context" -ForegroundColor White
Write-Host "* Entity caching in Supabase for performance" -ForegroundColor White
Write-Host "* Interactive highlights with tooltips in frontend" -ForegroundColor White
Write-Host "* Direct Wikipedia links for deeper learning" -ForegroundColor White
Write-Host ""
