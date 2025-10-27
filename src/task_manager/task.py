"""Task model with validation and business logic."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

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

    Attributes:
        task_id: Unique identifier for the task
        title: Task title (1-200 characters)
        description: Detailed task description
        status: Current task status
        priority: Task priority level
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        due_date: Optional deadline for the task
    """

    task_id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

    def __post_init__(self):
        """Validate task data after initialization."""
        self.validate()

    def validate(self) -> None:
        """
        Validate task data.

        Raises:
            ValidationError: If validation fails
        """
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
        """
        Update task title.

        Args:
            new_title: New title for the task

        Raises:
            ValidationError: If title is invalid
        """
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

    def set_priority(self, priority: TaskPriority) -> None:
        """Set task priority."""
        self.priority = priority
        self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """
        Check if task is overdue.

        Returns:
            True if task has a due date and it has passed, False otherwise
        """
        if not self.due_date:
            return False

        return (
            datetime.now() > self.due_date
            and self.status != TaskStatus.COMPLETED
            and self.status != TaskStatus.CANCELLED
        )

    def to_dict(self) -> dict:
        """
        Convert task to dictionary representation.

        Returns:
            Dictionary containing task data
        """
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
