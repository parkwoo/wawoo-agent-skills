#!/usr/bin/env python3
"""OpenRouter batch image generator (sibling of fal-gen).

- Default model: google/gemini-2.5-flash-image.
- Python standard library only (no pip deps).
- API key: OPENROUTER_API_KEY from this dir's .env (or an env var).
- Manifest JSON: {"output_dir", "defaults": {model?}, "images": [{id,prompt,model?,output?}]}
  output_dir is resolved relative to the manifest file's directory.

Usage:
  python3 openrouter_gen.py --manifest path/to/manifest.json            # generate all (skip existing)
  python3 openrouter_gen.py --manifest ... --only id1,id2               # only the given ids
  python3 openrouter_gen.py --manifest ... --force                      # overwrite existing
  python3 openrouter_gen.py --manifest ... --dry-run                    # validate, no API call
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
API = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash-image"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def generate_url(key: str, model: str, prompt: str, timeout: int) -> str:
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-Title": "openrouter-gen",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    msg = (data.get("choices") or [{}])[0].get("message", {})
    images = msg.get("images") or []
    if not images:
        raise RuntimeError(f"no image in response: {json.dumps(data)[:400]}")
    return images[0].get("image_url", {}).get("url", "")


def save_image(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if url.startswith("data:"):
        _, b64 = url.split(",", 1)
        raw = base64.b64decode(b64)
    else:
        req = urllib.request.Request(url, headers={"User-Agent": "openrouter-gen/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        ext = ".png"
    elif raw[:3] == b"\xff\xd8\xff":
        ext = ".jpg"
    elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        ext = ".webp"
    else:
        ext = ".png"
    want = dest.suffix.lower()
    matches = (
        (ext == ".jpg" and want in (".jpg", ".jpeg"))
        or (ext == ".png" and want == ".png")
        or (ext == ".webp" and want == ".webp")
    )
    if not matches:
        dest = dest.with_suffix(ext)
    dest.write_bytes(raw)
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description="OpenRouter batch image generation")
    ap.add_argument("--manifest", required=True, help="manifest JSON path")
    ap.add_argument("--only", help="comma-separated id list")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    load_env(HERE / ".env")
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not args.dry_run and not key:
        print(
            f"Error: OPENROUTER_API_KEY not found. Put it in {HERE / '.env'} "
            "(get one at https://openrouter.ai/keys).",
            file=sys.stderr,
        )
        return 2

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    defaults = manifest.get("defaults", {})
    out_dir = manifest_path.parent / manifest.get("output_dir", "generated")
    only = set(args.only.split(",")) if args.only else None

    done = skipped = 0
    for item in manifest["images"]:
        if only and item["id"] not in only:
            continue
        model = (
            item.get("model")
            or defaults.get("model")
            or os.environ.get("OPENROUTER_IMAGE_MODEL")
            or DEFAULT_MODEL
        )
        dest = out_dir / item.get("output", f"{item['id']}.png")
        if dest.exists() and not args.force:
            print(f"skip (exists) [{item['id']}]")
            skipped += 1
            continue
        if args.dry_run:
            print(f"dry-run [{item['id']}] {model} -> {dest.relative_to(out_dir.parent)}")
            skipped += 1
            continue
        print(f"generate [{item['id']}] {model} -> {dest.name}", flush=True)
        url = generate_url(key, model, item["prompt"], args.timeout)
        save_image(url, dest)
        done += 1
    print(f"\nDone: generated {done} / skipped {skipped}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
