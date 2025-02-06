import streamlit as st
from utils.youtube_api import YouTubeAPI
from utils.text_analysis import TextAnalyzer
from utils.report_generator import ReportGenerator
from utils.storage import JsonStorage  # 新しいJSONストレージユーティリティ
from components.video_info import display_video_info
from components.analysis_results import display_analysis_results
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="インタビュー分析ツール",
    page_icon="🎥",
    layout="wide"
)

def check_api_keys():
    """APIキーの存在確認と検証"""
    required_keys = {
        "YOUTUBE_API_KEY": st.secrets.get("YOUTUBE_API_KEY"),
        "GEMINI_API_KEY": st.secrets.get("GEMINI_API_KEY")
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    
    if missing_keys:
        st.error(f"⚠️ 以下のAPIキーが設定されていません: {', '.join(missing_keys)}")
        st.info("""
        APIキーの設定方法:
        1. `.streamlit/secrets.toml` ファイルを作成してください
        2. 以下の形式でAPIキーを設定してください:
           YOUTUBE_API_KEY = "あなたのYouTube APIキー"
           GEMINI_API_KEY = "あなたのGemini APIキー"
        """)
        return False
    return True

# Initialize APIs with caching
@st.cache_resource
def init_apis():
    youtube_api = YouTubeAPI(st.secrets["YOUTUBE_API_KEY"])
    text_analyzer = TextAnalyzer(st.secrets["GEMINI_API_KEY"])
    os.makedirs("data", exist_ok=True)
    storage = JsonStorage("data/interviews.json")
    return youtube_api, text_analyzer, storage

def main():
    st.title("🎥 インタビュー分析ツール")

    # APIキーのチェック
    if not check_api_keys():
        return

    try:
        youtube_api, text_analyzer, storage = init_apis()
    except Exception as e:
        logger.error(f"API initialization error: {str(e)}")
        st.error("⚠️ APIの初期化に失敗しました。APIキーを確認してください。")
        return

    # URL Input
    url = st.text_input(
        label="YouTube URL",
        placeholder="YouTubeの動画URLを入力してください"
    )

    if not url:
        st.info("""
        👋 インタビュー分析ツールへようこそ！

        使い方：
        1. 上記にYouTube動画のURLを貼り付けてください
        2. 動画に字幕が設定されていることを確認してください
        3. 分析が完了するまでお待ちください
        """)
        return

    try:
        # Process video
        video_id = youtube_api.extract_video_id(url)
        if not video_id:
            st.error("無効なYouTube URLです")
            return

        video_info = youtube_api.get_video_details(video_id)
        captions = youtube_api.get_captions(video_id)

        if not captions:
            st.error("この動画には字幕がありません")
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

        # Save to JSON storage
        try:
            interview_data = {
                "video_id": video_id,
                "video_title": video_info['title'],
                "transcript": captions,
                "analysis_results": analysis_results,
            }
            storage.save_interview(interview_data)
            logger.info(f"Successfully saved analysis for video: {video_id}")
        except Exception as e:
            logger.error(f"Storage error: {str(e)}")
            st.warning("⚠️ 分析結果の保存に失敗しました")

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        st.error(f"動画の処理中にエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()