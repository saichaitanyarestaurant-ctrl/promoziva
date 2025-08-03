from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from pydantic import BaseModel

from ..models.database import get_db
from ..core.orchestrator import AIOrchestrator, CommandRequest, CommandResponse
from ..models.task import Task, TaskStatus
from ..models.user import User
from ..models.conversation import Conversation

router = APIRouter()

# Pydantic models for API requests/responses
class CommandRequestModel(BaseModel):
    command: str
    user_id: int = None
    conversation_id: int = None
    context: Dict[str, Any] = None

class TaskStatusResponse(BaseModel):
    task_id: int
    title: str
    status: str
    created_at: str = None
    started_at: str = None
    completed_at: str = None
    result: Dict[str, Any] = None
    error_message: str = None

class QueueStatusResponse(BaseModel):
    queue_size: int
    active_tasks: int
    max_concurrent_tasks: int
    total_pending: int
    total_processing: int
    total_completed: int
    total_failed: int

class ServiceHealthResponse(BaseModel):
    services: Dict[str, bool]

# Global orchestrator instance
orchestrator = None

def get_orchestrator(db: Session = Depends(get_db)) -> AIOrchestrator:
    global orchestrator
    if orchestrator is None:
        orchestrator = AIOrchestrator(db)
    return orchestrator

@router.on_event("startup")
async def startup_event():
    """Initialize the orchestrator on startup."""
    global orchestrator
    db = next(get_db())
    orchestrator = AIOrchestrator(db)
    await orchestrator.start()

@router.on_event("shutdown")
async def shutdown_event():
    """Clean up the orchestrator on shutdown."""
    global orchestrator
    if orchestrator:
        await orchestrator.stop()

@router.post("/command", response_model=CommandResponse)
async def process_command(
    request: CommandRequestModel,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Process a natural language command.
    """
    try:
        command_request = CommandRequest(
            command=request.command,
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            context=request.context
        )
        
        response = await orchestrator.process_command(command_request)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: int,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Get the status of a specific task.
    """
    try:
        status = await orchestrator.get_task_status(task_id)
        return TaskStatusResponse(**status)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queue/status", response_model=QueueStatusResponse)
async def get_queue_status(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Get the current status of the task queue.
    """
    try:
        status = await orchestrator.get_queue_status()
        return QueueStatusResponse(**status)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/task/{task_id}")
async def cancel_task(
    task_id: int,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Cancel a pending task.
    """
    try:
        success = await orchestrator.cancel_task(task_id)
        if success:
            return {"message": f"Task {task_id} cancelled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to cancel task")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/health", response_model=ServiceHealthResponse)
async def get_service_health(
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Get the health status of all services.
    """
    try:
        services = await orchestrator.get_service_health()
        return ServiceHealthResponse(services=services)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks", response_model=List[TaskStatusResponse])
async def get_tasks(
    status: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get a list of tasks with optional filtering.
    """
    try:
        query = db.query(Task)
        
        if status:
            try:
                task_status = TaskStatus(status)
                query = query.filter(Task.status == task_status)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid status")
        
        tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
        
        return [
            TaskStatusResponse(
                task_id=task.id,
                title=task.title,
                status=task.status.value,
                created_at=task.created_at.isoformat() if task.created_at else None,
                started_at=task.started_at.isoformat() if task.started_at else None,
                completed_at=task.completed_at.isoformat() if task.completed_at else None,
                result=task.result,
                error_message=task.error_message
            )
            for task in tasks
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation")
async def create_conversation(
    user_id: int,
    title: str = None,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Create a new conversation session.
    """
    try:
        conversation_id = await orchestrator.create_conversation(user_id, title)
        return {"conversation_id": conversation_id, "message": "Conversation created successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}")
async def get_conversation_history(
    conversation_id: int,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    """
    Get the conversation history.
    """
    try:
        history = await orchestrator.get_conversation_history(conversation_id)
        return history
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "message": "AI Orchestrator is running"}

@router.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "AI Orchestrator API",
        "version": "1.0.0",
        "endpoints": {
            "command": "/command",
            "task_status": "/task/{task_id}",
            "queue_status": "/queue/status",
            "service_health": "/services/health",
            "tasks": "/tasks",
            "conversation": "/conversation",
            "health": "/health"
        }
    }