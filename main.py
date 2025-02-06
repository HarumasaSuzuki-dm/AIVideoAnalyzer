import streamlit as st
import os
from utils.youtube_api import YouTubeAPI
from utils.text_analysis import TextAnalyzer
from utils.report_generator import ReportGenerator
from utils.database import get_db, Interview
from components.video_info import display_video_info
from components.analysis_results import display_analysis_results
from sqlalchemy.orm import Session
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Interview Analysis Tool",
    page_icon="🎥",
    layout="wide"
)

# Initialize APIs
@st.cache_resource
def init_apis():
    if not st.secrets.get("YOUTUBE_API_KEY"):
        raise ValueError("YouTube API key is not set. Please set it in .streamlit/secrets.toml")
    if not st.secrets.get("GEMINI_API_KEY"):
        raise ValueError("Gemini API key is not set. Please set it in .streamlit/secrets.toml")

    youtube_api = YouTubeAPI(st.secrets["YOUTUBE_API_KEY"])
    text_analyzer = TextAnalyzer(st.secrets["GEMINI_API_KEY"])
    return youtube_api, text_analyzer

def save_analysis_to_db(
    db: Session,
    video_id: str,
    video_info: dict,
    analysis_results: dict,
    captions: str,
    video_url: str
):
    """Save analysis results to database."""
    interview = Interview(
        video_id=video_id,
        video_title=video_info['title'],
        video_url=video_url,
        transcript=captions,
        summary_brief=analysis_results['summary']['brief'],
        summary_detailed=analysis_results['summary']['detailed'],
        key_phrases=analysis_results['key_phrases'],
        sentiment_scores=analysis_results['sentiment'],
        created_at=datetime.utcnow()
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

def main():
    st.title("🎥 Interview Analysis Tool")

    # Initialize APIs
    try:
        youtube_api, text_analyzer = init_apis()
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        st.info("Please set up your API keys in the .streamlit/secrets.toml file to continue.")
        return
    except Exception as e:
        st.error(f"⚠️ Failed to initialize APIs: {str(e)}")
        return

    # Initialize database
    try:
        db = next(get_db())
    except Exception as e:
        st.error(f"⚠️ Failed to connect to database: {str(e)}")
        return

    # URL Input
    url = st.text_input("Enter YouTube Video URL")

    if url:
        with st.spinner("Processing video..."):
            try:
                # Extract video ID
                video_id = youtube_api.extract_video_id(url)
                if not video_id:
                    st.error("Invalid YouTube URL")
                    return

                # Get video details
                video_info = youtube_api.get_video_details(video_id)
                if not video_info:
                    st.error("Could not fetch video details")
                    return

                # Get captions
                captions = youtube_api.get_captions(video_id)
                if not captions:
                    st.error("No captions available for this video")
                    return

                # Analyze text
                analysis_results = text_analyzer.analyze_text(captions)

                # Save to database
                save_analysis_to_db(
                    db=db,
                    video_id=video_id,
                    video_info=video_info,
                    analysis_results=analysis_results,
                    captions=captions,
                    video_url=url
                )

                # Generate report
                report = ReportGenerator.generate_report(
                    video_info, 
                    analysis_results,
                    captions
                )

                # Display results
                display_video_info(video_info)
                st.divider()
                display_analysis_results(report)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Instructions
    else:
        st.info("""
        👋 Welcome to the Interview Analysis Tool!

        To get started:
        1. Paste a YouTube video URL above
        2. Make sure the video has captions enabled
        3. Wait for the analysis to complete

        You'll get:
        - Video summary
        - Key discussion points
        - Sentiment analysis
        - Full transcript
        """)

if __name__ == "__main__":
    main()