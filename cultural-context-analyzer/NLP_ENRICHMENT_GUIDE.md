# NLP and Cultural Context Enrichment Module

## 🎯 Overview

The NLP enrichment module adds **automatic detection and explanation of cultural, historical, and literary references** within any text. It combines spaCy's Named Entity Recognition (NER) with Wikipedia/Wikidata APIs to provide verified background summaries that appear as interactive highlights and tooltips in the frontend.

## 🏗️ Architecture

### Three-Layer Pipeline

```
Input Text
    ↓
[1] spaCy NER → Extract cultural entities
    ↓
[2] Wikipedia/Wikidata API → Fetch verified summaries
    ↓
[3] Supabase Cache → Store for performance
    ↓
Frontend Display → Interactive highlights with tooltips
```

## 🔧 Components

### Backend Services

#### 1. **nlp_service.py** - NLP Enrichment Orchestrator
- **Entity Extraction**: Uses spaCy `en_core_web_sm` model
- **Detected Types**: PERSON, ORG, GPE, EVENT, WORK_OF_ART, FAC, NORP, LANGUAGE
- **Filters**: Removes short entities, common words, duplicates
- **Enrichment**: Coordinates Wikipedia lookup with caching

**Key Functions:**
```python
extract_entities(text) → List[Entity]           # spaCy NER
enrich_entity(name, type) → EnrichedData        # Wikipedia + cache
analyze_text_with_entities(text) → FullAnalysis # Complete pipeline
get_entity_highlights(text) → Highlights        # Frontend-optimized
```

#### 2. **wikipedia_service.py** - Wikipedia/Wikidata Integration
- **Rate Limiting**: 100ms between requests (configurable)
- **Fallback**: Wikipedia → Wikidata if not found
- **Summary Extraction**: First 3 sentences, max 300 chars
- **Cultural Classification**: 9 categories (mythological, historical, literary, etc.)

**Key Functions:**
```python
get_entity_summary(name, type) → Summary        # Wikipedia lookup
get_wikidata_info(name) → WikidataData          # Wikidata fallback
enrich_entity(name, type) → CombinedData        # Both sources
```

**Cultural Significance Categories:**
- `mythological` - Mythology, folklore, legends
- `historical` - Ancient/classical/medieval periods
- `literary` - Books, poetry, novels
- `philosophical` - Philosophy, thinkers
- `religious` - Religious figures, texts
- `artistic` - Art, music, paintings
- `geographical` - Places, locations
- `biographical` - People, organizations
- `general` - Uncategorized

#### 3. **database.py** - Entity Caching
- **Table**: `entity_cache` (entity_name, type, summary, url, categories, etc.)
- **Unique Constraint**: (entity_name, entity_type) prevents duplicates
- **TTL**: `clear_old_entity_cache(days=30)` for cleanup

**New Functions:**
```python
get_cached_entity(name, type) → CachedData
save_entity_cache(data) → SavedRecord
get_all_cached_entities(limit) → List[Records]
clear_old_entity_cache(days) → void
```

### Frontend Components

#### 1. **EntityHighlight.jsx** - Interactive Text Highlighting
- **Segments**: Splits text into plain text + highlighted entities
- **Color Coding**: 9 colors based on cultural significance
- **Tooltips**: Appear on hover/click with:
  - Entity name + type badge
  - Cultural significance label
  - Wikipedia summary (3 sentences)
  - Source attribution
  - "Learn More" link to Wikipedia

#### 2. **EntityLegend.jsx** - Visual Guide
- Shows color meanings with emoji icons
- Usage hint for users

#### 3. **EntitySummary.jsx** - Statistics Card
- Total detected entities
- Enriched count (with Wikipedia data)
- Breakdown by significance type

### Database Schema

#### New Table: `entity_cache`
```sql
CREATE TABLE entity_cache (
    id BIGSERIAL PRIMARY KEY,
    entity_name TEXT NOT NULL,
    entity_type TEXT NOT NULL,          -- PERSON, ORG, GPE, etc.
    summary TEXT,                       -- Wikipedia summary
    url TEXT,                           -- Wikipedia URL
    categories JSONB DEFAULT '[]',      -- Cultural categories
    cultural_significance TEXT,         -- Classification
    wikidata JSONB,                     -- Wikidata metadata
    source TEXT,                        -- "Wikipedia" or "Wikidata"
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(entity_name, entity_type)
);
```

#### Updated Table: `analyses`
```sql
ALTER TABLE analyses 
ADD COLUMN detected_entities JSONB DEFAULT '[]';
```

**Entity Structure:**
```json
{
  "text": "Odysseus",
  "type": "PERSON",
  "start": 42,
  "end": 50,
  "summary": "In Greek mythology, Odysseus is the legendary...",
  "url": "https://en.wikipedia.org/wiki/Odysseus",
  "cultural_significance": "mythological",
  "source": "Wikipedia"
}
```

## 📡 API Endpoints

### Existing (Modified)

#### POST `/api/analyze`
**New Behavior**: Now includes NLP entity extraction automatically

**Response** (new fields):
```json
{
  "id": 123,
  "input_text": "...",
  "detected_entities": [
    {
      "text": "Zeus",
      "type": "PERSON",
      "start": 10,
      "end": 14,
      "summary": "Zeus is the sky god...",
      "cultural_significance": "mythological"
    }
  ],
  ... (existing fields)
}
```

### New Endpoints

#### POST `/api/entities/extract`
On-demand entity extraction without full Gemini analysis.

**Request:**
```json
{
  "text": "Achilles fought in the Trojan War"
}
```

**Response:**
```json
{
  "entities": [
    {
      "text": "Achilles",
      "type": "PERSON",
      "summary": "...",
      "cultural_significance": "mythological"
    },
    {
      "text": "Trojan War",
      "type": "EVENT",
      "summary": "...",
      "cultural_significance": "historical"
    }
  ],
  "total_detected": 2,
  "enriched_count": 2
}
```

#### GET `/api/entities/highlights?text={text}`
Frontend-optimized highlights format.

**Response:**
```json
{
  "highlights": [
    {
      "start": 0,
      "end": 8,
      "text": "Achilles",
      "type": "PERSON",
      "tooltip": {
        "title": "Achilles",
        "summary": "...",
        "significance": "mythological",
        "url": "https://...",
        "source": "Wikipedia"
      }
    }
  ],
  "count": 1
}
```

## 🎨 Frontend Integration

### App.jsx Changes

**New Import:**
```jsx
import { EntityHighlight, EntityLegend, EntitySummary } from './components/EntityHighlight';
```

**New Section** (appears first in results):
```jsx
{result.detected_entities && result.detected_entities.length > 0 && (
  <>
    <EntitySummary entities={result.detected_entities} />
    
    <div className="section-card">
      <EntityLegend />
      <EntityHighlight 
        text={result.input_text} 
        entities={result.detected_entities} 
      />
    </div>
  </>
)}
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```powershell
# Run automated setup
.\setup-nlp.ps1

# Or manually:
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Database Migration

Run in **Supabase SQL Editor**:
```sql
-- See: backend/entity_cache_migration.sql
CREATE TABLE entity_cache (...);
ALTER TABLE analyses ADD COLUMN detected_entities JSONB;
```

### 3. Verify Installation

**Check spaCy:**
```python
import spacy
nlp = spacy.load("en_core_web_sm")
print("✅ spaCy loaded")
```

**Check Wikipedia API:**
```python
from backend.wikipedia_service import wikipedia_service
result = wikipedia_service.get_entity_summary("Homer", "PERSON")
print(result["summary"])
```

## 🧪 Testing

### Sample Texts for Testing

**1. Greek Mythology:**
```
Odysseus, the cunning hero of Homer's Odyssey, journeyed 
for ten years after the Trojan War to return to Ithaca.
```

**Expected Entities:**
- Odysseus (PERSON, mythological)
- Homer (PERSON, literary)
- Odyssey (WORK_OF_ART, literary)
- Trojan War (EVENT, historical)
- Ithaca (GPE, geographical)

**2. Historical Reference:**
```
Julius Caesar crossed the Rubicon River in 49 BC, 
leading to the Roman Civil War.
```

**Expected Entities:**
- Julius Caesar (PERSON, biographical/historical)
- Rubicon (GPE, geographical/historical)
- Roman Civil War (EVENT, historical)

**3. Literary Work:**
```
Dante's Divine Comedy guides readers through Hell, 
Purgatory, and Paradise, exploring medieval theology.
```

**Expected Entities:**
- Dante (PERSON, literary)
- Divine Comedy (WORK_OF_ART, literary)
- Hell (LOC, religious)
- Purgatory (LOC, religious)
- Paradise (LOC, religious)

### Validation Checklist

- [ ] Entities detected with correct types
- [ ] Wikipedia summaries fetched (check tooltips)
- [ ] Colors match cultural significance
- [ ] Tooltips appear on hover
- [ ] "Learn More" links work
- [ ] Entity cache populated in Supabase
- [ ] Second analysis uses cache (faster)
- [ ] All 9 significance categories rendering
- [ ] Mobile-friendly tooltips
- [ ] No duplicate entities

## 🔍 Troubleshooting

### spaCy Model Not Found
```
❌ OSError: Can't find model 'en_core_web_sm'
```

**Solution:**
```powershell
python -m spacy download en_core_web_sm
```

### Wikipedia Rate Limiting
```
⚠️ Too many requests
```

**Solution**: Adjust `min_request_interval` in `wikipedia_service.py`:
```python
self.min_request_interval = 0.5  # Slower requests
```

### No Entities Detected
**Possible Causes:**
1. Text too short (< 10 chars)
2. No named entities in text
3. spaCy model not loaded

**Debug:**
```python
from backend.nlp_service import nlp_service
entities = nlp_service.extract_entities("Your text here")
print(f"Found: {len(entities)} entities")
```

### Entity Cache Not Working
**Check Supabase:**
1. Table `entity_cache` exists?
2. Unique constraint on (entity_name, entity_type)?
3. Check backend logs for Supabase errors

**Manual Query:**
```sql
SELECT * FROM entity_cache WHERE entity_name = 'Odysseus';
```

## 📊 Performance Optimization

### Caching Strategy
- **First lookup**: ~1-2 seconds (Wikipedia API call)
- **Cached lookup**: ~50ms (Supabase query)
- **Cache TTL**: 30 days (configurable)

### Enrichment Limits
```python
# nlp_service.py
max_enrich = 10 if enrich_all else 5
```

**Rationale**: Enriching 100 entities would take 100+ seconds. Limit to 5-10 for reasonable response time.

### Optimization Tips
1. **Batch Processing**: Process multiple texts in background job
2. **Pre-warming**: Cache common entities (Greek gods, famous authors)
3. **CDN**: Serve Wikipedia summaries from CDN
4. **Async Processing**: Use async Wikipedia calls (future enhancement)

## 🎓 Educational Value

### Learning Outcomes
1. **Contextual Understanding**: Students see cultural background instantly
2. **Cross-References**: Discover related entities through Wikipedia links
3. **Visual Learning**: Color-coded significance aids memory
4. **Curiosity Driven**: "Learn More" encourages deeper exploration
5. **Historical Awareness**: Timeline + entity data creates full picture

### Use Cases
- **Literature Classes**: Identify allusions in poetry, novels
- **History Studies**: Understand historical figures/events
- **World Religions**: Recognize religious figures, texts
- **Art History**: Discover artists, movements, artworks
- **Philosophy**: Learn about thinkers, concepts

## 🔮 Future Enhancements

### Planned Features
1. **Hugging Face Classification**: Semantic analysis of cultural significance
2. **Entity Relationships**: Show connections between entities
3. **Multi-language Support**: spaCy models for other languages
4. **Custom Entity Types**: User-defined cultural categories
5. **Wikidata Knowledge Graph**: Rich metadata (birth dates, locations)
6. **Image Integration**: Entity photos from Wikipedia
7. **Audio Pronunciations**: Learn how to say names correctly
8. **Similar Entities**: "People also viewed" recommendations

### Code Placeholders
```python
# nlp_service.py - Line 250
def classify_cultural_significance_ml(self, text, entity_text):
    # TODO: Implement HF transformers classification
    # Use distilbert-base-uncased fine-tuned for cultural categories
    pass
```

## 📚 References

- **spaCy Documentation**: https://spacy.io/usage/linguistic-features#named-entities
- **Wikipedia API**: https://wikipedia-api.readthedocs.io/
- **Wikidata API**: https://www.wikidata.org/w/api.php
- **NER Best Practices**: https://spacy.io/usage/training#ner

## 🤝 Contributing

### Adding New Entity Types
1. Update `cultural_entity_types` in `nlp_service.py`
2. Add color mapping in `EntityHighlight.jsx`
3. Update significance classifier in `wikipedia_service.py`

### Improving Wikipedia Summaries
1. Adjust `max_sentences` in `_extract_summary()`
2. Enhance category filtering in `_get_cultural_categories()`
3. Add custom extraction rules for specific entity types

---

**Built with ❤️ for educational enrichment**
