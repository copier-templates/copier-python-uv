# Internal template development Makefile (NOT copied to generated projects)
# Provides conveniences for running the template validation tests.

PYTHON ?= uv run

.PHONY: help test install clean

help: ## Display available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install development dependencies (copier, pytest)
	@if [ ! -d ".venv" ]; then \
		uv venv; \
	fi
	@uv sync --dev
	@pre-commit install


# Run internal validation tests
# Use environment variable EXTRA_PYTEST_ARGS to pass additional args.
test: clean install ## Run internal template validation tests
	@$(PYTHON) pytest -v my_tests $$EXTRA_PYTEST_ARGS || (echo "\nHint: run 'make install' first to install copier & pytest" >&2; exit 1)

clean:
	@rm -rf .{pytest_cache,ruff_cache}
	@find . -type d -name "__pycache__" -exec rm -rf {} +
