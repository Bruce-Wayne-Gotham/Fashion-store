"""Generate product images from tools/ai-image-prompts.json.

Providers (pick with --provider, default "auto"):
  huggingface  FLUX.1 [schnell] via Hugging Face Inference Providers.
               Needs HF_TOKEN (free account → huggingface.co/settings/tokens).
  pollinations Pollinations.ai FLUX. Uses POLLINATIONS_API_KEY if set
               (enter.pollinations.ai), otherwise the keyless endpoint.
  gemini       Google Gemini image model. Needs GEMINI_API_KEY with billing.
  auto         Hugging Face if HF_TOKEN is set, falling back to Pollinations
               for any image that fails (only with POLLINATIONS_API_KEY — the
               keyless tier watermarks images and ignores product-only prompts).

Setup:
    pip install huggingface_hub pillow          # + google-genai for gemini

Run from the repo root:
    python3 tools/generate-ai-images.py                       # all missing images
    python3 tools/generate-ai-images.py denim-jacket          # just one (overwrites)
    python3 tools/generate-ai-images.py --force               # regenerate everything
    python3 tools/generate-ai-images.py --provider pollinations

Images are saved to images/ai/<name>.png. The page picks them up automatically;
until a file exists the card shows its bundled illustration instead.
"""
import argparse
import io
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "tools" / "ai-image-prompts.json"
OUT_DIR = ROOT / "images" / "ai"
WIDTH, HEIGHT = 896, 1120  # 4:5, multiples of 16 for FLUX
HF_MODEL = os.environ.get("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
HF_PROVIDER = os.environ.get("HF_PROVIDER") or "auto"  # e.g. hf-inference, fal-ai, nscale, together
GEMINI_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")


def to_png(data):
    from PIL import Image

    img = Image.open(io.BytesIO(data))
    img.load()
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "PNG", optimize=True)
    return buf.getvalue()


def huggingface(prompt):
    from huggingface_hub import InferenceClient

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is not set")
    client = InferenceClient(provider=HF_PROVIDER, api_key=token)
    image = client.text_to_image(prompt, model=HF_MODEL, width=WIDTH, height=HEIGHT)
    buf = io.BytesIO()
    image.save(buf, "PNG")
    return buf.getvalue()


def _fetch_image(url, headers):
    req = urllib.request.Request(url, headers={"User-Agent": "fashion-store-image-generator", **headers})
    with urllib.request.urlopen(req, timeout=180) as resp:
        ctype = resp.headers.get("Content-Type", "")
        data = resp.read()
    if not ctype.startswith("image/"):
        raise RuntimeError(f"expected an image, got {ctype or 'unknown'}: {data[:200]!r}")
    return data


def pollinations(prompt):
    params = {"width": WIDTH, "height": HEIGHT, "model": "flux", "nologo": "true", "seed": random.randint(1, 10**6)}
    path = urllib.parse.quote(prompt, safe="")
    key = os.environ.get("POLLINATIONS_API_KEY")
    endpoints = []
    if key:
        endpoints.append((f"https://gen.pollinations.ai/image/{path}", {"Authorization": f"Bearer {key}"}))
    endpoints.append((f"https://image.pollinations.ai/prompt/{path}", {}))

    errors = []
    for base, headers in endpoints:
        for attempt in range(3):  # the free endpoint is often busy; back off and retry
            try:
                return to_png(_fetch_image(f"{base}?{urllib.parse.urlencode(params)}", headers))
            except (urllib.error.URLError, RuntimeError, OSError) as err:
                errors.append(f"{base.split('/')[2]}: {err}")
                time.sleep(5 * (attempt + 1))
    raise RuntimeError("; ".join(errors[-2:]))


def gemini(prompt):
    from google import genai
    from google.genai import types

    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY is not set")
    response = genai.Client().models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="4:5"),
        ),
    )
    for cand in response.candidates or []:
        for part in cand.content.parts or []:
            if part.inline_data:
                return to_png(part.inline_data.data)
    raise RuntimeError("no image returned (try rewording the prompt)")


PROVIDERS = {"huggingface": huggingface, "pollinations": pollinations, "gemini": gemini}


def provider_chain(choice):
    if choice != "auto":
        return [choice]
    chain = (["huggingface"] if os.environ.get("HF_TOKEN") else []) + (
        ["pollinations"] if os.environ.get("POLLINATIONS_API_KEY") else []
    )
    if not chain:
        sys.exit("No image provider configured: add an HF_TOKEN (or POLLINATIONS_API_KEY) secret.")
    return chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="only generate these images (always overwrites)")
    parser.add_argument("--force", action="store_true", help="overwrite images that already exist")
    parser.add_argument("--provider", default="auto", choices=["auto", *PROVIDERS])
    args = parser.parse_args()

    spec = json.loads(PROMPTS.read_text())
    unknown = set(args.names) - spec["images"].keys()
    if unknown:
        sys.exit(f"Unknown image name(s): {', '.join(sorted(unknown))}")

    chain = provider_chain(args.provider)
    print(f"providers: {' → '.join(chain)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []

    for name, prompt in spec["images"].items():
        out = OUT_DIR / f"{name}.png"
        if args.names and name not in args.names:
            continue
        if out.exists() and not (args.force or args.names):
            print(f"skip   {name} (exists)")
            continue

        print(f"create {name} ...", flush=True)
        for provider in chain:
            try:
                data = PROVIDERS[provider](f"{prompt} {spec['style']}")
            except Exception as err:  # keep going so one failure doesn't stop the batch
                print(f"  {provider} failed: {err}", flush=True)
                continue
            out.write_bytes(data)
            print(f"  saved {out.relative_to(ROOT)} via {provider}", flush=True)
            break
        else:
            failed.append(name)

    if failed:
        sys.exit(f"{len(failed)} image(s) failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
