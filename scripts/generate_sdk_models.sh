#!/bin/bash
# Generate SDK models from spec/ schemas.
#
# Python: Pydantic v2 models via datamodel-codegen
# TypeScript: Interfaces via json-schema-to-typescript

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Generating Python Pydantic models ==="
if command -v datamodel-codegen &>/dev/null; then
  datamodel-codegen \
    --input "$ROOT_DIR/spec/schemas/" \
    --input-file-type jsonschema \
    --output "$ROOT_DIR/generated/python/" \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.11
  echo "Python models written to generated/python/"
else
  echo "SKIP: datamodel-codegen not installed (pip install datamodel-code-generator)"
fi

echo ""
echo "=== Generating TypeScript types ==="
if command -v npx &>/dev/null; then
  npx json-schema-to-typescript \
    --input "$ROOT_DIR/spec/schemas/" \
    --output "$ROOT_DIR/generated/types.ts"
  echo "TypeScript types written to generated/types.ts"
else
  echo "SKIP: npx not available"
fi

echo ""
echo "Done."
