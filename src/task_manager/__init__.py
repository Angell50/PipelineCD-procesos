"""Task Manager - A professional task management application."""

__version__ = "1.0.0"
__author__ = "Senior Dev Team"

from .exceptions import DuplicateTaskError, TaskNotFoundError, ValidationError
from .task import Task, TaskPriority, TaskStatus
from .task_manager import TaskManager

__all__ = [
    "Task",
    "TaskStatus",
    "TaskPriority",
    "TaskManager",
    "TaskNotFoundError",
    "DuplicateTaskError",
    "ValidationError",
]
