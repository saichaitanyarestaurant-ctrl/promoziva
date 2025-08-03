import json
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..models.task import TaskType, TaskPriority
from ..services.llm_service import llm_service
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ParsedCommand(BaseModel):
    task_type: TaskType
    title: str
    description: str
    priority: TaskPriority
    target_service: str
    service_endpoint: str
    parameters: Dict[str, Any]
    confidence: float

class CommandParser:
    def __init__(self):
        self.system_prompt = """
You are an AI command parser for an AI Orchestrator system. Your job is to parse natural language commands and convert them into structured task specifications.

Available task types:
- browser_automation: Web browsing, form filling, website interactions, Make.com workflows, Canva design creation
- document_management: Google Sheets/Docs creation, editing, file management
- communication: Voice calls, text-to-speech, speech recognition, conversation management
- media_processing: Video/audio transcription, content summarization, script generation
- bot_builder: Creating AI bots, generating configurations, API endpoints
- general: General tasks that don't fit other categories

Available priorities: low, medium, high, urgent

Available services:
- browser_service: For web automation tasks
- document_service: For Google Docs/Sheets operations
- communication_service: For voice and messaging
- media_service: For video/audio processing
- bot_builder_service: For creating AI bots

Return a JSON object with the following structure:
{
    "task_type": "one_of_the_task_types",
    "title": "Brief task title",
    "description": "Detailed task description",
    "priority": "one_of_the_priorities",
    "target_service": "service_name",
    "service_endpoint": "specific_endpoint_if_known",
    "parameters": {
        "key": "value"
    },
    "confidence": 0.95
}
"""

    async def parse_command(self, command: str, context: Optional[Dict[str, Any]] = None) -> ParsedCommand:
        """
        Parse a natural language command into a structured task specification.
        """
        try:
            # Build the prompt with context
            user_prompt = f"Parse this command: {command}"
            if context:
                user_prompt += f"\nContext: {json.dumps(context)}"
            
            # Call OpenRouter API via LLM service
            response = await llm_service.chat_completion(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            content = response["choices"][0]["message"]["content"]
            parsed_data = json.loads(content)
            
            # Create ParsedCommand object
            parsed_command = ParsedCommand(
                task_type=TaskType(parsed_data["task_type"]),
                title=parsed_data["title"],
                description=parsed_data["description"],
                priority=TaskPriority(parsed_data["priority"]),
                target_service=parsed_data["target_service"],
                service_endpoint=parsed_data.get("service_endpoint", ""),
                parameters=parsed_data.get("parameters", {}),
                confidence=parsed_data.get("confidence", 0.8)
            )
            
            logger.info(f"Successfully parsed command: {command} -> {parsed_command.task_type}")
            return parsed_command
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse command response: {e}")
        except Exception as e:
            logger.error(f"Error parsing command '{command}': {e}")
            raise

    def validate_parsed_command(self, parsed_command: ParsedCommand) -> bool:
        """
        Validate the parsed command for completeness and correctness.
        """
        # Basic validation
        if not parsed_command.title or not parsed_command.description:
            return False
        
        if parsed_command.confidence < 0.5:
            return False
            
        # Service-specific validation
        if parsed_command.task_type == TaskType.BROWSER_AUTOMATION:
            if parsed_command.target_service != "browser_service":
                return False
        elif parsed_command.task_type == TaskType.DOCUMENT_MANAGEMENT:
            if parsed_command.target_service != "document_service":
                return False
        # Add more validations as needed
        
        return True