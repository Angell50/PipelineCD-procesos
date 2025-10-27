"""Unit tests for Task class."""

from datetime import datetime, timedelta

import pytest

from src.task_manager import Task, TaskPriority, TaskStatus, ValidationError


class TestTaskCreation:
    """Tests for task creation and validation."""

    def test_create_valid_task(self):
        """Test creating a valid task."""
        task = Task(task_id=1, title="Test Task", description="Test Description")

        assert task.task_id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.PENDING
        # FALLA INTENCIONAL #1: Esperamos prioridad HIGH pero es MEDIUM
        assert task.priority == TaskPriority.HIGH  # Este test fallará

    def test_create_task_with_priority(self):
        """Test creating a task with specific priority."""
        task = Task(task_id=1, title="High Priority", priority=TaskPriority.HIGH)

        assert task.priority == TaskPriority.HIGH

    def test_create_task_with_due_date(self):
        """Test creating a task with a due date."""
        due_date = datetime.now() + timedelta(days=7)
        task = Task(task_id=1, title="Task", due_date=due_date)

        assert task.due_date == due_date

    def test_create_task_empty_title_raises_error(self):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            Task(task_id=1, title="")

    def test_create_task_whitespace_title_raises_error(self):
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            Task(task_id=1, title="   ")

    def test_create_task_long_title_raises_error(self):
        """Test that title exceeding 200 characters raises ValidationError."""
        long_title = "a" * 201
        with pytest.raises(ValidationError, match="cannot exceed 200 characters"):
            Task(task_id=1, title=long_title)

    def test_create_task_negative_id_raises_error(self):
        """Test that negative task ID raises ValidationError."""
        with pytest.raises(ValidationError, match="must be non-negative"):
            Task(task_id=-1, title="Test")

    def test_create_task_past_due_date_raises_error(self):
        """Test that due date before creation raises ValidationError."""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValidationError, match="cannot be before creation date"):
            Task(task_id=1, title="Test", due_date=past_date)


class TestTaskStatusTransitions:
    """Tests for task status transitions."""

    def test_mark_task_in_progress(self, sample_task):
        """Test marking a task as in progress."""
        original_time = sample_task.updated_at
        sample_task.mark_in_progress()

        assert sample_task.status == TaskStatus.IN_PROGRESS
        assert sample_task.updated_at >= original_time

    def test_mark_task_completed(self, sample_task):
        """Test marking a task as completed."""
        sample_task.mark_completed()

        assert sample_task.status == TaskStatus.COMPLETED

    def test_mark_task_cancelled(self, sample_task):
        """Test marking a task as cancelled."""
        sample_task.mark_cancelled()

        assert sample_task.status == TaskStatus.CANCELLED

    def test_cannot_modify_completed_task(self, sample_task):
        """Test that completed tasks cannot be modified."""
        sample_task.mark_completed()

        with pytest.raises(ValidationError, match="Cannot modify a completed task"):
            sample_task.mark_in_progress()

    def test_cannot_modify_cancelled_task(self, sample_task):
        """Test that cancelled tasks cannot be modified."""
        sample_task.mark_cancelled()

        with pytest.raises(ValidationError, match="Cannot modify a cancelled task"):
            sample_task.mark_in_progress()

    def test_cannot_complete_cancelled_task(self, sample_task):
        """Test that cancelled tasks cannot be completed."""
        sample_task.mark_cancelled()

        with pytest.raises(ValidationError, match="Cannot complete a cancelled task"):
            sample_task.mark_completed()

    def test_cannot_cancel_completed_task(self, sample_task):
        """Test that completed tasks cannot be cancelled."""
        sample_task.mark_completed()

        with pytest.raises(ValidationError, match="Cannot cancel a completed task"):
            sample_task.mark_cancelled()


class TestTaskUpdates:
    """Tests for updating task properties."""

    def test_update_title(self, sample_task):
        """Test updating task title."""
        new_title = "Updated Title"
        sample_task.update_title(new_title)

        # FALLA INTENCIONAL #2: Esperamos un título diferente
        assert sample_task.title == "Wrong Title"  # Este test fallará

    def test_update_title_empty_raises_error(self, sample_task):
        """Test that updating to empty title raises error."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            sample_task.update_title("")

    def test_update_title_too_long_raises_error(self, sample_task):
        """Test that updating to long title raises error."""
        long_title = "a" * 201
        with pytest.raises(ValidationError, match="cannot exceed 200 characters"):
            sample_task.update_title(long_title)

    def test_update_description(self, sample_task):
        """Test updating task description."""
        new_desc = "Updated description"
        sample_task.update_description(new_desc)

        assert sample_task.description == new_desc

    def test_set_priority(self, sample_task):
        """Test setting task priority."""
        sample_task.set_priority(TaskPriority.CRITICAL)

        assert sample_task.priority == TaskPriority.CRITICAL


class TestTaskOverdue:
    """Tests for overdue task detection."""

    def test_task_without_due_date_not_overdue(self, sample_task):
        """Test that task without due date is not overdue."""
        assert not sample_task.is_overdue()

    def test_task_with_future_due_date_not_overdue(self, task_with_due_date):
        """Test that task with future due date is not overdue."""
        assert not task_with_due_date.is_overdue()

    def test_task_with_past_due_date_is_overdue(self, overdue_task):
        """Test that task with past due date is overdue."""
        assert overdue_task.is_overdue()

    def test_completed_task_not_overdue(self, overdue_task):
        """Test that completed task is not considered overdue."""
        overdue_task.mark_completed()
        assert not overdue_task.is_overdue()

    def test_cancelled_task_not_overdue(self, overdue_task):
        """Test that cancelled task is not considered overdue."""
        overdue_task.mark_cancelled()
        assert not overdue_task.is_overdue()


class TestTaskSerialization:
    """Tests for task serialization."""

    def test_to_dict(self, sample_task):
        """Test converting task to dictionary."""
        task_dict = sample_task.to_dict()

        assert task_dict["task_id"] == sample_task.task_id
        assert task_dict["title"] == sample_task.title
        assert task_dict["description"] == sample_task.description
        assert task_dict["status"] == sample_task.status.value
        assert task_dict["priority"] == sample_task.priority.value
        assert "created_at" in task_dict
        assert "updated_at" in task_dict
        assert "is_overdue" in task_dict

    def test_to_dict_with_due_date(self, task_with_due_date):
        """Test dictionary representation includes due date."""
        task_dict = task_with_due_date.to_dict()

        assert task_dict["due_date"] is not None
        assert task_dict["due_date"] == task_with_due_date.due_date.isoformat()

    def test_to_dict_without_due_date(self, sample_task):
        """Test dictionary representation with no due date."""
        task_dict = sample_task.to_dict()

        assert task_dict["due_date"] is None
