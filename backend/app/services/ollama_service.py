import json
from typing import Dict, Any, Optional

import requests


class OllamaService:
    def __init__(self, base_url: str = "http://ollama:11434"):
        self.base_url = base_url

    def generate_course_content(self, prompt: str, model: str = "gemma3:270m") -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to generate content: {str(e)}")

    def process_course_materials(self, materials: Dict[str, Any], model: str = "gemma3:270m") -> Optional[
        Dict[str, Any]]:
        try:
            prompt = f"Process and enhance the following course materials: {json.dumps(materials)}"
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to process materials: {str(e)}")
