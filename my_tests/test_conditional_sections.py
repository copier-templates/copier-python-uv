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
