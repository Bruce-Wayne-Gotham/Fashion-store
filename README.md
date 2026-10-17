# Gotham Edit — affiliate fashion storefront

A static, Apple-style product page that sends visitors to Myntra, Amazon and AJIO through your affiliate links.

- Frosted-glass sticky nav, scroll progress bar
- Hero with floating parallax image collage and animated gradient glow
- Brand marquee
- Scroll-driven "expanding image" section (Apple product-page style)
- Store segmented control + category chips with animated filtering
- 3D tilt + spotlight hover on product cards
- "Trending deals" snap carousel (sorted by biggest discount)
- Store tiles linking to your store-level affiliate links
- Light/dark mode, `prefers-reduced-motion` support, mobile layout
- Affiliate disclosure in the footer (required by Amazon Associates)

No build step and no dependencies — just HTML, CSS and JS.

## Add your affiliate links

Everything you need to edit is in **`products.js`**:

| Setting | What to put there |
| --- | --- |
| `AMAZON_TAG` | Your Amazon Associates tracking ID (e.g. `yourname-21`). It's added to every amazon.in link that doesn't already have a `tag`. |
| `STORES.*.url` | Your store-level affiliate link for Myntra, Amazon and AJIO. |
| `PRODUCTS[].url` | The affiliate deep link for each product (Amazon SiteStripe, or Myntra/AJIO links from EarnKaro, Cuelinks, Admitad, etc.). |
| `PRODUCTS[].image` | The product photo URL. Placeholder Unsplash photos are used until you swap them. |

Add or remove products by copying an entry in `PRODUCTS`. `store` must be `myntra`, `amazon` or `ajio`; `category` can be anything — the filter chips are generated from it.

All outbound links open in a new tab with `rel="sponsored noopener noreferrer"`.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

Push to GitHub and enable **Settings → Pages → Deploy from branch** (root). Netlify, Vercel or Cloudflare Pages also work with zero config.
