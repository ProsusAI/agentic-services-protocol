# Order Tracking Extension

**Extension:** `dev.asp.services.order_tracking`
**Version:** `2026-02-19`
**Extends:** `dev.ucp.shopping.order`
**Schema:** [`order_tracking.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/order_tracking.json)

## Purpose

Extends UCP order with granular fulfillment status tracking. Supports both polling (GET) and push (webhook) models for real-time updates.

## Status Progression

```
accepted → in_progress → en_route → completed
                                   → cancelled (from any state)
```

## Schema: Fulfillment Status

{{ schema_fields("spec/schemas/services/types/fulfillment_status.json") }}

## Polling Endpoint

```
GET /orders/{order_id}/tracking
```

Returns the current `fulfillment_status` object.

## Push Model: Webhooks

The marketplace sends a `status_update_event` to the agent/platform whenever the order status changes:

```json
{
  "event_type": "order.status_updated",
  "order_id": "order-12345",
  "status": {
    "order_id": "order-12345",
    "status": "en_route",
    "estimated_service_minutes": 12,
    "updated_at": "2026-02-19T12:45:00Z",
    "agent_location": {
      "latitude": 37.7751,
      "longitude": -122.4180
    }
  },
  "timestamp": "2026-02-19T12:45:00Z"
}
```

### Webhook Registration

Webhook endpoints are declared in the discovery profile or negotiated during checkout. The marketplace POSTs `status_update_event` payloads to the registered URL.

## Status History

The `history` array provides an ordered timeline of status transitions, enabling agents to narrate the full journey:

```json
{
  "order_id": "order-12345",
  "status": "en_route",
  "updated_at": "2026-02-19T12:45:00Z",
  "history": [
    { "status": "accepted", "timestamp": "2026-02-19T12:30:00Z" },
    { "status": "in_progress", "timestamp": "2026-02-19T12:35:00Z" },
    { "status": "en_route", "timestamp": "2026-02-19T12:45:00Z", "note": "Driver picked up order" }
  ]
}
```

Agent says: *"Accepted at 12:30, started preparing at 12:35, driver picked up at 12:45."*

## Delay Awareness

Two optional fields let agents proactively warn users:

| Field | Type | Description |
|---|---|---|
| `is_delayed` | boolean | Whether the order is running behind the original estimate |
| `delay_minutes` | integer | How many minutes behind |

Agent says: *"Heads up, your order is running about 10 minutes late."*

## Domain-Specific Statuses

The 5 base statuses are intentionally abstract. Domain profiles can define granular statuses that map to the base set, giving agents richer vocabulary without breaking compatibility.

For example, the **food delivery** domain profile maps 10 granular statuses to the 5 base — see [Food Delivery Domain](domains.md#food-delivery) for the full mapping table. An agent that only understands the base statuses still works; the granular statuses are additive.

## Agent Behavior

Agents should proactively surface status changes to the user:

- **accepted**: "Your order has been accepted!"
- **in_progress**: "Your order is being prepared."
- **en_route**: "Your order is on its way! ETA: 12 minutes."
- **completed**: "Your order is complete. Enjoy!"
- **delayed**: "Heads up, your order is running about 10 minutes late."

The `estimated_service_minutes` field updates with each status change, allowing the agent to show a live countdown.

## Agent Location

The optional `agent_location` field (latitude/longitude) enables live map tracking during the `en_route` phase. This is opt-in — marketplaces that don't support live tracking simply omit the field.

## Live Streaming

**Extension:** `dev.asp.services.streaming`
**Extends:** `dev.asp.services.order_tracking`
**Schema:** [`streaming.json`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/schemas/services/streaming.json)
**Transport:** [`asyncapi.yaml`](https://github.com/ProsusAI/agentic-services-protocol/blob/main/source/services/live_services/asyncapi.yaml)

For continuous agent location tracking (e.g. rendering a live delivery map), ASP provides a WebSocket streaming channel defined via AsyncAPI 3.0.

### WebSocket Channel

```
wss://<host>/asp/v1/ws → /orders/{order_id}/tracking/stream
```

### Message Types

The server sends three event types, discriminated by `event_type`:

| Event | When | Frequency |
|---|---|---|
| `location_update` | Agent GPS position changed | Every 3-5 seconds during `en_route` |
| `status_changed` | Order status transition | ~5 per order lifecycle |
| `heartbeat` | Keep-alive | Every 30 seconds |

### Connection Lifecycle

1. Client opens WebSocket to `wss://<host>/asp/v1/ws`
2. Client sends `subscribe` with `order_id` and bearer `token` (first-message auth)
3. Server validates and sends a `status_changed` snapshot of current state
4. Server streams `location_update` events during `en_route` phase
5. Server sends `heartbeat` every 30s
6. On terminal status (`completed`/`cancelled`), server sends final `status_changed` and closes with code 1000

### Location Update Payload

```json
{
  "event_type": "location_update",
  "order_id": "order-12345",
  "payload": {
    "status": "en_route",
    "agent_location": {
      "latitude": 37.7751,
      "longitude": -122.4180,
      "heading": 45.0,
      "speed_kmh": 28.5
    },
    "estimated_service_minutes": 8,
    "updated_at": "2026-02-19T12:45:03Z"
  },
  "timestamp": "2026-02-19T12:45:03Z"
}
```

The `heading` (compass degrees) and `speed_kmh` fields enable rotating map markers and smooth interpolation between updates.

### Reconnection

If the connection drops, the client should:

1. Wait with exponential backoff (1s, 2s, 4s, max 30s)
2. Reconnect and send a new `subscribe` message
3. The server resends the current state snapshot

No events are buffered during disconnection — the client gets the latest state on reconnect.

### Fallback

Clients that cannot use WebSocket should fall back to polling `GET /orders/{order_id}/tracking`. The webhook push model continues to fire on status transitions regardless of whether a WebSocket connection is active.
