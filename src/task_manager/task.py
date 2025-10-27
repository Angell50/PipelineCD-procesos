"""Task model with validation and business logic."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from .exceptions import ValidationError


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Enumeration of task priorities."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """
    Represents a task with validation and business logic.
    """

    task_id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    # Nota: este default solo aplica si NO te pasan priority en el constructor.
    priority: Union[TaskPriority, int, str, None] = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

    def __post_init__(self):
        """Validate and normalize task data after initialization."""
        # --- Normalización de priority ---
        # Si viene como str / int, conviértelo a TaskPriority.
        if isinstance(self.priority, str):
            self.priority = TaskPriority[self.priority.upper()]
        elif isinstance(self.priority, int):
            self.priority = TaskPriority(self.priority)
        elif self.priority is None:
            self.priority = TaskPriority.MEDIUM
        # A partir de aquí, priority SIEMPRE es TaskPriority.

        self.validate()

    def validate(self) -> None:
        """Validate task data."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValidationError("Title cannot be empty")

        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

        if self.task_id < 0:
            raise ValidationError("Task ID must be non-negative")

        if self.due_date and self.due_date < self.created_at:
            raise ValidationError("Due date cannot be before creation date")

    def mark_in_progress(self) -> None:
        """Mark task as in progress."""
        if self.status == TaskStatus.COMPLETED:
            raise ValidationError("Cannot modify a completed task")
        if self.status == TaskStatus.CANCELLED:
            raise ValidationError("Cannot modify a cancelled task")

        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def mark_completed(self) -> None:
        """Mark task as completed."""
        if self.status == TaskStatus.CANCELLED:
            raise ValidationError("Cannot complete a cancelled task")

        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_cancelled(self) -> None:
        """Mark task as cancelled."""
        if self.status == TaskStatus.COMPLETED:
            raise ValidationError("Cannot cancel a completed task")

        self.status = TaskStatus.CANCELLED
        self.updated_at = datetime.now()

    def update_title(self, new_title: str) -> None:
        """Update task title."""
        if not new_title or len(new_title.strip()) == 0:
            raise ValidationError("Title cannot be empty")
        if len(new_title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

        self.title = new_title
        self.updated_at = datetime.now()

    def update_description(self, new_description: str) -> None:
        """Update task description."""
        self.description = new_description
        self.updated_at = datetime.now()

    def set_priority(self, priority: Union[TaskPriority, str, int]) -> None:
        """Set task priority (acepta enum, str o int)."""
        if isinstance(priority, str):
            self.priority = TaskPriority[priority.upper()]
        elif isinstance(priority, int):
            self.priority = TaskPriority(priority)
        else:
            self.priority = priority
        self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date:
            return False
        return (
            datetime.now() > self.due_date
            and self.status != TaskStatus.COMPLETED
            and self.status != TaskStatus.CANCELLED
        )

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_overdue": self.is_overdue(),
        }
