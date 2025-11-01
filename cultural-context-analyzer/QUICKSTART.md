# Quick Start Guide

Get the Cultural Context Analyzer running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 14+ installed and running
- [ ] Gemini API key obtained

## Quick Setup (5 Steps)

### 1. Create Database (1 minute)

```powershell
psql -U postgres
CREATE DATABASE cultural_context_db;
\q
```

### 2. Configure Backend (1 minute)

Create `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/cultural_context_db
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 3. Setup Backend (2 minutes)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Setup Frontend (1 minute)

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

```powershell
cd frontend
npm install
```

### 5. Run Application

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

**Open Browser:** http://localhost:5173

## Test It!

Try this sample text:
```
The Ramayana is an ancient Indian epic that tells the story of Prince Rama's 
quest to rescue his wife Sita from the demon king Ravana.
```

You should get:
1. ✅ Cultural Origin analysis
2. ✅ Cross-cultural connections
3. ✅ Modern analogy
4. ✅ Visualization description

## Common Issues

**Database connection failed?**
- Check PostgreSQL is running
- Verify password in `.env`

**Gemini API error?**
- Verify API key is correct
- Check internet connection

**Port already in use?**
- Backend: Change port in `main.py`
- Frontend: Change port in `vite.config.js`

## Next Steps

- Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- Read [README.md](README.md) for full documentation
- Try different languages and texts!

---

**Need help?** Check the troubleshooting section in SETUP_GUIDE.md
