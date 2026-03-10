# Horizon GA4 Data Layer Integration

A guide to wiring the Horizon embed API to a Google Analytics 4 ecommerce `dataLayer` via Google Tag Manager.

---

## Overview

The Horizon embed (`<ip-embed-leaflet>`) exposes a JavaScript API you can use to listen for user interactions — such as clicking an offer — and forward structured ecommerce events to `window.dataLayer`. GTM picks those events up and sends them to GA4.

```
User clicks offer
     │
     ▼
Horizon embed API  ──►  mapOfferToEcommerce()  ──►  dataLayer.push()
                                                          │
                                                          ▼
                                                   Google Tag Manager
                                                          │
                                                          ▼
                                                    Google Analytics 4
```

---

## Prerequisites

- A **GTM container** with a GA4 configuration tag already set up.
- Access to add scripts to your page's `<head>`.
- Your Horizon **alias** (e.g. `mystore/mystorefront`).

---

## Step 1 — Install Google Tag Manager

Paste the GTM snippet into the `<head>` and `<body>` of every page. Replace `GTM-XXXXXXXX` with your container ID.

```html
<!-- ① Paste inside <head>, as high as possible -->
<script>
  (function (w, d, s, l, i) {
    w[l] = w[l] || [];
    w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var f = d.getElementsByTagName(s)[0],
        j = d.createElement(s),
        dl = l != "dataLayer" ? "&l=" + l : "";
    j.async = true;
    j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
    f.parentNode.insertBefore(j, f);
  })(window, document, "script", "dataLayer", "GTM-XXXXXXXX");
</script>

<!-- ② Paste immediately after the opening <body> tag -->
<noscript>
  <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXXX"
    height="0" width="0" style="display:none;visibility:hidden"></iframe>
</noscript>
```

---

## Step 2 — Add the Horizon embed component

Place the web component anywhere in your `<body>`, and load the embed script once at the bottom of the page.

```html
<!-- Horizon embed -->
<ip-embed-leaflet
  id="horizon"
  alias="mystore/mystorefront"
></ip-embed-leaflet>

<!-- Load the embed bundle once, at the end of <body> -->
<script defer src="https://embed.ipaper.io/web.js" type="module"></script>
```

> **Note:** `defer` + `type="module"` ensures the bundle loads without blocking page render.

---

## Step 3 — Initialise tracking

Add the following script block to your `<head>` (after GTM). It waits for the DOM and the Horizon component to be ready, then subscribes to content events.

```html
<script>
  // Returns a Promise that resolves once the Horizon element fires "ready".
  function whenHorizonReady(horizonEl) {
    if (!horizonEl) return Promise.reject(new Error("No horizon element found"));
    if (horizonEl.getAttribute("ready") === "true") return Promise.resolve(true);
    return new Promise((resolve) => {
      horizonEl.addEventListener("ready", () => resolve(true), { once: true });
    });
  }

  // Pushes an object to window.dataLayer.
  function dlPush(obj) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(obj);
  }

  // Prevents the subscription being registered more than once (e.g. in SPAs).
  function ensureSingleInit(key) {
    window.__horizonInit = window.__horizonInit || {};
    if (window.__horizonInit[key]) return false;
    window.__horizonInit[key] = true;
    return true;
  }

  // Converts a raw Horizon offer object into a GA4-compatible ecommerce payload.
  function mapOfferToEcommerce(offer, alias) {
    const products = Array.isArray(offer.products) ? offer.products : [];
    // Horizon prices are in micro-units; divide by 1 000 000 for real currency.
    const toGA4Price = (v) => typeof v === "number" ? v / 1_000_000 : null;
    const offerPrice = offer.sales_price ? toGA4Price(offer.sales_price.value) : null;

    return {
      item_list_id:   offer.contentGuid || null,
      item_list_name: offer.header      || null,
      value:    offerPrice,
      currency: "DKK",           // ← update to match your currency
      items: products.map((p, index) => {
        const price     = p.price      ? toGA4Price(p.price.value)      : null;
        const salePrice = p.sale_price ? toGA4Price(p.sale_price.value) : null;
        return {
          index,
          item_id:        p.sku   || null,
          item_name:      p.title || null,
          item_brand:     p.brand || null,
          price,
          discount: price !== null && salePrice !== null
            ? parseFloat((price - salePrice).toFixed(2))
            : null,
          quantity:       1,
          item_list_id:   offer.contentGuid || null,
          item_list_name: offer.header      || null,
          affiliation:    alias             || null,
        };
      }),
    };
  }

  async function initHorizonToDataLayer() {
    if (!ensureSingleInit("content-subscribe")) return;

    const horizonEl = document.getElementById("horizon");
    await whenHorizonReady(horizonEl);

    const alias = horizonEl.getAttribute("alias") || null;
    const api   = await horizonEl.getApi();

    const subscription = api.content.subscribe((contentEvent) => {
      if (!contentEvent) return;
      const { action, source, value: c } = contentEvent;

      // Filter: only track offer clicks
      if (!c || c.$type !== "offer" || action !== "click") return;

      const ecommerce = mapOfferToEcommerce(c, alias);

      // GA4 requires clearing ecommerce before each push to prevent data bleed.
      (window.dataLayer = window.dataLayer || []).push({ ecommerce: null });

      dlPush({
        event:            "select_item",
        horizon_alias:    alias,
        horizon_source:   source || null,  // "content" | "price" | "splash" | "cta"
        ecommerce,
      });
    });

    // Expose cleanup function for SPAs
    window.__horizonUnsubscribe = () => subscription?.unsubscribe?.();
  }

  document.addEventListener("DOMContentLoaded", () => {
    initHorizonToDataLayer().catch((err) => {
      dlPush({ event: "horizon_init_error", message: String(err?.message ?? err) });
      console.error(err);
    });
  });
</script>
```

---

## API Reference

### `whenHorizonReady(element)`

Resolves when the Horizon web component has finished bootstrapping. Safe to call at any time — if the component is already ready it resolves immediately.

| Parameter | Type          | Description                              |
|-----------|---------------|------------------------------------------|
| `element` | `HTMLElement` | The `<ip-embed-leaflet>` DOM node.       |
| **Returns** | `Promise<true>` |                                        |

---

### `element.getApi()`

Async method exposed by the Horizon web component. Returns the top-level API object once the embed is initialised.

```js
const api = await horizonEl.getApi();
```

| Returns               | Description                                               |
|-----------------------|-----------------------------------------------------------|
| `Promise<HorizonApi>` | Resolves to the Horizon API object. Contains the `content` namespace. |

---

### `api.content.subscribe(callback)`

Registers a listener that fires on every content interaction event inside the embed.

```js
const subscription = api.content.subscribe((contentEvent) => {
  const { action, source, value } = contentEvent;
  // action: "click" | "hover" | ...
  // source: "content" | "price" | "splash" | "cta"
  // value:  the content object (offer, article, etc.)
});

// To stop listening:
subscription.unsubscribe();
```

| Field              | Type     | Description                                                                 |
|--------------------|----------|-----------------------------------------------------------------------------|
| `action`           | `string` | `"click"`, `"hover"`, or other interaction verbs.                          |
| `source`           | `string` | Clickable zone: `"content"`, `"price"`, `"splash"`, or `"cta"`.           |
| `value.$type`      | `string` | Content type — track `"offer"` for ecommerce events.                       |
| `value.contentGuid`| `string` | Unique identifier of the offer (maps to GA4 `item_list_id`).               |
| `value.header`     | `string` | Offer title (maps to GA4 `item_list_name`).                                |
| `value.sales_price.value` | `number` | Offer-level price in **micro-units**. Divide by 1,000,000.       |
| `value.products`   | `Product[]` | Line items within the offer.                                            |

---

### `mapOfferToEcommerce(offer, alias)`

Converts a raw Horizon offer object into a GA4-compatible ecommerce payload.

| Parameter | Type            | Description                                                     |
|-----------|-----------------|-----------------------------------------------------------------|
| `offer`   | `object`        | The `value` from the content event (`$type === "offer"`).       |
| `alias`   | `string \| null`| The Horizon alias. Stored as `affiliation` on each GA4 item.   |
| **Returns** | GA4 `ecommerce` object ready to push to `dataLayer`. |         |

---

## dataLayer Events

### `select_item` — offer click

Fired when a user clicks an offer inside the embed.

```json
{
  "event":          "select_item",
  "horizon_alias":  "mystore/mystorefront",
  "horizon_source": "cta",
  "ecommerce": {
    "item_list_id":   "abc123",
    "item_list_name": "Summer Deals",
    "value":          49.95,
    "currency":       "DKK",
    "items": [
      {
        "index":          0,
        "item_id":        "SKU-001",
        "item_name":      "Wireless Headphones",
        "item_brand":     "SoundBrand",
        "price":          499.00,
        "discount":       49.05,
        "quantity":       1,
        "item_list_id":   "abc123",
        "item_list_name": "Summer Deals",
        "affiliation":    "mystore/mystorefront"
      }
    ]
  }
}
```

`horizon_source` possible values:

| Value       | Description                        |
|-------------|------------------------------------|
| `"content"` | Clicked on the main content area.  |
| `"price"`   | Clicked on the price element.      |
| `"splash"`  | Clicked on a splash/banner.        |
| `"cta"`     | Clicked a call-to-action button.   |

---

### `horizon_init_error` — initialisation failure

Pushed if `initHorizonToDataLayer()` throws. Use this event in GTM to trigger error-monitoring tags.

```json
{
  "event":   "horizon_init_error",
  "message": "No horizon element found"
}
```

---

## Price Units

All price values from the Horizon API are in **micro-units** (multiplied by 1,000,000). Always divide by 1,000,000 before pushing to `dataLayer`.

> **Warning:** Pushing raw micro-unit values to GA4 inflates revenue reports by a factor of one million.

```js
// Horizon raw value  →  GA4 price
// 49950000           →  49.95
// 100000000          →  100.00

const toGA4Price = (v) => typeof v === "number" ? v / 1_000_000 : null;
```

---

## Preventing Double-Init

In single-page applications (SPAs), scripts may re-run on navigation. The `ensureSingleInit(key)` guard writes a flag to `window.__horizonInit` so the subscription is only registered once per page lifecycle.

```js
function ensureSingleInit(key) {
  window.__horizonInit = window.__horizonInit || {};
  if (window.__horizonInit[key]) return false; // already initialised
  window.__horizonInit[key] = true;
  return true;
}
```

---

## Cleanup / Unsubscribe

To tear down the listener (e.g. before a route change in an SPA):

```js
window.__horizonUnsubscribe?.();
```

> **Tip:** After calling `__horizonUnsubscribe()`, also reset `window.__horizonInit["content-subscribe"]` to `false` if you want `initHorizonToDataLayer()` to be callable again on the same page.

---

## Error Handling

The init function is async and wrapped in a `.catch()`. Unhandled errors are pushed to `dataLayer` as `horizon_init_error` events so they surface in GTM's debug preview.

```js
document.addEventListener("DOMContentLoaded", () => {
  initHorizonToDataLayer().catch((err) => {
    dlPush({ event: "horizon_init_error", message: String(err?.message ?? err) });
    console.error(err);
  });
});
```

Common error causes:

| Message                     | Cause                                                                                  |
|-----------------------------|----------------------------------------------------------------------------------------|
| `No horizon element found`  | `getElementById("horizon")` returned `null`. Check the element ID and script order.   |
| `getApi is not a function`  | The embed script (`web.js`) has not loaded. Ensure it is included and not blocked.    |
