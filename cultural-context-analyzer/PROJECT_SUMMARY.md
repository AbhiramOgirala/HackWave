# Cultural Context Analyzer - Project Summary

## Overview

The **Cultural Context Analyzer** is a full-stack web application that helps students and educators understand cultural and historical references in literature and texts. It uses Google's Gemini AI to provide comprehensive analysis in four key areas.

## Problem Statement

Literature and historical texts often contain cultural references that students miss. This tool bridges that gap by:
- Identifying cultural origins
- Explaining cross-cultural connections
- Providing modern analogies for better comprehension
- Suggesting visual representations

## Solution Architecture

### Technology Stack

**Backend:**
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Robust relational database for data persistence
- **SQLAlchemy**: ORM for database operations
- **Google Gemini API**: AI-powered cultural analysis
- **Python 3.9+**: Core programming language

**Frontend:**
- **React 18**: Modern UI library
- **Vite**: Fast build tool and dev server
- **TailwindCSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **Axios**: HTTP client for API calls

**Database:**
- **PostgreSQL 14+**: Stores all analysis history with full-text search capabilities

## Key Features

### 1. Four-Way Analysis
Every text input receives comprehensive analysis:

1. **Cultural Origin**: Identifies the primary culture, time period, and geographical context
2. **Cross-Cultural Connections**: Shows how the concept relates to or influenced other cultures
3. **Modern Analogy**: Provides relatable contemporary parallels
4. **Visualization Description**: Suggests visual representations with detailed prompts

### 2. Multi-Language Support
- Supports 12+ languages including:
  - English, Hindi, Spanish, French, German
  - Chinese, Japanese, Arabic
  - Bengali, Tamil, Telugu, Marathi
- Language detection and context-aware analysis

### 3. Analysis History
- Stores all analyses in PostgreSQL
- Quick access to previous analyses
- Search and filter capabilities
- Delete unwanted entries

### 4. Modern UI/UX
- Clean, intuitive interface
- Responsive design (mobile-friendly)
- Real-time loading states
- Beautiful gradient designs
- Smooth animations

## Project Structure

```
cultural-context-analyzer/
├── backend/
│   ├── main.py                    # FastAPI application & routes
│   ├── database.py                # SQLAlchemy models & connection
│   ├── gemini_service.py          # Gemini API integration
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment template
│   └── venv/                     # Virtual environment (created)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main React component
│   │   ├── main.jsx              # React entry point
│   │   └── index.css             # TailwindCSS styles
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── tailwind.config.js        # TailwindCSS config
│   ├── postcss.config.js         # PostCSS config
│   ├── .env.example              # Environment template
│   └── node_modules/             # Dependencies (created)
│
├── README.md                      # Main documentation
├── SETUP_GUIDE.md                # Detailed setup instructions
├── QUICKSTART.md                 # Quick start guide
├── DATABASE_COMMANDS.md          # PostgreSQL reference
├── PROJECT_SUMMARY.md            # This file
├── setup.ps1                     # Automated setup script
└── .gitignore                    # Git ignore rules
```

## API Endpoints

### POST /api/analyze
Analyzes text for cultural context

**Request:**
```json
{
  "text": "The Ramayana is an ancient Indian epic...",
  "language": "en"
}
```

**Response:**
```json
{
  "id": 1,
  "input_text": "The Ramayana is an ancient Indian epic...",
  "language": "en",
  "cultural_origin": "Detailed cultural origin analysis...",
  "cross_cultural_connections": "Cross-cultural connections...",
  "modern_analogy": "Modern analogy explanation...",
  "visualization_description": "Visualization details...",
  "image_url": "Enhanced image generation prompt...",
  "created_at": "2024-01-01T00:00:00"
}
```

### GET /api/history
Returns list of previous analyses (paginated)

### GET /api/analysis/{id}
Retrieves specific analysis by ID

### DELETE /api/analysis/{id}
Deletes specific analysis

### GET /api/stats
Returns statistics about analyses

## Database Schema

### Table: analyses

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| input_text | TEXT | Original text input |
| language | VARCHAR(10) | Language code (e.g., 'en', 'hi') |
| cultural_origin | TEXT | Cultural origin analysis |
| cross_cultural_connections | TEXT | Cross-cultural connections |
| modern_analogy | TEXT | Modern analogy explanation |
| visualization_description | TEXT | Visualization description |
| image_url | VARCHAR(500) | Enhanced image prompt |
| created_at | TIMESTAMP | Creation timestamp |

## Setup & Installation

### Quick Setup (5 Steps)

1. **Create Database**
   ```powershell
   psql -U postgres
   CREATE DATABASE cultural_context_db;
   ```

2. **Configure Backend** - Create `backend/.env`
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/cultural_context_db
   GEMINI_API_KEY=your_api_key
   ```

3. **Install Backend**
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Configure Frontend** - Create `frontend/.env`
   ```env
   VITE_API_URL=http://localhost:8000
   ```

5. **Install Frontend**
   ```powershell
   cd frontend
   npm install
   ```

### Running the Application

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```
Access at: http://localhost:8000

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```
Access at: http://localhost:5173

## Usage Examples

### Example 1: Indian Epic
**Input:**
```
The Ramayana is an ancient Indian epic that tells the story of 
Prince Rama's quest to rescue his wife Sita from the demon king Ravana.
```

**Output:**
- **Cultural Origin**: Ancient Indian Sanskrit epic, Hindu tradition
- **Cross-Cultural**: Influenced Southeast Asian cultures (Thailand, Indonesia)
- **Modern Analogy**: Like a superhero origin story with moral lessons
- **Visualization**: Traditional Indian miniature painting style

### Example 2: Japanese Poetry
**Input:**
```
Haiku is a traditional form of Japanese poetry consisting of three 
lines with a 5-7-5 syllable pattern, often focusing on nature.
```

**Output:**
- **Cultural Origin**: Japanese Edo period poetry tradition
- **Cross-Cultural**: Adopted by Western poets, influenced Imagism
- **Modern Analogy**: Like Twitter's character limit forcing creativity
- **Visualization**: Japanese scroll with calligraphy and nature scenes

### Example 3: European Renaissance
**Input:**
```
The Renaissance was a period of cultural rebirth in Europe, marked 
by renewed interest in classical art, literature, and learning.
```

**Output:**
- **Cultural Origin**: 14th-17th century European cultural movement
- **Cross-Cultural**: Spread from Italy across Europe
- **Modern Analogy**: Like the digital revolution transforming society
- **Visualization**: Renaissance art and architecture montage

## Key Implementation Details

### Gemini API Integration
- Uses `gemini-pro` model for text analysis
- Structured JSON responses for consistent parsing
- Error handling and fallback responses
- Prompt engineering for educational context

### Database Design
- Normalized schema for efficient storage
- Indexes on frequently queried columns
- Timestamp tracking for history
- Support for full-text search

### Frontend Architecture
- Component-based React design
- State management with hooks
- Responsive grid layout
- Loading states and error handling
- Real-time API communication

### Security Considerations
- Environment variables for sensitive data
- CORS configuration for API access
- SQL injection prevention via ORM
- Input validation and sanitization

## Performance Optimizations

1. **Database**: Indexed queries, connection pooling
2. **API**: Async/await for non-blocking operations
3. **Frontend**: Code splitting, lazy loading
4. **Caching**: Browser caching for static assets

## Future Enhancements

### Potential Features
- [ ] Image generation integration (DALL-E, Stable Diffusion)
- [ ] Audio explanations (text-to-speech)
- [ ] User authentication and personal libraries
- [ ] Collaborative annotations
- [ ] Export to PDF/Word
- [ ] Mobile app (React Native)
- [ ] Advanced search and filtering
- [ ] Cultural timeline visualization
- [ ] Interactive cultural maps
- [ ] Quiz generation from analyses

### Technical Improvements
- [ ] Redis caching for frequent queries
- [ ] WebSocket for real-time updates
- [ ] GraphQL API alternative
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Unit and integration tests
- [ ] API rate limiting
- [ ] Monitoring and analytics

## Documentation Files

1. **README.md**: Main project documentation
2. **SETUP_GUIDE.md**: Detailed setup instructions with troubleshooting
3. **QUICKSTART.md**: 5-minute quick start guide
4. **DATABASE_COMMANDS.md**: Complete PostgreSQL reference
5. **PROJECT_SUMMARY.md**: This comprehensive overview

## Commands Reference

### Database Commands
```sql
-- View all analyses
SELECT * FROM analyses ORDER BY created_at DESC;

-- Count by language
SELECT language, COUNT(*) FROM analyses GROUP BY language;

-- Backup database
pg_dump -U postgres cultural_context_db > backup.sql
```

### Development Commands
```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# Frontend
cd frontend
npm run dev

# Build frontend
npm run build
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify credentials in `.env`
   - Test connection: `psql -U postgres`

2. **Gemini API Error**
   - Verify API key is valid
   - Check internet connection
   - Review API quota limits

3. **Port Already in Use**
   - Backend: `netstat -ano | findstr :8000`
   - Frontend: `netstat -ano | findstr :5173`
   - Kill process: `taskkill /PID <PID> /F`

## Dependencies

### Backend (Python)
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- python-dotenv==1.0.0
- google-generativeai==0.3.1
- pillow==10.1.0
- python-multipart==0.0.6

### Frontend (Node.js)
- react==18.2.0
- react-dom==18.2.0
- axios==1.6.2
- lucide-react==0.294.0
- vite==5.0.8
- tailwindcss==3.3.6

## License

MIT License - Free for educational and commercial use

## Support & Resources

- **Gemini API**: https://makersuite.google.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## Conclusion

The Cultural Context Analyzer is a production-ready application that demonstrates:
- Modern full-stack development practices
- AI integration for educational purposes
- Clean architecture and code organization
- Comprehensive documentation
- User-friendly interface design

Perfect for educational institutions, students, researchers, and anyone interested in understanding cultural contexts in literature and historical texts.

---

**Created**: 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
