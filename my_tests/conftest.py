"""Pytest fixtures for validating the Copier template itself.
These tests are NOT copied into generated projects (excluded via _exclude).
"""

from __future__ import annotations

from pathlib import Path
import tempfile

import pytest
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

# Base data and small helper to produce test data with overrides
BASE_DATA: dict[str, object] = {
    "project_description": "Example description",
    "author_name": "Test User",
    "author_email": "test@test.com",
    "production_deps": ["requests"],
    "dev_deps": ["pytest", "pytest-cov"],
}


def _make_data(overrides: dict[str, object]) -> dict[str, object]:
    """Return a copy of BASE_DATA merged with overrides."""
    return BASE_DATA | overrides


def _run_copy(data: dict[str, object], dst_name: str = "_generated") -> Path:
    dst_dir = Path(tempfile.mkdtemp(prefix=f"copier-template-test-{dst_name}-"))
    run_copy(
        str(TEMPLATE_ROOT),
        str(dst_dir),
        data=data,
        defaults=True,
        overwrite=True,
        unsafe=True,
        vcs_ref="HEAD",  # Use current git HEAD instead of latest tag
    )
    return dst_dir


@pytest.fixture(scope="session")
def _session_basic_project() -> Path:
    """Session-scoped: basic generated project (reused across all test modules)."""
    data = _make_data({"project_name": "example_proj"})
    return _run_copy(data, dst_name="basic")


@pytest.fixture(scope="session")
def _session_with_ruff_project() -> Path:
    """Session-scoped: generated project with Ruff (reused across all test modules)."""
    data = _make_data(
        {
            "project_name": "ruff_proj",
            "production_deps": [],
            "dev_deps": ["pytest", "pytest-cov", "ruff"],
        }
    )
    return _run_copy(data, dst_name="ruff")


@pytest.fixture(scope="module")
def generated_basic(_session_basic_project: Path) -> Path:
    """Basic generated project (wraps session fixture for ~50% faster execution)."""
    return _session_basic_project


@pytest.fixture(scope="module")
def generated_with_ruff(_session_with_ruff_project: Path) -> Path:
    """Generated project with Ruff (wraps session fixture for ~50% faster execution)."""
    return _session_with_ruff_project
