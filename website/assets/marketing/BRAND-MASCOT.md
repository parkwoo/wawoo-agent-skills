# 小章鱼品牌角色（正本）

## 正本

- 文件：`docs/assets/wawoo-skills-logo.png`（与 `parkwoo/wawoo-agent-skills` README 相同）
- 特征：**Q 版白色线稿**、对称、眼睛 / 触手 / 手持光点等细节以 PNG 为准

## 禁止

- 用文生图（含 OpenRouter Gemini）**另造**章鱼形象用于站内可见区域（易错眼、手、发光点）
- 已误生成文件归档在 `_rejected_ai/`

## 多姿态

需要不同动作时，应 **在正本线稿上派生**（设计师改稿或 SVG 分图层），而不是 AI 自由发挥。

## 站点用法

| 位置 | 素材 |
|------|------|
| Hero | `/wawoo-skills-logo-transparent.png`（黑底已抠）· 全页 `kit-ambience.js`（圆泡上升 + 角色游动） |
| OG | `python3 scripts/compose_kit_brand_images.py` → `og-home-brand-1200x630.png` |