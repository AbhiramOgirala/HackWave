from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime
from urllib.parse import quote_plus

# PostgreSQL connection configuration
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DATABASE = "postgres"
PG_USER = "postgres"
PG_PASSWORD = "Abhiram@007"
PG_TABLE = ""

# Construct database URL with properly encoded password
# URL-encode the password to handle special characters like @
DATABASE_URL = f"postgresql://{PG_USER}:{quote_plus(PG_PASSWORD)}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Analysis(Base):
    """Database model for storing cultural context analyses"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, default="en")
    cultural_origin = Column(Text, nullable=False)
    cross_cultural_connections = Column(Text, nullable=False)
    modern_analogy = Column(Text, nullable=False)
    visualization_description = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def migrate_image_url_column():
    """Migrate image_url column from VARCHAR(500) to TEXT"""
    try:
        with engine.begin() as conn:
            # Check if column exists and is VARCHAR(500)
            result = conn.execute(text("""
                SELECT data_type, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'analyses' 
                AND column_name = 'image_url'
            """))
            column_info = result.fetchone()
            
            if column_info and column_info[1] == 500:
                # Alter column to TEXT
                conn.execute(text("ALTER TABLE analyses ALTER COLUMN image_url TYPE TEXT"))
                print("✅ Successfully migrated image_url column from VARCHAR(500) to TEXT")
                return True
            elif column_info and column_info[0] == 'text':
                print("✅ image_url column is already TEXT type")
                return True
            else:
                print("⚠️  image_url column not found or already migrated")
                return False
    except Exception as e:
        print(f"⚠️  Migration error: {e}")
        return False


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
