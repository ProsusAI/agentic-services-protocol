---
hide:
  - toc
---

<div class="asp-hero" markdown>

# Agentic Services Protocol

<p class="asp-subtitle">
An open protocol for end-to-end agent-to-service transactions — food delivery, ride-hailing, travel, and on-demand services. ASP covers the full transaction lifecycle from discovery to reviews, giving AI agents everything they need to interact with service marketplaces. For checkout and payment, ASP is compatible with <a href="https://developers.google.com/merchant/ucp">UCP</a>.
</p>

<div class="asp-cta">
  <a href="documentation/core-concepts/" class="asp-cta-primary">Get started</a>
  <a href="https://github.com/ProsusAI/agentic-services-protocol" class="asp-cta-secondary">GitHub</a>
</div>

</div>

<div class="asp-section-header" markdown>

## Capabilities & Extensions

</div>

<p class="asp-section-subtext">ASP covers the full transaction lifecycle — pre-purchase, purchase, and post-purchase — with standalone capabilities and UCP-compatible extensions for checkout.</p>

<div class="asp-cards" markdown>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
<span class="asp-card-badge capability">Capability</span>
<div class="asp-card-title"><a href="specification/discovery/">Discovery</a></div>
<div class="asp-card-desc">Search providers by location, category, rating, and availability</div>
</div>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg></span>
<span class="asp-card-badge capability">Capability</span>
<div class="asp-card-title"><a href="specification/catalog/">Catalog</a></div>
<div class="asp-card-desc">Browse catalogs with sections, items, modifier groups, and reorder from history</div>
</div>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg></span>
<span class="asp-card-badge extension">Extension</span>
<div class="asp-card-title"><a href="specification/fulfillment/">Fulfillment</a></div>
<div class="asp-card-desc">Multi-type fulfillment, per-item customization, fees, tips, loyalty discounts</div>
</div>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></span>
<span class="asp-card-badge extension">Extension</span>
<div class="asp-card-title"><a href="specification/order-tracking/">Order Tracking</a></div>
<div class="asp-card-desc">Status progression, ETA updates, granular stages, delay tracking</div>
</div>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg></span>
<span class="asp-card-badge extension">Extension</span>
<div class="asp-card-title"><a href="specification/order-tracking/#live-streaming">Live Streaming</a></div>
<div class="asp-card-desc">Real-time WebSocket location tracking and status change events</div>
</div>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
<span class="asp-card-badge capability">Capability</span>
<div class="asp-card-title"><a href="specification/personalization/">Personalization</a></div>
<div class="asp-card-desc">User profiles, order history, dietary preferences, and promotions</div>
</div>

<div class="asp-card" markdown>
<span class="asp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
<span class="asp-card-badge capability">Capability</span>
<div class="asp-card-title"><a href="specification/overview/#capabilities-standalone">Reviews</a></div>
<div class="asp-card-desc">Post-service ratings with category scores and comments</div>
</div>

</div>

<div class="asp-section-header" markdown>

## Design Principles

</div>

<div class="asp-principles" markdown>

<div class="asp-principle" markdown>
<strong>Minimal surface</strong>
<span>Only the primitives needed for live service transactions</span>
</div>

<div class="asp-principle" markdown>
<strong>Composable</strong>
<span>Modular capabilities; checkout extensions are compatible with UCP via allOf</span>
</div>

<div class="asp-principle" markdown>
<strong>Marketplace-controlled</strong>
<span>The marketplace owns its data; ASP provides structured transport</span>
</div>

<div class="asp-principle" markdown>
<strong>Agent-friendly</strong>
<span>Every schema is designed for conversational AI consumption</span>
</div>

<div class="asp-principle" markdown>
<strong>Vertical-agnostic</strong>
<span>Core schemas work across verticals; domain profiles add specialization</span>
</div>

</div>

<div class="asp-section-header" markdown>

## Quick Start

</div>

<div class="asp-quickstart" markdown>

```bash
# Validate schemas
python validate_specs.py

# Generate spec/ from source/
python generate_schemas.py

# Build documentation
mkdocs serve
```

</div>

<div class="asp-section-header" markdown>

## Learn More

</div>

<div class="asp-links" markdown>

<a href="documentation/core-concepts/" class="asp-link">
<span class="asp-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span> Core Concepts
</a>

<a href="specification/domains/" class="asp-link">
<span class="asp-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></span> Domain Profiles
</a>

<a href="documentation/schema-authoring/" class="asp-link">
<span class="asp-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></span> Schema Authoring Guide
</a>

<a href="https://github.com/ProsusAI/asp-samples" class="asp-link">
<span class="asp-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></span> Samples
</a>

<a href="documentation/implementation-checklist/" class="asp-link">
<span class="asp-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></span> Implementation Checklist
</a>

<a href="documentation/roadmap/" class="asp-link">
<span class="asp-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg></span> Roadmap
</a>

</div>
