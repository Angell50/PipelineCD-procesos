"""Task manager for managing multiple tasks."""

from typing import Dict, List, Optional

from .exceptions import TaskNotFoundError
from .task import Task, TaskPriority, TaskStatus


class TaskManager:
    """
    Manages a collection of tasks with CRUD operations.

    This class provides a comprehensive interface for managing tasks,
    including creation, retrieval, updating, and deletion operations.
    """

    def __init__(self):
        """Initialize an empty task manager."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date=None,
    ) -> Task:
        """
        Add a new task to the manager.

        Args:
            title: Task title
            description: Task description
            priority: Task priority level
            due_date: Optional deadline

        Returns:
            The created Task object

        Raises:
            ValidationError: If task data is invalid
        """
        task = Task(
            task_id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )

        self._tasks[task.task_id] = task
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The requested Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        return self._tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return list(self._tasks.values())

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """
        Get all tasks with a specific status.

        Args:
            status: The status to filter by

        Returns:
            List of tasks matching the status
        """
        return [task for task in self._tasks.values() if task.status == status]

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """
        Get all tasks with a specific priority.

        Args:
            priority: The priority to filter by

        Returns:
            List of tasks matching the priority
        """
        return [task for task in self._tasks.values() if task.priority == priority]

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks.

        Returns:
            List of overdue tasks
        """
        return [task for task in self._tasks.values() if task.is_overdue()]

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
    ) -> Task:
        """
        Update task details.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If update data is invalid
        """
        task = self.get_task(task_id)

        if title is not None:
            task.update_title(title)

        if description is not None:
            task.update_description(description)

        if priority is not None:
            task.set_priority(priority)

        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]

    def mark_task_in_progress(self, task_id: int) -> Task:
        """
        Mark a task as in progress.

        Args:
            task_id: ID of the task

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If status transition is invalid
        """
        task = self.get_task(task_id)
        task.mark_in_progress()
        return task

    def mark_task_completed(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: ID of the task

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If status transition is invalid
        """
        task = self.get_task(task_id)
        task.mark_completed()
        return task

    def mark_task_cancelled(self, task_id: int) -> Task:
        """
        Mark a task as cancelled.

        Args:
            task_id: ID of the task

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If status transition is invalid
        """
        task = self.get_task(task_id)
        task.mark_cancelled()
        return task

    def get_task_count(self) -> int:
        """
        Get total number of tasks.

        Returns:
            Number of tasks
        """
        return len(self._tasks)

    def get_statistics(self) -> dict:
        """
        Get statistics about tasks.

        Returns:
            Dictionary containing task statistics
        """
        total = len(self._tasks)
        completed = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        in_progress = len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        pending = len(self.get_tasks_by_status(TaskStatus.PENDING))
        cancelled = len(self.get_tasks_by_status(TaskStatus.CANCELLED))
        overdue = len(self.get_overdue_tasks())

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "cancelled": cancelled,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
        }

    def clear_all_tasks(self) -> None:
        """Clear all tasks from the manager."""
        self._tasks.clear()
        self._next_id = 1
