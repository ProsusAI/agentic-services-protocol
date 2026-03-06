# Changelog

All notable changes to the Agentic Services Protocol will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/) for tooling and [date-based versioning](https://calver.org/) (`YYYY-MM-DD`) for schemas.

## [Unreleased]

## [1.0.0] — 2026-03-03

Initial public release of the Agentic Services Protocol.

### Capabilities

- **Discovery** — Search providers by location, category, rating, and availability
- **Catalog** — Structured catalogs with sections, items, modifier groups, and dietary/tag metadata
- **Personalization** — User profiles, order history, preferred categories, and promotions
- **Reviews** — Submit and retrieve provider reviews with category scores

### Extensions (UCP)

- **Fulfillment** — Multi-type fulfillment (delivery, pickup, dine-in), per-item customization, loyalty discounts; extends UCP Checkout
- **Order Tracking** — Status progression, ETA updates, webhook push model; extends UCP Order
- **Live Streaming** — Real-time order status updates via WebSocket; extends Order Tracking

### Domain Profiles

- **Food Delivery** — Cuisine types, dietary restrictions, restaurant-specific modifiers
- **Ride-Hailing** — Vehicle categories, ride fulfillment types, driver tracking
- **Travel** — Accommodation categories, booking fulfillment, check-in/check-out

### Transport Bindings

- REST / OpenAPI
- MCP (LLM tool use) / OpenRPC
- A2A (agent delegation) / Agent Card
- WebSocket (live streaming) / AsyncAPI

### Tooling

- `validate_specs.py` — JSON Schema validation for all source and spec schemas
- `generate_schemas.py` — Source-to-spec schema generation pipeline
- TypeScript type generation (`npm run generate:types`)
- Python Pydantic model generation (`npm run generate:pydantic`)
- MkDocs documentation site with interactive schema reference
