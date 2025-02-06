import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    logger.error("DATABASE_URL is not set")
    raise ValueError("DATABASE_URL is not set")

try:
    # Create database engine
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    # Define Interview model
    class Interview(Base):
        __tablename__ = "interviews"

        id = Column(Integer, primary_key=True)
        video_id = Column(String, unique=True)
        video_title = Column(String)
        transcript = Column(Text)
        created_at = Column(DateTime, default=datetime.utcnow)

    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

except Exception as e:
    logger.error(f"Database initialization error: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()