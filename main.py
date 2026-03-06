"""MkDocs macros plugin for ASP documentation.

Provides Jinja2 macros that auto-generate Markdown tables from JSON schemas.
"""

import json
from pathlib import Path


def define_env(env):
    """Define MkDocs macros."""

    @env.macro
    def schema_fields(schema_path: str, schema_object_path: str | None = None) -> str:
        """Generate a Markdown table of properties from a JSON schema file.

        Usage in docs: {{ schema_fields("spec/schemas/services/types/provider.json") }}
        """
        path = Path(schema_path)
        if not path.exists():
            return f"*Schema not found: `{schema_path}`*"

        def _resolve_pointer(obj: dict, pointer: str):
            """Resolve either dot-path ($defs.foo) or JSON pointer (/$defs/foo)."""
            if pointer.startswith("/"):
                parts = [p for p in pointer.strip("/").split("/") if p]
            else:
                parts = [p for p in pointer.split(".") if p]

            current = obj
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            return current

        def _load_json_file(file_path: Path):
            with open(file_path) as f:
                return json.load(f)

        def _resolve_ref(current_schema: dict, current_path: Path):
            """Resolve $ref from local schema files or internal fragments."""
            if "$ref" not in current_schema:
                return current_schema

            ref = current_schema["$ref"]
            ref_file, _, ref_fragment = ref.partition("#")

            # Internal reference within the same schema object.
            if not ref_file:
                target = _resolve_pointer(current_schema, ref_fragment or "/")
                return target if isinstance(target, dict) else current_schema

            target_path = (current_path.parent / ref_file).resolve()
            if not target_path.exists():
                return current_schema

            target_schema = _load_json_file(target_path)
            if ref_fragment:
                resolved = _resolve_pointer(target_schema, ref_fragment)
                if isinstance(resolved, dict):
                    return resolved
            return target_schema

        schema = _load_json_file(path)
        if schema_object_path:
            scoped = _resolve_pointer(schema, schema_object_path)
            if not isinstance(scoped, dict):
                return f"*Schema object path not found: `{schema_object_path}` in `{schema_path}`*"
            schema = scoped

        schema = _resolve_ref(schema, path)

        # Handle enum schemas
        if "enum" in schema and schema.get("type") == "string":
            values = ", ".join(f"`{v}`" for v in schema["enum"])
            return f"**Enum values:** {values}"

        props = schema.get("properties", {})
        if not props:
            return "*No properties defined.*"

        required = set(schema.get("required", []))

        rows = []
        rows.append("| Field | Type | Required | Description |")
        rows.append("|---|---|---|---|")

        for name, prop in props.items():
            # Determine type
            if "$ref" in prop:
                ref = prop["$ref"].split("/")[-1].replace(".json", "")
                type_str = f"[{ref}]"
            elif "type" in prop:
                type_str = prop["type"]
                if type_str == "array" and "items" in prop:
                    items = prop["items"]
                    if "$ref" in items:
                        item_ref = items["$ref"].split("/")[-1].replace(".json", "")
                        type_str = f"array\\<{item_ref}\\>"
                    elif "type" in items:
                        type_str = f"array\\<{items['type']}\\>"
            elif "const" in prop:
                type_str = f"const: `{prop['const']}`"
            else:
                type_str = "object"

            is_required = "Yes" if name in required else "No"
            description = prop.get("description", "")

            # Add enum values inline
            if "enum" in prop:
                values = ", ".join(f"`{v}`" for v in prop["enum"])
                description += f" Values: {values}"

            # Add default
            if "default" in prop:
                description += f" Default: `{prop['default']}`"

            rows.append(f"| `{name}` | {type_str} | {is_required} | {description} |")

        return "\n".join(rows)

    @env.macro
    def method_fields(openapi_path: str, operation_id: str) -> str:
        """Generate request/response docs for an OpenAPI operation.

        Usage: {{ method_fields("spec/services/live_services/openapi.yaml", "provider_search") }}
        """
        path = Path(openapi_path)
        if not path.exists():
            return f"*OpenAPI spec not found: `{openapi_path}`*"

        try:
            import yaml

            with open(path) as f:
                spec = yaml.safe_load(f)
        except ImportError:
            return "*pyyaml not installed*"

        # Find the operation
        for path_str, methods in spec.get("paths", {}).items():
            for method, op in methods.items():
                if isinstance(op, dict) and op.get("operationId") == operation_id:
                    rows = []
                    rows.append(f"**`{method.upper()} {path_str}`**")
                    rows.append("")
                    if op.get("summary"):
                        rows.append(f"*{op['summary']}*")
                        rows.append("")
                    if op.get("description"):
                        rows.append(op["description"])
                    return "\n".join(rows)

        return f"*Operation `{operation_id}` not found in `{openapi_path}`*"
