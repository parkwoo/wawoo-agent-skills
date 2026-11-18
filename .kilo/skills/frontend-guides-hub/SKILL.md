---
name: frontend-guides-hub
description: Frontend/UI skill ラッター — /ui-delivery 向けに既存 skill へ段階的にルートする（110 個平铺を避ける）。
license: MIT
---

# Frontend guides hub

**Workflow 入口**: `/ui-delivery` · `/design-review`

平铺カタログを読まない。下の **層** から 1 本ずつ `skill_get` する。

## 層 0 — Workflow

| 名前 | 用途 |
|------|------|
| `/ui-delivery` | 実装〜 a11y/品質〜 change-readiness |
| `/design-review` | デザインレビュー専線 |

## 層 1 — 発見・仕様

| skill | いつ |
|-------|------|
| `design-brief` | 要件が曖昧 |
| `reference-design-contract` | 参照 URL/スクショから DESIGN へ |
| `design-md` | DESIGN.md 作成・更新 |
| `frontend-design` | ビジュアル実装方針 |

## 層 2 — レビュー・品質

| skill | いつ |
|-------|------|
| `web-design-guidelines` | Vercel Web Interface Guidelines 準拠チェック |
| `web-design-guidelines` → `expectations.md` | 観測可能な受入（uplift pilot） |
| `accessibility-audit` | a11y 監査 |
| `web-experience-design` | 体験・階層・操作 |
| `performance-audit` | 代表ワークロード計測 |

## 層 3 — 現代 Web プラットフォーム（外部）

| skill | いつ |
|-------|------|
| `modern-web-guidance-bridge` | Dialog/Popover/View Transitions 等の **ネイティブ API** 手順が必要 |
| `legacy-web-scan` | レガシー JS/CSS ライブラリの掃除候補 |

## 層 4 — ゲート

| skill | いつ |
|-------|------|
| `design-review` | ビジュアル修正 |
| `change-readiness` | 引き渡し前 |
| `security-review` / `privacy-review` | 必要時 |

## 読み順（最小）

1. 本 hub で層を決める  
2. **1 skill だけ** `skill_get`  
3. 現代 API が要れば **`modern-web-guidance-bridge`**（search → retrieve 1 本）  
4. 完了証拠は workflow の ACTIVE / PR