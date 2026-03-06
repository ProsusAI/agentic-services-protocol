"""Validate all ASP schemas and specs.

Checks:
- All JSON files are valid JSON
- All JSON Schema files have required metadata ($schema, $id, title, description)
- Capability schemas have name and version
- Type/shared schemas do NOT have name or version
- All $ref relative references resolve to existing files
- All $id values use relative ./ prefix convention
- OpenAPI spec is valid YAML

Usage: python validate_specs.py
"""

import json
import sys
from pathlib import Path

SCHEMA_DIRS = [Path("source/schemas"), Path("spec/schemas")]
SERVICE_DIRS = [Path("source/services"), Path("spec/services")]

# Capability schemas live directly under services/ (not in types/ or shared/)
CAPABILITY_PREFIXES = {
    "discovery",
    "catalog",
    "fulfillment",
    "order_tracking",
    "personalization",
    "streaming",
    "reviews",
}

errors: list[str] = []


def error(msg: str):
    errors.append(msg)
    print(f"  FAIL  {msg}")


def validate_json_files():
    """Validate all JSON files parse correctly."""
    print("\n--- Validating JSON files ---")
    for schema_dir in SCHEMA_DIRS:
        if not schema_dir.exists():
            continue
        for f in sorted(schema_dir.rglob("*.json")):
            try:
                with open(f) as fh:
                    json.load(fh)
            except json.JSONDecodeError as e:
                error(f"{f}: invalid JSON — {e}")


def validate_schema_metadata():
    """Validate schema metadata fields."""
    print("\n--- Validating schema metadata ---")
    for schema_dir in SCHEMA_DIRS:
        if not schema_dir.exists():
            continue
        for f in sorted(schema_dir.rglob("*.json")):
            with open(f) as fh:
                data = json.load(fh)

            for field in ["$schema", "$id", "title", "description"]:
                if field not in data:
                    error(f"{f}: missing {field}")

            # Check $id convention — all schemas use relative ./ prefix
            if "$id" in data:
                id_val = data["$id"]
                if not id_val.startswith("./"):
                    error(f"{f}: $id should use relative ./ prefix, got: {id_val}")

            # Capability vs type check
            stem = f.stem
            is_capability = stem in CAPABILITY_PREFIXES and "types" not in str(f) and "shared" not in str(f)

            if is_capability:
                if "name" not in data:
                    error(f"{f}: capability schema missing 'name'")
                if "version" not in data:
                    error(f"{f}: capability schema missing 'version'")
            else:
                # Meta schemas (asp.json, capability.json) are allowed name/version
                if f.stem not in ("asp", "capability"):
                    if "name" in data:
                        error(f"{f}: type/shared schema should NOT have 'name'")
                    if "version" in data:
                        error(f"{f}: type/shared schema should NOT have 'version'")


def validate_refs():
    """Validate all $ref relative references resolve to existing files."""
    print("\n--- Validating $ref references ---")
    for schema_dir in SCHEMA_DIRS:
        if not schema_dir.exists():
            continue

        def collect_refs(obj, file_path):
            if isinstance(obj, dict):
                if "$ref" in obj:
                    ref = obj["$ref"]
                    base_ref = ref.split("#")[0]
                    # Skip fragment-only refs (e.g. #/properties/foo)
                    if not base_ref:
                        pass
                    elif base_ref.startswith("./") or base_ref.startswith("../"):
                        # Resolve relative path from the file's directory
                        target = (file_path.parent / base_ref).resolve()
                        if not target.exists():
                            error(f"{file_path}: unresolved $ref → {ref} (expected {target})")
                    elif base_ref.startswith("https://ucp.dev/"):
                        pass  # External UCP references are expected
                    elif base_ref.startswith("https://"):
                        error(f"{file_path}: $ref should use relative path, not URL: {ref}")
                for v in obj.values():
                    collect_refs(v, file_path)
            elif isinstance(obj, list):
                for item in obj:
                    collect_refs(item, file_path)

        for f in sorted(schema_dir.rglob("*.json")):
            with open(f) as fh:
                data = json.load(fh)
            collect_refs(data, f)


def validate_service_json():
    """Validate JSON files in service directories."""
    print("\n--- Validating service JSON files ---")
    for service_dir in SERVICE_DIRS:
        if not service_dir.exists():
            continue
        for f in sorted(service_dir.rglob("*.json")):
            try:
                with open(f) as fh:
                    json.load(fh)
                print(f"  OK  {f}")
            except json.JSONDecodeError as e:
                error(f"{f}: invalid JSON — {e}")


def validate_openapi():
    """Validate OpenAPI spec is valid YAML."""
    print("\n--- Validating OpenAPI spec ---")
    for service_dir in SERVICE_DIRS:
        for f in sorted(service_dir.rglob("*.yaml")) if service_dir.exists() else []:
            try:
                import yaml

                with open(f) as fh:
                    yaml.safe_load(fh)
                print(f"  OK  {f}")
            except ImportError:
                print(f"  SKIP  {f} (pyyaml not installed)")
            except Exception as e:
                error(f"{f}: invalid YAML — {e}")


def main():
    validate_json_files()
    validate_schema_metadata()
    validate_refs()
    validate_service_json()
    validate_openapi()

    print(f"\n{'=' * 50}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
