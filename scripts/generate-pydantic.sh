#!/usr/bin/env bash
# Generate Pydantic v2 models from the bundled ASP schema.
# Run after bundle-schemas.mjs (e.g. via npm run generate:pydantic).
# Requires: pip install datamodel-code-generator

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
BUNDLE_JSON="${ROOT_DIR}/generated/schemas_bundle.json"
OUT_DIR="${ROOT_DIR}/generated/python"

if [[ ! -f "$BUNDLE_JSON" ]]; then
  echo "Missing $BUNDLE_JSON — run: npm run generate:pydantic (which runs bundle first)" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

CODEGEN_ARGS=(
  --input "$BUNDLE_JSON"
  --input-file-type jsonschema
  --output "$OUT_DIR/models.py"
  --output-model-type pydantic_v2.BaseModel
  --target-python-version 3.11
)

if command -v datamodel-codegen &>/dev/null; then
  datamodel-codegen "${CODEGEN_ARGS[@]}"
  echo "Pydantic models written to $OUT_DIR/models.py"
elif python3 -c "import datamodel_code_generator" 2>/dev/null; then
  python3 -m datamodel_code_generator "${CODEGEN_ARGS[@]}"
  echo "Pydantic models written to $OUT_DIR/models.py"
else
  echo "SKIP: datamodel-code-generator not installed. Install with: pip install datamodel-code-generator" >&2
  exit 1
fi
