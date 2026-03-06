# Checkout & Fulfillment Extension

**Extension:** `dev.asp.services.fulfillment`
**Version:** `2026-02-19`
**Extends:** `dev.ucp.shopping.checkout`
**Schema:** [`fulfillment.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/fulfillment.json)

## Purpose

Adds fulfillment as a first-class type to UCP checkout, alongside per-item customization (special instructions, selected modifiers) and loyalty-tier discounts. Supports multiple fulfillment types: delivery, pickup, ride, booking, and on-site.

## Composition

This extension uses `allOf` to compose with the UCP checkout schema:

```json
{
  "allOf": [
    { "$ref": "https://ucp.dev/schemas/shopping/checkout.json" },
    {
      "properties": {
        "fulfillment": { "$ref": "fulfillment.json" },
        "line_items": [{ "allOf": ["ucp_line_item", "item_customization"] }],
        "loyalty": { "$ref": "loyalty_discount.json" }
      }
    }
  ]
}
```

Any valid UCP checkout remains valid. The fulfillment extension adds optional fields alongside.

## Schema: Fulfillment

{{ schema_fields("spec/schemas/services/types/fulfillment.json") }}

### Fee Breakdown

The `fees` array itemizes charges beyond the base price, letting agents explain cost breakdowns:

| Field | Type | Description |
|---|---|---|
| `type` | enum | `delivery`, `service`, `small_order`, `platform`, `surge`, `booking`, `bag` |
| `label` | string | Display name, e.g. "Delivery fee" |
| `amount_cents` | integer | Fee amount in minor currency units |

Domain profiles can define which fee types are common for their vertical (e.g. food: `delivery`, `bag`, `small_order`; rides: `surge`; travel: `booking`).

### Tipping

The optional `tip` object supports gratuity:

| Field | Type | Description |
|---|---|---|
| `type` | enum | `percentage` or `fixed` |
| `percentage` | number | Tip as percentage (0–100), when type is `percentage` |
| `amount_cents` | integer | Resolved tip amount |

### Scheduling

For non-ASAP fulfillment, use `is_asap: false` with `scheduled_for`:

| Field | Type | Description |
|---|---|---|
| `scheduled_for` | datetime | Requested service time |
| `available_time_slots` | array | Slots the provider offers, each with `start`, `end`, `is_available` |

The agent presents available slots: *"They have slots at 6pm, 6:30pm, or 7pm."*

## Schema: Item Customization

{{ schema_fields("spec/schemas/services/types/item_customization.json") }}

## Schema: Loyalty Discount

{{ schema_fields("spec/schemas/services/types/loyalty_discount.json") }}

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/checkouts` | Create a checkout with fulfillment |
| `PATCH` | `/checkouts/{checkout_id}` | Update checkout fields |
| `POST` | `/checkouts/{checkout_id}/complete` | Finalize and pay |

## Example: Create Checkout (Food Delivery)

```json
{
  "line_items": [
    {
      "item_id": "margherita",
      "title": "Margherita Pizza",
      "quantity": 1,
      "price_cents": 1799,
      "special_instructions": "Extra basil",
      "modifiers": ["large", "extra-cheese"]
    }
  ],
  "fulfillment": {
    "type": "delivery",
    "estimated_service_minutes": 35,
    "service_fee_cents": 299,
    "address": {
      "street_line_1": "123 Main St",
      "city": "San Francisco",
      "postal_code": "94105",
      "country_code": "US"
    },
    "instructions": "Leave at the front door",
    "is_asap": true,
    "fees": [
      { "type": "delivery", "label": "Delivery fee", "amount_cents": 299 },
      { "type": "service", "label": "Service fee", "amount_cents": 199 }
    ],
    "tip": {
      "type": "percentage",
      "percentage": 15,
      "amount_cents": 270
    }
  },
  "loyalty": {
    "loyalty_tier": "gold",
    "loyalty_discount_percent": 15
  }
}
```

## Example: Create Checkout (Ride-Hailing)

```json
{
  "line_items": [
    {
      "item_id": "sedan-ride",
      "title": "Sedan Ride",
      "quantity": 1,
      "price_cents": 1500
    }
  ],
  "fulfillment": {
    "type": "ride",
    "estimated_service_minutes": 12,
    "service_fee_cents": 200,
    "address": {
      "street_line_1": "123 Main St",
      "city": "San Francisco",
      "postal_code": "94105",
      "country_code": "US"
    },
    "is_asap": true
  }
}
```
