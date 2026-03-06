#!/usr/bin/env node
/**
 * Bundles ASP JSON Schemas into a single resolved schema for Pydantic generation.
 *
 * Uses @apidevtools/json-schema-ref-parser with a custom resolver so that:
 *   - Relative refs (./types/..., ../shared/...) resolve from spec/schemas/
 *   - https://ucp.dev/... refs are fetched (with a fix for known-broken UCP URLs)
 *
 * Output: generated/schemas_bundle.json — one schema with internal $ref only,
 * suitable for datamodel-code-generator (Pydantic).
 */

import $RefParser from "@apidevtools/json-schema-ref-parser";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { join, resolve } from "node:path";

const ROOT = resolve(import.meta.dirname, "..");
const SCHEMA_DIR = join(ROOT, "spec", "schemas");
const GENERATED_DIR = join(ROOT, "generated");
const BUNDLE_ENTRY = join(GENERATED_DIR, "bundle_entry.json");
const BUNDLE_OUT = join(GENERATED_DIR, "schemas_bundle.json");

// Workaround: ucp.dev sometimes references "https://ucp.dev/services/service.json"
// but the correct URL is "https://ucp.dev/schemas/service.json".
const UCP_URL_FIXES = {
  "https://ucp.dev/services/service.json":
    "https://ucp.dev/schemas/service.json",
};

const ucpFixResolver = {
  order: 1,
  canRead(file) {
    const url = typeof file === "string" ? file : file.url;
    return !!UCP_URL_FIXES[url];
  },
  async read(file) {
    const url = typeof file === "string" ? file : file.url;
    const target = UCP_URL_FIXES[url];
    const resp = await fetch(target);
    if (!resp.ok) throw new Error(`HTTP ${resp.status} for ${target}`);
    return resp.text();
  },
};

/**
 * Entry schema that references all capability schemas so the bundle pulls in
 * the full graph (including UCP refs from fulfillment and order_tracking).
 */
const bundleEntry = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  $id: "bundle-entry",
  title: "ASP Schema Bundle",
  description: "Resolved bundle of all ASP schemas for code generation.",
  type: "object",
  $defs: {
    Discovery: { $ref: "../spec/schemas/services/discovery.json" },
    Catalog: { $ref: "../spec/schemas/services/catalog.json" },
    Fulfillment: { $ref: "../spec/schemas/services/fulfillment.json" },
    OrderTracking: { $ref: "../spec/schemas/services/order_tracking.json" },
    Reviews: { $ref: "../spec/schemas/services/reviews.json" },
    Streaming: { $ref: "../spec/schemas/services/streaming.json" },
    Personalization: { $ref: "../spec/schemas/services/personalization.json" },
    Asp: { $ref: "../spec/schemas/asp.json" },
    Capability: { $ref: "../spec/schemas/capability.json" },
  },
};

async function main() {
  await mkdir(GENERATED_DIR, { recursive: true });
  await writeFile(
    BUNDLE_ENTRY,
    JSON.stringify(bundleEntry, null, 2),
    "utf-8",
  );

  console.log("Bundling schemas (resolving $refs, including UCP)...");
  const bundled = await $RefParser.bundle(BUNDLE_ENTRY, {
    resolve: {
      ucpFix: ucpFixResolver,
    },
  });

  // datamodel-code-generator treats refs like "bundle-entry#/..." as file paths.
  // Rewrite to same-document refs "#/...". Fix any "#//" (invalid) to "#/".
  let bundledStr = JSON.stringify(bundled, null, 2);
  bundledStr = bundledStr.replace(/"bundle-entry#/g, '"#/').replace(/"#\/\//g, '"#/');
  const parsed = JSON.parse(bundledStr);
  parsed.$id = "./schemas/bundle.json";

  // Flatten nested $defs to root so datamodel-code-generator emits models for all types.
  // Root has $defs.Discovery, $defs.Catalog, ... each with $defs.search_request, etc.
  // We hoist Discovery__search_request, Discovery__search_response, etc. to root.$defs
  // and rewrite refs so the generator sees every definition.
  const flatDefs = {};
  const pathToFlat = new Map(); // "/$defs/Discovery/$defs/search_request" -> "Discovery__search_request"

  function collectDefs(obj, pathSegments, pathStr) {
    if (!obj || typeof obj !== "object" || !obj.$defs) return;
    for (const [k, v] of Object.entries(obj.$defs)) {
      const segs = [...pathSegments, k];
      const flatName = segs.join("__");
      const p = `${pathStr}/$defs/${k}`;
      pathToFlat.set(p, flatName);
      flatDefs[flatName] = v;
      collectDefs(v, segs, p);
    }
  }

  for (const [key, val] of Object.entries(parsed.$defs || {})) {
    if (val && typeof val === "object" && val.$defs) {
      collectDefs(val, [key], `/$defs/${key}`);
    } else {
      flatDefs[key] = val;
    }
  }

  // Sort ref paths by length descending so we replace longest first
  const sortedPaths = [...pathToFlat.entries()].sort((a, b) => b[0].length - a[0].length);

  function rewriteRefs(obj) {
    if (!obj || typeof obj !== "object") return;
    if (Array.isArray(obj)) {
      obj.forEach(rewriteRefs);
      return;
    }
    if (obj.$ref && typeof obj.$ref === "string" && obj.$ref.startsWith("#/")) {
      const r = obj.$ref.slice(1); // strip "#" -> "/$defs/..."
      for (const [path, flatName] of sortedPaths) {
        if (r === path || r.startsWith(`${path}/`)) {
          obj.$ref = `#/$defs/${flatName}${r.slice(path.length)}`;
          break;
        }
      }
    }
    for (const v of Object.values(obj)) {
      if (v && typeof v === "object") rewriteRefs(v);
    }
  }

  rewriteRefs(flatDefs);
  parsed.$defs = flatDefs;

  await writeFile(BUNDLE_OUT, JSON.stringify(parsed, null, 2), "utf-8");
  console.log(`Wrote ${BUNDLE_OUT}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
