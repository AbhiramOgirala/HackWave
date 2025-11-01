from datetime import datetime
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

# Supabase connection configuration (NO PASSWORD NEEDED!)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project-ref.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "your-anon-key")

if not SUPABASE_URL or not SUPABASE_ANON_KEY or "your-" in SUPABASE_URL or "your-" in SUPABASE_ANON_KEY:
    raise ValueError(
        "❌ Missing Supabase configuration!\n"
        "Please add SUPABASE_URL and SUPABASE_ANON_KEY to your .env file.\n"
        "Get them from: Supabase Dashboard > Project Settings > API"
    )

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
print(f"✅ Connected to Supabase at {SUPABASE_URL}")


class Analysis:
    """Data model for cultural context analyses"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.input_text = kwargs.get('input_text')
        self.language = kwargs.get('language', 'en')
        self.cultural_origin = kwargs.get('cultural_origin')
        self.cross_cultural_connections = kwargs.get('cross_cultural_connections')
        self.modern_analogy = kwargs.get('modern_analogy')
        self.visualization_description = kwargs.get('visualization_description')
        self.image_url = kwargs.get('image_url')
        self.timeline_events = kwargs.get('timeline_events', [])
        self.geographic_locations = kwargs.get('geographic_locations', [])
        self.key_concepts = kwargs.get('key_concepts', [])
        self.external_resources = kwargs.get('external_resources', {})
        self.created_at = kwargs.get('created_at', datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Supabase insert"""
        return {
            'input_text': self.input_text,
            'language': self.language,
            'cultural_origin': self.cultural_origin,
            'cross_cultural_connections': self.cross_cultural_connections,
            'modern_analogy': self.modern_analogy,
            'visualization_description': self.visualization_description,
            'image_url': self.image_url,
            'timeline_events': self.timeline_events,
            'geographic_locations': self.geographic_locations,
            'key_concepts': self.key_concepts,
            'external_resources': self.external_resources,
            'created_at': self.created_at
        }


def init_db():
    """Initialize database tables - Not needed with Supabase (use SQL Editor instead)"""
    print("ℹ️  Using Supabase - Tables should be created via SQL Editor in Supabase Dashboard")
    print("ℹ️  Run the SQL script from supabase_setup.sql if you haven't already")


def save_analysis(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save analysis to Supabase"""
    try:
        response = supabase.table('analyses').insert(analysis_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"❌ Error saving analysis: {e}")
        raise


def get_analysis(analysis_id: int) -> Optional[Dict[str, Any]]:
    """Get analysis by ID from Supabase"""
    try:
        response = supabase.table('analyses').select('*').eq('id', analysis_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"❌ Error fetching analysis: {e}")
        raise


def get_all_analyses(limit: int = 100) -> List[Dict[str, Any]]:
    """Get all analyses from Supabase"""
    try:
        response = supabase.table('analyses').select('*').order('created_at', desc=True).limit(limit).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"❌ Error fetching analyses: {e}")
        raise


def get_db():
    """Dependency for database access - returns Supabase client"""
    return supabase
