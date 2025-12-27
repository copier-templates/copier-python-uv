"""Test LICENSE file is optional and excluded by default."""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import _make_data, _run_copy


@pytest.fixture(scope="module")
def generated_without_license() -> Path:
    """Generate project without LICENSE file (default behavior)."""
    data = _make_data({"project_name": "no_license_proj", "include_license": False})
    return _run_copy(data, dst_name="no_license")


@pytest.fixture(scope="module")
def generated_with_license() -> Path:
    """Generate project with LICENSE file explicitly requested."""
    data = _make_data(
        {
            "project_name": "with_license_proj",
            "include_license": True,
        }
    )
    return _run_copy(data, dst_name="with_license")


def test_license_excluded_by_default(generated_without_license: Path):
    """Test that LICENSE file is NOT included when include_license=false (default)."""
    license_path = generated_without_license / "LICENSE"
    assert not license_path.exists(), "LICENSE should not exist when include_license=false (default)"


def test_license_included_when_requested(generated_with_license: Path):
    """Test that LICENSE file IS included when include_license=true."""
    license_path = generated_with_license / "LICENSE"
    assert license_path.is_file(), "LICENSE should exist when include_license=true"


def test_license_content_matches_template(generated_with_license: Path):
    """Test that generated LICENSE file contains expected content."""
    license_path = generated_with_license / "LICENSE"
    content = license_path.read_text()
    assert "MIT License" in content, "LICENSE should contain MIT License header"
    assert "Copyright" in content, "LICENSE should contain copyright notice"
