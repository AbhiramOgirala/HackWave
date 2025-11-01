# Complete Setup Guide - Cultural Context Analyzer

This guide will walk you through setting up the Cultural Context Analyzer from scratch.

## Prerequisites

Before starting, ensure you have the following installed:

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - LTS version recommended

3. **PostgreSQL 14 or higher**
   - Download from: https://www.postgresql.org/download/windows/
   - Remember the password you set for the `postgres` user during installation

4. **Google Gemini API Key**
   - Get it from: https://makersuite.google.com/app/apikey
   - Sign in with your Google account and create an API key

## Step-by-Step Setup

### 1. Database Setup

Open Command Prompt or PowerShell and run:

```powershell
# Connect to PostgreSQL
psql -U postgres

# Enter your PostgreSQL password when prompted

# Create the database
CREATE DATABASE cultural_context_db;

# Verify database was created
\l

# Exit psql
\q
```

### 2. Backend Configuration

Navigate to the backend folder and create the `.env` file:

```powershell
cd backend
```

Create a file named `.env` with the following content:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/cultural_context_db
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

**Important:** Replace:
- `YOUR_PASSWORD` with your PostgreSQL password
- `YOUR_GEMINI_API_KEY` with your actual Gemini API key

### 3. Backend Installation

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; import sqlalchemy; import google.generativeai; print('All packages installed successfully!')"
```

### 4. Frontend Configuration

Open a new terminal and navigate to the frontend folder:

```powershell
cd frontend
```

Create a file named `.env` with the following content:

```env
VITE_API_URL=http://localhost:8000
```

### 5. Frontend Installation

```powershell
# Install dependencies
npm install

# Verify installation
npm list react vite tailwindcss
```

## Running the Application

### Start Backend (Terminal 1)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

You should see:
```
✅ Database initialized successfully
🚀 Cultural Context Analyzer API is running
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start Frontend (Terminal 2)

```powershell
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Access the Application

Open your browser and go to: **http://localhost:5173**

## Testing the Setup

1. **Test Backend API**
   - Open: http://localhost:8000
   - You should see the API welcome message

2. **Test Frontend**
   - Open: http://localhost:5173
   - You should see the Cultural Context Analyzer interface

3. **Test Full Flow**
   - Enter sample text: "The Ramayana is an ancient Indian epic"
   - Select language: English
   - Click "Analyze Cultural Context"
   - You should see 4 sections of analysis

## Database Commands

### View Stored Data

```powershell
# Connect to database
psql -U postgres -d cultural_context_db

# View all analyses
SELECT id, language, LEFT(input_text, 50) as text_preview, created_at FROM analyses;

# View specific analysis
SELECT * FROM analyses WHERE id = 1;

# Count total analyses
SELECT COUNT(*) FROM analyses;

# Exit
\q
```

### Reset Database

```powershell
# Connect to database
psql -U postgres -d cultural_context_db

# Drop all data
DROP TABLE analyses;

# Exit
\q

# Restart backend to recreate tables
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

### Backup Database

```powershell
# Create backup
pg_dump -U postgres cultural_context_db > backup.sql

# Restore from backup
psql -U postgres cultural_context_db < backup.sql
```

## Troubleshooting

### Issue: "psql: command not found"

**Solution:** Add PostgreSQL to PATH
1. Find PostgreSQL installation (usually `C:\Program Files\PostgreSQL\15\bin`)
2. Add to System Environment Variables PATH
3. Restart terminal

### Issue: "Cannot connect to database"

**Solutions:**
1. Check PostgreSQL service is running:
   - Open Services (Win + R, type `services.msc`)
   - Find "postgresql-x64-XX" service
   - Start if not running

2. Verify connection string in `backend/.env`
3. Check password is correct

### Issue: "Gemini API Error"

**Solutions:**
1. Verify API key is correct in `backend/.env`
2. Check API key is active at https://makersuite.google.com/app/apikey
3. Ensure you have internet connection
4. Check API quota limits

### Issue: "Port already in use"

**Solutions:**

For Backend (port 8000):
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

For Frontend (port 5173):
```powershell
# Find process using port
netstat -ano | findstr :5173

# Kill process
taskkill /PID <PID> /F
```

### Issue: "Module not found" errors

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall
```

**Frontend:**
```powershell
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

### Issue: Virtual environment activation fails

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

## Project Structure

```
cultural-context-analyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database models
│   ├── gemini_service.py       # AI integration
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (create this)
│   └── venv/                   # Virtual environment (created by setup)
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Styles
│   ├── index.html
│   ├── package.json
│   ├── .env                    # Environment variables (create this)
│   └── node_modules/           # Dependencies (created by npm)
├── README.md                   # Main documentation
├── SETUP_GUIDE.md             # This file
└── setup.ps1                  # Automated setup script
```

## Usage Examples

### Example 1: Analyzing a Poem

**Input:**
```
Haiku is a traditional form of Japanese poetry consisting of three lines 
with a 5-7-5 syllable pattern, often focusing on nature and seasons.
```

**Expected Output:**
- Cultural Origin: Japanese poetry tradition
- Cross-Cultural Connections: Influence on Western poetry
- Modern Analogy: Like Twitter's character limit
- Visualization: Traditional Japanese scroll with haiku

### Example 2: Historical Text

**Input:**
```
The Renaissance was a period of cultural rebirth in Europe, marked by 
renewed interest in classical art, literature, and learning.
```

**Expected Output:**
- Cultural Origin: European cultural movement
- Cross-Cultural Connections: Spread across Europe
- Modern Analogy: Like the digital revolution
- Visualization: Renaissance art and architecture

## API Endpoints Reference

### POST /api/analyze
Analyze text for cultural context

**Request:**
```json
{
  "text": "Your text here",
  "language": "en"
}
```

**Response:**
```json
{
  "id": 1,
  "cultural_origin": "...",
  "cross_cultural_connections": "...",
  "modern_analogy": "...",
  "visualization_description": "...",
  "image_url": "...",
  "created_at": "2024-01-01T00:00:00"
}
```

### GET /api/history
Get analysis history (last 20 by default)

### GET /api/analysis/{id}
Get specific analysis by ID

### DELETE /api/analysis/{id}
Delete specific analysis

### GET /api/stats
Get statistics about analyses

## Support

If you encounter any issues not covered in this guide:

1. Check the error messages carefully
2. Verify all prerequisites are installed correctly
3. Ensure environment variables are set properly
4. Check that PostgreSQL service is running
5. Verify internet connection for Gemini API calls

## Next Steps

After successful setup:

1. Try analyzing different types of texts
2. Experiment with different languages
3. Review the analysis history
4. Explore the database to see stored data
5. Customize the UI or add new features

Happy analyzing! 🎉
