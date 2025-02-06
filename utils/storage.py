import json
import os
from pathlib import Path
from typing import Dict, Any

class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """ストレージディレクトリとファイルの存在確認・作成"""
        directory = os.path.dirname(self.file_path)
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_interviews(self) -> list:
        """保存された全インタビューデータの読み込み"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_interview(self, interview_data: Dict[str, Any]):
        """新しいインタビューデータの保存"""
        interviews = self.load_interviews()
        
        # 既存のデータの更新または新規追加
        video_id = interview_data['video_id']
        existing_index = next(
            (i for i, item in enumerate(interviews) 
             if item['video_id'] == video_id), 
            None
        )
        
        if existing_index is not None:
            interviews[existing_index] = interview_data
        else:
            interviews.append(interview_data)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(interviews, f, indent=2, ensure_ascii=False) 