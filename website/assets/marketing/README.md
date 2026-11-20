# 营销图（OpenRouter）

## 生成

```bash
python3 scripts/generate_kit_marketing_images.py --force
```

- モデル: `google/gemini-2.5-flash-image`（`manifest.json` で変更可）
- キー: `OPENROUTER_API_KEY` または `/home/git/zen-router/.env`

## ファイル

| 产出 | 说明 |
|------|------|
| `hero-bg*.png` | 首页 hero 背景（多姿态 Q 版线稿章鱼） |
| `og-home*.png` | OG / Twitter 卡片（1200×630 为裁剪版） |
| `manifest.json` | プロンプト SSOT |

- **Hero / OG**: 仅使用 README 正本 PNG。见 `BRAND-MASCOT.md`。
- **OG 合成**: `python3 scripts/compose_kit_brand_images.py`
- **AI 弃用图**: `_rejected_ai/`