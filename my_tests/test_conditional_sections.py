"""Tests for conditional README sections and dependency-driven rendering."""

from __future__ import annotations

from pathlib import Path


def test_readme_includes_tests_section_when_pytest(generated_basic: Path):
    readme = (generated_basic / "README.md").read_text()
    assert "Running Tests" in readme


def test_readme_includes_ruff_section_only_when_present(generated_with_ruff: Path):
    readme = (generated_with_ruff / "README.md").read_text()
    assert "Code Quality" in readme


def test_readme_excludes_ruff_section_when_not_selected(generated_basic: Path):
    readme = (generated_basic / "README.md").read_text()
    assert "Code Quality" not in readme


def test_pyproject_includes_license_field_when_selected(generated_with_license: Path):
    """Verify pyproject.toml includes license field when license is selected."""
    pyproject = (generated_with_license / "pyproject.toml").read_text()
    assert 'license = "MIT"' in pyproject, "pyproject.toml should include license field"


def test_pyproject_includes_license_files_when_license_selected(generated_with_license: Path):
    """Verify pyproject.toml includes license-files field when license is selected."""
    pyproject = (generated_with_license / "pyproject.toml").read_text()
    assert 'license-files = ["LICENSE"]' in pyproject, "pyproject.toml should include license-files field"


def test_pyproject_omits_license_field_when_not_selected(generated_basic: Path):
    """Verify pyproject.toml omits license field when license is not selected."""
    pyproject = (generated_basic / "pyproject.toml").read_text()
    assert "license =" not in pyproject, "pyproject.toml should not include license field when no license selected"
    assert "license-files" not in pyproject, "pyproject.toml should not include license-files when no license selected"
