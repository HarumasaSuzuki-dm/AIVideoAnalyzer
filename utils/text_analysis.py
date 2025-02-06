from typing import Dict, List, Tuple
import google.generativeai as genai

class TextAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_text(self, text: str) -> Dict:
        """Perform complete text analysis using Gemini API."""
        return {
            'summary': self._generate_summary(text),
            'key_phrases': self._extract_key_phrases(text),
            'sentiment': self._analyze_sentiment(text)
        }

    def _generate_summary(self, text: str) -> Dict[str, str]:
        """Generate both brief and detailed summaries."""
        brief_prompt = (
            "Summarize the following interview text in 2-3 sentences, "
            "focusing on the most important points: "
        )
        detailed_prompt = (
            "Provide a detailed summary of the following interview text "
            "in bullet points, highlighting key discussion points: "
        )

        brief_summary = self.model.generate_content(brief_prompt + text).text
        detailed_summary = self.model.generate_content(detailed_prompt + text).text

        return {
            'brief': brief_summary,
            'detailed': detailed_summary
        }

    def _extract_key_phrases(self, text: str) -> List[Dict[str, str]]:
        """Extract key phrases and their importance."""
        prompt = (
            "Extract the 5-7 most important phrases or technical terms from "
            "the following interview text. For each phrase, provide an importance "
            "score (1-5) and a brief explanation of its context: "
        )

        response = self.model.generate_content(prompt + text).text
        # Parse the response into structured format
        phrases = []
        for line in response.split('\n'):
            if ':' in line:
                phrase, explanation = line.split(':', 1)
                phrases.append({
                    'phrase': phrase.strip(),
                    'explanation': explanation.strip()
                })
        return phrases

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze the overall sentiment of the text."""
        prompt = (
            "Analyze the sentiment of the following interview text. "
            "Provide scores from 0 to 1 for: confidence, positivity, and engagement. "
            "Format the response as 'confidence: X, positivity: Y, engagement: Z': "
        )

        response = self.model.generate_content(prompt + text).text
        scores = {}
        for pair in response.split(','):
            key, value = pair.split(':')
            scores[key.strip()] = float(value.strip())
        return scores
