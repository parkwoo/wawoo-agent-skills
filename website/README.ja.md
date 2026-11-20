# wawoo-skills 公式サイト（静的ランディング）

[paseo.sh](https://paseo.sh/) と同系のダークテーマ・レイアウトを参考にした、公式トップページ用の静的ファイルです。MkDocs のドキュメントは `/docs/` に配信します。

## ローカルプレビュー

### よくある原因（真っ白・無スタイル）

1. **HTML をダブルクリック**（`file://`）で開いている → CSS が読めない。**必ず HTTP で見る**。
2. **ディレクトリが違う** — `skills/` やリポジトリ直下で `python3 -m http.server` しても、`website/` の中身は出ない。

### UI mock のみ（五ページ · MkDocs なし）

```bash
cd /home/git/workspace/skills/website
chmod +x preview-ui.sh
./preview-ui.sh
```

→ `/` · `/docs/` · `/guides/` · `/changelog/` · `/download/`

### 推奨（ランディング + 任意で docs）

```bash
cd /home/git/workspace/skills/website
chmod +x preview.sh
./preview.sh
```

→ **Windows のブラウザ**で http://localhost:8765/  
  （サーバーは WSL で動かす。`preview.sh` は `0.0.0.0` にバインド済み）

#### Windows から見られないとき

1. ファイアウォールが WSL のポートを塞いでいないか確認する。
2. `localhost` が通らない場合、WSL の IP を使う（WSL ターミナルで `hostname -I | awk '{print $1}'`）→ `http://<そのIP>:8765/`
3. **HTML をエクスプローラでダブルクリックしない**（`file://` は使わない）。
4. 代替：**VS Code / Cursor** で `skills/website` を開き、拡張機能 **Live Server** で `index.html` をプレビュー（相対パス対応済み）。

初回のみ（WSL）:

```bash
cd /home/git/workspace/skills
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt
```

その後 `./preview.sh` は **ランディング + 全 docs ページ**を同じポートで配信します。

### ランディングだけ（最短）

```bash
cd /home/git/workspace/skills/website
python3 -m http.server 8765
```

同じ URL を開く。**Docs リンクは MkDocs 未ビルド時 404**（GitHub の USAGE を参照）。

## GitHub Pages

`.github/workflows/docs.yml` が次を行います。

1. `mkdocs build` → `site/docs/`
2. `website/` の静的ファイルを `site/` ルートへコピー
3. Pages にデプロイ → https://parkwoo.github.io/wawoo-skills/

## 構成

| ファイル | 役割 |
|----------|------|
| `index.html` | ランディング（英語） |
| `styles.css` | Paseo 系カラートークン（独自実装） |
| `main.js` | FAQ アコーディオン |
| `logo.svg` / `favicon.svg` | ブランドマーク |