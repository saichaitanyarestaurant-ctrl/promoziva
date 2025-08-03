import os
import httpx

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.default_model = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b")

    async def chat(self, messages, model=None, temperature=0.2, max_tokens=1000):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://yourapp.com",
            "X-Title": "Your AI App"
        }

        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]