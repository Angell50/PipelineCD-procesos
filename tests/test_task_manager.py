"""Unit tests for TaskManager class."""

from datetime import datetime, timedelta

import pytest

from src.task_manager import (
    TaskNotFoundError,
    TaskPriority,
    TaskStatus,
    ValidationError,
)


class TestTaskManagerCreation:
    """Tests for TaskManager initialization."""

    def test_create_task_manager(self, task_manager):
        """Test creating a new task manager."""
        assert task_manager is not None
        assert task_manager.get_task_count() == 0

    def test_task_manager_starts_empty(self, task_manager):
        """Test that new task manager has no tasks."""
        assert task_manager.get_all_tasks() == []


class TestAddTask:
    """Tests for adding tasks."""

    def test_add_task(self, task_manager):
        """Test adding a task."""
        task = task_manager.add_task(title="Test Task", description="Test Description")

        assert task.task_id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task_manager.get_task_count() == 1

    def test_add_multiple_tasks(self, task_manager):
        """Test adding multiple tasks."""
        task1 = task_manager.add_task(title="Task 1")
        task2 = task_manager.add_task(title="Task 2")
        task3 = task_manager.add_task(title="Task 3")

        assert task1.task_id == 1
        assert task2.task_id == 2
        assert task3.task_id == 3
        assert task_manager.get_task_count() == 3

    def test_add_task_with_priority(self, task_manager):
        """Test adding task with specific priority."""
        task = task_manager.add_task(title="High Priority", priority=TaskPriority.HIGH)

        assert task.priority == TaskPriority.HIGH

    def test_add_task_with_due_date(self, task_manager):
        """Test adding task with due date."""
        due_date = datetime.now() + timedelta(days=7)
        task = task_manager.add_task(title="Task", due_date=due_date)

        assert task.due_date == due_date

    def test_add_task_invalid_title_raises_error(self, task_manager):
        """Test that adding task with invalid title raises error."""
        with pytest.raises(ValidationError):
            task_manager.add_task(title="")


class TestGetTask:
    """Tests for retrieving tasks."""

    def test_get_existing_task(self, task_manager):
        """Test retrieving an existing task."""
        task = task_manager.add_task(title="Test Task")
        retrieved = task_manager.get_task(task.task_id)

        assert retrieved == task

    def test_get_nonexistent_task_raises_error(self, task_manager):
        """Test that getting non-existent task raises error."""
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            task_manager.get_task(999)

    def test_get_all_tasks(self, task_manager):
        """Test getting all tasks."""
        task1 = task_manager.add_task(title="Task 1")
        task2 = task_manager.add_task(title="Task 2")
        task3 = task_manager.add_task(title="Task 3")

        all_tasks = task_manager.get_all_tasks()

        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks


class TestGetTasksByStatus:
    """Tests for filtering tasks by status."""

    def test_get_pending_tasks(self, task_manager):
        """Test getting pending tasks."""
        task1 = task_manager.add_task(title="Pending Task")
        task2 = task_manager.add_task(title="Another Pending")
        completed_task = task_manager.add_task(title="To Complete")
        task_manager.mark_task_completed(completed_task.task_id)

        pending_tasks = task_manager.get_tasks_by_status(TaskStatus.PENDING)

        assert len(pending_tasks) == 2
        assert task1 in pending_tasks
        assert task2 in pending_tasks
        assert completed_task not in pending_tasks

    def test_get_completed_tasks(self, task_manager):
        """Test getting completed tasks."""
        task1 = task_manager.add_task(title="Task 1")
        task_manager.add_task(title="Task 2")

        task_manager.mark_task_completed(task1.task_id)

        completed_tasks = task_manager.get_tasks_by_status(TaskStatus.COMPLETED)

        assert len(completed_tasks) == 1
        assert task1 in completed_tasks

    def test_get_in_progress_tasks(self, task_manager):
        """Test getting in-progress tasks."""
        task1 = task_manager.add_task(title="Task 1")
        task_manager.mark_task_in_progress(task1.task_id)

        in_progress = task_manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)

        assert len(in_progress) == 1
        assert task1 in in_progress


class TestGetTasksByPriority:
    """Tests for filtering tasks by priority."""

    def test_get_high_priority_tasks(self, task_manager):
        """Test getting high priority tasks."""
        task1 = task_manager.add_task(title="High", priority=TaskPriority.HIGH)
        task_manager.add_task(title="Medium", priority=TaskPriority.MEDIUM)
        task_manager.add_task(title="Critical", priority=TaskPriority.CRITICAL)

        high_priority = task_manager.get_tasks_by_priority(TaskPriority.HIGH)

        assert len(high_priority) == 1
        assert task1 in high_priority

    def test_get_critical_priority_tasks(self, task_manager):
        """Test getting critical priority tasks."""
        task1 = task_manager.add_task(title="Critical 1", priority=TaskPriority.CRITICAL)
        task2 = task_manager.add_task(title="Critical 2", priority=TaskPriority.CRITICAL)
        task_manager.add_task(title="Low", priority=TaskPriority.LOW)

        critical_tasks = task_manager.get_tasks_by_priority(TaskPriority.CRITICAL)

        assert len(critical_tasks) == 2
        assert task1 in critical_tasks
        assert task2 in critical_tasks


class TestGetOverdueTasks:
    """Tests for getting overdue tasks."""

    def test_get_overdue_tasks(self, task_manager):
        """Test getting overdue tasks."""
        future_date = datetime.now() + timedelta(days=7)

        # Create task with future date first, then make it overdue
        overdue_task = task_manager.add_task(title="Overdue", due_date=future_date)
        overdue_task.created_at = datetime.now() - timedelta(days=10)
        overdue_task.due_date = datetime.now() - timedelta(days=1)

        task_manager.add_task(title="Future", due_date=future_date)
        task_manager.add_task(title="No Date")

        overdue_tasks = task_manager.get_overdue_tasks()

        assert len(overdue_tasks) == 1
        assert overdue_task in overdue_tasks

    def test_completed_tasks_not_overdue(self, task_manager):
        """Test that completed tasks are not in overdue list."""
        future_date = datetime.now() + timedelta(days=7)

        # Create task with future date first, then make it overdue
        task = task_manager.add_task(title="Overdue", due_date=future_date)
        task.created_at = datetime.now() - timedelta(days=10)
        task.due_date = datetime.now() - timedelta(days=1)

        task_manager.mark_task_completed(task.task_id)

        overdue_tasks = task_manager.get_overdue_tasks()

        assert len(overdue_tasks) == 0


class TestUpdateTask:
    """Tests for updating tasks."""

    def test_update_task_title(self, task_manager):
        """Test updating task title."""
        task = task_manager.add_task(title="Original Title")
        updated = task_manager.update_task(task.task_id, title="New Title")

        assert updated.title == "New Title"

    def test_update_task_description(self, task_manager):
        """Test updating task description."""
        task = task_manager.add_task(title="Task")
        updated = task_manager.update_task(task.task_id, description="New Description")

        assert updated.description == "New Description"

    def test_update_task_priority(self, task_manager):
        """Test updating task priority."""
        task = task_manager.add_task(title="Task")
        updated = task_manager.update_task(task.task_id, priority=TaskPriority.CRITICAL)

        assert updated.priority == TaskPriority.CRITICAL

    def test_update_nonexistent_task_raises_error(self, task_manager):
        """Test that updating non-existent task raises error."""
        with pytest.raises(TaskNotFoundError):
            task_manager.update_task(999, title="New Title")


class TestDeleteTask:
    """Tests for deleting tasks."""

    def test_delete_task(self, task_manager):
        """Test deleting a task."""
        task = task_manager.add_task(title="To Delete")
        assert task_manager.get_task_count() == 1

        task_manager.delete_task(task.task_id)

        assert task_manager.get_task_count() == 0

    def test_delete_nonexistent_task_raises_error(self, task_manager):
        """Test that deleting non-existent task raises error."""
        with pytest.raises(TaskNotFoundError):
            task_manager.delete_task(999)

    def test_delete_task_cannot_retrieve(self, task_manager):
        """Test that deleted task cannot be retrieved."""
        task = task_manager.add_task(title="To Delete")
        task_manager.delete_task(task.task_id)

        with pytest.raises(TaskNotFoundError):
            task_manager.get_task(task.task_id)


class TestTaskStatusMethods:
    """Tests for task status management methods."""

    def test_mark_task_in_progress(self, task_manager):
        """Test marking task as in progress."""
        task = task_manager.add_task(title="Task")
        updated = task_manager.mark_task_in_progress(task.task_id)

        assert updated.status == TaskStatus.IN_PROGRESS

    def test_mark_task_completed(self, task_manager):
        """Test marking task as completed."""
        task = task_manager.add_task(title="Task")
        updated = task_manager.mark_task_completed(task.task_id)

        assert updated.status == TaskStatus.COMPLETED

    def test_mark_task_cancelled(self, task_manager):
        """Test marking task as cancelled."""
        task = task_manager.add_task(title="Task")
        updated = task_manager.mark_task_cancelled(task.task_id)

        assert updated.status == TaskStatus.CANCELLED

    def test_mark_nonexistent_task_raises_error(self, task_manager):
        """Test that marking non-existent task raises error."""
        with pytest.raises(TaskNotFoundError):
            task_manager.mark_task_completed(999)


class TestStatistics:
    """Tests for task statistics."""

    def test_get_statistics_empty(self, task_manager):
        """Test statistics for empty task manager."""
        stats = task_manager.get_statistics()

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["in_progress"] == 0
        assert stats["pending"] == 0
        assert stats["cancelled"] == 0
        assert stats["overdue"] == 0
        assert stats["completion_rate"] == 0

    def test_get_statistics_with_tasks(self, task_manager):
        """Test statistics with various tasks."""
        task1 = task_manager.add_task(title="Task 1")
        task2 = task_manager.add_task(title="Task 2")
        task3 = task_manager.add_task(title="Task 3")
        task_manager.add_task(title="Task 4")

        task_manager.mark_task_completed(task1.task_id)
        task_manager.mark_task_completed(task2.task_id)
        task_manager.mark_task_in_progress(task3.task_id)

        stats = task_manager.get_statistics()

        assert stats["total"] == 4
        assert stats["completed"] == 2
        assert stats["in_progress"] == 1
        assert stats["pending"] == 1
        # FALLA INTENCIONAL #3: Esperamos 75% pero debería ser 50%
        assert stats["completion_rate"] == 75.0  # Este test fallará

    def test_get_statistics_with_overdue(self, task_manager):
        """Test statistics includes overdue tasks."""
        future_date = datetime.now() + timedelta(days=7)

        # Create task with future date first, then make it overdue
        task = task_manager.add_task(title="Overdue", due_date=future_date)
        task.created_at = datetime.now() - timedelta(days=10)
        task.due_date = datetime.now() - timedelta(days=1)

        stats = task_manager.get_statistics()

        assert stats["overdue"] == 1


class TestClearAllTasks:
    """Tests for clearing all tasks."""

    def test_clear_all_tasks(self, task_manager):
        """Test clearing all tasks."""
        task_manager.add_task(title="Task 1")
        task_manager.add_task(title="Task 2")
        task_manager.add_task(title="Task 3")

        assert task_manager.get_task_count() == 3

        task_manager.clear_all_tasks()

        assert task_manager.get_task_count() == 0

    def test_clear_resets_id_counter(self, task_manager):
        """Test that clearing tasks resets the ID counter."""
        task_manager.add_task(title="Task 1")
        task_manager.add_task(title="Task 2")
        task_manager.clear_all_tasks()

        new_task = task_manager.add_task(title="New Task")

        assert new_task.task_id == 1
