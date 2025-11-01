# Cultural Context Analyzer

A powerful tool that analyzes literature and historical texts to provide cultural context, cross-cultural connections, modern analogies, and visual representations. Supports multiple regional languages using Google's Gemini API.

## ✨ Enhanced Features (v2.0)

**NEW! Interactive Learning Tools:**
- 📅 **Interactive Timelines** - Chronological historical events with significance
- 🗺️ **Geographic Maps** - Interactive location mapping with Google Maps integration
- 📖 **Pop-Out Explainers** - Click to learn key cultural concepts in depth
- 🎯 **Advanced Analogies** - Contemporary references tailored for students (social media, gaming, tech culture)
- 🔗 **External Resources** - Curated links to timelines, maps, videos, and educational content

**[📖 See Full Feature Documentation →](ENHANCED_FEATURES.md)**

## Features

- **Cultural Origin Analysis**: Identifies the primary culture related to the text
- **Cross-Cultural Connections**: Shows how the content relates to other cultures
- **Modern Analogies**: Provides contemporary parallels for better understanding (now with student-friendly references!)
- **Visual Context**: Generates relevant images for visualization
- **Multi-language Support**: Works with various regional languages
- **History Tracking**: Stores all analyses in Supabase (PostgreSQL)
- **Interactive Timeline**: View historical events in chronological order ✨
- **Geographic Context**: Explore locations on interactive maps ✨
- **Concept Explainers**: Deep-dive into cultural terms and concepts ✨
- **Curated Resources**: Access verified educational materials ✨

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Supabase**: Cloud PostgreSQL database for storing analyses
- **SQLAlchemy**: ORM for database operations
- **Google Gemini API**: AI-powered cultural analysis
- **Pillow**: Image processing
- **python-multipart**: File upload support

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool
- **TailwindCSS**: Utility-first styling
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client

## Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase Account (free tier available)
- Google Gemini API Key

## Installation

### 1. Clone and Setup

```bash
cd cultural-context-analyzer
```

### 2. Database Setup (Supabase)

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database credentials from Project Settings → Database
4. See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed instructions

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example to .env and add your Supabase credentials
```

Create `backend/.env` file (see `.env.example` or `SUPABASE_SETUP.md`):
```env
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Database Connection
SUPABASE_DB_HOST=db.xxxxxxxxxxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-database-password
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
```

Create `frontend/.env` file:
```env
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend

```bash
cd backend
venv\Scripts\activate
python main.py
```

Backend will run on: `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

## Database Management

### Initialize Database Tables

The tables are automatically created when you first run the backend.

### View Database Data

Use the Supabase Dashboard:
1. Go to your project on [supabase.com](https://supabase.com)
2. Navigate to **Table Editor**
3. View the `analyses` table

Or use the SQL Editor:
```sql
-- List all analyses
SELECT * FROM analyses ORDER BY created_at DESC;

-- View specific analysis
SELECT * FROM analyses WHERE id = 1;

-- Count total analyses
SELECT COUNT(*) FROM analyses;
```

### Backup and Migration

Supabase provides automatic daily backups. For manual backups or migration from local PostgreSQL, see [SUPABASE_SETUP.md](SUPABASE_SETUP.md).

## API Endpoints

### POST /api/analyze
Analyze text for cultural context

**Request Body:**
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
Get analysis history

### GET /api/analysis/{id}
Get specific analysis by ID

## Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## Project Structure

```
cultural-context-analyzer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and connection
│   ├── gemini_service.py    # Gemini API integration
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component (Enhanced with interactive features!)
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── database_migration.sql   # NEW: Database schema updates
├── ENHANCED_FEATURES.md     # NEW: Complete feature documentation
├── UPDATE_GUIDE.md          # NEW: Quick update instructions
├── IMPLEMENTATION_SUMMARY.md # NEW: Implementation details
├── FEATURES_QUICK_REFERENCE.md # NEW: Visual quick reference
└── README.md
```

## 🚀 Enhanced Features Documentation

- **[ENHANCED_FEATURES.md](ENHANCED_FEATURES.md)** - Complete documentation of all new features
- **[UPDATE_GUIDE.md](UPDATE_GUIDE.md)** - Quick guide to update your existing installation
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[FEATURES_QUICK_REFERENCE.md](FEATURES_QUICK_REFERENCE.md)** - Visual quick reference guide

### What's New in v2.0?

#### 📅 Interactive Timelines
View historical events in beautiful, chronological timeline format with:
- Year/time period
- Event titles and descriptions
- Cultural significance explanations
- Expandable/collapsible interface

#### 🗺️ Geographic Map Integration
Explore cultural geography with:
- Exact GPS coordinates
- Historical and modern location names
- Direct Google Maps links
- Cultural significance of each location

#### 📖 Pop-Out Concept Explainers
Click any key concept to open a detailed modal with:
- Clear, student-friendly definitions
- Cultural context explanations
- Modern parallels and equivalents

#### 🎯 Advanced Contemporary Analogies
No more generic comparisons! Now get analogies that reference:
- Social media (TikTok, Instagram, Twitter/X)
- Gaming and streaming culture
- Technology and apps
- Current events and pop culture
- Gen Z/Millennial experiences

**Example:**
> Instead of: "Like a library"
> 
> You get: "Like having unlimited cloud storage with AI-powered search - vast information accessible instantly, organized intelligently for discovery, democratizing knowledge while requiring curation."

#### 🔗 Curated External Resources
Every analysis includes links to:
- Interactive timelines (Khan Academy, etc.)
- Interactive maps
- Educational videos (Crash Course, TED-Ed)
- Further reading materials

### Updating to v2.0

If you have an existing installation:

1. **Update database schema:**
   ```sql
   -- Run database_migration.sql in your Supabase SQL Editor
   ```

2. **Restart your services:**
   ```powershell
   # Backend
   cd backend
   .\venv\Scripts\Activate.ps1
   python main.py
   
   # Frontend
   cd frontend
   npm run dev
   ```

3. **See the full update guide:** [UPDATE_GUIDE.md](UPDATE_GUIDE.md)

## Troubleshooting

### Database Connection Issues
- Verify Supabase credentials in `.env`
- Check Supabase project is active
- Ensure database password is correct
- See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed troubleshooting

### Gemini API Errors
- Verify API key is valid
- Check API quota limits
- Ensure internet connection

### Port Already in Use
- Backend: Change port in `main.py` (default: 8000)
- Frontend: Change port in `vite.config.js` (default: 5173)

## License

MIT License
