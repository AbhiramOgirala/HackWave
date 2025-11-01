from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
import uvicorn

from database import (
    get_db, init_db, save_analysis, get_analysis, get_all_analyses,
    get_cached_analysis, save_analysis_cache, get_cache_statistics
)
from gemini_service import gemini_service
from nlp_service import nlp_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    init_db()
    print("✅ Database initialized successfully")
    print("🚀 Cultural Context Analyzer API is running")
    yield
    # Shutdown (if needed)


# Initialize FastAPI app
app = FastAPI(
    title="Cultural Context Analyzer API",
    description="API for analyzing cultural and historical context in texts",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class AnalyzeRequest(BaseModel):
    text: str
    language: Optional[str] = "en"


class AnalysisResponse(BaseModel):
    id: int
    input_text: str
    language: str
    cultural_origin: str
    cross_cultural_connections: str
    modern_analogy: str
    image_url: Optional[str]
    timeline_events: Optional[List[Dict[str, Any]]] = []
    geographic_locations: Optional[List[Dict[str, Any]]] = []
    key_concepts: Optional[List[Dict[str, Any]]] = []
    external_resources: Optional[Dict[str, Any]] = {}
    detected_entities: Optional[List[Dict[str, Any]]] = []
    created_at: datetime

    model_config = {"from_attributes": True}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cultural Context Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "history": "/api/history",
            "analysis": "/api/analysis/{id}"
        }
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text for cultural context with NLP entity enrichment
    
    This endpoint uses Supabase persistent caching to reduce API calls:
    - Check Supabase cache (30-day TTL)
    - On cache miss, call Gemini API and save to cache
    - NLP entity detection runs every time for accuracy
    
    This endpoint:
    1. Identifies the cultural origin
    2. Finds cross-cultural connections
    3. Provides modern analogies
    4. Generates visualization descriptions
    5. Detects and enriches cultural entities
    """
    
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text must be at least 10 characters long"
        )
    
    try:
        # Check Supabase persistent cache first
        print(f"🔍 Checking Supabase cache...")
        cached_result = get_cached_analysis(request.text, request.language or "en")
        
        if cached_result:
            print(f"🎯 Cache HIT! Skipping Gemini API call...")
            analysis_result = cached_result
        else:
            print(f"❌ Cache MISS. Calling Gemini API...")
            
            # Call Gemini API
            analysis_result = await gemini_service.analyze_cultural_context(
                text=request.text,
                language=request.language or "en"
            )
            
            # Save to Supabase cache for future requests
            print(f"💾 Saving to Supabase cache...")
            save_analysis_cache(request.text, request.language or "en", analysis_result)
        
        # Extract and enrich cultural entities with NLP (always runs for accuracy)
        print("🔍 Extracting cultural entities with NLP...")
        entity_analysis = nlp_service.analyze_text_with_entities(
            text=request.text,
            enrich_all=True
        )
        
        # Prepare data for Supabase
        analysis_data = {
            'input_text': request.text,
            'language': request.language,
            'cultural_origin': analysis_result["cultural_origin"],
            'cross_cultural_connections': analysis_result["cross_cultural_connections"],
            'modern_analogy': analysis_result["modern_analogy"],
            'image_url': None,  # Removed visualization feature
            'timeline_events': analysis_result.get("timeline_events", []),
            'geographic_locations': analysis_result.get("geographic_locations", []),
            'key_concepts': analysis_result.get("key_concepts", []),
            'external_resources': analysis_result.get("external_resources", {}),
            'detected_entities': entity_analysis.get("detected_entities", []),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Save to Supabase
        saved_analysis = save_analysis(analysis_data)
        
        print(f"✅ Analysis completed with {entity_analysis.get('enriched_count', 0)} enriched entities")
        
        return saved_analysis
        
    except Exception as e:
        print(f"Error in analyze_text: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )


@app.get("/api/history", response_model=List[AnalysisResponse])
async def get_history(
    skip: int = 0,
    limit: int = 20
):
    """
    Get analysis history
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
    """
    
    # Get all analyses from Supabase (already ordered by created_at desc)
    analyses = get_all_analyses(limit=limit)
    
    # Apply skip manually if needed
    if skip > 0:
        analyses = analyses[skip:]
    
    return analyses


@app.get("/api/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_by_id(analysis_id: int):
    """
    Get specific analysis by ID
    
    Args:
        analysis_id: ID of the analysis to retrieve
    """
    
    analysis = get_analysis(analysis_id)
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )
    
    return analysis


@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: int):
    """
    Delete specific analysis by ID
    
    Args:
        analysis_id: ID of the analysis to delete
    """
    
    supabase = get_db()
    
    # Check if exists
    analysis = get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )
    
    # Delete from Supabase
    try:
        supabase.table('analyses').delete().eq('id', analysis_id).execute()
        return {"message": f"Analysis {analysis_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting analysis: {str(e)}"
        )


@app.get("/api/stats")
async def get_stats():
    """Get statistics about analyses"""
    
    # Get all analyses to compute stats
    all_analyses = get_all_analyses(limit=1000)
    
    total_analyses = len(all_analyses)
    
    # Get language distribution
    language_distribution = {}
    for analysis in all_analyses:
        lang = analysis.get('language', 'en')
        language_distribution[lang] = language_distribution.get(lang, 0) + 1
    
    return {
        "total_analyses": total_analyses,
        "language_distribution": language_distribution
    }


class EntityExtractionRequest(BaseModel):
    text: str


@app.post("/api/entities/extract")
async def extract_entities(request: EntityExtractionRequest):
    """
    Extract and enrich cultural entities from text on-demand
    
    Args:
        request: Text to extract entities from
    
    Returns:
        List of detected and enriched entities
    """
    
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text must be at least 10 characters long"
        )
    
    try:
        result = nlp_service.analyze_text_with_entities(
            text=request.text,
            enrich_all=True
        )
        
        return {
            "entities": result["detected_entities"],
            "total_detected": result["total_detected"],
            "enriched_count": result["enriched_count"]
        }
        
    except Exception as e:
        print(f"Error extracting entities: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting entities: {str(e)}"
        )


@app.get("/api/entities/highlights")
async def get_entity_highlights(text: str):
    """
    Get entity highlights optimized for frontend display
    
    Args:
        text: Text to highlight (query parameter)
    
    Returns:
        List of highlight regions with tooltip data
    """
    
    if not text or len(text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text must be at least 10 characters long"
        )
    
    try:
        highlights = nlp_service.get_entity_highlights(text)
        
        return {
            "highlights": highlights,
            "count": len(highlights)
        }
        
    except Exception as e:
        print(f"Error getting highlights: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting highlights: {str(e)}"
        )


@app.get("/api/cache/stats")
async def get_cache_stats():
    """
    Get Supabase cache statistics
    
    Returns statistics for persistent Supabase cache:
    - Total cached entries
    - Cache hit counts
    - Hit rate percentage
    - Language distribution
    """
    
    try:
        # Get Supabase cache stats
        cache_stats = get_cache_statistics()
        
        return {
            "cache": cache_stats,
            "cache_info": {
                "type": "Supabase persistent cache",
                "ttl": "30 days",
                "scope": "Shared across all instances (cloud-ready)",
                "storage": "PostgreSQL JSONB columns"
            }
        }
        
    except Exception as e:
        print(f"Error fetching cache stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching cache statistics: {str(e)}"
        )


@app.post("/api/cache/clear")
async def clear_cache():
    """
    Clear expired Supabase cache entries
    
    Removes entries older than 30 days (or all if forced)
    
    Returns:
        Confirmation message with count of deleted entries
    """
    
    try:
        from database import cleanup_expired_cache
        deleted_count = cleanup_expired_cache(days_old=30)
        
        return {
            "message": "Cache cleared successfully",
            "entries_deleted": deleted_count,
            "cache_type": "supabase"
        }
        
    except Exception as e:
        print(f"Error clearing cache: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
