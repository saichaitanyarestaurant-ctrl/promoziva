import os
import httpx
import logging
from typing import List, Dict

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI-Orchestrator"
        }

    async def chat(self, messages: List[Dict]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]