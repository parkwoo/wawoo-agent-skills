# 連携：Paseo・Google・pstack

[English](INTEGRATIONS.md) · [日本語](INTEGRATIONS.ja.md) · [简体中文](INTEGRATIONS.zh-CN.md) · [한국어](INTEGRATIONS.ko.md)

公開キットが**公式に配線する外部スタック**です（社内専用 skill ではありません）。

## Paseo

[**Paseo**](https://github.com/getpaseo/paseo) は内蔵 **OpenCode** を使います。本キットはターミナル版と**同じ** `opencode.json` を対象にします。

| 項目 | 内容 |
|------|------|
| 設定 | `~/.config/opencode/opencode.json` |
| 導入 | `python3 scripts/install_opencode.py`（`memory_save` 要るなら `--memory-writable`） |
| env 変更後 | `paseo daemon stop && paseo daemon start` |
| MCP | Kilo / Cursor と同一 `wawoo-skills` サーバ |

手順: [CLIENT-INTEGRATION-GUIDE.ja.md](CLIENT-INTEGRATION-GUIDE.ja.md) · [MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md)

`getpaseo/paseo` の plugin skill と本キットは**別物**—MCP と daemon が通っていれば併用可。

## Google（Modern Web Guidance・design-md）

262 本の guide を repo にコピーしません。**必要時だけ npx ブリッジ**です。

| 要素 | 役割 |
|------|------|
| `modern-web-guidance-bridge` | いつ MWG を呼ぶか |
| MCP `mwg_*` | `npx modern-web-guidance@latest`（`WAWOO_MWG_DISABLE=1` で停止） |
| `design-md` | [Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/specification) 形式（Google Labs 系） |
| UI | `/ui-delivery` · [SKILL-UPLIFT-PILOT.ja.md](SKILL-UPLIFT-PILOT.ja.md) |

上流: [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)

`interpret_intent` の上流 LLM（OpenRouter 等）は**クライアント側設定**であり、「キット内蔵 Gemini」ではありません。

## pstack（原則・検証スキル）

**pstack**（Lauren Tan / Poteto、**MIT**）由来の skill を同梱。主に **`principle-*`** と検証系。

| 例 | 使い方 |
|----|--------|
| `principle-*` | フェーズごと **1〜2 個**だけ |
| `blast-radius` 等 | workflow が指名したとき |

ライセンス: `LICENSES/pstack-MIT.txt` · [ATTRIBUTION.md](../.kilo/skills/ATTRIBUTION.md) · 案内: `ask-matt`

**索引:** [GUIDES.ja.md](GUIDES.ja.md)