# Cultural Context Analyzer - AI Agent Instructions

## Project Overview
Full-stack educational app that analyzes cultural/historical context in texts using Google Gemini AI. Built with FastAPI (backend), React + Vite (frontend), and Supabase (PostgreSQL database).

**Purpose:** Help students understand cultural references in literature through AI-generated analysis covering cultural origins, cross-cultural connections, modern analogies, and visual descriptions.

## Architecture & Data Flow

### Three-Tier System
1. **Frontend (React)**: User input → API calls → Display results with interactive features
2. **Backend (FastAPI)**: API endpoints → Gemini AI orchestration → Database persistence
3. **Database (Supabase)**: Cloud PostgreSQL storing all analyses with enhanced v2.0 fields

**Critical Flow:**
- User submits text → `POST /api/analyze` → `gemini_service.analyze_cultural_context()` → Structured JSON parsing → `save_analysis()` → Supabase insert → Returns enriched analysis with ID

### Key Integration Points
- **Gemini API**: Uses `gemini-2.5-flash` model for all analysis, structured JSON responses required
- **Supabase SDK**: NOT raw SQL - uses Python Supabase client (`.table().insert()/.select()/.delete()`)
- **CORS**: Backend allows all origins (`allow_origins=["*"]`) - tighten for production

## Database Schema (Supabase)

**Table: `analyses`**
```sql
-- Core fields (v1.0)
id, input_text, language, cultural_origin, cross_cultural_connections, 
modern_analogy, visualization_description, image_url, created_at

-- Enhanced fields (v2.0 - JSONB columns)
timeline_events JSONB[]      -- Historical events with year/title/description/significance
geographic_locations JSONB[]  -- Places with coordinates, names, significance
key_concepts JSONB[]          -- Terms with definitions, context, modern_parallel
external_resources JSONB      -- Links to timelines, maps, further reading
```

**Schema managed via Supabase SQL Editor**, not migrations. See `supabase_setup.sql` or `database_migration.sql`.

## Development Workflow

### Running Locally (PowerShell)
```powershell
# Backend (Terminal 1)
cd backend
.\venv\Scripts\Activate.ps1
python main.py  # Runs on :8000, auto-reloads

# Frontend (Terminal 2)
cd frontend
npm run dev  # Runs on :5173, hot module reload
```

### Environment Setup
**Backend `.env`** (required):
```env
GEMINI_API_KEY=...
SUPABASE_URL=https://....supabase.co
SUPABASE_ANON_KEY=...
```

**Frontend `.env`** (optional):
```env
VITE_API_URL=http://localhost:8000  # Default fallback exists
```

### Database Operations
- **NO local psql needed** - use Supabase Dashboard > SQL Editor
- Table auto-initialization removed; schema must exist before first run
- Access client: `from database import get_db; supabase = get_db()`

## Critical Code Patterns

### 1. Gemini Response Parsing (`gemini_service.py`)
**Problem:** AI sometimes wraps JSON in markdown or adds commentary.

**Solution:**
```python
# Clean markdown code blocks
result_text = re.sub(r'^```json\s*', '', result_text, flags=re.IGNORECASE)

# Extract JSON by brace-counting (handles text before/after JSON)
start_idx = result_text.find('{')
# ... (see gemini_service.py lines ~120-135)
```

**Validation:** Always check required fields, provide empty arrays for optional enhanced fields (`timeline_events`, etc.) if missing.

### 2. Conditional Enhanced Features
Gemini prompt includes **conditional logic** - only populate enhanced fields when relevant:
- `timeline_events`: Only for historical context with dates/periods; **focus on cultural period, NOT author biography**
- `geographic_locations`: Only when specific places matter to understanding
- `key_concepts`: Only cultural/technical terms needing explanation
- `external_resources`: Only **real, verified URLs** from Khan Academy, National Geographic, etc.

**Return empty arrays/objects when not applicable** to avoid UI clutter.

### 3. Frontend State Management (`App.jsx`)
- Local state with `useState` - no Redux/Context (simple app)
- Collapsible sections: `showTimeline`, `showMap` control enhanced features visibility
- Modal explainers: `expandedConcept` tracks which concept popup is open
- History auto-refreshes after new analysis via `fetchHistory()`

### 4. API Response Model
Uses Pydantic with `model_config = {"from_attributes": True}` to convert Supabase dict responses to models.

## Common Tasks

### Adding New Analysis Field
1. Update Supabase schema via SQL Editor (JSONB for structured data)
2. Modify `Analysis` class in `database.py` (add to `__init__` and `to_dict()`)
3. Update Gemini prompt in `gemini_service.analyze_cultural_context()` 
4. Add to `AnalysisResponse` Pydantic model in `main.py`
5. Render in `App.jsx` with appropriate UI component

### Debugging Gemini Responses
Check backend terminal for:
```
🤖 AI Response length: X characters
📝 Cleaned JSON length: Y characters
✅ Analysis completed successfully
   - Timeline events: N
```

If JSON parse fails, response preview printed (first 500 chars).

### Supabase Connection Issues
- Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `.env`
- Check network (cloud service requires internet)
- Test in Supabase Dashboard first before blaming code
- Connection established at module load: `supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)`

## Testing Strategy

**Current state:** No automated tests (educational project).

**Manual testing checklist:**
- Try all 3 example texts in UI
- Test 12 supported languages
- Verify enhanced features (timeline/map/concepts) appear when relevant
- Check history delete functionality
- Test error states (empty text, API failures)

## Known Limitations & Design Decisions

1. **No authentication** - all analyses publicly stored in Supabase (RLS disabled)
2. **CORS wide open** - `allow_origins=["*"]` fine for local dev, needs restriction for deployment
3. **No rate limiting** - Gemini API quota managed externally
4. **No image generation** - `image_url` field stores *text prompt* for external generators (DALL-E, Midjourney)
5. **Synchronous DB calls** - Supabase client doesn't require async for simple CRUD
6. **Frontend single-component** - All logic in `App.jsx` (manageable at current scale)

## Project-Specific Conventions

- **Error handling**: Gemini failures return structured error objects (not exceptions) with helpful messages
- **Timestamps**: UTC via `datetime.utcnow().isoformat()`, Supabase stores as string
- **Language codes**: ISO 639-1 (2-letter: `en`, `hi`, `ja`)
- **Console logging**: Emoji prefixes for log levels (✅ success, ❌ error, ℹ️ info, 🤖 AI response)
- **File organization**: Backend single-level (3 files), frontend standard Vite structure

## External Dependencies

**Critical APIs:**
- Google Gemini API (`google-generativeai` Python SDK)
- Supabase (`supabase-py` client, NOT `psycopg2`)

**UI libraries:**
- Lucide React for icons (tree-shakeable)
- TailwindCSS via utility classes (no custom CSS beyond `index.css`)

## Quick Reference

**Find code for:**
- Gemini prompt engineering → `gemini_service.py:48-150`
- Database queries → `database.py:55-80`
- API endpoint definitions → `main.py:40-140`
- Enhanced features UI → `App.jsx:300-600`
- Environment validation → `database.py:10-20`

**Documentation files:**
- Architecture deep-dive → `PROJECT_SUMMARY.md`
- Setup instructions → `SETUP_GUIDE.md`, `SUPABASE_SETUP.md`
- Feature descriptions → `ENHANCED_FEATURES.md`
- Quick reference → `QUICKSTART.md`
