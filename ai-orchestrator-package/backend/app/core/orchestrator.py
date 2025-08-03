import logging
import asyncio
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .command_parser import CommandParser, ParsedCommand
from .task_router import TaskRouter
from .queue_manager import QueueManager
from ..models.task import Task, TaskStatus
from ..models.conversation import Conversation, ConversationMessage

logger = logging.getLogger(__name__)

class CommandRequest(BaseModel):
    command: str
    user_id: Optional[int] = None
    conversation_id: Optional[int] = None
    context: Optional[Dict[str, Any]] = None

class CommandResponse(BaseModel):
    task_id: int
    status: str
    message: str
    estimated_completion: Optional[str] = None

class AIOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.command_parser = CommandParser()
        self.task_router = TaskRouter(db)
        self.queue_manager = QueueManager(db)
        self.processing_task = None

    async def start(self):
        """
        Start the orchestrator and all its components.
        """
        logger.info("Starting AI Orchestrator")
        
        # Start the queue processing
        self.processing_task = asyncio.create_task(
            self.queue_manager.start_processing()
        )
        
        logger.info("AI Orchestrator started successfully")

    async def stop(self):
        """
        Stop the orchestrator gracefully.
        """
        logger.info("Stopping AI Orchestrator")
        
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        logger.info("AI Orchestrator stopped")

    async def process_command(self, request: CommandRequest) -> CommandResponse:
        """
        Process a natural language command through the entire pipeline.
        """
        try:
            logger.info(f"Processing command: {request.command}")
            
            # Step 1: Parse the command
            parsed_command = await self.command_parser.parse_command(
                request.command, 
                request.context
            )
            
            # Step 2: Validate the parsed command
            if not self.command_parser.validate_parsed_command(parsed_command):
                raise ValueError("Invalid command structure")
            
            # Step 3: Create task record
            task = Task(
                title=parsed_command.title,
                description=parsed_command.description,
                command=request.command,
                task_type=parsed_command.task_type,
                priority=parsed_command.priority,
                target_service=parsed_command.target_service,
                service_endpoint=parsed_command.service_endpoint,
                parameters=parsed_command.parameters,
                user_id=request.user_id,
                conversation_id=request.conversation_id
            )
            
            # Step 4: Add to queue
            success = await self.queue_manager.add_task(task)
            if not success:
                raise Exception("Failed to add task to queue")
            
            # Step 5: Log conversation message
            if request.conversation_id:
                await self._log_conversation_message(
                    request.conversation_id,
                    request.command,
                    "user"
                )
            
            logger.info(f"Command processed successfully, task ID: {task.id}")
            
            return CommandResponse(
                task_id=task.id,
                status="queued",
                message=f"Task '{parsed_command.title}' has been queued for processing",
                estimated_completion="2-5 minutes"
            )
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            raise

    async def get_task_status(self, task_id: int) -> Dict[str, Any]:
        """
        Get the current status of a task.
        """
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            return {
                "task_id": task.id,
                "title": task.title,
                "status": task.status.value,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result": task.result,
                "error_message": task.error_message
            }
            
        except Exception as e:
            logger.error(f"Error getting task status: {e}")
            raise

    async def get_queue_status(self) -> Dict[str, Any]:
        """
        Get the current status of the task queue.
        """
        return self.queue_manager.get_queue_status()

    async def cancel_task(self, task_id: int) -> bool:
        """
        Cancel a pending task.
        """
        return await self.queue_manager.cancel_task(task_id)

    async def get_service_health(self) -> Dict[str, bool]:
        """
        Get health status of all services.
        """
        return self.task_router.get_available_services()

    async def _log_conversation_message(
        self, 
        conversation_id: int, 
        content: str, 
        role: str
    ):
        """
        Log a message to the conversation history.
        """
        try:
            message = ConversationMessage(
                conversation_id=conversation_id,
                content=content,
                role=role,
                message_type="user" if role == "user" else "assistant"
            )
            self.db.add(message)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error logging conversation message: {e}")

    async def create_conversation(self, user_id: int, title: str = None) -> int:
        """
        Create a new conversation session.
        """
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title or "New Conversation",
                session_id=f"session_{user_id}_{asyncio.get_event_loop().time()}",
                conversation_type="text"
            )
            self.db.add(conversation)
            self.db.commit()
            
            logger.info(f"Created conversation {conversation.id} for user {user_id}")
            return conversation.id
            
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            raise

    async def get_conversation_history(self, conversation_id: int) -> Dict[str, Any]:
        """
        Get the conversation history.
        """
        try:
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found")
            
            messages = self.db.query(ConversationMessage).filter(
                ConversationMessage.conversation_id == conversation_id
            ).order_by(ConversationMessage.timestamp).all()
            
            return {
                "conversation_id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "messages": [
                    {
                        "id": msg.id,
                        "content": msg.content,
                        "role": msg.role,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in messages
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            raise