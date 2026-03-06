# Agentic Services Protocol (ASP)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**An open protocol for end-to-end agent-to-service transactions — food delivery, ride-hailing, travel, and on-demand services.**

ASP defines the full transaction lifecycle for live service marketplaces: provider discovery, catalog browsing, checkout, real-time order tracking, and post-service reviews. For checkout and payment, ASP is compatible with [UCP](https://developers.google.com/merchant/ucp), extending its schemas for live-service needs like fulfillment types, fees, and tips.

## Overview

| Capability | Type | What it does |
|---|---|---|
| **Discovery** | Capability | Search providers by location, category, rating, availability |
| **Catalog** | Capability | Catalogs with sections, items, modifier groups |
| **Fulfillment** | UCP-compatible | Multi-type fulfillment, per-item customization, loyalty discounts |
| **Order Tracking** | UCP-compatible | Status progression, ETA updates, webhook push model |
| **Live Streaming** | Extension | Real-time WebSocket location tracking and status events |
| **Personalization** | Capability | User profiles, order history, preferred categories, promotions |
| **Reviews** | Capability | Post-service ratings with category scores and comments |

## Quick Start

```bash
# Install Python dependencies
pip install -e ".[dev]"

# Install Node dependencies
npm install

# Validate all schemas
python validate_specs.py

# Generate spec/ from source/
python generate_schemas.py

# Generate TypeScript types
npm run generate:types

# Generate Pydantic models (bundles schemas, then runs datamodel-code-generator)
npm run generate:pydantic

# Build documentation
pip install -e ".[docs]"
mkdocs build
```

## Architecture

```
source/schemas/     Source-of-truth schemas
       │
       ▼
generate_schemas.py  Copies and formats schemas for publication
       │
       ▼
spec/schemas/       Published schemas (committed, consumed by SDKs)
       │
       ▼
generated/          Auto-generated SDK types (TypeScript, Python)

spec/schemas/domains/  Optional vertical-specific domain profiles
  food_delivery/       Cuisine types, dietary restrictions
  ride_hailing/        Vehicle categories, ride fulfillment
  travel/              Accommodation categories, booking fulfillment
```

## Documentation

- [Core Concepts](docs/documentation/core-concepts.md) — Capabilities vs Extensions, domain profiles, versioning, transport bindings
- **Specification:**
  - [Discovery](docs/specification/discovery.md)
  - [Catalog](docs/specification/catalog.md)
  - [Checkout & Fulfillment](docs/specification/fulfillment.md)
  - [Order Tracking](docs/specification/order-tracking.md)
  - [Personalization](docs/specification/personalization.md)
- [Schema Authoring Guide](docs/documentation/schema-authoring.md)
- [Roadmap](docs/documentation/roadmap.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Schema changes require regenerating `spec/` and committing the output.

## License

Apache 2.0 — see [LICENSE](LICENSE).
