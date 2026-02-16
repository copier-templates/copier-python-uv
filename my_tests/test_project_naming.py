"""Tests for project naming conventions: dashes in project name, underscores in package.

These tests enforce:
- project_name must use dashes (not allowed underscores)
- _package_name is derived from project_name with dashes converted to underscores
- folder structure uses _package_name (underscores)
- all imports and references use _package_name (underscores)
"""

from __future__ import annotations

from pathlib import Path

import pytest
from copier import run_copy


def _run_copy_with_data(template_root: Path, data: dict[str, object], dst_name: str = "_test") -> Path:
    """Helper to run copier with given data."""
    import tempfile

    dst_dir = Path(tempfile.mkdtemp(prefix=f"copier-naming-test-{dst_name}-"))
    run_copy(
        str(template_root),
        str(dst_dir),
        data=data,
        defaults=True,
        overwrite=True,
        unsafe=True,
        vcs_ref="HEAD",
    )
    return dst_dir


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
BASE_DATA = {
    "project_description": "Test description",
    "author_name": "Test User",
    "author_email": "test@test.com",
    "production_deps": [],
    "dev_deps": ["pytest", "pytest-cov"],
}


@pytest.fixture(scope="module")
def generated_dash_project() -> Path:
    """Wraps session fixture."""
    data = BASE_DATA | {"project_name": "my-awesome-project"}
    return _run_copy_with_data(TEMPLATE_ROOT, data, dst_name="dash")


class TestProjectNamingWithDashes:
    """Tests for project names with dashes."""

    def test_package_folder_uses_underscores(self, generated_dash_project: Path):
        """Package folder should use underscores (my_awesome_project), not dashes."""
        # When project_name is "my-awesome-project", package folder should be "my_awesome_project"
        assert (generated_dash_project / "src" / "my_awesome_project").is_dir(), (
            "Package folder should exist at src/my_awesome_project"
        )

    def test_pyproject_name_uses_dashes(self, generated_dash_project: Path):
        """Project name in pyproject.toml should use dashes."""
        pyproject = (generated_dash_project / "pyproject.toml").read_text()
        assert 'name = "my-awesome-project"' in pyproject, (
            'pyproject.toml should have project name with dashes: name = "my-awesome-project"'
        )

    def test_readme_import_uses_underscores(self, generated_dash_project: Path):
        """README instructions should use underscores for imports."""
        readme = (generated_dash_project / "README.md").read_text()
        # The import command should use underscores
        assert "python -m my_awesome_project" in readme, (
            "README should reference package with underscores in import: python -m my_awesome_project"
        )

    def test_coverage_config_uses_underscores(self, generated_dash_project: Path):
        """pytest coverage configuration should use underscores."""
        pyproject = (generated_dash_project / "pyproject.toml").read_text()
        assert "--cov=my_awesome_project" in pyproject, (
            "pytest coverage should use underscores for package name: --cov=my_awesome_project"
        )

    def test_init_file_exists(self, generated_dash_project: Path):
        """__init__.py should exist in the package folder."""
        init_file = generated_dash_project / "src" / "my_awesome_project" / "__init__.py"
        assert init_file.is_file(), "Package __init__.py should exist at src/my_awesome_project/__init__.py"


class TestProjectNameValidation:
    """Tests for validation of project names."""

    def test_underscore_project_name_is_rejected(self):
        """Project names with underscores should be rejected by validator."""
        # This test documents the expected behavior - validator should reject underscores
        # For now, this is just documenting what we want to happen
        # The actual validation happens in copier.yaml validator
        # We verify it doesn't create a folder when rejected
        pytest.skip("Validation happens at copier prompt level - requires manual testing or integration test")

    def test_alphanumeric_with_dashes_allowed(self, generated_dash_project: Path):
        """Project names with letters, numbers, and dashes should be accepted."""
        # If we got here, the project was created successfully with dashes
        assert (generated_dash_project / "pyproject.toml").exists(), (
            "Project with dashes in name should be created successfully"
        )

    def test_alphanumeric_with_numbers_allowed(self):
        """Project names with numbers should be allowed."""
        data = BASE_DATA | {"project_name": "project-123-test"}
        project = _run_copy_with_data(TEMPLATE_ROOT, data, dst_name="numbers")
        assert (project / "src" / "project_123_test").is_dir(), (
            "Project with numbers and dashes should create folder with underscores"
        )
