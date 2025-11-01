# Cultural Context Analyzer

A powerful tool that analyzes literature and historical texts to provide cultural context, cross-cultural connections, modern analogies, and visual representations. Supports multiple regional languages using Google's Gemini API.

## Features

- **Cultural Origin Analysis**: Identifies the primary culture related to the text
- **Cross-Cultural Connections**: Shows how the content relates to other cultures
- **Modern Analogies**: Provides contemporary parallels for better understanding
- **Visual Context**: Generates relevant images for visualization
- **Multi-language Support**: Works with various regional languages
- **History Tracking**: Stores all analyses in PostgreSQL database

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Robust database for storing analyses
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
- PostgreSQL 14+
- Google Gemini API Key

## Installation

### 1. Clone and Setup

```bash
cd cultural-context-analyzer
```

### 2. Database Setup

```bash
# Start PostgreSQL (if not running)
# Windows (if using PostgreSQL service):
# Services -> PostgreSQL -> Start

# Create database
psql -U postgres
CREATE DATABASE cultural_context_db;
\q
```

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
# Copy .env.example to .env and add your credentials
```

Create `backend/.env` file:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/cultural_context_db
GEMINI_API_KEY=your_gemini_api_key_here
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

## Database Commands

### Initialize Database Tables

The tables are automatically created when you first run the backend. To manually reset:

```bash
cd backend
venv\Scripts\activate
python -c "from database import init_db; init_db()"
```

### View Database Data

```bash
psql -U postgres -d cultural_context_db

# List all analyses
SELECT * FROM analyses;

# View specific analysis
SELECT * FROM analyses WHERE id = 1;

# Count total analyses
SELECT COUNT(*) FROM analyses;
```

### Backup Database

```bash
pg_dump -U postgres cultural_context_db > backup.sql
```

### Restore Database

```bash
psql -U postgres cultural_context_db < backup.sql
```

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
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check credentials in `.env`
- Verify database exists: `psql -U postgres -l`

### Gemini API Errors
- Verify API key is valid
- Check API quota limits
- Ensure internet connection

### Port Already in Use
- Backend: Change port in `main.py` (default: 8000)
- Frontend: Change port in `vite.config.js` (default: 5173)

## License

MIT License
