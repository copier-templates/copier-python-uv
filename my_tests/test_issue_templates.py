"""Tests for GitHub issue templates in generated projects."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

# Test data: expected template files and their characteristics
EXPECTED_TEMPLATES = [
    "01-bug.yml",
    "02-feature.yml",
    "03-docs.yml",
    "04-discussion.yml",
    "05-security.yml",
]


def _parse_yaml_safe(file_path: Path) -> dict:
    """Parse YAML file safely, converting to native types."""
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize("template_file", EXPECTED_TEMPLATES, ids=lambda x: f"template:{x}")
def test_issue_template_file_exists(generated_basic: Path, template_file: str):
    """Test each expected issue template file exists in generated project."""
    template_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / template_file
    assert template_path.is_file(), f"Missing expected issue template: {template_file}"


def test_github_issue_template_config_exists(generated_basic: Path):
    """Test that config.yml exists in .github/ISSUE_TEMPLATE."""
    config_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    assert config_path.is_file(), "Missing .github/ISSUE_TEMPLATE/config.yml"


@pytest.mark.parametrize("template_file", EXPECTED_TEMPLATES, ids=lambda x: f"yaml:{x}")
def test_issue_template_yaml_syntax_valid(generated_basic: Path, template_file: str):
    """Test each template has valid YAML syntax."""
    template_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / template_file
    try:
        data = _parse_yaml_safe(template_path)
        assert isinstance(data, dict), f"{template_file} did not parse to a dict"
    except Exception as e:
        pytest.fail(f"Failed to parse {template_file}: {e}")


@pytest.mark.parametrize("template_file", EXPECTED_TEMPLATES, ids=lambda x: f"required:{x}")
def test_issue_template_has_required_fields(generated_basic: Path, template_file: str):
    """Test each template has name, description, type, and body."""
    template_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / template_file
    data = _parse_yaml_safe(template_path)

    # Required fields per GitHub's form schema
    assert "name" in data, f"{template_file} missing 'name' field"
    assert "description" in data, f"{template_file} missing 'description' field"
    assert "type" in data, f"{template_file} missing 'type' field"
    assert "body" in data, f"{template_file} missing 'body' array"
    assert isinstance(data["body"], list), f"{template_file} body must be an array"


def test_issue_template_body_has_elements(generated_basic: Path):
    """Test that each template body contains at least one form element."""
    template_dir = generated_basic / ".github" / "ISSUE_TEMPLATE"
    for template_file in EXPECTED_TEMPLATES:
        template_path = template_dir / template_file
        data = _parse_yaml_safe(template_path)
        body = data.get("body", [])
        assert len(body) > 0, f"{template_file} body is empty, should contain form elements"


def test_config_yml_yaml_syntax_valid(generated_basic: Path):
    """Test config.yml has valid YAML syntax."""
    config_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    try:
        data = _parse_yaml_safe(config_path)
        assert isinstance(data, dict), "config.yml did not parse to a dict"
    except Exception as e:
        pytest.fail(f"Failed to parse config.yml: {e}")


def test_config_yml_disables_blank_issues(generated_basic: Path):
    """Test that config.yml disables blank issues for template enforcement."""
    config_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    data = _parse_yaml_safe(config_path)
    assert "blank_issues_enabled" in data, "config.yml missing 'blank_issues_enabled'"
    assert data["blank_issues_enabled"] is False, "blank_issues_enabled should be false to enforce templates"


def test_bug_template_includes_reproduction_steps(generated_basic: Path):
    """Bug template should guide users to reproduce the issue."""
    template_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / "01-bug.yml"
    data = _parse_yaml_safe(template_path)
    body_text = str(data.get("body", []))
    # Check if reproduction/steps-related fields exist
    assert "reproduction" in body_text.lower() or "steps" in body_text.lower(), (
        "Bug template should include reproduction information"
    )


def test_feature_template_includes_use_case(generated_basic: Path):
    """Feature template should ask for use case/motivation."""
    template_path = generated_basic / ".github" / "ISSUE_TEMPLATE" / "02-feature.yml"
    data = _parse_yaml_safe(template_path)
    body_text = str(data.get("body", []))
    assert "use case" in body_text.lower() or "motivation" in body_text.lower(), (
        "Feature template should include use case information"
    )


def test_templates_include_labels(generated_basic: Path):
    """Test that templates assign appropriate labels."""
    template_dir = generated_basic / ".github" / "ISSUE_TEMPLATE"
    label_mapping = {
        "01-bug.yml": "bug",
        "02-feature.yml": "feature",
        "03-docs.yml": "docs",
        "04-discussion.yml": "question",
        "05-security.yml": ["security", "bug"],
    }

    for template_file, expected_labels in label_mapping.items():
        template_path = template_dir / template_file
        data = _parse_yaml_safe(template_path)
        labels = data.get("labels", [])
        if isinstance(expected_labels, str):
            assert expected_labels in labels, f"{template_file} should have '{expected_labels}' label"
        else:
            for label in expected_labels:
                assert label in labels, f"{template_file} should have '{label}' label"


def test_issue_templates_present_when_github_integration_enabled(
    generated_with_github_integration: Path,
):
    """Test that issue templates are present when GitHub integration is enabled."""
    template_dir = generated_with_github_integration / ".github" / "ISSUE_TEMPLATE"
    assert template_dir.is_dir(), "GitHub integration should create .github/ISSUE_TEMPLATE directory"

    for template_file in EXPECTED_TEMPLATES:
        template_path = template_dir / template_file
        assert template_path.is_file(), f"GitHub integration should include {template_file}"


def test_issue_templates_absent_when_github_integration_disabled(
    generated_without_github_integration: Path,
):
    """Test that issue templates are excluded when GitHub integration is disabled."""
    issue_template_dir = generated_without_github_integration / ".github" / "ISSUE_TEMPLATE"

    # Directory should not exist or be empty
    if issue_template_dir.exists():
        contents = list(issue_template_dir.iterdir())
        assert len(contents) == 0, (
            f"GitHub integration disabled should not contain issue templates, but found: {[item.name for item in contents]}"
        )


def test_github_config_present_when_integration_enabled(
    generated_with_github_integration: Path,
):
    """Test that config.yml exists when GitHub integration is enabled."""
    config_path = generated_with_github_integration / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    assert config_path.is_file(), "config.yml should exist when GitHub integration is enabled"


def test_github_config_absent_when_integration_disabled(
    generated_without_github_integration: Path,
):
    """Test that config.yml does not exist when GitHub integration is disabled."""
    config_path = generated_without_github_integration / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    assert not config_path.exists(), "config.yml should not exist when GitHub integration is disabled"


def test_workflows_present_when_github_integration_enabled(
    generated_with_github_integration: Path,
):
    """Test that GitHub workflows are present when GitHub integration is enabled."""
    workflows_dir = generated_with_github_integration / ".github" / "workflows"
    assert workflows_dir.is_dir(), "GitHub integration should create .github/workflows directory"

    # At minimum, test.yml workflow should be present
    test_workflow = workflows_dir / "test.yml"
    assert test_workflow.is_file(), "GitHub integration should include test.yml workflow"


def test_workflows_absent_when_github_integration_disabled(
    generated_without_github_integration: Path,
):
    """Test that GitHub workflows are excluded when GitHub integration is disabled."""
    workflows_dir = generated_without_github_integration / ".github" / "workflows"

    # Directory should not exist or be empty
    if workflows_dir.exists():
        contents = list(workflows_dir.iterdir())
        assert len(contents) == 0, (
            f"GitHub integration disabled should not contain workflows, but found: {[item.name for item in contents]}"
        )
