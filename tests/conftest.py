"""Pytest configuration and fixtures."""

from datetime import datetime, timedelta

import pytest

from src.task_manager import Task, TaskManager, TaskPriority


@pytest.fixture
def task_manager():
    """Provide a fresh TaskManager instance for each test."""
    return TaskManager()


@pytest.fixture
def sample_task():
    """Provide a sample task for testing."""
    return Task(
        task_id=1,
        title="Sample Task",
        description="This is a sample task for testing",
        priority=TaskPriority.MEDIUM,
    )


@pytest.fixture
def high_priority_task():
    """Provide a high priority task for testing."""
    return Task(
        task_id=2,
        title="High Priority Task",
        description="This task has high priority",
        priority=TaskPriority.HIGH,
    )


@pytest.fixture
def task_with_due_date():
    """Provide a task with a due date for testing."""
    return Task(
        task_id=3,
        title="Task with Due Date",
        description="This task has a due date",
        due_date=datetime.now() + timedelta(days=7),
    )


@pytest.fixture
def overdue_task():
    """Provide an overdue task for testing."""
    created = datetime.now() - timedelta(days=7)
    due = datetime.now() - timedelta(days=1)
    task = Task(
        task_id=4,
        title="Overdue Task",
        description="This task is overdue",
        created_at=created,
        updated_at=created,
        due_date=due,
    )
    return task
