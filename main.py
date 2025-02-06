import streamlit as st
from utils.youtube_api import YouTubeAPI
from utils.text_analysis import TextAnalyzer
from utils.report_generator import ReportGenerator
from utils.database import get_db, Interview
from components.video_info import display_video_info
from components.analysis_results import display_analysis_results
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Interview Analysis Tool",
    page_icon="🎥",
    layout="wide"
)

# Initialize APIs with caching
@st.cache_resource
def init_apis():
    youtube_api = YouTubeAPI(st.secrets["YOUTUBE_API_KEY"])
    text_analyzer = TextAnalyzer(st.secrets["GEMINI_API_KEY"])
    return youtube_api, text_analyzer

def main():
    st.title("🎥 Interview Analysis Tool")

    try:
        youtube_api, text_analyzer = init_apis()
    except Exception as e:
        logger.error(f"API initialization error: {str(e)}")
        st.error("⚠️ Failed to initialize APIs. Please check your API keys.")
        return

    # URL Input
    url = st.text_input("Enter YouTube Video URL")

    if url:
        try:
            # Process video
            video_id = youtube_api.extract_video_id(url)
            if not video_id:
                st.error("Invalid YouTube URL")
                return

            video_info = youtube_api.get_video_details(video_id)
            captions = youtube_api.get_captions(video_id)

            if not captions:
                st.error("No captions available for this video")
                return

            # Analyze text and generate report
            analysis_results = text_analyzer.analyze_text(captions)
            report = ReportGenerator.generate_report(
                video_info, 
                analysis_results,
                captions
            )

            # Display results
            display_video_info(video_info)
            st.divider()
            display_analysis_results(report)

            # Simple database logging
            try:
                db = next(get_db())
                interview = Interview(
                    video_id=video_id,
                    video_title=video_info['title'],
                    transcript=captions
                )
                db.add(interview)
                db.commit()
                logger.info(f"Successfully saved analysis for video: {video_id}")
            except Exception as e:
                logger.error(f"Database error: {str(e)}")
                st.warning("⚠️ Failed to save analysis to database")

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            st.error(f"An error occurred while processing the video: {str(e)}")
    else:
        st.info("""
        👋 Welcome to the Interview Analysis Tool!

        To get started:
        1. Paste a YouTube video URL above
        2. Make sure the video has captions enabled
        3. Wait for the analysis to complete
        """)

if __name__ == "__main__":
    main()