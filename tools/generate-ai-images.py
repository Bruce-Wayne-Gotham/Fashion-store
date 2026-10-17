"""Generate product images with Google's Gemini API (Google AI Studio).

Setup (once):
    pip install google-genai
    export GEMINI_API_KEY="your-key-from-aistudio.google.com"

Run from the repo root:
    python3 tools/generate-ai-images.py                 # all missing images
    python3 tools/generate-ai-images.py denim-jacket    # just one (overwrites)
    python3 tools/generate-ai-images.py --force         # regenerate everything

Images are saved to images/ai/<name>.png. The page picks them up automatically;
until a file exists the card shows its bundled illustration instead.

Model: image model names change often. The default below is set with --model or
the GEMINI_IMAGE_MODEL env var — check the image models listed in AI Studio
and use the newest one available to you.
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "tools" / "ai-image-prompts.json"
OUT_DIR = ROOT / "images" / "ai"
DEFAULT_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="only generate these images (always overwrites)")
    parser.add_argument("--force", action="store_true", help="overwrite images that already exist")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini image model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.exit("Missing SDK — run: pip install google-genai")
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("Set GEMINI_API_KEY first (create one at https://aistudio.google.com/apikey)")

    spec = json.loads(PROMPTS.read_text())
    unknown = set(args.names) - spec["images"].keys()
    if unknown:
        sys.exit(f"Unknown image name(s): {', '.join(sorted(unknown))}")

    client = genai.Client()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, prompt in spec["images"].items():
        out = OUT_DIR / f"{name}.png"
        if args.names and name not in args.names:
            continue
        if out.exists() and not (args.force or args.names):
            print(f"skip   {name} (exists)")
            continue

        print(f"create {name} ...", flush=True)
        try:
            response = client.models.generate_content(
                model=args.model,
                contents=f"{prompt} {spec['style']}",
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="4:5"),
                ),
            )
        except Exception as err:  # keep going so one failure doesn't stop the batch
            print(f"  failed: {err}")
            continue

        image = next(
            (p.inline_data.data for c in response.candidates or [] for p in c.content.parts or [] if p.inline_data),
            None,
        )
        if image is None:
            print("  failed: no image returned (try rewording the prompt)")
            continue
        out.write_bytes(image)
        print(f"  saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
