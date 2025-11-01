from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from contextlib import asynccontextmanager
import uvicorn

from database import get_db, init_db, migrate_image_url_column, Analysis
from gemini_service import gemini_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    init_db()
    migrate_image_url_column()
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
    created_at: datetime

    class Config:
        from_attributes = True


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
async def analyze_text(request: AnalyzeRequest, db: Session = Depends(get_db)):
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
            language=request.language
        )
        
        # Generate enhanced image description
        image_prompt = await gemini_service.generate_image_description(
            analysis_result["visualization_description"]
        )
        
        # Store in database
        db_analysis = Analysis(
            input_text=request.text,
            language=request.language,
            cultural_origin=analysis_result["cultural_origin"],
            cross_cultural_connections=analysis_result["cross_cultural_connections"],
            modern_analogy=analysis_result["modern_analogy"],
            visualization_description=analysis_result["visualization_description"],
            image_url=image_prompt  # Store the enhanced prompt as image_url
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        return db_analysis
        
    except Exception as e:
        db.rollback()
        print(f"Error in analyze_text: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )


@app.get("/api/history", response_model=List[AnalysisResponse])
async def get_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get analysis history
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
    """
    
    analyses = db.query(Analysis)\
        .order_by(Analysis.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return analyses


@app.get("/api/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get specific analysis by ID
    
    Args:
        analysis_id: ID of the analysis to retrieve
    """
    
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )
    
    return analysis


@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Delete specific analysis by ID
    
    Args:
        analysis_id: ID of the analysis to delete
    """
    
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )
    
    db.delete(analysis)
    db.commit()
    
    return {"message": f"Analysis {analysis_id} deleted successfully"}


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about analyses"""
    
    total_analyses = db.query(Analysis).count()
    
    # Get language distribution
    language_stats = db.query(
        Analysis.language,
        db.func.count(Analysis.id)
    ).group_by(Analysis.language).all()
    
    return {
        "total_analyses": total_analyses,
        "language_distribution": {lang: count for lang, count in language_stats}
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
