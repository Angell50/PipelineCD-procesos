# Task Manager Application

A professional Python task management system built with clean architecture, comprehensive testing, and code quality tools.

## Features

- **Task Management**: Create, update, delete, and track tasks
- **Task Properties**: Title, description, status, priority, and due dates
- **Status Tracking**: Pending, In Progress, Completed, Cancelled
- **Priority Levels**: Low, Medium, High, Critical
- **Overdue Detection**: Automatic identification of overdue tasks
- **Statistics**: Comprehensive task statistics and completion rates

## Project Structure

```
.
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── exceptions.py
│       ├── task.py
│       └── task_manager.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_task.py
│   └── test_task_manager.py
├── .flake8
├── .pylintrc
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Makefile
└── README.md
```

## Installation

### Basic Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Development Installation

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Running the Application

### 1. Interactive CLI Application

Run the interactive command-line application:

```bash
python main.py
```

This will start an interactive menu where you can:
- Add new tasks
- View all tasks
- Filter tasks by status or priority
- Mark tasks as in progress or completed
- Update and delete tasks
- View statistics
- See overdue tasks

### 2. Simple Example

Run a demonstration script:

```bash
python ejemplo_simple.py
```

This will demonstrate all features with example tasks.

### 3. Use as a Library

Import and use in your own Python code:

```python
from src.task_manager import TaskManager, TaskPriority

# Create a task manager
manager = TaskManager()

# Add tasks
task1 = manager.add_task(
    title="Complete project documentation",
    description="Write comprehensive README and API docs",
    priority=TaskPriority.HIGH
)

task2 = manager.add_task(
    title="Fix bug #123",
    priority=TaskPriority.CRITICAL
)

# Update task status
manager.mark_task_in_progress(task1.task_id)
manager.mark_task_completed(task2.task_id)

# Get all pending tasks
pending_tasks = manager.get_tasks_by_status(TaskStatus.PENDING)

# Get statistics
stats = manager.get_statistics()
print(f"Completion rate: {stats['completion_rate']}%")
```

## Testing

### Run All Tests

```bash
# Using pytest
pytest

# Using make
make test
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html --cov-report=term-missing

# Using make
make coverage
```

The coverage report will be generated in `htmlcov/index.html`.

### Test Coverage Goals

- Minimum coverage: 90%
- Branch coverage enabled
- Missing lines reported

## Code Quality

This project uses multiple tools to ensure code quality:

### Formatting

```bash
# Format code with Black
black src tests

# Sort imports with isort
isort src tests

# Format everything
make format
```

### Linting

```bash
# Run flake8
flake8 src tests

# Run pylint
pylint src

# Run mypy
mypy src

# Run all linters
make lint
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Or use make
make pre-commit-run
```

## Code Quality Tools Configuration

### Black
- Line length: 100 characters
- Target: Python 3.9+

### Flake8
- Max line length: 100
- Max complexity: 10
- Plugins: bugbear, comprehensions, simplify

### Pylint
- Output: colorized
- Max line length: 100
- Max arguments: 7

### Pytest
- Coverage threshold: 90%
- Branch coverage enabled
- HTML and XML reports

## Development Workflow

1. **Write Code**: Implement your feature or fix
2. **Format**: `make format`
3. **Lint**: `make lint`
4. **Test**: `make test`
5. **Coverage**: `make coverage`
6. **All Checks**: `make all`

## API Documentation

### Task Class

Main properties:
- `task_id`: Unique identifier
- `title`: Task title (1-200 characters)
- `description`: Detailed description
- `status`: Current status (TaskStatus enum)
- `priority`: Priority level (TaskPriority enum)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `due_date`: Optional deadline

Key methods:
- `mark_in_progress()`: Change status to in progress
- `mark_completed()`: Mark as completed
- `mark_cancelled()`: Mark as cancelled
- `update_title(new_title)`: Update title
- `update_description(new_desc)`: Update description
- `set_priority(priority)`: Change priority
- `is_overdue()`: Check if task is overdue

### TaskManager Class

Key methods:
- `add_task(title, description, priority, due_date)`: Create new task
- `get_task(task_id)`: Retrieve task by ID
- `get_all_tasks()`: Get all tasks
- `get_tasks_by_status(status)`: Filter by status
- `get_tasks_by_priority(priority)`: Filter by priority
- `get_overdue_tasks()`: Get overdue tasks
- `update_task(task_id, ...)`: Update task properties
- `delete_task(task_id)`: Remove task
- `mark_task_in_progress(task_id)`: Update status
- `mark_task_completed(task_id)`: Complete task
- `mark_task_cancelled(task_id)`: Cancel task
- `get_statistics()`: Get task statistics

## Contributing

1. Follow PEP 8 style guidelines
2. Write comprehensive tests (90%+ coverage)
3. Update documentation
4. Run all quality checks before committing
5. Use pre-commit hooks

## License

MIT License

## Author

Senior Dev Team
