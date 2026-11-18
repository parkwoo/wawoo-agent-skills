---
name: openrouter-gen
description: Batch-generate design images via OpenRouter image models (default google/gemini-2.5-flash-image). Use for generated design assets or when the user mentions OpenRouter / OPENROUTER_API_KEY.
---

# openrouter-gen — OpenRouter batch image generation

The OpenRouter sibling of `fal-gen`. Generate the images a design phase needs (avatars, illustrations, hero backgrounds, textures…) in batches. Default model **`google/gemini-2.5-flash-image`**. The script uses only the Python standard library.

## One-time setup (API key)

Write the key into `.env` in this skill directory (if missing, copy the template and ask the user to fill it — **do not** invent a key):

```bash
cp .env.example .env
# edit: OPENROUTER_API_KEY=sk-or-v1-...
# get one: https://openrouter.ai/keys
```

`OPENROUTER_IMAGE_MODEL` is optional (default `google/gemini-2.5-flash-image`). `.env` contains a secret: never commit it or echo its contents.

## Usage

Write a manifest JSON in the project, then:

```bash
S=.kilo/skills/openrouter-gen
python3 $S/openrouter_gen.py --manifest <project>/or-manifest.json --dry-run   # validate, no API call
python3 $S/openrouter_gen.py --manifest <project>/or-manifest.json             # generate (skip existing)
python3 $S/openrouter_gen.py --manifest ... --only id1,id2                      # selected ids only
python3 $S/openrouter_gen.py --manifest ... --force                            # regenerate
```

- `output_dir` is resolved relative to the manifest file.
- Existing outputs are skipped by default → idempotent and safe to re-run.
- Image format is detected (PNG/JPEG/WebP) and the extension is corrected automatically.

## Manifest format

```json
{
  "output_dir": "generated",
  "defaults": { "model": "google/gemini-2.5-flash-image" },
  "images": [
    { "id": "hero", "prompt": "minimal black background, white line-art hero illustration, no text" },
    { "id": "avatar", "prompt": "friendly line-art avatar, flat vector, no text" }
  ]
}
```

- Prompts work best in English. To avoid text/watermarks, say so explicitly ("no text, no watermark").
- Cheaper model: `google/gemini-3.1-flash-lite-image`. Stronger: `google/gemini-2.5-flash-image` or `google/gemini-3-pro-image`. Override per item via `"model"`.
- Cost: OpenRouter bills per token/image and varies by model — check https://openrouter.ai/models before a large batch.

## Working rules

1. Run `--dry-run` first; generate only after the user confirms (generation costs real money).
2. Inspect each image; if it is not good, adjust the prompt and regenerate with `--force --only <id>`.
3. Put outputs in the project's design-asset directory, not in source folders.
4. Never commit `.env` or echo the key.

## Attribution

Authored in this repository — **MIT**, Copyright (c) 2026 **wawoo.jp**.
