import asyncio
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from ..models.task import Task, TaskStatus, TaskPriority
from datetime import datetime
import heapq

logger = logging.getLogger(__name__)

class QueueManager:
    def __init__(self, db: Session):
        self.db = db
        self.processing_queue = asyncio.Queue()
        self.priority_queue = []
        self.max_concurrent_tasks = 5
        self.active_tasks = 0
        self.task_workers = []

    async def add_task(self, task: Task) -> bool:
        """
        Add a task to the processing queue.
        """
        try:
            # Set initial status
            task.status = TaskStatus.PENDING
            task.created_at = datetime.utcnow()
            self.db.add(task)
            self.db.commit()
            
            # Add to priority queue
            priority_score = self._calculate_priority_score(task)
            heapq.heappush(self.priority_queue, (-priority_score, task.id, task))
            
            logger.info(f"Task {task.id} added to queue with priority score {priority_score}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding task to queue: {e}")
            self.db.rollback()
            return False

    def _calculate_priority_score(self, task: Task) -> float:
        """
        Calculate priority score for task ordering.
        Higher score = higher priority.
        """
        base_score = {
            TaskPriority.LOW: 1.0,
            TaskPriority.MEDIUM: 2.0,
            TaskPriority.HIGH: 3.0,
            TaskPriority.URGENT: 4.0
        }.get(task.priority, 2.0)
        
        # Add time-based boost (older tasks get higher priority)
        time_boost = 0.1  # Small boost per minute
        return base_score

    async def get_next_task(self) -> Optional[Task]:
        """
        Get the next task from the queue based on priority.
        """
        try:
            if not self.priority_queue:
                return None
                
            # Get highest priority task
            _, task_id, task = heapq.heappop(self.priority_queue)
            
            # Verify task is still pending
            current_task = self.db.query(Task).filter(Task.id == task_id).first()
            if not current_task or current_task.status != TaskStatus.PENDING:
                return await self.get_next_task()  # Try next task
                
            return current_task
            
        except Exception as e:
            logger.error(f"Error getting next task: {e}")
            return None

    async def start_processing(self):
        """
        Start the task processing loop.
        """
        logger.info("Starting task processing queue")
        while True:
            try:
                # Check if we can process more tasks
                if self.active_tasks >= self.max_concurrent_tasks:
                    await asyncio.sleep(1)
                    continue
                
                # Get next task
                task = await self.get_next_task()
                if not task:
                    await asyncio.sleep(1)
                    continue
                
                # Start processing task
                self.active_tasks += 1
                asyncio.create_task(self._process_task(task))
                
            except Exception as e:
                logger.error(f"Error in task processing loop: {e}")
                await asyncio.sleep(1)

    async def _process_task(self, task: Task):
        """
        Process a single task.
        """
        try:
            logger.info(f"Processing task {task.id}: {task.title}")
            
            # Update task status
            task.status = TaskStatus.PROCESSING
            task.started_at = datetime.utcnow()
            self.db.commit()
            
            # Here you would call the task router to execute the task
            # For now, we'll just simulate processing
            await asyncio.sleep(2)  # Simulate processing time
            
            # Mark as completed
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Task {task.id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing task {task.id}: {e}")
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            self.db.commit()
            
        finally:
            self.active_tasks -= 1

    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current queue status and statistics.
        """
        try:
            total_pending = self.db.query(Task).filter(Task.status == TaskStatus.PENDING).count()
            total_processing = self.db.query(Task).filter(Task.status == TaskStatus.PROCESSING).count()
            total_completed = self.db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count()
            total_failed = self.db.query(Task).filter(Task.status == TaskStatus.FAILED).count()
            
            return {
                "queue_size": len(self.priority_queue),
                "active_tasks": self.active_tasks,
                "max_concurrent_tasks": self.max_concurrent_tasks,
                "total_pending": total_pending,
                "total_processing": total_processing,
                "total_completed": total_completed,
                "total_failed": total_failed
            }
            
        except Exception as e:
            logger.error(f"Error getting queue status: {e}")
            return {}

    def get_pending_tasks(self, limit: int = 10) -> List[Task]:
        """
        Get list of pending tasks ordered by priority.
        """
        try:
            return self.db.query(Task).filter(
                Task.status == TaskStatus.PENDING
            ).order_by(
                desc(Task.priority),
                asc(Task.created_at)
            ).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting pending tasks: {e}")
            return []

    async def cancel_task(self, task_id: int) -> bool:
        """
        Cancel a pending task.
        """
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
                
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
                self.db.commit()
                logger.info(f"Task {task_id} cancelled")
                return True
            else:
                logger.warning(f"Cannot cancel task {task_id} - not in pending status")
                return False
                
        except Exception as e:
            logger.error(f"Error cancelling task {task_id}: {e}")
            return False