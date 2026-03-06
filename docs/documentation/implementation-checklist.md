# Implementation Checklist

ASP (Agentic Services Protocol) adds live-service transactions on top of UCP — discovery, catalogs, fulfillment, tracking, and personalization. Two sides implement it: **marketplaces** expose the APIs, **agents** consume them. The core protocol is domain-agnostic; optional domain profiles add vertical-specific fields.

---

## Marketplace Side

You run a marketplace with merchants. Build the following so agents can discover and transact with your merchants.

### Discovery

- Expose `/.well-known/asp` returning your discovery profile — protocol version, REST/MCP endpoints, and declared capabilities
- Implement `POST /discovery/search` — accept a `provider_filter` (location required; category, rating, availability, price level, free-text query optional), `sort_by`, `sort_order`, `page`, `page_size`; return paginated `providers[]`
- Each provider must include: `id`, `name`, `category`, `rating`, `estimated_service_minutes`, `service_fee_cents`, `minimum_order_cents`, `price_level`, `is_open_now`, `image`, `address`, `is_promoted`, and `tags`; optionally `rating_count`, `images`, `operating_hours`, `next_opens_at`

### Catalog

- Implement `GET /catalog/{provider_id}/catalog` returning a `service_catalog`
- Structure: catalog → sections → items → modifier groups → options
- Each item: `id`, `title`, `price_cents`, `is_available`; optional `description`, `image`
- Each modifier group: `id`, `title`, `options[]`, `required` flag, `min_selections`, `max_selections`
- Each modifier option: `id`, `label`, `price_delta_cents`

### Checkout & Fulfillment

- Implement `POST /checkouts` — accept line items with per-item customizations (selected modifier option IDs, special instructions), fulfillment details (type, address, ASAP flag, instructions, fees breakdown, optional tip, optional scheduling), and optional loyalty discount (tier + discount percent)
- Implement `PATCH /checkouts/{checkout_id}` — allow updates before payment
- Implement `POST /checkouts/{checkout_id}/complete` — finalize with `payment_method`, return order confirmation
- Supported fulfillment types: `delivery`, `pickup`, `ride`, `booking`, `on_site`
- Include `fees[]` for itemized cost breakdown and optional `tip` for gratuity
- For scheduled fulfillment: `is_asap: false` + `scheduled_for` datetime; expose `available_time_slots` so agents can present options

### Order Tracking

- Implement `GET /orders/{order_id}/tracking` — return current `fulfillment_status` with status enum, `updated_at`, optional `estimated_service_minutes`, `agent_location`, `history[]`, `is_delayed`, `delay_minutes`
- Push status updates via webhook — POST a `status_update_event` to the agent on each transition: `accepted` → `in_progress` → `en_route` → `completed` / `cancelled`
- Include `history` array for full status timeline narration
- Set `is_delayed` and `delay_minutes` when orders run behind schedule

### Personalization

- Implement `GET /personalization/profile` — return user's `loyalty_tier`, `loyalty_points`, `order_history`, `preferred_categories`, `default_address`
- Implement `GET /personalization/promotions` — return promotions filtered by optional `provider_id` and `limit`

### Catalog: Reorder

- Implement `POST /catalog/reorder` — accept `order_id` and `provider_id`, return current availability and pricing for original items
- Include `unavailable_items[]` with `item_id`, `title`, and `reason` for items no longer available
- Support optional `scheduled_for` to schedule reorders

### Reviews

**Capability:** `dev.asp.services.reviews`

- Implement `POST /reviews` — accept `order_id`, `provider_id`, `rating`, optional `comment` and category `scores`
- Implement `GET /reviews/{provider_id}` — return paginated reviews with `average_rating` and `total_reviews`
- Support `page` and `page_size` for pagination (uses the shared `pagination` type)

### Auth & Errors

- All endpoints require Bearer token authentication
- Errors follow the shape: `{ error: { code, message, details? } }`

### Optional: MCP Transport

- Expose the same capabilities as MCP tools (JSON-RPC) for direct agent integration
- Implement resource subscriptions on `order://{order_id}/status` for live push updates

!!! tip "Domain Profile"
    If your marketplace operates in a specific vertical, also implement the relevant domain profile extensions. See the [addendum below](#domain-profile-addendum) and [Domain Profiles](../specification/domains.md) for full details.

---

## Agent Side

You're building an agent that helps users order food, book rides, or use other live services. Here's how to integrate with any ASP-compliant marketplace.

### Protocol Negotiation

- Fetch `/.well-known/asp` from the marketplace
- Parse the discovery profile: extract protocol version, endpoint URLs, and supported capabilities
- Only call endpoints for capabilities the marketplace declares

### Discovery

- Build a `provider_filter` — `location` is always required; add `category`, `is_open_now`, `min_rating`, `query` as relevant
- Use `sort_by` (e.g. `rating`, `distance`) and `sort_order` to rank results
- Use `page` and `page_size` for pagination; call `POST /discovery/search`, parse `providers[]`, surface results to the user
- Handle pagination via `has_more` / `total_results`
- Use `rating_count` alongside `rating` for confident recommendations: *"4.8 stars from 2,300 reviews"*
- Use `operating_hours` and `next_opens_at` to inform users when closed providers reopen

### Catalog Browsing

- Call `GET /catalog/{provider_id}/catalog` for the user's selected provider
- Parse the sections → items → modifier groups hierarchy
- Enforce modifier constraints: check `required`, respect `min_selections` / `max_selections`
- Calculate total price: `price_cents` + sum of selected `price_delta_cents` values

### Checkout

- Build a `fulfillment_checkout` body:
    - `line_items[]` — each with `item_id`, `quantity`, `modifiers[]` (selected option IDs), `special_instructions`
    - `fulfillment` — `type`, `address`, `is_asap`, `instructions`
    - `loyalty` (optional) — `loyalty_tier` + `loyalty_discount_percent` from user profile
- `POST /checkouts` → obtain `checkout_id`
- Optionally `PATCH /checkouts/{checkout_id}` to modify before payment
- `POST /checkouts/{checkout_id}/complete` with `payment_method` to finalize

### Order Tracking

- Poll `GET /orders/{order_id}/tracking` or receive webhook `status_update_event` pushes
- Map the status enum (`accepted`, `in_progress`, `en_route`, `completed`, `cancelled`) to user-friendly messages
- Use `estimated_service_minutes` for countdowns; display `agent_location` on a map if present
- Use `history[]` to narrate the full journey: *"Accepted at 7:01, picked up at 7:15"*
- Watch `is_delayed` / `delay_minutes` to proactively warn: *"Heads up, running about 10 minutes late"*
- After delivery, prompt for a review via `POST /reviews`

### Personalization

- Fetch `GET /personalization/profile` to pre-fill addresses, read loyalty tier, and personalize category filters
- Fetch `GET /personalization/promotions` to surface relevant deals
- Pass `loyalty_tier` and `loyalty_discount_percent` back into checkout to apply discounts

!!! tip "Domain Profile"
    When integrating with a vertical-specific marketplace, expect extra fields on catalog items and providers. See the [addendum below](#domain-profile-addendum) for what each profile adds.

---

## Domain Profile Addendum

Domain profiles are optional extensions that add vertical-specific fields. If the marketplace uses one, both sides need to handle the extra data.

| Profile | Extended Catalog Item Fields | Extended Provider Fields | Extra Fulfillment Fields |
|---|---|---|---|
| **Food Delivery** | `dietary_tags`, `calories`, `prep_time_minutes`, `tags`, `available_for_scheduling` | `cuisine_types`, `dietary_options`, `minimum_order_cents`, `accepts_scheduled_orders` | Granular statuses (10 mapping to 5 base), `dine_in` fulfillment, substitution preferences |
| **Ride Hailing** | `vehicle_category`, `max_passengers`, `max_luggage_pieces`, `vehicle_features`, `surge_multiplier`, `estimated_arrival_minutes`, `availableForScheduling` | `vehicle_categories`, `coverage_area` | `pickup_location`, `dropoff_location`, `estimated_distance_km`, `route_polyline` |
| **Travel** | `room_type`, `max_guests`, `amenities`, `cancellation_policy`, `price_per_night_cents`, `check_in_time`, `check_out_time` | `accommodation_type`, `star_rating`, `amenities`, `total_units` | `check_in_date`, `check_out_date`, `guests`, `special_requests`, `confirmation_code` |

Each profile also constrains `service_categories` and `fulfillment_types` to a fixed enum, and maps abstract fulfillment statuses to domain-specific meanings. See [Domain Profiles](../specification/domains.md) for the full specification.

---

## Quick Reference: Endpoints

| Method | Path | Capability | Description |
|---|---|---|---|
| `GET` | `/.well-known/asp` | — | Discovery profile |
| `POST` | `/discovery/search` | discovery | Search providers by filters |
| `GET` | `/catalog/{provider_id}/catalog` | catalog | Full catalog for a provider |
| `POST` | `/checkouts` | fulfillment | Create checkout |
| `PATCH` | `/checkouts/{checkout_id}` | fulfillment | Update checkout |
| `POST` | `/checkouts/{checkout_id}/complete` | fulfillment | Complete checkout |
| `GET` | `/orders/{order_id}/tracking` | order_tracking | Current fulfillment status |
| `POST` | *(webhook)* | order_tracking | Status update push |
| `GET` | `/personalization/profile` | personalization | User profile |
| `GET` | `/personalization/promotions` | personalization | Promotions list |
| `POST` | `/catalog/reorder` | catalog | Reorder from previous order |
| `POST` | `/reviews` | reviews | Submit a review |
| `GET` | `/reviews/{provider_id}` | reviews | Get provider reviews |
