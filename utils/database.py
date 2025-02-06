from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

class Interview(Base):
    """Model for storing interview analysis results."""
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    video_title = Column(String)
    video_url = Column(String)
    transcript = Column(Text)
    summary_brief = Column(Text)
    summary_detailed = Column(Text)
    key_phrases = Column(JSON)
    sentiment_scores = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)
