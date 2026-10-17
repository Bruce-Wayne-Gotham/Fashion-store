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

## AI product images

Myntra and AJIO products load AI images from `images/ai/`. Until a file exists, the card shows its bundled illustration (`art` in `products.js`). Prompts live in `tools/ai-image-prompts.json`.

**Generate them with GitHub Actions:** open the **Actions** tab, choose **Generate AI images**, then **Run workflow**. New images are committed to `images/ai/` and the site redeploys automatically.

| Provider | Secret (Settings → Secrets and variables → Actions) | Notes |
| --- | --- | --- |
| `huggingface` | `HF_TOKEN` (free at huggingface.co/settings/tokens, "Make calls to Inference Providers" permission) | FLUX.1 [schnell]. Free monthly credits. |
| `pollinations` | `POLLINATIONS_API_KEY` *(from enter.pollinations.ai)* | Free. Without a key it still runs if chosen explicitly, but images are watermarked and often ignore the prompt, so they aren't fit for the site. |
| `gemini` | `GEMINI_API_KEY` | Requires billing on the Google project. |
| `auto` *(default)* | n/a | Hugging Face if `HF_TOKEN` is set, then Pollinations if `POLLINATIONS_API_KEY` is set. |

Workflow fields: **names** limits the run to specific images (e.g. `wrap-dress`). **force** regenerates existing images.

Run it locally instead:
```bash
pip install huggingface_hub pillow
export HF_TOKEN=...          # optional
python3 tools/generate-ai-images.py [--provider pollinations] [names...]
```

Amazon products keep illustrations. Use Amazon's own product photos for those (Associates rules). AI images won't exactly match the real item, so make sure each picture is close to the product being sold.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

The site deploys automatically to GitHub Pages via `.github/workflows/deploy-pages.yml` on every push to the branch, and again after the AI image workflow runs.

**Live URL:** https://bruce-wayne-gotham.github.io/Fashion-store/

If the first deploy fails with a Pages "not enabled" error, open **Settings → Pages**, set **Source** to **GitHub Actions**, then re-run the workflow.
