# Contributing to ASP

Thank you for your interest in contributing to the Agentic Services Protocol.

## Getting started

```bash
pip install -e ".[dev]"
npm install
python validate_specs.py
```

## Workflow

1. Fork the repository and create a feature branch from `main`
2. Make your changes
3. Run validation (see below)
4. Open a pull request against `main`

For anything beyond a typo fix — new fields, new capabilities, constraint changes — please open a GitHub issue first so maintainers can discuss the design before you write code.

## Schema changes

All schema work happens in `source/schemas/`. Never edit `spec/` or `generated/` directly — they're derived.

After changing any file in `source/schemas/`:

```bash
python validate_specs.py              # validate all schemas
python generate_schemas.py            # regenerate spec/
npm run generate:types                # regenerate TypeScript types
npm run generate:pydantic             # regenerate Python models
```

Commit the regenerated `spec/` and `generated/` output alongside your source changes.

## Adding a new domain profile

Domain profiles live in `source/schemas/domains/<vertical>/`. Open a proposal issue before starting, then:

1. Create `source/schemas/domains/<vertical>/` with a `domain_profile.json`
2. Follow the conventions in the [Schema Authoring Guide](docs/documentation/schema-authoring.md)
3. Run `validate_specs.py` and `generate_schemas.py`
4. Add docs in `docs/specification/` and update `docs/specification/overview.md`

## Running tests

```bash
python validate_specs.py              # schema validation
mkdocs build --strict                 # docs build (pip install -e ".[docs]" first)
ruff check . && ruff format --check . # Python lint
npx biome check .                     # JSON formatting
```

## Commit convention

PR titles follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.

## Review process

All PRs require at least one maintainer approval. Schema changes to capabilities or extensions require an approved issue first. See [MAINTAINERS.md](MAINTAINERS.md).
