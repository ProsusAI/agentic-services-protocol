# Playground

Experience the ASP protocol flow in your browser. Walk through a complete transaction — from discovering a restaurant, browsing its menu, placing an order, to tracking delivery — all with real protocol messages.

<style>
  .pg-stepper { display: flex; gap: 0; margin: 2rem 0 1.5rem; border-radius: 8px; overflow: hidden; border: 1px solid var(--md-default-fg-color--lightest); }
  .pg-step-btn { flex: 1; padding: 0.75rem 0.5rem; text-align: center; cursor: pointer; border: none; background: var(--md-default-bg-color); color: var(--md-default-fg-color--light); font-size: 0.8rem; font-weight: 500; transition: all 0.2s; border-right: 1px solid var(--md-default-fg-color--lightest); }
  .pg-step-btn:last-child { border-right: none; }
  .pg-step-btn:hover { background: var(--md-accent-fg-color--transparent); }
  .pg-step-btn.active, .md-typeset .pg-step-btn.active { background: #1136A8 !important; color: #fff !important; font-weight: 600; }
  .pg-step-btn.active .pg-num { color: #fff !important; }
  .pg-step-btn .pg-num { display: block; font-size: 1.1rem; font-weight: 700; margin-bottom: 2px; }
  .pg-card { background: var(--md-default-bg-color); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; display: none; }
  .pg-card.active { display: block; }
  .pg-card h3 { margin-top: 0; }
  .pg-panels { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; }
  @media (max-width: 768px) { .pg-panels { grid-template-columns: 1fr; } .pg-stepper { flex-wrap: wrap; } .pg-step-btn { flex: 1 1 25%; } }
  .pg-panel { border: 1px solid var(--md-default-fg-color--lightest); border-radius: 6px; overflow: hidden; }
  .pg-panel-header { background: var(--md-default-fg-color--lightest); padding: 0.5rem 0.8rem; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; gap: 0.5rem; flex-wrap: nowrap; }
  .pg-panel-header > span { display: inline-flex !important; align-items: center; gap: 0.4rem; white-space: nowrap; }
  .pg-panel pre { margin: 0 !important; padding: 0.8rem !important; font-size: 0.78rem; line-height: 1.5; overflow-x: auto; max-height: 400px; overflow-y: auto; background: var(--md-code-bg-color) !important; }
  .pg-badge { display: inline-block !important; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 600; line-height: 1.4; vertical-align: middle; }
  .pg-badge-post { background: #49cc90 !important; color: #fff !important; }
  .pg-badge-get { background: #61affe !important; color: #fff !important; }
  .pg-badge-webhook { background: #f93e3e !important; color: #fff !important; }
  .pg-badge-ws { background: #9b59b6 !important; color: #fff !important; }
  .pg-ws-log { margin: 0 !important; padding: 0.8rem !important; font-size: 0.78rem; line-height: 1.5; overflow-x: auto; max-height: 400px; overflow-y: auto; background: var(--md-code-bg-color) !important; font-family: var(--md-text-font), sans-serif; white-space: pre; }
  .pg-ws-log .ws-send { color: #49cc90; }
  .pg-ws-log .ws-recv { color: #61affe; }
  .pg-ws-log .ws-info { color: var(--md-default-fg-color--lighter); }
  .pg-ws-log .ws-close { color: #f93e3e; }
  .pg-actions { display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; align-items: center; }
  .pg-btn { padding: 0.5rem 1.2rem; border-radius: 6px; border: none; cursor: pointer; font-weight: 600; font-size: 0.85rem; transition: all 0.15s; color: inherit; }
  .pg-btn-primary, .md-typeset .pg-btn-primary, button.pg-btn-primary { background: #1136A8 !important; color: #fff !important; }
  .pg-btn-primary:hover { opacity: 0.9; }
  .pg-btn-secondary { background: var(--md-default-fg-color--lightest); color: var(--md-default-fg-color); }
  .pg-btn-secondary:hover { background: var(--md-default-fg-color--lighter); }
  .pg-desc { color: var(--md-default-fg-color--light); margin: 0.25rem 0 1rem; line-height: 1.6; }
  .pg-config { display: flex; gap: 1rem; flex-wrap: wrap; margin: 0.75rem 0; align-items: center; }
  .pg-config label { font-size: 0.85rem; font-weight: 500; }
  .pg-config select, .pg-config input { padding: 0.35rem 0.6rem; border-radius: 4px; border: 1px solid var(--md-default-fg-color--lightest); font-size: 0.85rem; background: var(--md-default-bg-color); color: var(--md-default-fg-color); }
  .pg-status { padding: 0.4rem 0.8rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500; }
  .pg-status-ok { background: #d4edda; color: #155724; }
  .pg-status-pending { background: #fff3cd; color: #856404; }
  .pg-arrow { font-size: 1.5rem; color: var(--md-default-fg-color--lighter); text-align: center; margin: 0.5rem 0; }
  .pg-tag { display: inline-block; background: var(--md-primary-fg-color--transparent); color: var(--md-primary-fg-color); padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.75rem; margin-right: 0.25rem; }
</style>

<div class="pg-stepper">
  <button class="pg-step-btn active" onclick="pgGo(0)"><span class="pg-num">1</span>Discovery</button>
  <button class="pg-step-btn" onclick="pgGo(1)"><span class="pg-num">2</span>Catalog</button>
  <button class="pg-step-btn" onclick="pgGo(2)"><span class="pg-num">3</span>Checkout</button>
  <button class="pg-step-btn" onclick="pgGo(3)"><span class="pg-num">4</span>Tracking</button>
  <button class="pg-step-btn" onclick="pgGo(4)"><span class="pg-num">5</span>Live Stream</button>
  <button class="pg-step-btn" onclick="pgGo(5)"><span class="pg-num">6</span>Review</button>
</div>

<!-- STEP 1: Discovery -->
<div class="pg-card active" id="pg-step-0">
  <h3>Step 1: Discover Providers</h3>
  <p class="pg-desc">
    An agent searches for nearby service providers. Configure the filters below and run the search to see matching results.
  </p>

  <div class="pg-config">
    <label>Domain:
      <select id="pg-domain" onchange="pgUpdateDiscovery()">
        <option value="food">Food Delivery</option>
        <option value="ride">Ride Hailing</option>
        <option value="travel">Travel & Hotels</option>
      </select>
    </label>
    <label>Category:
      <select id="pg-category">
        <option value="italian">Italian</option>
        <option value="sushi">Sushi</option>
        <option value="thai">Thai</option>
      </select>
    </label>
    <label>Min Rating:
      <select id="pg-rating">
        <option value="4.0">4.0+</option>
        <option value="3.5">3.5+</option>
        <option value="0">Any</option>
      </select>
    </label>
  </div>

  <div class="pg-panels">
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Request</span>
        <span><span class="pg-badge pg-badge-post">POST</span> /discovery/search</span>
      </div>
      <pre id="pg-discovery-req"></pre>
    </div>
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Response</span>
        <span class="pg-status pg-status-pending" id="pg-discovery-status">waiting</span>
      </div>
      <pre id="pg-discovery-res"><span style="color:var(--md-default-fg-color--lighter)">Click "Search Providers" to run the request...</span></pre>
    </div>
  </div>

  <div class="pg-actions">
    <button class="pg-btn pg-btn-primary" onclick="pgRunDiscovery()">Search Providers</button>
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(1)">Next Step →</button>
  </div>
</div>

<!-- STEP 2: Catalog -->
<div class="pg-card" id="pg-step-1">
  <h3>Step 2: Browse Catalog</h3>
  <p class="pg-desc">
    After selecting a provider, the agent fetches their catalog — organized into sections with items and modifier groups for customization.
  </p>

  <div class="pg-config">
    <label>Provider:
      <select id="pg-provider" onchange="pgUpdateCatalog()">
        <option value="pizza-palace">Pizza Palace (★ 4.7)</option>
        <option value="sakura-sushi">Sakura Sushi (★ 4.5)</option>
      </select>
    </label>
  </div>

  <div class="pg-panels">
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Request</span>
        <span><span class="pg-badge pg-badge-get">GET</span> /catalog/{provider_id}/catalog</span>
      </div>
      <pre id="pg-catalog-req"></pre>
    </div>
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Response</span>
        <span class="pg-status pg-status-pending" id="pg-catalog-status">waiting</span>
      </div>
      <pre id="pg-catalog-res"><span style="color:var(--md-default-fg-color--lighter)">Click "Fetch Catalog" to load the menu...</span></pre>
    </div>
  </div>

  <div class="pg-actions">
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(0)">← Back</button>
    <button class="pg-btn pg-btn-primary" onclick="pgRunCatalog()">Fetch Catalog</button>
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(2)">Next Step →</button>
  </div>
</div>

<!-- STEP 3: Checkout -->
<div class="pg-card" id="pg-step-2">
  <h3>Step 3: Create Checkout</h3>
  <p class="pg-desc">
    The agent creates a UCP checkout with ASP's fulfillment extension — specifying items with modifiers, delivery details, and optional loyalty info.
  </p>

  <div class="pg-config">
    <label>Fulfillment:
      <select id="pg-fulfillment" onchange="pgUpdateCheckout()">
        <option value="delivery">Delivery</option>
        <option value="pickup">Pickup</option>
      </select>
    </label>
    <label>Loyalty Tier:
      <select id="pg-loyalty" onchange="pgUpdateCheckout()">
        <option value="none">None</option>
        <option value="gold">Gold (15% off)</option>
        <option value="silver">Silver (10% off)</option>
      </select>
    </label>
  </div>

  <div class="pg-panels">
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Request</span>
        <span><span class="pg-badge pg-badge-post">POST</span> /checkouts</span>
      </div>
      <pre id="pg-checkout-req"></pre>
    </div>
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Response</span>
        <span class="pg-status pg-status-pending" id="pg-checkout-status">waiting</span>
      </div>
      <pre id="pg-checkout-res"><span style="color:var(--md-default-fg-color--lighter)">Click "Create Checkout" to place the order...</span></pre>
    </div>
  </div>

  <div class="pg-actions">
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(1)">← Back</button>
    <button class="pg-btn pg-btn-primary" onclick="pgRunCheckout()">Create Checkout</button>
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(3)">Next Step →</button>
  </div>
</div>

<!-- STEP 4: Order Tracking -->
<div class="pg-card" id="pg-step-3">
  <h3>Step 4: Track Order</h3>
  <p class="pg-desc">
    After checkout, the marketplace sends status updates via webhooks. Click through to simulate the order progressing from confirmed to delivered.
  </p>

  <div class="pg-panels">
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Webhook Event</span>
        <span><span class="pg-badge pg-badge-webhook">WEBHOOK</span> order.status_update</span>
      </div>
      <pre id="pg-tracking-req"></pre>
    </div>
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Order Status</span>
        <span class="pg-status pg-status-pending" id="pg-tracking-status">pending</span>
      </div>
      <pre id="pg-tracking-res"></pre>
    </div>
  </div>

  <div class="pg-actions">
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(2)">← Back</button>
    <button class="pg-btn pg-btn-primary" id="pg-tracking-btn" onclick="pgRunTracking()">Simulate: Confirmed</button>
    <button class="pg-btn pg-btn-secondary" onclick="pgReset()">↺ Start Over</button>
  </div>
</div>

<!-- STEP 5: Live Streaming -->
<div class="pg-card" id="pg-step-4">
  <h3>Step 5: Live Streaming (WebSocket)</h3>
  <p class="pg-desc">
    For truly live updates — GPS location every 3-5 seconds — ASP provides a WebSocket streaming channel. This simulates the full connection lifecycle: subscribe, status snapshot, live location updates during <code>en_route</code>, heartbeats, and graceful close on completion.
  </p>

  <div class="pg-panels">
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>WebSocket Messages</span>
        <span><span class="pg-badge pg-badge-ws">WS</span> wss://host/asp/v1/ws</span>
      </div>
      <div class="pg-ws-log" id="pg-stream-log"><span class="ws-info">Click "Connect & Stream" to open the WebSocket...</span></div>
    </div>
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Latest Event</span>
        <span class="pg-status pg-status-pending" id="pg-stream-status">disconnected</span>
      </div>
      <pre id="pg-stream-event"><span style="color:var(--md-default-fg-color--lighter)">No events yet...</span></pre>
    </div>
  </div>

  <div class="pg-actions">
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(3)">← Back</button>
    <button class="pg-btn pg-btn-primary" id="pg-stream-btn" onclick="pgRunStream()">Connect & Stream</button>
    <button class="pg-btn pg-btn-secondary" onclick="pgReset()">↺ Start Over</button>
  </div>
</div>

<!-- STEP 6: Review -->
<div class="pg-card" id="pg-step-5">
  <h3>Step 6: Submit Review</h3>
  <p class="pg-desc">
    After delivery, the agent submits a review on behalf of the user — an overall rating, optional comment, and category-specific scores.
  </p>

  <div class="pg-config">
    <label>Rating:
      <select id="pg-review-rating" onchange="pgUpdateReview()">
        <option value="5">5 — Excellent</option>
        <option value="4">4 — Good</option>
        <option value="3">3 — Average</option>
        <option value="2">2 — Poor</option>
        <option value="1">1 — Terrible</option>
      </select>
    </label>
  </div>

  <div class="pg-panels">
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Request</span>
        <span><span class="pg-badge pg-badge-post">POST</span> /reviews</span>
      </div>
      <pre id="pg-review-req"></pre>
    </div>
    <div class="pg-panel">
      <div class="pg-panel-header">
        <span>Response</span>
        <span class="pg-status pg-status-pending" id="pg-review-status">waiting</span>
      </div>
      <pre id="pg-review-res"><span style="color:var(--md-default-fg-color--lighter)">Click "Submit Review" to send the review...</span></pre>
    </div>
  </div>

  <div class="pg-actions">
    <button class="pg-btn pg-btn-secondary" onclick="pgGo(4)">← Back</button>
    <button class="pg-btn pg-btn-primary" onclick="pgRunReview()">Submit Review</button>
    <button class="pg-btn pg-btn-secondary" onclick="pgReset()">↺ Start Over</button>
  </div>
</div>

<script>
// --- State ---
var pgStep = 0;
var pgTrackStage = 0;
var pgStreamTimer = null;
var pgSelectedProvider = null;  // { id, name, fee }
var pgSelectedItem = null;      // { id, title, price_cents, modifiers[], modifier_ids[], description }

// --- Navigation ---
function pgGo(n) {
  pgStep = n;
  document.querySelectorAll('.pg-step-btn').forEach(function(b, i) { b.classList.toggle('active', i === n); });
  document.querySelectorAll('.pg-card').forEach(function(c, i) { c.classList.toggle('active', i === n); });
  if (n === 0) pgUpdateDiscovery();
  if (n === 1) pgUpdateCatalog();
  if (n === 2) pgUpdateCheckout();
  if (n === 3) pgUpdateTracking();
}

function pgReset() {
  pgTrackStage = 0;
  if (pgStreamTimer) { clearTimeout(pgStreamTimer); pgStreamTimer = null; }
  pgGo(0);
  ['pg-discovery-res','pg-catalog-res','pg-checkout-res','pg-review-res'].forEach(function(id) {
    document.getElementById(id).innerHTML = '<span style="color:var(--md-default-fg-color--lighter)">Click the action button to run...</span>';
  });
  ['pg-discovery-status','pg-catalog-status','pg-checkout-status','pg-tracking-status','pg-review-status'].forEach(function(id) {
    var el = document.getElementById(id);
    el.textContent = 'waiting';
    el.className = 'pg-status pg-status-pending';
  });
  document.getElementById('pg-stream-log').innerHTML = '<span class="ws-info">Click "Connect & Stream" to open the WebSocket...</span>';
  document.getElementById('pg-stream-event').innerHTML = '<span style="color:var(--md-default-fg-color--lighter)">No events yet...</span>';
  pgSetStatus('pg-stream-status', 'disconnected', false);
  var streamBtn = document.getElementById('pg-stream-btn');
  streamBtn.textContent = 'Connect & Stream';
  streamBtn.disabled = false;
}

function pgJson(obj) {
  return JSON.stringify(obj, null, 2);
}

function pgSetStatus(id, text, ok) {
  var el = document.getElementById(id);
  el.textContent = text;
  el.className = 'pg-status ' + (ok ? 'pg-status-ok' : 'pg-status-pending');
}

// --- Data ---
var pgDomainData = {
  food: {
    categories: ['italian','sushi','thai'],
    providers: {
      'pizza-palace': { name: 'Pizza Palace', category: 'italian', rating: 4.7, est: 30, fee: 299, price_level: 'moderate' },
      'sakura-sushi': { name: 'Sakura Sushi', category: 'sushi', rating: 4.5, est: 35, fee: 349, price_level: 'moderate' }
    },
    catalogs: {
      'pizza-palace': {
        provider_name: 'Pizza Palace',
        sections: [{
          id: 'pizzas', title: 'Pizzas',
          items: [{
            id: 'margherita', title: 'Margherita Pizza',
            description: 'Classic tomato, mozzarella, and basil',
            price_cents: 1299, is_available: true,
            modifier_groups: [{
              id: 'size', title: 'Size', required: true,
              min_selections: 1, max_selections: 1,
              options: [
                { id: 'small', label: 'Small', price_delta_cents: 0 },
                { id: 'medium', label: 'Medium', price_delta_cents: 300 },
                { id: 'large', label: 'Large', price_delta_cents: 500 }
              ]
            },{
              id: 'extras', title: 'Extras', required: false,
              max_selections: 3,
              options: [
                { id: 'extra-cheese', label: 'Extra Cheese', price_delta_cents: 150 },
                { id: 'mushrooms', label: 'Mushrooms', price_delta_cents: 100 }
              ]
            }]
          },{
            id: 'pepperoni', title: 'Pepperoni Pizza',
            description: 'Loaded with pepperoni and mozzarella',
            price_cents: 1499, is_available: true,
            modifier_groups: [{
              id: 'size', title: 'Size', required: true,
              min_selections: 1, max_selections: 1,
              options: [
                { id: 'small', label: 'Small', price_delta_cents: 0 },
                { id: 'medium', label: 'Medium', price_delta_cents: 300 },
                { id: 'large', label: 'Large', price_delta_cents: 500 }
              ]
            }]
          }]
        },{
          id: 'drinks', title: 'Drinks',
          items: [{
            id: 'cola', title: 'Cola', description: 'Classic cola drink',
            price_cents: 249, is_available: true, modifier_groups: []
          }]
        }]
      },
      'sakura-sushi': {
        provider_name: 'Sakura Sushi',
        sections: [{
          id: 'rolls', title: 'Signature Rolls',
          items: [{
            id: 'dragon-roll', title: 'Dragon Roll',
            description: 'Eel, avocado, cucumber with unagi sauce',
            price_cents: 1599, is_available: true,
            modifier_groups: [{
              id: 'pieces', title: 'Pieces', required: true,
              min_selections: 1, max_selections: 1,
              options: [
                { id: '8pc', label: '8 pieces', price_delta_cents: 0 },
                { id: '12pc', label: '12 pieces', price_delta_cents: 400 }
              ]
            }]
          },{
            id: 'salmon-nigiri', title: 'Salmon Nigiri (2pc)',
            description: 'Fresh Atlantic salmon over pressed rice',
            price_cents: 699, is_available: true, modifier_groups: []
          }]
        }]
      }
    }
  },
  ride: {
    categories: ['sedan','suv','economy'],
    providers: {
      'city-rides': { name: 'CityRides', category: 'sedan', rating: 4.6, est: 8, fee: 200, price_level: 'moderate' },
      'eco-cab': { name: 'EcoCab', category: 'economy', rating: 4.3, est: 5, fee: 150, price_level: 'budget' }
    }
  },
  travel: {
    categories: ['hotel','resort','hostel'],
    providers: {
      'grand-hotel': { name: 'Grand Hotel SF', category: 'hotel', rating: 4.8, est: 0, fee: 0, price_level: 'luxury' },
      'bay-hostel': { name: 'Bay Area Hostel', category: 'hostel', rating: 4.1, est: 0, fee: 0, price_level: 'budget' }
    }
  }
};

// --- Discovery ---
function pgUpdateDiscovery() {
  var domain = document.getElementById('pg-domain').value;
  var cats = pgDomainData[domain].categories;
  var catSel = document.getElementById('pg-category');
  catSel.innerHTML = '';
  cats.forEach(function(c) {
    var o = document.createElement('option');
    o.value = c; o.textContent = c.charAt(0).toUpperCase() + c.slice(1);
    catSel.appendChild(o);
  });
  var rating = document.getElementById('pg-rating').value;
  var req = {
    filters: {
      location: {
        street_line_1: '123 Main St',
        city: 'San Francisco',
        postal_code: '94105',
        country_code: 'US',
        latitude: 37.7749,
        longitude: -122.4194
      },
      category: cats[0],
      is_open_now: true,
      min_rating: parseFloat(rating)
    }
  };
  document.getElementById('pg-discovery-req').textContent = pgJson(req);
}

function pgRunDiscovery() {
  var domain = document.getElementById('pg-domain').value;
  var cat = document.getElementById('pg-category').value;
  var rating = parseFloat(document.getElementById('pg-rating').value);
  var data = pgDomainData[domain];

  // Update request to reflect current selections
  var req = {
    filters: {
      location: {
        street_line_1: '123 Main St',
        city: 'San Francisco',
        postal_code: '94105',
        country_code: 'US',
        latitude: 37.7749,
        longitude: -122.4194
      },
      category: cat,
      is_open_now: true,
      min_rating: rating
    }
  };
  document.getElementById('pg-discovery-req').textContent = pgJson(req);

  var providers = [];
  Object.keys(data.providers).forEach(function(id) {
    var p = data.providers[id];
    if (p.rating >= rating && p.category === cat) {
      providers.push({
        id: id,
        name: p.name,
        category: p.category,
        rating: p.rating,
        estimated_service_minutes: p.est,
        service_fee_cents: p.fee,
        price_level: p.price_level,
        is_open_now: true
      });
    }
  });

  var res = { providers: providers, total_results: providers.length, has_more: false };
  document.getElementById('pg-discovery-res').textContent = pgJson(res);
  pgSetStatus('pg-discovery-status', '200 OK', true);

  // Update provider dropdown for catalog step
  var provSel = document.getElementById('pg-provider');
  provSel.innerHTML = '';
  providers.forEach(function(p) {
    var o = document.createElement('option');
    o.value = p.id;
    o.textContent = p.name + ' (★ ' + p.rating + ')';
    provSel.appendChild(o);
  });

  // Pre-select first provider and its catalog item
  if (providers.length > 0) {
    var firstId = providers[0].id;
    var firstProv = data.providers[firstId];
    pgSelectedProvider = { id: firstId, name: firstProv.name, fee: firstProv.fee };
    var catalogs = data.catalogs;
    if (catalogs && catalogs[firstId]) {
      pgSelectedItem = pgPickFirstItem(catalogs[firstId].sections);
    } else {
      pgSelectedItem = { id: 'service-1', title: 'Standard Service', price_cents: 1500, modifiers: [], modifier_ids: [], description: 'Standard service' };
    }
  }
}

// --- Catalog ---
function pgUpdateCatalog() {
  var provId = document.getElementById('pg-provider').value;
  var domain = document.getElementById('pg-domain').value;
  var provData = pgDomainData[domain].providers[provId];
  var req = { endpoint: 'GET /catalog/' + provId + '/catalog', headers: { 'Accept': 'application/json' } };
  document.getElementById('pg-catalog-req').textContent = pgJson(req);

  // Update selected provider and item when dropdown changes
  if (provData) {
    pgSelectedProvider = { id: provId, name: provData.name, fee: provData.fee };
    var catalogs = pgDomainData[domain].catalogs;
    if (catalogs && catalogs[provId]) {
      pgSelectedItem = pgPickFirstItem(catalogs[provId].sections);
    } else {
      pgSelectedItem = { id: 'service-1', title: 'Standard Service', price_cents: 1500, modifiers: [], modifier_ids: [], description: 'Standard service' };
    }
  }
}

function pgPickFirstItem(sections) {
  // Pick the first available item from the catalog and select its first modifier option per group
  for (var s = 0; s < sections.length; s++) {
    var items = sections[s].items;
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      if (!item.is_available) continue;
      var totalCents = item.price_cents;
      var modifierIds = [];
      var modifierLabels = [];
      var groups = item.modifier_groups || [];
      for (var g = 0; g < groups.length; g++) {
        var opts = groups[g].options;
        if (opts && opts.length > 0) {
          // Pick last option for required groups (e.g. largest size), first for optional
          var pick = groups[g].required ? opts[opts.length - 1] : opts[0];
          totalCents += pick.price_delta_cents;
          modifierIds.push(pick.id);
          modifierLabels.push(pick.label);
        }
      }
      return { id: item.id, title: item.title, description: item.description, price_cents: totalCents, modifiers: modifierLabels, modifier_ids: modifierIds };
    }
  }
  return null;
}

function pgRunCatalog() {
  var provId = document.getElementById('pg-provider').value;
  var domain = document.getElementById('pg-domain').value;
  var provData = pgDomainData[domain].providers[provId];

  var req = { endpoint: 'GET /catalog/' + provId + '/catalog', headers: { 'Accept': 'application/json' } };
  document.getElementById('pg-catalog-req').textContent = pgJson(req);

  pgSelectedProvider = { id: provId, name: provData.name, fee: provData.fee };

  var catalogs = pgDomainData[domain].catalogs;
  var sections;
  if (catalogs && catalogs[provId]) {
    sections = catalogs[provId].sections;
    var cat = Object.assign({ provider_id: provId }, catalogs[provId]);
    document.getElementById('pg-catalog-res').textContent = pgJson(cat);
  } else {
    sections = [{ id: 'main', title: 'Services', items: [{ id: 'service-1', title: 'Standard Service', price_cents: 1500, is_available: true, modifier_groups: [] }] }];
    document.getElementById('pg-catalog-res').textContent = pgJson({
      provider_id: provId,
      provider_name: provData.name,
      sections: sections
    });
  }

  pgSelectedItem = pgPickFirstItem(sections);
  pgSetStatus('pg-catalog-status', '200 OK', true);
}

// --- Checkout ---
function pgGetItemForCheckout() {
  if (pgSelectedItem) return pgSelectedItem;
  // Default fallback before any catalog is fetched
  return { id: 'margherita', title: 'Margherita Pizza', price_cents: 1949, modifiers: ['Large', 'Extra Cheese'], modifier_ids: ['large', 'extra-cheese'], description: 'Classic tomato, mozzarella, and basil' };
}

function pgGetProviderForCheckout() {
  if (pgSelectedProvider) return pgSelectedProvider;
  return { id: 'pizza-palace', name: 'Pizza Palace', fee: 299 };
}

function pgComputeCheckout() {
  var item = pgGetItemForCheckout();
  var prov = pgGetProviderForCheckout();
  var type = document.getElementById('pg-fulfillment').value;
  var loyalty = document.getElementById('pg-loyalty').value;
  var serviceFee = type === 'delivery' ? prov.fee : 0;
  var subtotal = item.price_cents;
  var discountPercent = loyalty === 'gold' ? 15 : loyalty === 'silver' ? 10 : 0;
  var discountCents = Math.round(subtotal * discountPercent / 100);
  var total = subtotal - discountCents + serviceFee;
  return { item: item, provider: prov, type: type, loyalty: loyalty, serviceFee: serviceFee, subtotal: subtotal, discountPercent: discountPercent, discountCents: discountCents, total: total };
}

function pgUpdateCheckout() {
  var c = pgComputeCheckout();

  var lineItem = {
    item_id: c.item.id,
    title: c.item.title,
    quantity: 1,
    price_cents: c.item.price_cents
  };
  if (c.item.modifier_ids && c.item.modifier_ids.length > 0) {
    lineItem.modifiers = c.item.modifier_ids;
    lineItem.special_instructions = 'As listed';
  }

  var req = {
    line_items: [lineItem],
    fulfillment: {
      type: c.type,
      estimated_service_minutes: c.type === 'delivery' ? 35 : 20,
      service_fee_cents: c.serviceFee,
      address: {
        street_line_1: '123 Main St',
        city: 'San Francisco',
        postal_code: '94105',
        country_code: 'US'
      },
      instructions: c.type === 'delivery' ? 'Leave at the front door' : 'Will pick up in 20 minutes',
      is_asap: true
    }
  };

  if (c.loyalty !== 'none') {
    req.loyalty = {
      loyalty_tier: c.loyalty,
      loyalty_discount_percent: c.discountPercent
    };
  }

  document.getElementById('pg-checkout-req').textContent = pgJson(req);
}

function pgRunCheckout() {
  pgUpdateCheckout();
  var c = pgComputeCheckout();

  var resLineItem = {
    item_id: c.item.id,
    title: c.item.title,
    quantity: 1,
    price_cents: c.item.price_cents
  };
  if (c.item.modifier_ids && c.item.modifier_ids.length > 0) {
    resLineItem.modifiers = c.item.modifier_ids;
  }

  var res = {
    checkout_id: 'chk_' + Math.random().toString(36).substr(2, 9),
    status: 'confirmed',
    order_id: 'ord_' + Math.random().toString(36).substr(2, 9),
    line_items: [resLineItem],
    fulfillment: {
      type: c.type,
      service_fee_cents: c.serviceFee
    },
    subtotal_cents: c.subtotal,
    service_fee_cents: c.serviceFee,
    currency: 'USD'
  };

  if (c.loyalty !== 'none') {
    res.loyalty = {
      loyalty_tier: c.loyalty,
      loyalty_discount_percent: c.discountPercent
    };
    res.loyalty_discount_cents = c.discountCents;
  }

  res.total_cents = c.total;
  res.created_at = new Date().toISOString();

  document.getElementById('pg-checkout-res').textContent = pgJson(res);
  pgSetStatus('pg-checkout-status', '201 Created', true);
}

// --- Order Tracking ---
function pgGetTrackStages() {
  var provName = pgSelectedProvider ? pgSelectedProvider.name : 'Pizza Palace';
  return [
    { status: 'confirmed', label: 'Confirmed', eta: 35, detail: 'Order received by ' + provName },
    { status: 'preparing', label: 'Preparing', eta: 28, detail: provName + ' is preparing your order' },
    { status: 'ready', label: 'Ready', eta: 15, detail: 'Order is ready for pickup by driver' },
    { status: 'en_route', label: 'En Route', eta: 10, detail: 'Driver is on the way to you' },
    { status: 'delivered', label: 'Delivered', eta: 0, detail: 'Order has been delivered. Enjoy!' }
  ];
}

function pgUpdateTracking() {
  var stages = pgGetTrackStages();
  var stage = stages[pgTrackStage];
  var btn = document.getElementById('pg-tracking-btn');
  btn.textContent = 'Simulate: ' + stage.label;
  if (pgTrackStage >= stages.length - 1) {
    btn.textContent = '✓ Order Complete';
    btn.disabled = true;
  } else {
    btn.disabled = false;
  }

  var timeline = stages.slice(0, pgTrackStage).map(function(s) {
    return { status: s.status, detail: s.detail, timestamp: new Date().toISOString() };
  });

  document.getElementById('pg-tracking-res').textContent = pgJson({
    order_id: 'ord_abc123',
    current_status: pgTrackStage > 0 ? stages[pgTrackStage - 1].status : 'pending',
    timeline: timeline.length > 0 ? timeline : '(no updates yet)'
  });

  document.getElementById('pg-tracking-req').textContent = pgJson({
    event: 'order.status_update',
    order_id: 'ord_abc123',
    status: stage.status,
    estimated_minutes_remaining: stage.eta,
    detail: stage.detail,
    timestamp: new Date().toISOString()
  });
}

function pgRunTracking() {
  var stages = pgGetTrackStages();
  if (pgTrackStage >= stages.length) return;

  var stage = stages[pgTrackStage];

  var webhook = {
    event: 'order.status_update',
    order_id: 'ord_abc123',
    status: stage.status,
    estimated_minutes_remaining: stage.eta,
    detail: stage.detail,
    timestamp: new Date().toISOString()
  };
  document.getElementById('pg-tracking-req').textContent = pgJson(webhook);

  pgTrackStage++;

  var timeline = stages.slice(0, pgTrackStage).map(function(s) {
    return { status: s.status, detail: s.detail, timestamp: new Date().toISOString() };
  });

  document.getElementById('pg-tracking-res').textContent = pgJson({
    order_id: 'ord_abc123',
    current_status: stage.status,
    estimated_minutes_remaining: stage.eta,
    timeline: timeline
  });

  pgSetStatus('pg-tracking-status', stage.status, stage.status === 'delivered');

  var btn = document.getElementById('pg-tracking-btn');
  if (pgTrackStage < stages.length) {
    btn.textContent = 'Simulate: ' + stages[pgTrackStage].label;
  } else {
    btn.textContent = '✓ Order Complete';
    btn.disabled = true;
  }
}

// --- Live Streaming ---
function pgStreamLog(cls, text) {
  var log = document.getElementById('pg-stream-log');
  var line = document.createElement('div');
  line.className = cls;
  line.textContent = text;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

function pgRunStream() {
  var btn = document.getElementById('pg-stream-btn');
  btn.textContent = 'Streaming...';
  btn.disabled = true;
  var log = document.getElementById('pg-stream-log');
  log.innerHTML = '';

  // Simulated GPS path (driver approaching delivery address)
  var baseLat = 37.7749;
  var baseLng = -122.4194;
  var path = [
    { lat: baseLat + 0.008, lng: baseLng - 0.006, heading: 180, speed: 32 },
    { lat: baseLat + 0.006, lng: baseLng - 0.004, heading: 200, speed: 28 },
    { lat: baseLat + 0.004, lng: baseLng - 0.003, heading: 210, speed: 25 },
    { lat: baseLat + 0.003, lng: baseLng - 0.002, heading: 190, speed: 30 },
    { lat: baseLat + 0.002, lng: baseLng - 0.001, heading: 175, speed: 22 },
    { lat: baseLat + 0.001, lng: baseLng, heading: 160, speed: 15 },
    { lat: baseLat + 0.0003, lng: baseLng + 0.0001, heading: 150, speed: 5 }
  ];

  var events = [];
  var orderId = 'ord_abc123';
  var now = new Date();

  // 1. Connection opened
  events.push({ delay: 300, action: function() {
    pgStreamLog('ws-info', '--- WebSocket opened to wss://api.example.com/asp/v1/ws ---');
    pgSetStatus('pg-stream-status', 'connected', true);
  }});

  // 2. Client sends subscribe
  var subscribeMsg = { action: 'subscribe', order_id: orderId, token: 'Bearer eyJ...' };
  events.push({ delay: 600, action: function() {
    pgStreamLog('ws-send', '► SEND: ' + JSON.stringify(subscribeMsg));
  }});

  // 3. Server sends status snapshot (en_route)
  var snapshot = {
    event_type: 'status_changed',
    order_id: orderId,
    payload: { status: 'en_route', previous_status: 'ready', estimated_service_minutes: 12, updated_at: new Date(now.getTime()).toISOString() },
    timestamp: new Date(now.getTime()).toISOString()
  };
  events.push({ delay: 1000, action: function() {
    pgStreamLog('ws-recv', '◄ RECV: ' + JSON.stringify(snapshot));
    document.getElementById('pg-stream-event').textContent = pgJson(snapshot);
    pgSetStatus('pg-stream-status', 'en_route', true);
  }});

  // 4. Location updates along the path
  for (var i = 0; i < path.length; i++) {
    (function(idx) {
      var eta = Math.max(1, 12 - idx * 2);
      var ts = new Date(now.getTime() + (idx + 1) * 4000).toISOString();
      var locEvent = {
        event_type: 'location_update',
        order_id: orderId,
        payload: {
          status: 'en_route',
          agent_location: {
            latitude: Math.round(path[idx].lat * 10000) / 10000,
            longitude: Math.round(path[idx].lng * 10000) / 10000,
            heading: path[idx].heading,
            speed_kmh: path[idx].speed
          },
          estimated_service_minutes: eta,
          updated_at: ts
        },
        timestamp: ts
      };
      events.push({ delay: 1800 + idx * 800, action: function() {
        pgStreamLog('ws-recv', '◄ RECV: ' + JSON.stringify(locEvent));
        document.getElementById('pg-stream-event').textContent = pgJson(locEvent);
      }});
    })(i);
  }

  // 5. Heartbeat
  var heartbeatDelay = 1800 + 3 * 800;
  events.push({ delay: heartbeatDelay, action: function() {
    var hb = { event_type: 'heartbeat', timestamp: new Date().toISOString() };
    pgStreamLog('ws-recv', '◄ RECV: ' + JSON.stringify(hb));
  }});

  // 6. Final status_changed → completed
  var finalDelay = 1800 + path.length * 800 + 500;
  var completedEvent = {
    event_type: 'status_changed',
    order_id: orderId,
    payload: { status: 'completed', previous_status: 'en_route', estimated_service_minutes: 0, updated_at: new Date(now.getTime() + 60000).toISOString() },
    timestamp: new Date(now.getTime() + 60000).toISOString()
  };
  events.push({ delay: finalDelay, action: function() {
    pgStreamLog('ws-recv', '◄ RECV: ' + JSON.stringify(completedEvent));
    document.getElementById('pg-stream-event').textContent = pgJson(completedEvent);
    pgSetStatus('pg-stream-status', 'completed', true);
  }});

  // 7. Connection closed
  events.push({ delay: finalDelay + 600, action: function() {
    pgStreamLog('ws-close', '--- WebSocket closed (code: 1000, reason: order completed) ---');
    btn.textContent = 'Stream Complete';
  }});

  // Schedule all events
  events.forEach(function(evt) {
    pgStreamTimer = setTimeout(evt.action, evt.delay);
  });
}

// --- Review ---
function pgUpdateReview() {
  var rating = parseInt(document.getElementById('pg-review-rating').value);
  var prov = pgGetProviderForCheckout();
  var req = {
    order_id: 'ord_abc123',
    provider_id: prov.id,
    rating: rating,
    comment: rating >= 4 ? 'Great food, fast delivery!' : 'Could be better.',
    scores: { food: Math.min(5, rating + 1), delivery: rating }
  };
  document.getElementById('pg-review-req').textContent = pgJson(req);
}

function pgRunReview() {
  pgUpdateReview();
  var rating = parseInt(document.getElementById('pg-review-rating').value);
  var prov = pgGetProviderForCheckout();
  var res = {
    id: 'rev_' + Math.random().toString(36).substr(2, 9),
    order_id: 'ord_abc123',
    provider_id: prov.id,
    rating: rating,
    comment: rating >= 4 ? 'Great food, fast delivery!' : 'Could be better.',
    scores: { food: Math.min(5, rating + 1), delivery: rating },
    created_at: new Date().toISOString()
  };
  document.getElementById('pg-review-res').textContent = pgJson(res);
  pgSetStatus('pg-review-status', '201 Created', true);
}

// --- Init ---
document.addEventListener('DOMContentLoaded', function() {
  pgUpdateDiscovery();
  pgUpdateCatalog();
  pgUpdateCheckout();
  pgUpdateTracking();
  pgUpdateReview();
});
// Also run immediately in case DOM is already loaded
if (document.readyState !== 'loading') {
  pgUpdateDiscovery();
  pgUpdateCatalog();
  pgUpdateCheckout();
  pgUpdateTracking();
  pgUpdateReview();
}
</script>

---

## How It Works

This playground simulates the six core steps of an ASP transaction:

| Step | Capability | What Happens |
|------|-----------|--------------|
| **Discovery** | `dev.asp.services.discovery` | Agent searches for providers by location, category, and rating |
| **Catalog** | `dev.asp.services.catalog` | Agent fetches the provider's menu with items and customization options |
| **Checkout** | `dev.asp.services.fulfillment` | Agent creates a UCP checkout extended with ASP fulfillment details |
| **Tracking** | `dev.asp.services.order_tracking` | Marketplace pushes status updates via webhooks |
| **Live Stream** | `dev.asp.services.streaming` | WebSocket connection streams GPS location updates in real-time |
| **Review** | `dev.asp.services.reviews` | Agent submits a post-service review with rating and category scores |

All messages follow the ASP specification schemas. See the [Specification Overview](specification/overview.md) for the full protocol details.
