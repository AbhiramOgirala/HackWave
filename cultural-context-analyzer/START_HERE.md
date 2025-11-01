# 🚀 START HERE - Cultural Context Analyzer

Welcome! This is your starting point for the Cultural Context Analyzer project.

## 📋 What is This?

A full-stack web application that analyzes literature and historical texts to provide:
1. **Cultural Origin** - Which culture is it from?
2. **Cross-Cultural Connections** - How does it relate to other cultures?
3. **Modern Analogy** - What's a contemporary parallel?
4. **Visualization** - How can we visualize it?

## 🎯 Quick Navigation

Choose your path:

### 🏃 I Want to Get Started Quickly (5 minutes)
→ Read **[QUICKSTART.md](QUICKSTART.md)**

### 📚 I Want Detailed Setup Instructions
→ Read **[SETUP_GUIDE.md](SETUP_GUIDE.md)**

### 💾 I Need Database Commands
→ Read **[DATABASE_COMMANDS.md](DATABASE_COMMANDS.md)**

### ⚡ I Need Quick Command Reference
→ Read **[COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)**

### 📖 I Want Complete Project Overview
→ Read **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**

### 🔧 I Want Technical Documentation
→ Read **[README.md](README.md)**

## ⚡ Super Quick Start

If you have everything installed (Python, Node.js, PostgreSQL):

```powershell
# 1. Create database
psql -U postgres -c "CREATE DATABASE cultural_context_db;"

# 2. Setup backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Create .env file with DATABASE_URL and GEMINI_API_KEY

# 3. Setup frontend (new terminal)
cd frontend
npm install
# Create .env file with VITE_API_URL

# 4. Run backend (terminal 1)
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# 5. Run frontend (terminal 2)
cd frontend
npm run dev

# 6. Open browser
# http://localhost:5173
```

## 📁 Project Structure

```
cultural-context-analyzer/
├── 📄 START_HERE.md              ← You are here!
├── 📄 QUICKSTART.md              ← 5-minute setup
├── 📄 SETUP_GUIDE.md             ← Detailed setup
├── 📄 README.md                  ← Main documentation
├── 📄 PROJECT_SUMMARY.md         ← Complete overview
├── 📄 DATABASE_COMMANDS.md       ← Database reference
├── 📄 COMMANDS_CHEATSHEET.md     ← Quick commands
├── 📄 setup.ps1                  ← Automated setup
├── 📄 .gitignore                 ← Git ignore rules
│
├── 📁 backend/                   ← Python FastAPI backend
│   ├── main.py                   ← API routes
│   ├── database.py               ← Database models
│   ├── gemini_service.py         ← AI integration
│   ├── requirements.txt          ← Python packages
│   └── .env.example              ← Environment template
│
└── 📁 frontend/                  ← React frontend
    ├── src/
    │   ├── App.jsx               ← Main component
    │   ├── main.jsx              ← Entry point
    │   └── index.css             ← Styles
    ├── package.json              ← Node packages
    ├── vite.config.js            ← Build config
    ├── tailwind.config.js        ← CSS config
    └── .env.example              ← Environment template
```

## ✅ Prerequisites Checklist

Before starting, make sure you have:

- [ ] **Python 3.9+** - [Download](https://www.python.org/downloads/)
- [ ] **Node.js 18+** - [Download](https://nodejs.org/)
- [ ] **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- [ ] **Gemini API Key** - [Get Key](https://makersuite.google.com/app/apikey)

## 🎓 How to Use the Application

1. **Enter Text**: Type or paste any literary or historical text
2. **Select Language**: Choose from 12+ supported languages
3. **Analyze**: Click "Analyze Cultural Context"
4. **View Results**: Get 4 comprehensive sections of analysis
5. **Review History**: Access previous analyses anytime

## 🌟 Example Use Cases

### For Students
- Understanding Shakespeare's cultural references
- Learning about ancient civilizations
- Connecting historical events to modern times
- Preparing for literature exams

### For Educators
- Creating engaging lesson materials
- Explaining cultural contexts
- Making history relatable
- Generating discussion topics

### For Researchers
- Cross-cultural analysis
- Historical documentation
- Cultural preservation
- Academic writing support

## 🔑 Key Features

✨ **AI-Powered Analysis** - Uses Google Gemini for intelligent insights  
🌍 **Multi-Language Support** - Works with 12+ languages  
💾 **History Tracking** - All analyses saved in PostgreSQL  
🎨 **Beautiful UI** - Modern, responsive design  
⚡ **Fast & Reliable** - Built with FastAPI and React  
📊 **Data Persistence** - Never lose your analyses  

## 🛠️ Technology Stack

**Backend:**
- FastAPI (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Google Gemini API (AI)

**Frontend:**
- React 18 (UI library)
- Vite (Build tool)
- TailwindCSS (Styling)
- Axios (HTTP client)

## 📞 Need Help?

### Common Issues

**Can't connect to database?**
→ Check [SETUP_GUIDE.md](SETUP_GUIDE.md) - Troubleshooting section

**Gemini API errors?**
→ Verify your API key at https://makersuite.google.com/app/apikey

**Port already in use?**
→ See [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md) - Kill Processes section

**Module not found errors?**
→ Reinstall dependencies (see SETUP_GUIDE.md)

## 🎯 Next Steps

1. **Choose your setup path** (Quick or Detailed)
2. **Follow the instructions** step by step
3. **Test the application** with sample texts
4. **Explore the features** and documentation
5. **Customize** as needed for your use case

## 📚 Documentation Index

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **START_HERE.md** | Navigation hub | First time here |
| **QUICKSTART.md** | Fast setup | Know what you're doing |
| **SETUP_GUIDE.md** | Detailed setup | Need step-by-step help |
| **README.md** | Main docs | Want overview |
| **PROJECT_SUMMARY.md** | Complete overview | Need full details |
| **DATABASE_COMMANDS.md** | DB reference | Working with database |
| **COMMANDS_CHEATSHEET.md** | Quick commands | Need quick reference |

## 🚀 Ready to Start?

1. **Quick Setup** → Go to [QUICKSTART.md](QUICKSTART.md)
2. **Detailed Setup** → Go to [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. **Learn More** → Go to [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 💡 Pro Tips

- **Use the automated setup script**: Run `setup.ps1` for automatic installation
- **Keep both terminals open**: One for backend, one for frontend
- **Check the API docs**: Visit http://localhost:8000/docs when backend is running
- **Save your API key**: Store it securely in the `.env` file
- **Backup regularly**: Use the database backup commands
- **Try examples first**: Use the provided example texts to test

## 🎉 What You'll Build

By following this guide, you'll have:
- ✅ A fully functional web application
- ✅ AI-powered cultural analysis
- ✅ Beautiful, modern UI
- ✅ Persistent data storage
- ✅ Multi-language support
- ✅ Complete documentation

## 📖 Sample Analysis

**Input:**
> "The Ramayana is an ancient Indian epic that tells the story of Prince Rama"

**Output:**
1. **Cultural Origin**: Ancient Indian Sanskrit epic from Hindu tradition, 5th-4th century BCE
2. **Cross-Cultural**: Influenced Southeast Asian cultures, adapted in Thailand, Indonesia, Cambodia
3. **Modern Analogy**: Like Marvel's interconnected universe with moral lessons and heroic journeys
4. **Visualization**: Traditional Indian miniature painting with vibrant colors, depicting key scenes

## 🌈 Let's Get Started!

Choose your path and begin your journey with the Cultural Context Analyzer!

**Recommended for beginners**: Start with [QUICKSTART.md](QUICKSTART.md)

**Recommended for developers**: Start with [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Questions?** Check the troubleshooting sections in SETUP_GUIDE.md

**Ready?** Let's build something amazing! 🚀

---

*Last Updated: 2024*  
*Version: 1.0.0*  
*Status: Production Ready ✅*
