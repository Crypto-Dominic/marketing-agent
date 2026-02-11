#!/usr/bin/env bash
# Non-interactive content generation script.
# Usage:
#   ./scripts/generate.sh "Your prompt here"
#   ./scripts/generate.sh "Your prompt here" output/result.md
#
# Cron example (every Monday at 9am):
#   0 9 * * 1 cd /path/to/marketing-agent && ./scripts/generate.sh "Draft weekly social media posts" output/weekly.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load .env if it exists
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

PROMPT="${1:?Usage: $0 \"prompt\" [output_file]}"
OUTPUT="${2:-}"

cd "$PROJECT_DIR"

if [ -n "$OUTPUT" ]; then
    python -m src.cli --prompt "$PROMPT" --output "$OUTPUT"
else
    python -m src.cli --prompt "$PROMPT"
fi
