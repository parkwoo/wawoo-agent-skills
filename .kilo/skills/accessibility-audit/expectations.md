# accessibility-audit — expectations（uplift pilot）

静的ヒューリスティック。ルール id は `scripts/uplift_pilot.py` の `ACTIVE_STATIC_RULES` と一致。

## 構造・フォーム

- `[a11y-html-lang]` ルート `html` に `lang`
- `[a11y-page-h1]` ページに見出し `h1`（1 ファイルスコープ）
- `[a11y-input-label]` `input`/`select`/`textarea` に `id`+`label[for]` または `aria-label` / `aria-labelledby`
- `[a11y-button-type]` フォーム内の `button` に明示 `type`（`submit` 誤爆防止）
- `[a11y-skip-link]` 本文先頭付近に skip link（`#main` 等）— ランディング級 HTML のみ目安

## 限界

テンプレ断片・コンポーネント単体では `h1`/`skip-link` が偽陽性になりうる。ディレクトリ単位で走らせ、finding は手で triage する。

## 検証

```bash
python3 scripts/skill_uplift_check.py accessibility-audit --path <ui-root>
```