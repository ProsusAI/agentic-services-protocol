# Reviews

**Capability:** `dev.asp.services.reviews`  
**Version:** `2026-02-19`  
**Schema:** [`reviews.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/reviews.json)

## Purpose

Enables agents to close the service loop by submitting post-service reviews and retrieving provider review history for better recommendations.

## Endpoints

```text
POST /reviews
GET  /reviews/{provider_id}
```

## Submit Review

### Request payload (`submit_review_request`)

{{ schema_fields("spec/schemas/services/reviews.json", "$defs.submit_review_request") }}

### Response payload

{{ schema_fields("spec/schemas/services/types/review.json") }}

## Get Provider Reviews

### Request

{{ schema_fields("spec/schemas/services/reviews.json", "$defs.get_reviews_request") }}

### Response payload (`get_reviews_response`)

{{ schema_fields("spec/schemas/services/reviews.json", "$defs.get_reviews_response") }}

## Example

```json
{
  "order_id": "ord_123",
  "provider_id": "pizza-palace",
  "rating": 5,
  "comment": "Excellent service and fast delivery.",
  "scores": {
    "food": 5,
    "delivery": 5,
    "value": 4
  }
}
```
