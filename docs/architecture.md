# Template Architecture

This document describes the structure and design of the Copier template.

## Overview

The template is built using [Copier](https://copier.readthedocs.io/), a project templating tool that uses Jinja2 for dynamic content generation.

## Configuration

### `copier.yaml`

The main template configuration file that defines:
- **Questions**: Interactive prompts for template variables
- **Conditional Files**: Using `_if_` prefix for dynamic file inclusion
- **Exclusions**: Files/directories not copied to generated projects via `_exclude`
- **Jinja Extensions**: Custom Jinja filters and extensions
- **Tasks**: Post-generation operations (migrations, setup scripts)

## Template Structure

```
├── src/{{project_name}}/        # Main source code directory (templated)
│   ├── __init__.py.jinja        # Package initialization
│   └── main.py.jinja            # Main module
├── tests/                       # Test directory structure (templated)
│   ├── __init__.py.jinja
│   └── unit/
│       └── test_init.py.jinja
├── pyproject.toml.jinja         # Project configuration (templated)
├── README.md.jinja              # Project README (templated)
├── Makefile.jinja               # Development tasks (templated)
├── .copier-answers.yml.jinja    # Answers tracking (templated)
├── {{ _copier_conf.answers_file }}.jinja  # Answers file configuration
│
├── samples/                     # Example data files (EXCLUDED)
│   └── config-basic.yml         # Sample answers file
├── my_tests/                    # Test suite (EXCLUDED)
│   ├── conftest.py
│   ├── test_core_structure.py
│   ├── test_exclusions.py
│   └── test_conditional_sections.py
├── copier.yaml                  # Template configuration
└── README.md                    # Template documentation
```

## Excluded Directories

Files in these directories are **NOT** copied to generated projects:

- `samples/` - Example configuration and data files
- `my_tests/` - Template validation tests
- `.git/` - Git metadata (Copier default)
- `__pycache__/` - Python cache (Copier default)

Exclusion is configured in `copier.yaml` via the `_exclude` key.

## Templating Conventions

### Variable Interpolation

Use double-brace syntax for Jinja2 variables:

```jinja
Project: {{ project_name }}
Author: {{ author_name }}
Python: {{ python_version }}
```

### Conditional Sections

Use `_if_` prefix to conditionally include files:

```
file_name_if_condition.py.jinja
```

This file is only included when the condition evaluates to `true`.

### File Extensions

- `.jinja` - Files that require template rendering
- No extension - Static files copied as-is

Example:
```
README.md.jinja       # Rendered with Jinja2
LICENSE               # Copied without processing
```

## Testing

The template includes comprehensive tests in `my_tests/`:

| Test | Purpose |
|------|---------|
| `test_core_structure.py` | Validates project structure, required files, and directories |
| `test_exclusions.py` | Ensures excluded files aren't rendered in generated projects |
| `test_conditional_sections.py` | Tests conditional rendering based on configuration |

### Test Fixtures

Defined in `my_tests/conftest.py`:

- **Session-scoped fixtures**: Generate test projects once per session, reused across tests
- **Module-scoped wrappers**: Provide clean API with performance optimizations
- **Read-only operations**: All tests are non-mutating to enable fixture reuse

## Variable Types

Variables are defined in `copier.yaml` with type hints:

- **String**: Simple text values
- **Boolean**: Yes/No choices
- **Choice**: Dropdown selection from predefined options
- **Integer**: Numeric values
- **Float**: Decimal values

## Answer Files

### `.copier-answers.yml`

Auto-maintained file created in generated projects. Used for:
- Tracking user responses
- Enabling future template updates via `copier update`
- Never manually edited

### Sample Configuration

`samples/config-basic.yml` provides:
- Example variable values
- Used with `copier copy --data-file` for non-interactive generation
- Excluded from generated projects

## Best Practices

1. **Always use relative paths** in template files
2. **Keep templates DRY**: Use Jinja2 includes for shared content
3. **Test conditionals thoroughly**: Edge cases matter
4. **Document variables**: Include helpful descriptions in `copier.yaml`
5. **Version templates**: Use Git tags for reproducible generations
6. **Commit before testing**: Copier uses Git to detect files
7. **Keep exclusions updated**: Remove deprecated files from templates

## Common Tasks

### Add a New Template Variable

1. Add question in `copier.yaml`:
   ```yaml
   _questions:
     my_variable:
       type: str
       help: "Description of this variable"
   ```

2. Use in template files:
   ```jinja
   {{ my_variable }}
   ```

3. Add test case in `my_tests/`

### Create a Conditional File

1. Rename file with `_if_` prefix:
   ```
   optional_file_if_include_feature.py.jinja
   ```

2. Define condition in `copier.yaml`

3. Add test to `test_conditional_sections.py`

### Update Generated Projects

Users can sync with template changes:
```bash
copier update --answers-file .copier-answers.yml
```

## References

- [Copier Documentation](https://copier.readthedocs.io/en/stable/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Python Packaging Guide](https://packaging.python.org/)
