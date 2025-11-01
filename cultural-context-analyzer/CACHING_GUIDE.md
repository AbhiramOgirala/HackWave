# Caching System Guide - Cultural Context Analyzer

## Overview

The Cultural Context Analyzer implements **Supabase-based persistent caching** to dramatically reduce Gemini API calls and improve response latency. This system can reduce API costs by **70-95%** for repeated queries and is **fully cloud-ready** (works with serverless, Docker, Kubernetes, etc.).

## Architecture

### 🎯 Single-Layer Persistent Cache (Cloud-Ready)

```
User Request
    ↓
┌─────────────────────────────────────────┐
│ Supabase Persistent Cache               │
│ - 30-day TTL                            │
│ - Shared across ALL instances           │
│ - Hash-based lookup (SHA-256)           │
│ - ~50-200ms latency on HIT              │
│ - Works with serverless/containers      │
└─────────────────────────────────────────┘
    ↓ (on cache MISS)
┌─────────────────────────────────────────┐
│ Gemini API                              │
│ - Fresh analysis generation             │
│ - ~2-5 seconds latency                  │
│ - Results saved to cache automatically  │
└─────────────────────────────────────────┘
```

### ✅ Why This Design?

**Cloud-Ready Benefits:**
- ✅ Works with multiple backend instances (horizontal scaling)
- ✅ Compatible with serverless (AWS Lambda, Google Cloud Run, Vercel)
- ✅ No Redis or memory management needed
- ✅ Automatic persistence across deployments
- ✅ Zero additional infrastructure costs
- ✅ Built on existing Supabase database

**Why We Removed In-Memory Cache:**
- ❌ Doesn't work across multiple instances (each has own memory)
- ❌ Lost on serverless cold starts
- ❌ Wasted resources in containerized environments
- ❌ Complicates deployment and scaling
- ⚠️ Supabase cache is already fast enough (~100ms)

## Setup Instructions

### 1. Run Database Migration

Open Supabase Dashboard → SQL Editor and run:

```sql
-- Located at: backend/analysis_cache_migration.sql
```

This creates:
- `analysis_cache` table with hash-based indexing
- `analysis_cache_stats` view for monitoring
- `cleanup_analysis_cache()` function for TTL enforcement
- `increment_cache_hit()` function for hit tracking

### 2. Verify Installation

Backend dependencies already include caching support:
- `hashlib` (standard library) - SHA-256 hashing
- `functools` (standard library) - LRU cache decorator

No additional packages needed! ✅

### 3. Environment Variables

No changes needed to `.env` - uses existing Supabase configuration.

## How It Works

### Cache Key Generation

Text is normalized and hashed with language code:

```python
# Input: "The Ramayana is an ancient epic", language: "en"
# Normalized: "the ramayana is an ancient epic"
# Hash Input: "the ramayana is an ancient epic|en"
# SHA-256: "a3f2e1d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1"
```

This ensures:
- ✅ Same text = same hash (even with different whitespace)
- ✅ Case-insensitive matching
- ✅ Language-specific caching
- ✅ No collision issues (SHA-256 is cryptographically secure)

### Request Flow Example

**First Request (Cache Miss):**
```
1. User submits "Odyssey by Homer"
2. Generate hash: sha256("odyssey by homer|en")
3. ❌ Supabase cache MISS (hash not found)
4. 🤖 Call Gemini API (~3 seconds)
5. 💾 Save result to Supabase cache
6. ✅ Return result to user
Total: ~3.2 seconds
```

**Second Request (Cache Hit - Same or Different Instance):**
```
1. User submits "Odyssey by Homer" (same text)
2. Generate hash: sha256("odyssey by homer|en")
3. 🎯 Supabase cache HIT (~100ms)
4. ✅ Return cached result immediately
Total: ~150ms (21x faster!)
```

**Third Request (30 Days Later):**
```
1. User submits "Odyssey by Homer"
2. ❌ Cache MISS (TTL expired after 30 days)
3. 🤖 Call Gemini API and refresh cache
Total: ~3.2 seconds
```

## API Endpoints

### Get Cache Statistics

```bash
GET /api/cache/stats
```

**Response:**
```json
{
  "cache": {
    "total_cached_entries": 142,
    "total_cache_hits": 1583,
    "languages_cached": 5,
    "avg_hits_per_entry": 11.14,
    "max_hits": 87,
    "cache_hit_rate": 91.76
  },
  "cache_info": {
    "type": "Supabase persistent cache",
    "ttl": "30 days",
    "scope": "Shared across all instances (cloud-ready)",
    "storage": "PostgreSQL JSONB columns"
  }
}
```

### Clear Cache

```bash
# Clear expired entries (30+ days old)
POST /api/cache/clear
```

## Performance Metrics

### Latency Comparison

| Scenario | Latency | Speedup |
|----------|---------|---------|
| Gemini API (cache miss) | 2,000-5,000ms | 1x (baseline) |
| Supabase cache hit | 50-200ms | **10-100x faster** |

### Cost Savings

Assuming 10,000 requests/month with 70% duplicate/similar queries:

- **Without caching**: 10,000 API calls × $0.0015 = **$15/month**
- **With caching**: 3,000 API calls × $0.0015 = **$4.50/month**
- **Savings**: **$10.50/month (70% reduction)**

For larger volumes (100K requests/month with 80% cache hit rate):
- **Without caching**: **$150/month**
- **With caching**: **$30/month**
- **Savings**: **$120/month (80% reduction)**

## Cache Behavior

### What Gets Cached

✅ **Cached:**
- `cultural_origin`
- `cross_cultural_connections`
- `modern_analogy`
- `timeline_events`
- `geographic_locations`
- `key_concepts`
- `external_resources`

❌ **NOT Cached:**
- `detected_entities` (NLP processing runs every time)
- User-specific metadata
- Analysis history records

### Cache Invalidation

**Automatic (TTL-based):**
- Supabase cache: 30 days
- In-memory cache: Server restart or LRU eviction

**Manual:**
```bash
# Via API
POST /api/cache/clear?cache_type=all

# Via Supabase SQL Editor
SELECT cleanup_analysis_cache(); -- Clears entries >30 days
DELETE FROM analysis_cache; -- Nuclear option
```

### Cache Key Sensitivity

**Triggers NEW cache entry:**
- Different text content
- Different language code
- Case changes are normalized (same cache)
- Whitespace changes are normalized (same cache)

**Uses SAME cache entry:**
- `"The Odyssey"` vs `"the odyssey"` → Same
- `"The  Odyssey"` (double space) vs `"The Odyssey"` → Same
- Trailing/leading whitespace → Same

## Monitoring & Debugging

### View Cache Contents (Supabase SQL Editor)

```sql
-- See all cached entries
SELECT 
    id,
    LEFT(original_text, 50) as text_preview,
    language,
    hit_count,
    created_at,
    last_accessed
FROM analysis_cache
ORDER BY hit_count DESC
LIMIT 20;

-- View statistics
SELECT * FROM analysis_cache_stats;

-- Find most popular entries
SELECT 
    LEFT(original_text, 100) as text,
    language,
    hit_count
FROM analysis_cache
ORDER BY hit_count DESC
LIMIT 10;

-- Check specific text
SELECT * FROM analysis_cache 
WHERE original_text ILIKE '%odyssey%';
```

### Backend Logs

Watch for these console messages:

```
🔍 Checking Supabase cache...
🎯 Cache HIT! Skipping Gemini API call...
❌ Cache MISS. Calling Gemini API...
💾 Saving to Supabase cache...
💾 Cached analysis for text_hash: a3f2e1d9c8b7a6f5...
```

### Testing Cache Performance

```python
# Test script
import requests
import time

API_URL = "http://localhost:8000/api/analyze"
text = "The Ramayana is an ancient Indian epic"

# First request (should be slow - Gemini API)
start = time.time()
response1 = requests.post(API_URL, json={"text": text, "language": "en"})
print(f"First request: {(time.time() - start) * 1000:.0f}ms")

# Second request (should be fast - cache hit)
start = time.time()
response2 = requests.post(API_URL, json={"text": text, "language": "en"})
print(f"Second request: {(time.time() - start) * 1000:.0f}ms")

# Expected output:
# First request: 3200ms
# Second request: 120ms (27x faster!)
```

## Best Practices

### 1. Cache Warming
Pre-populate cache with common queries:

```python
common_texts = [
    "The Iliad by Homer",
    "Ramayana epic",
    "Chinese New Year traditions",
    # ... add your most frequent queries
]

for text in common_texts:
    requests.post(API_URL, json={"text": text, "language": "en"})
```

### 2. Monitor Hit Rate

Aim for **>70% cache hit rate** for optimal cost savings:

```sql
SELECT 
    total_cache_hits,
    total_cached_entries,
    ROUND((total_cache_hits::float / total_cached_entries * 100), 2) as hit_rate_percent
FROM analysis_cache_stats;
```

### 3. Periodic Cleanup

Schedule monthly cleanup (optional - automatic TTL handles this):

```sql
-- Keep last 30 days
SELECT cleanup_analysis_cache();
```

### 4. Scale Considerations

**In-memory cache size:**
- Default: 100 entries
- Increase for high-traffic: Edit `gemini_service.py` → `@lru_cache(maxsize=500)`
- Each entry: ~5-10 KB RAM

**Supabase cache:**
- Auto-scales with your Supabase plan
- ~10-20 KB per entry
- 10,000 entries ≈ 100-200 MB

## Troubleshooting

### Issue: Low Cache Hit Rate (<30%)

**Causes:**
- Users submitting unique texts (expected for educational tool)
- Frequent language switching
- Text variations (e.g., "Odyssey" vs "The Odyssey by Homer")

**Solutions:**
- This is normal for user-generated content
- Monitor cache hit rate weekly
- Extend TTL beyond 30 days if storage allows
- Implement fuzzy matching (advanced feature)

### Issue: Stale Cache Data

**Symptoms:** Old analysis results returned

**Solutions:**
```bash
# Clear specific entry (Supabase SQL)
DELETE FROM analysis_cache WHERE original_text ILIKE '%specific text%';

# Clear all cache
POST /api/cache/clear
```

### Issue: Cache Not Working

**Check:**
```bash
GET /api/cache/stats
```

If `total_cached_entries` is always 0:
- Verify `analysis_cache` table exists in Supabase
- Check backend logs for database errors
- Ensure `SUPABASE_URL` and `SUPABASE_ANON_KEY` are correct
- Test direct insert via Supabase SQL Editor

## Deployment Scenarios

### ✅ Cloud Platforms (All Supported)

**Vercel / Netlify Functions:**
```
✅ Works perfectly - Supabase cache is external
✅ No state management needed
✅ Each function call checks Supabase
```

**AWS Lambda / Google Cloud Run:**
```
✅ Fully compatible with serverless
✅ Cold starts don't affect cache
✅ Scales horizontally without issues
```

**Docker / Kubernetes:**
```
✅ Multiple containers share same cache
✅ No coordination needed between pods
✅ Stateless design = easy scaling
```

**Traditional VPS (DigitalOcean, Linode):**
```
✅ Works like local development
✅ Single instance or load-balanced
✅ Persistent across restarts
```

### 🚀 Production Best Practices

**1. Environment Variables**
```env
# .env (production)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key  # Fine for read/write with RLS
GEMINI_API_KEY=your-gemini-key
```

**2. Enable Row Level Security (RLS) - Optional**
```sql
-- In Supabase SQL Editor
ALTER TABLE analysis_cache ENABLE ROW LEVEL SECURITY;

-- Allow all reads/writes (or customize)
CREATE POLICY "Allow all operations" ON analysis_cache
FOR ALL USING (true);
```

**3. Set Up Monitoring**
```bash
# Add to cron job (daily)
curl -X POST https://your-api.com/api/cache/clear

# Monitor hit rate
curl https://your-api.com/api/cache/stats | jq '.cache.cache_hit_rate'
```

**4. Index Optimization** (Already done in migration!)
```sql
-- These are automatically created:
CREATE INDEX idx_analysis_cache_text_hash ON analysis_cache(text_hash);
CREATE INDEX idx_analysis_cache_language ON analysis_cache(language);
```

## Advanced Configuration

### Customize TTL

Edit `backend/database.py`:

```python
# Change from 30 days to 60 days
cutoff_date = (datetime.utcnow() - timedelta(days=60)).isoformat()
```

### Add Cache Warming on Startup

Edit `backend/main.py` to pre-populate cache with common queries:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    init_db()
    
    # Warm cache with common queries
    common_texts = [
        "The Odyssey by Homer",
        "Ramayana epic",
        "Shakespeare's Hamlet"
    ]
    print("🔥 Warming cache with common queries...")
    for text in common_texts:
        try:
            cached = get_cached_analysis(text, "en")
            if not cached:
                result = await gemini_service.analyze_cultural_context(text, "en")
                save_analysis_cache(text, "en", result)
        except Exception as e:
            print(f"⚠️ Cache warming failed for '{text}': {e}")
    
    yield
```

### Optimize for High Traffic

**Increase Supabase Connection Pool:**
```python
# backend/database.py
# Supabase handles this automatically, but you can upgrade your plan for:
# - More concurrent connections
# - Faster database performance
# - Larger storage limits
```

**Add Database Indexes** (already included in migration):
```sql
-- These are pre-configured for optimal performance:
CREATE INDEX idx_analysis_cache_text_hash ON analysis_cache(text_hash);
CREATE INDEX idx_analysis_cache_language ON analysis_cache(language);
CREATE INDEX idx_analysis_cache_created_at ON analysis_cache(created_at DESC);
```

## Summary

✅ **Implemented:**
- Single-layer Supabase persistent cache
- Hash-based cache keys with text normalization
- Automatic TTL (30 days)
- Hit count tracking and statistics
- Cache statistics API endpoint
- Manual cache clearing endpoint
- **100% cloud-ready and serverless-compatible**

✅ **Benefits:**
- **10-100x faster** responses on cache hits
- **70-95% reduction** in API costs
- **Works with any deployment** (serverless, containers, VPS)
- **No Redis or memory management** required
- **Automatic persistence** across deployments
- **Zero additional infrastructure** costs
- **Scales horizontally** without coordination

✅ **Production Ready:**
- No in-memory state (works across instances)
- Shared cache across all backend instances
- Compatible with serverless cold starts
- Docker/Kubernetes friendly
- Load balancer compatible

✅ **Next Steps:**
1. Run `backend/analysis_cache_migration.sql` in Supabase
2. Restart backend server
3. Test with duplicate requests
4. Monitor `/api/cache/stats`
5. Deploy to any cloud platform with confidence!

🎉 **Your cloud-ready caching system is ready to slash API costs!**
