from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
import uvicorn

from database import get_db, init_db, save_analysis, get_analysis, get_all_analyses
from gemini_service import gemini_service


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
    visualization_description: str
    image_url: Optional[str]
    timeline_events: Optional[List[Dict[str, Any]]] = []
    geographic_locations: Optional[List[Dict[str, Any]]] = []
    key_concepts: Optional[List[Dict[str, Any]]] = []
    external_resources: Optional[Dict[str, Any]] = {}
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
    Analyze text for cultural context
    
    This endpoint:
    1. Identifies the cultural origin
    2. Finds cross-cultural connections
    3. Provides modern analogies
    4. Generates visualization descriptions
    """
    
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text must be at least 10 characters long"
        )
    
    try:
        # Analyze using Gemini API
        analysis_result = await gemini_service.analyze_cultural_context(
            text=request.text,
            language=request.language or "en"
        )
        
        # Generate enhanced image description
        image_prompt = await gemini_service.generate_image_description(
            analysis_result["visualization_description"]
        )
        
        # Prepare data for Supabase
        analysis_data = {
            'input_text': request.text,
            'language': request.language,
            'cultural_origin': analysis_result["cultural_origin"],
            'cross_cultural_connections': analysis_result["cross_cultural_connections"],
            'modern_analogy': analysis_result["modern_analogy"],
            'visualization_description': analysis_result["visualization_description"],
            'image_url': image_prompt,  # Store the enhanced prompt as image_url
            'timeline_events': analysis_result.get("timeline_events", []),
            'geographic_locations': analysis_result.get("geographic_locations", []),
            'key_concepts': analysis_result.get("key_concepts", []),
            'external_resources': analysis_result.get("external_resources", {}),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Save to Supabase
        saved_analysis = save_analysis(analysis_data)
        
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
