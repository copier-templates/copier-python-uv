<div align="center">

[![tests](https://github.com/patryk-gpl/copier-python-uv/actions/workflows/test.yml/badge.svg)](https://github.com/patryk-gpl/copier-python-uv/actions)
foll[![uv](https://img.shields.io/badge/uv-enabled-blue)](https://docs.astral.sh/uv/)
[![ruff](https://img.shields.io/badge/ruff-enabled-black)](https://docs.astral.sh/ruff/)
[![copier](https://img.shields.io/badge/copier-template-orange)](https://copier.readthedocs.io/)
[![License](https://img.shields.io/github/license/patryk-gpl/copier-python-uv)](LICENSE)

# 🎯 Python Project Template



This template provides a standardized Python project structure with sensible defaults, tailored to use in Python projects. It streamlines project setup and encourages best practices from the start.

</div>

---

## 📋 Prerequisites

The following tools must be installed:
- Python 3.10 or newer
- uv or pipx (if you want to install Copier in an isolated environment, accessible everywhere)
- copier

## 🚀 Usage

1. **Install Copier** (if not already):
   ```bash
   pipx install copier
   ```

   or

   ```bash
   uv tool install copier
   ```

2. **Generate files in your target repository (interactive):**
   ```bash
   copier copy /path/to/copier-template /path/to/your-repo
   ```
   Replace `/path/to/copier-template` with the path to this template, and `/path/to/your-repo` with your target repository.

3. **Generate non-interactively using the provided sample data file:**
   A sample data file is provided at `examples/config-basic.yml`.
   ```bash
   copier copy --data-file examples/config-basic.yml /path/to/copier-template /path/to/your-repo
   ```
   You can duplicate and modify that file to create variants (e.g., `data-with-ruff.yml`).

4. **(Optional) Override specific values at the CLI:**
   You can still override one or more answers on the fly:
   ```bash
   copier copy --data-file examples/config-basic.yml -d project_name=override_name /path/to/template /dest
   ```

5. **Review and commit the generated files:**
   ```bash
   cd /path/to/your-repo
   git add .
   git commit -m "feat: Bootstrap repository from template"
   ```

### 📦 Answers Files Explained
| File | Purpose |
|------|---------|
| `.copier-answers.yml` | Auto-maintained answers file for future updates (never edit manually). Now explicitly generated because the template includes `.copier-answers.yml.jinja`. |
| `examples/config-basic.yml` | Example data file passed with `--data-file` (excluded from rendered projects). |

### ⚙️ Internal Template Artifacts Not Copied
The template excludes helper folders (`examples/`, `my_tests/`) from generated projects via `_exclude` in `copier.yaml`. This keeps consumer projects clean.

To create a new variant template from existing data file configuration:
```bash
copier copy --data-file /path/to/config-basic.yml /path/to/template /dest
```
For advanced configuration (tasks, migrations, multiple templates) see the Copier docs sections: tasks, migrations, applying multiple templates.

## ✏️ Customization

You can edit the template files (`*.jinja`) to fit your team's standards. See [Copier documentation](https://copier.readthedocs.io/en/stable/) for advanced templating and options.

## 🧪 Testing the Template

This template includes comprehensive validation tests to ensure generated projects meet expected standards.

### ▶️ Running Tests

```bash
# Run all validation tests
make test
```

### ⚡ Test Performance

Tests use session-scoped fixtures for optimal performance:
- **Session-scoped fixtures:** Generated projects created once per test session, reused across all test modules
- **Module-scoped wrappers:** Clean test API with ~50% faster execution vs module scope alone
- **All tests read-only:** No mutations to generated projects ensures fixture reuse is safe

### 📁 Test Files

Test files are located in `my_tests/` folder.

| File | Purpose |
|------|---------|
| `test_core_structure.py` | Validates required files, directories, and project structure |
| `test_exclusions.py` | Ensures excluded files (`copier.yaml`, etc.) are not rendered |
| `test_conditional_sections.py` | Tests conditional rendering based on dependencies (e.g., Ruff) |

See `my_tests/conftest.py` for fixture definitions.

## 📚 Local Documentation

Project-specific guides and workflows:

| Topic | Location |
|-------|----------|
| CI/CD Pipeline | [docs/ci.md](docs/ci.md) |
| Development Setup | [docs/development.md](docs/development.md) |
| Template Architecture | [docs/architecture.md](docs/architecture.md) |

## 🔗 External References

For framework and tool documentation:

- **Copier Framework**: [Copier Documentation](https://copier.readthedocs.io/en/stable/)
- **Python Packaging**: [PEP 621 - pyproject.toml](https://peps.python.org/pep-0621/)
- **UV Package Manager**: [UV Documentation](https://docs.astral.sh/uv/)
- **Ruff Formatter**: [Ruff Documentation](https://docs.astral.sh/ruff/)
- **Pre-commit Hooks**: [pre-commit Framework](https://pre-commit.com/)
