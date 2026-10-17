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
| `PRODUCTS[].image` | A product photo URL from the store, or a bundled illustration from `images/` (the default). Illustrations ship with the repo so the page always has visuals; regenerate them with `python3 tools/generate-illustrations.py images`. |

Add or remove products by copying an entry in `PRODUCTS`. `store` must be `myntra`, `amazon` or `ajio`; `category` can be anything — the filter chips are generated from it.

All outbound links open in a new tab with `rel="sponsored noopener noreferrer"`.

## AI product images (Myntra & AJIO)

Myntra and AJIO products load AI images from `images/ai/`. Until those files exist, each card shows its bundled illustration (`art` in `products.js`). Amazon products keep illustrations. Swap in Amazon's own product photos (SiteStripe / PA-API) rather than AI images, because Amazon Associates requires them.

**Option A: AI Studio website (no code)**
1. Open [aistudio.google.com](https://aistudio.google.com) and choose an image-generation model.
2. For each entry in `tools/ai-image-prompts.json`, paste the item prompt followed by the `style` line.
3. Download each result as `images/ai/<name>.png` (e.g. `images/ai/denim-jacket.png`).

**Option B: script (all 8 in one go)**
```bash
pip install google-genai
export GEMINI_API_KEY="your key from https://aistudio.google.com/apikey"
python3 tools/generate-ai-images.py                       # creates missing images
python3 tools/generate-ai-images.py wrap-dress            # redo one you don't like
python3 tools/generate-ai-images.py --model <newer-model> # pick a newer image model
```

Then commit the `images/ai/` folder. Never commit your API key.

Tip: AI images won't exactly match the item being sold. Make sure each picture is close to the real product so shoppers aren't surprised.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

Push to GitHub and enable **Settings → Pages → Deploy from branch** (root). Netlify, Vercel or Cloudflare Pages also work with zero config.
