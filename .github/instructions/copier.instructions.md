---
applyTo: "**"
---

# Copier Documentation

Quick reference for the `copier` project templating tool.

## Documentation Links
- **Main Docs:** https://copier.readthedocs.io/en/stable/
- **Creating Templates:** https://copier.readthedocs.io/en/stable/creating/
- **Configuration:** https://copier.readthedocs.io/en/stable/configuring/
- **Generating Projects:** https://copier.readthedocs.io/en/stable/generating/
- **Updating Projects:** https://copier.readthedocs.io/en/stable/updating/
- **Settings:** https://copier.readthedocs.io/en/stable/settings/
- **FAQ:** https://copier.readthedocs.io/en/stable/faq/

# LICENSE file
- The type of LICENSEs supported can be found here: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#choosing-the-right-license

## Key Concepts
- Use `copier copy` to generate projects from templates
- Use `copier update` to sync existing projects with template changes
- Templates use Jinja2 for dynamic content
- Configuration is defined in `copier.yml` or `copier.yaml`

## Common Tasks
- Template creation: Define questions and file structure in `copier.yml`
- Variable interpolation: Use `{{ variable }}` syntax

## Critical: Git Repository Requirement for Testing

**Copier only includes Git-tracked files when using `vcs_ref="HEAD"`**

When testing Copier templates locally with `vcs_ref="HEAD"`:
- Copier uses Git to determine which files to include in the template
- **Uncommitted files in the working directory are IGNORED** by Copier
- This means:
  - Template files must be committed to Git before running tests
  - Tests will fail if template files are not tracked by Git
  - Template rendering will be incomplete or fail with missing files

### Why This Matters for Template Development

By default, Copier copies from the latest Git tag (PEP 440 sorted). When using `vcs_ref="HEAD"` for development:
1. Copier clones/uses the template from Git
2. Only Git-tracked files are included in the operation
3. Untracked or uncommitted files are silently excluded
4. Template rendering fails because expected files are missing

# IMPORTANT

**Action Items for Copilot before running tests**
- When working with Copier templates, before running tests ensure all template files are staged and committed in Git
- If tests fail with "file not found" errors, check `git status` first, and commit any untracked changes
- Use module-scoped pytest fixtures to reuse generated projects and improve test performance
