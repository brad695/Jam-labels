# Greys Label Studio

A single-page label maker for **Greys Fine Cheese** (Memphis, TN) — jams, mustards
and dressings. Replaces the old Python CSV workflow with one self-contained
HTML page: no install, no server code, works offline.

## What it does

Pick a product in the sidebar, edit anything, watch the label redraw live, and
export a print-ready **1800 × 600 PNG** per flavor.

The page handles:

**Label layout** — brand wordmark (League Spartan), flavor title in small caps
with per-product accent color (Liberation Sans), price, address block, tagline,
jar size, and QR code.

**UPC-A barcodes** — full 12-digit codes rendered exactly as entered; 11-digit
codes get the check digit computed and appended, leading zeros are preserved,
and an invalid check digit shows a warning before it ever reaches a scanner.

**Nutrition Facts** — an FDA-style panel drawn to match the printed labels.
The *Auto Nutrition* section estimates the whole panel from the label's
ingredient list alone: list order implies descending weight, jam-type products
use standard preserve fruit-to-sugar ratios, minor ingredients (herbs, spices,
salt, pectin) get typical pinch-sized fractions, and everything is rounded per
FDA labeling rules. Estimates only — verify before a production print run.

**Data** — products live inside the HTML file itself. The **Save page** button
downloads an updated copy of the page with your edits baked in; swap it in for
the old file (or commit it here as the new `index.html`).

## Running it

Open `index.html` in any browser. That's the whole deployment story — the
fonts, QR code and product data are embedded in the file.

Hosted on Render as a static site via `render.yaml`.

## Development

`build/` contains the un-baked `template.html` (with `__PLACEHOLDER__` slots),
the raw assets, `products.json`, and `build.py` which bakes them into
`index.html`:

```
python3 build/build.py               # bake from build/products.json
python3 build/build.py saved.html    # bake, pulling products from a saved page
```

Edit `template.html` for layout/logic changes, then rebuild. The ingredient
nutrition database (`ING_DB`) and label renderer live in the template's script
block.
