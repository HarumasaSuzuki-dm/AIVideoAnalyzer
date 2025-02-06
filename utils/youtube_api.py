from typing import Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

logger = logging.getLogger(__name__)

class YouTubeAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_video_details(self, video_id: str) -> Dict:
        """Get video metadata."""
        try:
            response = self.youtube.videos().list(
                part='snippet,contentDetails',
                id=video_id
            ).execute()

            if not response['items']:
                return None

            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'thumbnail': video['snippet']['thumbnails']['high']['url'],
                'description': video['snippet']['description'],
                'duration': video['contentDetails']['duration']
            }
        except HttpError as e:
            logger.error(f"Error fetching video details: {str(e)}")
            raise

    def get_captions(self, video_id: str) -> Optional[str]:
        """Get video captions including auto-generated ones"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            try:
                transcript = transcript_list.find_transcript(['ja'])
            except:
                try:
                    transcript = transcript_list.find_transcript(['en'])
                except:
                    try:
                        transcript = transcript_list.find_generated_transcript(['ja', 'en'])
                    except Exception as e:
                        logger.error(f"No transcripts found: {str(e)}")
                        return None

            formatter = TextFormatter()
            return formatter.format_transcript(transcript.fetch())
            
        except Exception as e:
            logger.error(f"Caption error for video {video_id}: {str(e)}")
            return None

    def _clean_caption_text(self, caption_text: str) -> str:
        """Clean caption text by removing timestamps and formatting."""
        # Remove timestamps and numbers
        cleaned_text = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', caption_text)
        cleaned_text = re.sub(r'^\d+$', '', cleaned_text, flags=re.MULTILINE)

        # Remove extra whitespace and newlines
        cleaned_text = ' '.join(cleaned_text.split())

        return cleaned_text