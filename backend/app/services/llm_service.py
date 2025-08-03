import os
import json
import aiohttp
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for handling LLM interactions using OpenRouter API
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenRouter
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to OPENROUTER_MODEL env var)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Dictionary containing the API response
        """
        if not model:
            model = self.default_model
            
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            **kwargs
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/saichaitanyarestaurant-ctrl/promoziva",
            "X-Title": "Promoziva AI Orchestrator"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                        raise Exception(f"OpenRouter API error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {str(e)}")
            raise
    
    async def get_response_text(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Get just the response text from a chat completion
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            The response text content
        """
        response = await self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        if response.get("choices") and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise Exception("No response content received from OpenRouter")
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio using OpenRouter's Whisper model
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/saichaitanyarestaurant-ctrl/promoziva",
            "X-Title": "Promoziva AI Orchestrator"
        }
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {'file': audio_file}
                data = {'model': 'whisper-1'}
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/audio/transcriptions",
                        headers=headers,
                        data=data,
                        files=files
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            return result.get("text", "")
                        else:
                            error_text = await response.text()
                            logger.error(f"OpenRouter transcription error: {response.status} - {error_text}")
                            raise Exception(f"Transcription error: {response.status} - {error_text}")
                            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from OpenRouter
        
        Returns:
            List of available models
        """
        # This would typically make an API call to get models
        # For now, return a curated list of popular models
        return [
            {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet"},
            {"id": "anthropic/claude-3-opus", "name": "Claude 3 Opus"},
            {"id": "openai/gpt-4", "name": "GPT-4"},
            {"id": "openai/gpt-4-turbo", "name": "GPT-4 Turbo"},
            {"id": "google/gemini-pro", "name": "Gemini Pro"},
            {"id": "meta-llama/llama-3.1-8b-instruct", "name": "Llama 3.1 8B Instruct"},
        ]

# Global instance
llm_service = LLMService()