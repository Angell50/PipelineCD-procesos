"""Custom exceptions for the task manager application."""


class TaskManagerError(Exception):
    """Base exception for all task manager errors."""


class TaskNotFoundError(TaskManagerError):
    """Raised when a task is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class DuplicateTaskError(TaskManagerError):
    """Raised when attempting to add a duplicate task."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} already exists")


class ValidationError(TaskManagerError):
    """Raised when task validation fails."""

    def __init__(self, message: str):
        super().__init__(f"Validation error: {message}")
