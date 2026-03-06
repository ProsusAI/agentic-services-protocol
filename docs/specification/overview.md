# Specification Overview

ASP defines **4 capabilities** and **3 extensions** that together cover the full transaction lifecycle for live services, incorporating UCP for cart, checkout, and payment.

## Protocol Components

### Capabilities (standalone)

| Capability | Identifier | Purpose |
|---|---|---|
| Discovery | `dev.asp.services.discovery` | Find providers by location, category, rating, availability |
| Catalog | `dev.asp.services.catalog` | Browse catalogs with sections, items, modifiers; reorder from history |
| Personalization | `dev.asp.services.personalization` | User profiles, order history, promotions |
| Reviews | `dev.asp.services.reviews` | Submit and retrieve post-service reviews and ratings |

### Extensions (compose on UCP)

| Extension | Identifier | Extends | Purpose |
|---|---|---|---|
| Fulfillment | `dev.asp.services.fulfillment` | `dev.ucp.shopping.checkout` | Fulfillment types, item customization, loyalty |
| Order Tracking | `dev.asp.services.order_tracking` | `dev.ucp.shopping.order` | Status progression, ETA, webhooks |
| Live Streaming | `dev.asp.services.streaming` | `dev.asp.services.order_tracking` | Continuous WebSocket location tracking |

## Transaction Flow

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant MP as Marketplace

    rect rgb(219, 228, 255)
    Note over Agent,MP: 1. Discovery
    Agent->>MP: POST /discovery/search {filters}
    MP-->>Agent: providers[], total_results, has_more
    end

    rect rgb(219, 228, 255)
    Note over Agent,MP: 2. Catalog
    Agent->>MP: GET /catalog/{provider_id}/catalog
    MP-->>Agent: sections[], items[], modifiers[]
    end

    rect rgb(229, 219, 255)
    Note over Agent,MP: 3. Checkout (UCP + ASP Fulfillment Extension)
    Agent->>MP: POST /checkouts {items, fulfillment, loyalty}
    MP-->>Agent: checkout confirmation
    end

    rect rgb(255, 216, 168)
    Note over Agent,MP: 4. Payment (UCP)
    Agent->>MP: POST /checkouts/{id}/complete
    MP-->>Agent: order confirmation
    end

    rect rgb(178, 242, 187)
    Note over Agent,MP: 5. Order Tracking (Push)
    MP-->>Agent: webhook: status → accepted
    MP-->>Agent: webhook: status → in_progress
    MP-->>Agent: webhook: status → en_route
    end

    rect rgb(178, 242, 187)
    Note over Agent,MP: 6. Live Streaming (WebSocket)
    Agent->>MP: ws: subscribe to order tracking
    loop Every 3-5 seconds
        MP-->>Agent: ws: location_update {lat, lng, ETA}
    end
    MP-->>Agent: ws: status_changed → completed
    end

    rect rgb(255, 236, 179)
    Note over Agent,MP: 7. Reviews
    Agent->>MP: POST /reviews {rating, comment, scores}
    MP-->>Agent: review confirmation
    end
```

## Schema Files

All schemas live in `source/schemas/`:

- `asp.json`, `capability.json` — Meta schemas
- `services/shared/` — Shared types (money, postal_address, image)
- `services/types/` — Domain types (provider, catalog_item, fulfillment_status, etc.)
- `services/discovery.json` — Discovery capability
- `services/catalog.json` — Catalog capability
- `services/fulfillment.json` — Fulfillment extension
- `services/order_tracking.json` — Order tracking extension
- `services/streaming.json` — Live streaming extension
- `services/personalization.json` — Personalization capability
- `services/reviews.json` — Reviews capability
- `services/shared/pagination.json` — Shared pagination type

Published versions are generated to `spec/schemas/` via `python generate_schemas.py`.

## Domain Profiles

Optional vertical-specific schemas live in `source/schemas/domains/`:

- `food_delivery/` — Cuisine types, dietary restrictions, food-specific provider extensions
- `ride_hailing/` — Vehicle categories, ride fulfillment with pickup/dropoff
- `travel/` — Accommodation categories, booking fulfillment with check-in/out

Domain profiles use `allOf` to extend core types for a specific vertical. They are reference examples, not required by the protocol.
