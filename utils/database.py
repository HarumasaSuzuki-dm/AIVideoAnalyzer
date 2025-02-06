from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
import streamlit as st

# Get database URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    # Construct URL from individual components if not available directly
    host = os.getenv('PGHOST') or st.secrets.get("postgresql_host")
    port = os.getenv('PGPORT') or st.secrets.get("postgresql_port")
    user = os.getenv('PGUSER') or st.secrets.get("postgresql_user")
    password = os.getenv('PGPASSWORD') or st.secrets.get("postgresql_password")
    database = os.getenv('PGDATABASE') or st.secrets.get("postgresql_database")

    if all([host, port, user, password, database]):
        DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError("Database configuration is incomplete. Please check environment variables or secrets.")

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

# Initialize database tables
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

# Create tables on import
init_db()