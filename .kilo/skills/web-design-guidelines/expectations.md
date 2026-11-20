# web-design-guidelines — expectations（uplift pilot）

ルール id は `scripts/uplift_pilot.py` の `ACTIVE_STATIC_RULES` と一致。チェッカーは **ファイル単位のヒューリスティック**（偽陽性あり）。

## 画像・アクセシビリティ

- `[img-alt]` `img` に `alt`（装飾は `alt=""`）
- `[img-alt]` アイコンボタンにアクセシブル名（`aria-label` 等）

## フォーカス・入力

- `[tabindex-positive]` 正の `tabindex` を安易に使わない
- `[outline-none]` `outline: none|0` 時は同一ファイル内に代替フォーカススタイル

## モーション

- `[reduced-motion]` アニメありで当該ファイルに `prefers-reduced-motion` 無し →要確認（グローバル CSS は未追跡）

## インタラクション

- `[clickable-div]` `div`/`span` の `onclick` に `role="button"` 等

## 限界（偽陽性）

- 複数ファイルに分かれたスタイルは未結合
- Bootstrap 5 の `bootstrap.js` は本 pilot では対象外（`legacy_web_scan` は v3 系 URL のみ）

## 検証コマンド

```bash
python3 scripts/skill_uplift_check.py web-design-guidelines --path <file-or-dir>
```

証拠: `docs/evidence/skill-uplift/` · 設計: `docs/SKILL-UPLIFT-PILOT.ja.md`