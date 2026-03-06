# Domain Profiles

ASP core schemas are **vertical-agnostic** — they define abstract types like `provider`, `catalog_item`, and `fulfillment` without assuming any specific industry. **Domain profiles** specialize these abstractions for a concrete vertical.

Profiles live in `source/schemas/domains/` and use JSON Schema's `allOf` to extend core types with domain-specific fields.

!!! note
    Domain profiles are reference examples. Marketplaces may define their own profiles or use the core schemas directly.

## How Profiles Work

Each profile defines:

1. **Constrained enums** — narrows `service_categories`, `fulfillment_types`, and other open fields to a fixed set of values
2. **Extended types** — uses `allOf` to add domain-specific properties onto core types like `catalog_item`, `provider`, and `fulfillment`
3. **Status mappings** — maps abstract fulfillment statuses (`accepted`, `in_progress`, `completed`, etc.) to domain-specific meanings

```json
{
  "allOf": [
    { "$ref": "../../services/types/catalog_item.json" },
    {
      "type": "object",
      "properties": {
        "dietary_tags": { "type": "array", "items": { ... } },
        "calories": { "type": "integer" }
      }
    }
  ]
}
```

The base `catalog_item` stays intact — the profile only adds properties alongside it.

---

## Food Delivery

**Schema:** `source/schemas/domains/food_delivery/profile.json`

For food delivery and grocery marketplaces — restaurants, cloud kitchens, and grocery stores.

### Service Categories

`italian` · `japanese` · `chinese` · `indian` · `thai` · `mexican` · `american` · `mediterranean` · `korean` · `vietnamese` · `pizza` · `burgers` · `sushi` · `healthy` · `desserts` · `coffee` · `bakery` · `groceries` · `alcohol`

### Fulfillment Types

`delivery` · `pickup` · `dine_in`

### Extended Types

| Type | Extends | Added Fields |
|------|---------|-------------|
| `food_catalog_item` | `catalog_item` | `dietary_tags`, `calories`, `prep_time_minutes`, `tags`, `available_for_scheduling` |
| `food_provider` | `provider` | `cuisine_types`, `dietary_options`, `minimum_order_cents`, `accepts_scheduled_orders` |
| `food_item_customization` | `item_customization` | `substitution_allowed`, `substitution_preference` |

### Dietary Tags

`vegetarian` · `vegan` · `gluten_free` · `halal` · `kosher` · `dairy_free` · `nut_free` · `organic` · `sugar_free` · `keto` · `paleo`

### Substitution Preferences

The `food_item_customization` extends base item customization with:

| Field | Type | Description |
|---|---|---|
| `substitution_allowed` | boolean | Whether the provider can substitute this item if unavailable (default: false) |
| `substitution_preference` | enum | `similar_item`, `refund`, or `contact_me` |

Agent handles: *"The Coke is out of stock. Want a Pepsi instead, a refund, or should I ask the restaurant?"*

### Fulfillment Status Mapping

The food domain adds **granular statuses** that map to the 5 base statuses. Agents that only understand the base still work — they just see "in progress" instead of "driver at restaurant."

| Granular Status | Base Status | Agent Says |
|---|---|---|
| `accepted` | accepted | "Restaurant confirmed your order" |
| `preparing` | in_progress | "Your food is being prepared" |
| `ready_for_pickup` | in_progress | "Your order is ready for pickup" |
| `assigning_driver` | in_progress | "Finding a driver..." |
| `driver_assigned` | in_progress | "A driver has been assigned" |
| `driver_at_restaurant` | in_progress | "Driver is at the restaurant" |
| `en_route` | en_route | "Your food is on its way" |
| `driver_arriving` | en_route | "Driver is almost there" |
| `delivered` | completed | "Your food has been delivered" |
| `cancelled` | cancelled | "Order was cancelled" |

### Modifier Examples

- **Spice Level** — Mild, Medium, Hot, Extra Hot (single select, no price delta)
- **Size** — Small, Regular (+$2), Large (+$4) (required, single select)
- **Extra Toppings** — Extra Cheese (+$1.50), Mushrooms (+$1), Olives (+$1) (optional, up to 5)

---

## Ride Hailing

**Schema:** `source/schemas/domains/ride_hailing/profile.json`

For ride-hailing and mobility marketplaces — taxis, ride-shares, and on-demand drivers.

### Service Categories

`economy` · `sedan` · `suv` · `luxury` · `van` · `motorcycle` · `auto_rickshaw` · `pool` · `xl` · `electric` · `accessible`

### Fulfillment Types

`ride`

### Extended Types

| Type | Extends | Added Fields |
|------|---------|-------------|
| `ride_catalog_item` | `catalog_item` | `vehicle_category`, `max_passengers`, `max_luggage_pieces`, `vehicle_features`, `surge_multiplier`, `estimated_arrival_minutes`, `availableForScheduling` |
| `ride_provider` | `provider` | `vehicle_categories`, `coverage_area` (center lat/lng + radius) |
| `ride_fulfillment` | `fulfillment` | `pickup_location`, `dropoff_location`, `estimated_distance_km`, `route_polyline` |

### Vehicle Features

`air_conditioning` · `wifi` · `child_seat` · `wheelchair_accessible` · `pet_friendly` · `luggage_space` · `quiet_ride` · `premium_audio`

### Fulfillment Status Mapping

| Abstract Status | Ride Hailing Meaning |
|---|---|
| `accepted` | Driver has accepted the ride request |
| `in_progress` | Driver is en route to the pickup location |
| `en_route` | Rider is in the vehicle; trip is underway |
| `completed` | Rider has been dropped off at the destination |
| `cancelled` | Ride was cancelled by driver or rider |

### Modifier Examples

- **Ride Extras** — Child Seat (+$5), Quiet Ride (free), Extra Stop (+$3) (optional, up to 3)

---

## Travel & Accommodation

**Schema:** `source/schemas/domains/travel/profile.json`

For travel, accommodation, and booking marketplaces — hotels, vacation rentals, hostels, and resorts.

### Service Categories

`hotel` · `villa` · `hostel` · `apartment` · `resort` · `boutique` · `bed_and_breakfast` · `vacation_rental` · `motel` · `guesthouse` · `campsite` · `serviced_apartment`

### Fulfillment Types

`booking`

### Extended Types

| Type | Extends | Added Fields |
|------|---------|-------------|
| `travel_catalog_item` | `catalog_item` | `room_type`, `max_guests`, `amenities`, `cancellation_policy`, `price_per_night_cents`, `check_in_time`, `check_out_time` |
| `travel_provider` | `provider` | `accommodation_type`, `star_rating`, `amenities`, `total_units` |
| `travel_fulfillment` | `fulfillment` | `check_in_date`, `check_out_date`, `guests`, `special_requests`, `confirmation_code` |

### Room Types

`single` · `double` · `twin` · `suite` · `family` · `penthouse` · `studio` · `dormitory` · `entire_property`

### Amenity Tags

`wifi` · `pool` · `spa` · `gym` · `parking` · `breakfast_included` · `air_conditioning` · `kitchen` · `laundry` · `pet_friendly` · `airport_shuttle` · `room_service` · `concierge` · `beach_access` · `balcony` · `ev_charging` · `accessible`

### Cancellation Policies

`free_cancellation` · `flexible` · `moderate` · `strict` · `non_refundable`

### Fulfillment Status Mapping

| Abstract Status | Travel Meaning |
|---|---|
| `accepted` | Booking confirmed by the property |
| `in_progress` | Guest has checked in; stay is active |
| `en_route` | Not applicable — unused for bookings |
| `completed` | Guest has checked out |
| `cancelled` | Booking was cancelled per cancellation policy |

### Modifier Examples

- **Meal Plan** — Room Only, Breakfast (+$25), Half Board (+$50), Full Board (+$80) (single select)
- **Extras** — Airport Transfer (+$40), Late Checkout (+$30), Extra Bed (+$20), Parking (+$15) (optional, up to 4)
