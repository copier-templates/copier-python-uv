#!/usr/bin/env bash
# Sync GitHub issue template files
# Copies .jinja files from .github/ISSUE_TEMPLATE to corresponding .yml files
# Jinja files are used for templating by copier, while .yml files are the actual issue templates used by GitHub for this repository
set -e

TEMPLATES_DIR=".github/ISSUE_TEMPLATE"
SYNC_COUNT=0
FAIL_COUNT=0

if [[ ! -d "$TEMPLATES_DIR" ]]; then
    echo "Error: $TEMPLATES_DIR directory not found"
    exit 1
fi

# Find all .jinja files in the templates directory
while IFS= read -r -d '' jinja_file; do
    # Get the base name without .jinja extension
    yml_file="${jinja_file%.jinja}"

    if [[ "$yml_file" == "$jinja_file" ]]; then
        # File doesn't end with .jinja, skip it
        continue
    fi

    if cp "$jinja_file" "$yml_file"; then
        echo "✓ Synced: $jinja_file → $yml_file"
        SYNC_COUNT=$((SYNC_COUNT + 1))
    else
        echo "✗ Failed to sync: $jinja_file → $yml_file" >&2
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done < <(find "$TEMPLATES_DIR" -name "*.jinja" -print0)

echo ""
echo "Summary: $SYNC_COUNT file(s) synced"

if [[ $FAIL_COUNT -gt 0 ]]; then
    echo "Error: $FAIL_COUNT file(s) failed to sync" >&2
    exit 1
fi

exit 0
