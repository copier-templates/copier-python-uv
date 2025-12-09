# Internal template development Makefile (NOT copied to generated projects)
# Provides conveniences for running the template validation tests.

PYTHON ?= uv run

.PHONY: help clean check install test

help: ## Display available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

check:
	@for tools in "uv pre-commit"; do \
		if ! command -v $$tools >/dev/null 2>&1; then \
			echo "Error: '$$tools' is not installed. Please install it first." >&2; \
			exit 1; \
		fi; \
	done

install: check ## Install development dependencies (copier, pytest)
	@uv sync --all-extras
	@pre-commit install

# Run internal validation tests, use environment variable EXTRA_PYTEST_ARGS to pass additional args.
test: clean install ## Run internal template validation tests
	@$(PYTHON) pytest -v my_tests $$EXTRA_PYTEST_ARGS || (echo "\nHint: run 'make install' first to install copier & pytest" >&2; exit 1)

clean:
	@rm -rf .{pytest_cache,ruff_cache}
	@find . -type d -name "__pycache__" -exec rm -rf {} +
