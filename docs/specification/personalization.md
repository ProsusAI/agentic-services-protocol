# User Profile & Personalization

**Capability:** `dev.asp.services.personalization`
**Version:** `2026-02-19`
**Schema:** [`personalization.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/personalization.json)

## Purpose

Enables the marketplace to communicate user preferences, loyalty status, order history, and personalized promotions to the agent. The marketplace retains full ownership of its personalization models — the protocol simply provides structured transport.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/personalization/profile` | Get user profile |
| `GET` | `/personalization/promotions` | Get personalized promotions |

## Schema: User Profile

{{ schema_fields("spec/schemas/services/types/user_profile.json") }}

### Example

```json
{
  "name": "Sarah",
  "loyalty_tier": "gold",
  "loyalty_points": 2850,
  "preferred_categories": ["italian", "japanese"],
  "order_history": [
    {
      "order_id": "ord-001",
      "provider_id": "pizza-palace",
      "provider_name": "Pizza Palace",
      "items": [{ "item_id": "margherita", "title": "Margherita Pizza", "quantity": 1 }],
      "ordered_at": "2026-02-10T19:30:00Z",
      "total_cents": 1799
    }
  ],
  "default_address": {
    "street_line_1": "123 Main St",
    "city": "San Francisco",
    "postal_code": "94105",
    "country_code": "US"
  }
}
```

### Loyalty Tier

The `loyalty_tier` field is a free-form string — each marketplace defines its own tier names (e.g. `"gold"`, `"premium"`, `"VIP"`, `"level_3"`). ASP does not prescribe a fixed set of tiers. The agent should display the tier value as provided by the marketplace.

## Schema: Promotion

{{ schema_fields("spec/schemas/services/types/promotion.json") }}

### Promotion Types

| Type | Description |
|---|---|
| `discount` | Percentage or flat discount, often tier-specific |
| `reorder` | Suggestion to reorder a previous favorite |
| `category` | New items matching preferred categories |
| `loyalty` | Loyalty program milestone or reward |

### Example

```json
{
  "promotions": [
    {
      "id": "promo-gold-pizza",
      "title": "15% Off Your Usual",
      "description": "Sarah, your Margherita Pizza from Pizza Palace is 15% off today — Gold member exclusive.",
      "type": "discount",
      "discount_percent": 15,
      "applicable_provider_id": "pizza-palace",
      "valid_until": "2026-02-20T00:00:00Z"
    }
  ]
}
```

## Authentication

Personalization endpoints require a bearer token obtained via UCP Identity Linking (OAuth 2.0). The marketplace resolves the token to a user internally — **no user ID is passed in the request or required in the response**. The agent never knows the marketplace's internal user identifier.

```
GET /personalization/profile
Authorization: Bearer <access_token>
```

## Privacy Considerations

- User profile data is provided by the marketplace, not collected by the agent
- The agent should not store profile data beyond the session
- Preferred categories and order history are opt-in on the marketplace side
- The protocol does not define consent flows — marketplaces handle this per their privacy policies
- No internal user identifiers are exposed to the agent — the bearer token is the sole identity mechanism
