# Schema Authoring Guide

How to contribute new schemas to ASP.

## Schema Categories

| Category | Location | Has `name`/`version`? | Purpose |
|---|---|---|---|
| Meta | `source/schemas/` | No | Protocol-level definitions (asp.json, capability.json) |
| Shared | `source/schemas/services/shared/` | No | Reusable types (money, address, image) |
| Type | `source/schemas/services/types/` | No | Domain types (provider, catalog_item, etc.) |
| Capability | `source/schemas/services/` | Yes | Standalone capabilities (discovery, catalog, personalization) |
| Extension | `source/schemas/services/` | Yes + `extends` | UCP schema extensions (fulfillment, order_tracking) |
| Domain Profile | `source/schemas/domains/<vertical>/` | No | Vertical-specific constraints and extensions |

## Required Metadata

Every schema file must include:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "./schemas/...",
  "title": "Human-Readable Title",
  "description": "What this schema represents."
}
```

Capability and extension schemas additionally require:

```json
{
  "name": "dev.asp.services.<name>",
  "version": "YYYY-MM-DD"
}
```

Extension schemas also require:

```json
{
  "extends": "dev.ucp.shopping.<capability>"
}
```

## Naming Conventions

- **Files**: `snake_case.json` (e.g. `catalog_item.json`, `fulfillment_status.json`)
- **Capability names**: `dev.asp.services.<name>` (reverse-domain)
- **Property names**: `snake_case` (e.g. `service_fee_cents`, `is_open_now`)
- **Enum values**: `snake_case` (e.g. `en_route`, `in_progress`)

## `$ref` Conventions

Use relative paths for all references:

```json
{ "$ref": "./services/types/provider.json" }
```

For `$defs` within the same file:

```json
{ "$ref": "#/$defs/search_request" }
```

## Adding a New Capability

1. Create type schemas in `source/schemas/services/types/`
2. Create the capability schema in `source/schemas/services/<name>.json` with `name` and `version`
3. Add `$defs` for request/response if the capability has endpoints
4. Add endpoints to the OpenAPI spec
5. Run `python generate_schemas.py` and `python validate_specs.py`
6. Add documentation in `docs/specification/<name>.md`
7. Update `docs/specification/overview.md` and `docs/specification/reference.md`

## Adding a New Extension

Same as above, but also:

1. Set `extends` to the UCP capability being extended
2. Use `allOf` to compose with the UCP schema
3. Document the composition in the spec page

## Adding a Domain Profile

1. Create a directory in `source/schemas/domains/<vertical>/`
2. Add schema files that use `allOf` to extend core types
3. Add a `README.md` documenting the mapping to core types
4. Domain profiles do not require `name`/`version` fields

## Generation

Running `python generate_schemas.py` copies and formats schemas from `source/schemas/` to `spec/schemas/` for publication. Always commit the `spec/` output alongside source changes.
