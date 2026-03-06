# Extended Catalog

**Capability:** `dev.asp.services.catalog`
**Version:** `2026-02-19`
**Schema:** [`catalog.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/catalog.json)

## Purpose

Retrieves a provider's complete catalog with hierarchical sections, items with pricing, and modifier groups for customization.

## Endpoint

```
GET /catalog/{provider_id}/catalog
```

## Response Structure

A catalog is organized as:

```
Service Catalog
├── provider_id, provider_name
└── sections[]
    ├── id, title
    └── items[]
        ├── id, title, description, price_cents, images[]
        └── modifier_groups[]
            ├── id, title, required, min/max_selections
            └── options[]
                ├── id, label, price_delta_cents
```

## Schema: Catalog Item

{{ schema_fields("spec/schemas/services/types/catalog_item.json") }}

## Schema: Modifier Group

{{ schema_fields("spec/schemas/services/types/modifier_group.json") }}

## Schema: Modifier Option

{{ schema_fields("spec/schemas/services/types/modifier_option.json") }}

## Example

```json
{
  "provider_id": "pizza-palace",
  "provider_name": "Pizza Palace",
  "sections": [
    {
      "id": "pizzas",
      "title": "Pizzas",
      "items": [
        {
          "id": "margherita",
          "title": "Margherita Pizza",
          "description": "Classic tomato, mozzarella, and basil",
          "price_cents": 1299,
          "images": [
            { "url": "https://img.example.com/margherita.jpg", "type": "thumbnail", "alt_text": "Margherita Pizza" }
          ],
          "modifier_groups": [
            {
              "id": "size",
              "title": "Size",
              "required": true,
              "min_selections": 1,
              "max_selections": 1,
              "options": [
                { "id": "small", "label": "Small", "price_delta_cents": 0 },
                { "id": "medium", "label": "Medium", "price_delta_cents": 300 },
                { "id": "large", "label": "Large", "price_delta_cents": 500 }
              ]
            },
            {
              "id": "extras",
              "title": "Extras",
              "required": false,
              "max_selections": 3,
              "options": [
                { "id": "extra-cheese", "label": "Extra Cheese", "price_delta_cents": 150 },
                { "id": "mushrooms", "label": "Mushrooms", "price_delta_cents": 100 }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Availability

Items include an `is_available` flag (default `true`). Unavailable items should be displayed as greyed-out or hidden, depending on the agent's UX.

## Reorder

Agents can reorder from a previous order, receiving current availability and pricing for the original items.

### Endpoint

```
POST /catalog/reorder
```

### Request

| Field | Type | Required | Description |
|---|---|---|---|
| `order_id` | string | Yes | The previous order to reorder from |
| `provider_id` | string | Yes | The provider of the original order |
| `scheduled_for` | datetime | No | Optional scheduled time (integrates with `available_for_scheduling`) |

### Response

| Field | Type | Description |
|---|---|---|
| `items` | array of CatalogItem | Items from the original order with current availability and pricing |
| `unavailable_items` | array | Items no longer available, each with `item_id`, `title`, and `reason` |

### Example

```json
{
  "order_id": "order-98765",
  "provider_id": "pizza-palace"
}
```

Response:

```json
{
  "items": [
    {
      "id": "margherita",
      "title": "Margherita Pizza",
      "price_cents": 1299,
      "is_available": true
    }
  ],
  "unavailable_items": [
    {
      "item_id": "tiramisu",
      "title": "Tiramisu",
      "reason": "Out of stock"
    }
  ]
}
```
