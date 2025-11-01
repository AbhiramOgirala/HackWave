# Commands Cheatsheet - Cultural Context Analyzer

Quick reference for all common commands.

## Initial Setup

```powershell
# 1. Create Database
psql -U postgres
CREATE DATABASE cultural_context_db;
\q

# 2. Setup Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Setup Frontend
cd frontend
npm install
```

## Running the Application

```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Database Operations

### Connect to Database
```powershell
psql -U postgres -d cultural_context_db
```

### Common Queries
```sql
-- View all analyses
SELECT * FROM analyses ORDER BY created_at DESC LIMIT 10;

-- Count total
SELECT COUNT(*) FROM analyses;

-- Search by text
SELECT * FROM analyses WHERE input_text ILIKE '%ramayana%';

-- Delete by ID
DELETE FROM analyses WHERE id = 1;

-- Clear all data
DELETE FROM analyses;
```

### Backup & Restore
```powershell
# Backup
pg_dump -U postgres cultural_context_db > backup.sql

# Restore
psql -U postgres cultural_context_db < backup.sql
```

## Development Commands

### Backend
```powershell
# Activate virtual environment
cd backend
.\venv\Scripts\Activate.ps1

# Install new package
pip install package_name
pip freeze > requirements.txt

# Run backend
python main.py

# Deactivate virtual environment
deactivate
```

### Frontend
```powershell
# Install new package
npm install package_name

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Troubleshooting

### Check Services
```powershell
# Check PostgreSQL service
Get-Service postgresql*

# Start PostgreSQL
Start-Service postgresql-x64-XX

# Check ports
netstat -ano | findstr :8000
netstat -ano | findstr :5173
```

### Kill Processes
```powershell
# Find process by port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Reset Everything
```powershell
# Reset database
psql -U postgres
DROP DATABASE cultural_context_db;
CREATE DATABASE cultural_context_db;
\q

# Reset backend
cd backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Reset frontend
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

## API Testing

### Using PowerShell
```powershell
# Test root endpoint
Invoke-RestMethod -Uri "http://localhost:8000/"

# Analyze text
$body = @{
    text = "The Ramayana is an ancient Indian epic"
    language = "en"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/analyze" -Method POST -Body $body -ContentType "application/json"

# Get history
Invoke-RestMethod -Uri "http://localhost:8000/api/history"

# Get stats
Invoke-RestMethod -Uri "http://localhost:8000/api/stats"
```

### Using curl
```bash
# Test root endpoint
curl http://localhost:8000/

# Analyze text
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"The Ramayana is an ancient Indian epic","language":"en"}'

# Get history
curl http://localhost:8000/api/history

# Get specific analysis
curl http://localhost:8000/api/analysis/1

# Delete analysis
curl -X DELETE http://localhost:8000/api/analysis/1
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/cultural_context_db
GEMINI_API_KEY=your_api_key_here
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## Git Commands

```powershell
# Initialize repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote
git remote add origin <repository_url>

# Push
git push -u origin main
```

## Database Schema

```sql
-- Create table manually
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    input_text TEXT NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    cultural_origin TEXT NOT NULL,
    cross_cultural_connections TEXT NOT NULL,
    modern_analogy TEXT NOT NULL,
    visualization_description TEXT NOT NULL,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_language ON analyses(language);
CREATE INDEX idx_created_at ON analyses(created_at);
```

## Quick Fixes

### "Module not found"
```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### "Permission denied" (Virtual Environment)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Database does not exist"
```powershell
psql -U postgres
CREATE DATABASE cultural_context_db;
\q
```

### "Port already in use"
```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Useful psql Commands

```
\l              List databases
\c dbname       Connect to database
\dt             List tables
\d tablename    Describe table
\du             List users
\q              Quit
\?              Help
\timing         Toggle timing
\x              Toggle expanded display
```

## Package Management

### Backend
```powershell
# List installed packages
pip list

# Show package info
pip show package_name

# Uninstall package
pip uninstall package_name

# Update package
pip install --upgrade package_name
```

### Frontend
```powershell
# List installed packages
npm list

# Show package info
npm info package_name

# Uninstall package
npm uninstall package_name

# Update package
npm update package_name

# Check for outdated packages
npm outdated
```

## Monitoring

### View Logs
```powershell
# Backend logs (in terminal running python main.py)
# Frontend logs (in terminal running npm run dev)
# PostgreSQL logs (check PostgreSQL data directory)
```

### Check Database Size
```sql
SELECT pg_size_pretty(pg_database_size('cultural_context_db'));
```

### Check Table Size
```sql
SELECT pg_size_pretty(pg_total_relation_size('analyses'));
```

## Production Deployment

### Build Frontend
```powershell
cd frontend
npm run build
# Output in dist/ folder
```

### Run Backend in Production
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Automated Scripts

### Daily Backup
```powershell
# Create backup_daily.ps1
$date = Get-Date -Format 'yyyyMMdd'
pg_dump -U postgres cultural_context_db > "backup_$date.sql"
```

### Cleanup Old Data
```powershell
# Create cleanup.ps1
psql -U postgres -d cultural_context_db -c "DELETE FROM analyses WHERE created_at < NOW() - INTERVAL '90 days';"
```

## URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Support Links

- **Gemini API**: https://makersuite.google.com/app/apikey
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **TailwindCSS Docs**: https://tailwindcss.com/docs

---

**Tip**: Bookmark this file for quick reference! 📌
