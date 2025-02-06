from typing import Dict
import pandas as pd

class ReportGenerator:
    @staticmethod
    def generate_report(video_info: Dict, text_analysis: Dict, full_text: str) -> Dict:
        """Generate a structured report from analysis results."""
        return {
            'video_info': {
                'title': video_info['title'],
                'thumbnail': video_info['thumbnail'],
                'duration': video_info['duration']
            },
            'summaries': text_analysis['summary'],
            'key_phrases': text_analysis['key_phrases'],
            'sentiment': text_analysis['sentiment'],
            'full_text': full_text
        }

    @staticmethod
    def format_key_phrases(phrases: list) -> pd.DataFrame:
        """Convert key phrases to a DataFrame for display."""
        return pd.DataFrame(phrases)

    @staticmethod
    def format_sentiment(sentiment: Dict) -> Dict:
        """Format sentiment scores for display."""
        return {k: f"{v:.2%}" for k, v in sentiment.items()}
