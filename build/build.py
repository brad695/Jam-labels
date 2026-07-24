#!/usr/bin/env python3
"""Build index.html from template.html + assets + products.json.

The app itself stores product data inside index.html ("Save page" button).
This build script exists for development: editing the template (layout, fonts,
ingredient database) and re-baking a fresh index.html.

Usage:  python3 build/build.py            (run from the repo root)
        python3 build/build.py mypage.html  (re-bake using products from an
                                             existing saved page instead of
                                             build/products.json)
"""
import base64, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
ASSETS = os.path.join(BUILD, "assets")

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def upc_check(d11):
    odd = sum(int(d11[i]) for i in range(0, 11, 2))
    even = sum(int(d11[i]) for i in range(1, 11, 2))
    return (10 - ((odd * 3 + even) % 10)) % 10

def norm_upc(v):
    d = "".join(ch for ch in str(v) if ch.isdigit())
    if len(d) >= 12:
        return d[:12]
    d = d.zfill(11)
    return d + str(upc_check(d))

def load_products():
    if len(sys.argv) > 1:  # pull products back out of a saved page
        html = open(sys.argv[1], encoding="utf-8").read()
        m = re.search(r'<script type="application/json" id="productData">(.*?)</script>',
                      html, re.S)
        return json.loads(m.group(1))
    return json.load(open(os.path.join(BUILD, "products.json"), encoding="utf-8"))

def main():
    tpl = open(os.path.join(BUILD, "template.html"), encoding="utf-8").read()
    products = load_products()
    for p in products:
        p.setdefault("Unit", "6 oz.")
        p["Price"] = p.get("Price", "").strip()
        p["UPC"] = norm_upc(p.get("UPC", ""))
    pj = json.dumps(products, indent=1).replace("<", "\\u003c")
    out = (tpl
           .replace("__TITLE_B64__", b64(os.path.join(ASSETS, "LiberationSansRegular.ttf")))
           .replace("__SPARTAN_B64__", b64(os.path.join(ASSETS, "league-spartan-700.woff2")))
           .replace("__QR_B64__", b64(os.path.join(ASSETS, "qr_code.png")))
           .replace("__PRODUCTS_JSON__", pj))
    dest = os.path.join(ROOT, "index.html")
    open(dest, "w", encoding="utf-8").write(out)
    print(f"built {dest} ({len(out):,} bytes, {len(products)} products)")

if __name__ == "__main__":
    main()
