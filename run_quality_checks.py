#!/usr/bin/env python
"""
Script to run all quality checks for the project.
This includes: formatting, linting, type checking, and tests.
"""

import subprocess
import sys
from typing import List, Tuple


def run_command(cmd: List[str], description: str) -> Tuple[bool, str]:
    """
    Run a command and return success status and output.

    Args:
        cmd: Command to run as list of strings
        description: Human-readable description of the command

    Returns:
        Tuple of (success: bool, output: str)
    """
    print(f"\n{'=' * 70}")
    print(f"Running: {description}")
    print(f"{'=' * 70}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, shell=True)

        output = result.stdout + result.stderr

        if result.returncode == 0:
            print(f"[PASS] {description} passed")
            return True, output
        else:
            print(f"[FAIL] {description} failed")
            print(output)
            return False, output

    except Exception as e:
        print(f"[ERROR] Error running {description}: {e}")
        return False, str(e)


def main():
    """Run all quality checks."""
    print("\n" + "=" * 70)
    print("TASK MANAGER - QUALITY CHECKS")
    print("=" * 70)

    checks = [
        (["black", "--check", "src", "tests"], "Code formatting (Black)"),
        (["isort", "--check-only", "src", "tests"], "Import sorting (isort)"),
        (["flake8", "src", "tests"], "Linting (Flake8)"),
        (["pylint", "src"], "Code analysis (Pylint)"),
        (["mypy", "src"], "Type checking (MyPy)"),
        (
            [
                "pytest",
                "-v",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html",
            ],
            "Unit tests with coverage",
        ),
    ]

    results = []

    for cmd, description in checks:
        success, _ = run_command(cmd, description)
        results.append((description, success))

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    all_passed = True
    for description, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status:8} - {description}")
        if not success:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("\nAll quality checks passed!")
        return 0
    else:
        print("\nSome quality checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
