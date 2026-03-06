# Provider Discovery

**Capability:** `dev.asp.services.discovery`
**Version:** `2026-02-19`
**Schema:** [`discovery.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/discovery.json)

## Purpose

Enables agents to search for providers by location, category, rating, service time, price level, and availability. Returns structured provider objects that can be rendered as browsable carousels or lists.

## Endpoint

```
POST /discovery/search
```

## Request

The request body wraps a `provider_filter` object with optional sorting and pagination:

{{ schema_fields("spec/schemas/services/types/provider_filter.json") }}

### Sorting

| Field | Type | Description |
|---|---|---|
| `sort_by` | enum | `relevance` (default), `rating`, `distance`, `price_low`, `price_high`, `estimated_time`, `newest` |
| `sort_order` | enum | `asc` or `desc` (default) |

### Pagination

| Field | Type | Description |
|---|---|---|
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Results per page, 1–100 (default: 20) |

### Example

```json
{
  "filters": {
    "location": {
      "street_line_1": "123 Main St",
      "city": "San Francisco",
      "postal_code": "94105",
      "country_code": "US",
      "latitude": 37.7749,
      "longitude": -122.4194
    },
    "category": "italian",
    "is_open_now": true,
    "min_rating": 4.0,
    "max_service_minutes": 45
  },
  "sort_by": "rating",
  "sort_order": "desc",
  "page": 1,
  "page_size": 20
}
```

## Response

{{ schema_fields("spec/schemas/services/types/provider.json") }}

### Response Envelope

| Field | Type | Description |
|---|---|---|
| `providers` | array of Provider | Matching providers |
| `total_results` | integer | Total count of matches |
| `has_more` | boolean | Whether more pages exist |

### Example

```json
{
  "providers": [
    {
      "id": "pizza-palace",
      "name": "Pizza Palace",
      "category": "italian",
      "rating": 4.5,
      "rating_count": 2300,
      "estimated_service_minutes": 30,
      "service_fee_cents": 299,
      "price_level": "moderate",
      "is_open_now": true,
      "operating_hours": [
        { "day": "monday", "open_time": "11:00", "close_time": "22:00" },
        { "day": "tuesday", "open_time": "11:00", "close_time": "22:00" }
      ],
      "next_opens_at": "2026-02-28T11:00:00Z",
      "images": [
        { "url": "https://img.example.com/pizza-palace-thumb.jpg", "type": "thumbnail", "alt_text": "Pizza Palace" },
        { "url": "https://img.example.com/pizza-palace-banner.jpg", "type": "banner", "alt_text": "Pizza Palace storefront" }
      ]
    }
  ],
  "total_results": 1,
  "has_more": false
}
```

## Operating Hours

Providers include an optional `operating_hours` array (weekly schedule) and `next_opens_at` (datetime). When `is_open_now` is `false`, the agent can use `next_opens_at` to inform the user: *"Pizza Palace is closed right now — opens tomorrow at 11am."*

The `operating_hours` array contains one entry per day with `day`, `open_time`, and `close_time` in `HH:MM` format. Not all days need to be present — missing days imply the provider is closed that day.

## Image Types

Providers and catalog items support an `images` array where each image has a `type` field:

| Type | Use Case |
|---|---|
| `thumbnail` | Search result cards, compact lists |
| `banner` | Provider detail page header |
| `logo` | Brand identity, small icons |
| `hero` | Full-width featured placement |

Agents should select the appropriate image type based on the rendering context.

## Filter Semantics

- `location` is **required** — all other filters are optional
- `is_open_now: true` excludes providers that are currently closed
- `min_rating` is inclusive (4.0 matches providers rated 4.0+)
- `query` performs free-text search across provider name and category
- Filters are AND-combined: all specified criteria must match
- `sort_by` defaults to `relevance`; use `distance` or `rating` to re-rank results
- `page` and `page_size` control pagination; check `has_more` to know if another page exists
