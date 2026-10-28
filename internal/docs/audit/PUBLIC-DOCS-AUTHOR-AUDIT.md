# 公開ドキュメント監査（ベストセラー著者の視点）

- **対象（公開ツリーの英主ドキュメント）**: `README.md` / `AGENTS.md` / `docs/USAGE.md` / `docs/METHODOLOGY.md` / `docs/PROCESS-PHILOSOPHY.md` / `docs/INTENT-ROUTING.md` / `docs/VERSIONING.md` / `docs/README.md` / `docs/PUBLICATION.md` / `SECURITY.md` / `CHANGELOG.md`
- **非対象**: `internal/`（非公開）、`*.ja.md`（従版）、`.kilo/**` の実体（別途の資産監査）
- **観点**: 「**人に読まれ、覚えられ、勧められるか**」。ノンフィクションのベストセラー著者が原稿を赤入れする視点（フック／読者像／一本の主張／具体→抽象／記憶に残る言葉／読了後の行動）
- **方法**: 全文読解＋機械的検証（件数・境界・用語衝突）。**推測と実測を区別**する
- **記録**: 本ファイルは**監査記録＝内部資料**（`docs/PUBLICATION.md` の境界に従い `internal/` 配下。公開ツリーには入れない）

---

## 0. 総評（1ページ）

**内容の質は高い。問題は「売り方」と「記憶への残り方」にある。**

このリポジトリには、はっきりした主張がある——「**能力はあるのに呼ばれない**（the capability exists but is never invoked）」。これは強い。だが現在の公開ドキュメントは、その主張を**4段落目に埋め**、代わりにカテゴリ説明（"A generic kit of…"）で開いている。

ベストセラー著者の第一原理は「**読者は最初の 30 秒で続きを読むか決める**」。いまの README は最初の 30 秒で「これは何か」を説明するが、「**なぜ私（読者）が困っていて、この本がそれを解く**」を突きつけない。

加えて、**読者を実際に落とす地雷が 2 つ**ある（いずれも実測で確認）:

1. **同じ記号 L0–L3 が 2 つの意味**（儀式レベル／ルーティング層）。「L1 で」が一義に決まらない。
2. **境界文書の不一致**：`docs/README.md` が public 扱いする `METHODOLOGY.md`・`PROCESS-PHILOSOPHY.md` が、`docs/PUBLICATION.md` の外部一覧に**無い**。

> **検証で訂正（収束ゲート）**: 当初「件数が陈旧（実体 65/17 に対し記載 63/16）」と疑ったが、`python3 scripts/validate_assets.py` は `OK: skills=63 agents=22 commands=16` を返し、`ls` の 65/17 は **非ディレクトリの `README.md`・`ATTRIBUTION.md` を数えていた**だけだった。**公開文書の件数は正しい**。この仮説は棄却する（F3 を「低」に格下げ）。

**処方（要約）**: (a) 冒頭を「問い」に置換、(b) 記号衝突を解消、(c) 数値を単一化＋CI 検証、(d) 一本の主張を全ドキュメントで反復、(e) 具体→抽象の実例を冒頭に、(f) 読者像と「向かない人」を明示。

---

## 1. そのまま残すべき強み（Keep）

| # | 強み | なぜ効くか |
|---|---|---|
| K1 | **中心となる洞察がある**（"capability exists but never invoked"） | 本になり得る「一つの強い主張」。減点要素ではない |
| K2 | **§0 in one sentence**（METHODOLOGY / PROCESS-PHILOSOPHY） | ベストセラーの「章頭の一行要約」と同じ発想。良い |
| K3 | **Why の表**（METHODOLOGY §1 症状→原因→答え） | 問題→解決の対応が見える。読者が自分事化しやすい |
| K4 | **正直さ**（METHODOLOGY §1.1「runtime 強制はしない」、PROCESS-PHILOSOPHY §7） | 誇張しない。信頼の源。売り文句にもなる |
| K5 | **ライセンス・帰属の明快さ**（README 末尾、`ATTRIBUTION.md`, `LICENSES/`） | OSS の信頼信号。維持 |
| K6 | **セキュリティ方針の具体性**（`SECURITY.md`） | 監査者・企業導入の安心材料 |

---

## 2. 指摘（優先度順）

各項: **何が / 読者にどう効くか / 実測証拠 / 改善案（before→after）**。

### F1【高】フックが「陳列」で始まり、「問い」で始まっていない

- **何が**: `README.md` の第 1 文は `"A generic kit of reusable skills / agents / workflows / MCP servers for AI coding agents."`。これはカテゴリの陳列であって、読者の痛みに触れていない。真のフックは L9 の "**Why this kit**" 段落にあり、折り返しの下に埋没。
- **読者にどう効くか**: 検索・SNS・GitHub の一覧で、これを見た人が「これは自分向けだ」と 3 秒で判断できない。OV（オープニングビュー）で離脱する。
- **証拠**: `README.md:3` vs `README.md:9-11`。
- **改善案**:
  - Before: `A generic kit of reusable skills / agents / workflows / MCP servers for AI coding agents.`
  - After: `**Your agent has the skills. It just doesn't use them.** wawoo-skills is a kit that designs *the invocation* — so the same request takes the same steps every time.`
- **補足**: ベストセラーの型は「**痛点の断定 → 約束 → 証拠**」。1 文目に痛み、2 文目に約束を置く。

### F2【高】記号 `L0–L3` が二重の意味を持ち、読者が迷子になる

- **何が**: 同じ `L0–L3` が 2 用途で使われる——(a) **儀式レベル**（`METHODOLOGY.md` §5、`USAGE.md` §5: L0 単発 / L1 ACTIVE / L2 トラッカー / L3 プロセス改善）と (b) **ルーティング層**（`INTENT-ROUTING.md` §1: L0 slash / L1 learned / L2 upstream / L3 delegation）。
- **読者にどう効くか**: 「L1 でやって」と言われたとき、**どちらの L1 か**決まらない。`PROCESS-PHILOSOPHY.md` §9 は WARO の「A」と D ステージの混同を**明示的に戒めている**のに、L0–L3 の衝突は未解決。学習コストと誤解の温床。
- **証拠**: `docs/METHODOLOGY.md:99-110`、`docs/USAGE.md:97`、`docs/INTENT-ROUTING.md:21-28`。
- **改善案**: 片方を改名する。例: 儀式 = **`C0–C3`（Ceremony）**、ルーティング = **`R0–R3`（Route）**。最低限、各初出で「本稿の L は儀式レベルでありルーティング層とは別」と 1 行注記。
- **原則**: 一つの記号に一つの意味（"one symbol, one meaning"）。ベストセラーは用語の再定義を嫌う。

### F3【低】件数が 4 文書に重複記載（現状は正しいが、将来のドリフト余地）

- **何が**: 実体の件数（skills 63 / agents 22 / commands 16）は**公開文書と一致**しており、**現状は誤りではない**（実測・検証済み）。ただし同じ数値が `README.md`・`AGENTS.md`・`docs/USAGE.md` に重複記載され、正本が 1 つに定まっていない。
- **読者にどう効くか**: 現在は無害だが、資産追加のたびに 3〜4 箇所を手で直す必要があり、**過去に件数表記が揺れた事実**（CHANGELOG/`internal` の記録に 55/21→57/22 の修正履歴）を踏まえると、再ドリフトの蓋然性が高い。数字が 1 つ古くなるだけで README 全体の信頼が落ちる。
- **証拠（検証済み）**:
  - `python3 scripts/validate_assets.py` → `OK: skills=63 agents=22 commands=16`（＝記載と一致）
  - `README.md:59,61`、`AGENTS.md:29`、`docs/USAGE.md:15` に同一数値が重複
  - 注: `ls .kilo/skills | wc -l` は 65 を返すが、これは非ディレクトリの `README.md`・`ATTRIBUTION.md` を含むため（誤読注意）
- **改善案**:
  - 件数は **`CAPABILITIES.md`（生成物）を正本**とし、README / AGENTS / USAGE は「see the generated catalog」に置換する（`gen_capabilities.py` が既にある）。
  - 任意で `validate_assets.py` に「文書内の件数 vs 実体」の突合を足し、陳腐化を機械で止める。

### F4【中】読者像（Who it's for / not for）が無い

- **何が**: 誰に向く／向かないの宣言が無い。`AGENTS.md` は「エージェント契約」、`USAGE.md` は操作。だが「**あなたはこの読者か**」を最初に問う頁が無い。
- **読者にどう効くか**: ベストセラーは必ず「この本は◯◯な人のために書いた」を置く。無いと「自分向けか分からない」層が離脱。
- **改善案**: README 冒頭近くに 2 列表を追加。
  - **向く**: Kilo / Cursor を使い、skills・agents を既に用意したが「守られない」経験がある人／工程を再現可能にしたいチーム。
  - **向かない**: 単発のコード生成だけが欲しい人／プロセスより自由な即興を優先したい人。
- **基準**: 「読者を選ぶことは、読者を失わない最良の方法」。

### F5【中】一本の主張（through-line）が磨かれていない

- **何が**: 主張自体（"designing the invocation"）はあるが、名前が固定されず、文書ごとに言い回しが揺れる（reproducible orchestration / workflow-driven / rails of steps…）。§0 の一行も文書ごとに別表現。
- **読者にどう効くか**: 読後 1 日で「あのリポジトリは何だったか」を説明できない。口コミ（紹介）が発生しない。
- **改善案**: 商品名のような**固定フレーズを 1 つ**決め、README・各 doc の §0・`CAPABILITIES.md` 冒頭で**同一文**を反復。例: **"Invocation by design"**（能力ではなく、呼び出し方を設計する）。
- **基準**: 売れる本は「一つの言葉」で想起される。

### F6【中】具体 → 抽象の順序が逆。走る実例が無い

- **何が**: `METHODOLOGY.md`（WARO、3 層）、`PROCESS-PHILOSOPHY.md`（D0–D7、Gₐ/Gₑ/Gₒ）は**抽象概念を先に**提示する。README にも worked example が無い。
- **読者にどう効くか**: ベストセラーは「**一つの具体例を巻頭に置き、全章で使い回す**」。いまは用語集を先に読まされる。
- **改善案**: README 冒頭に「**2 分の before/after**」を置く。
  - Before（routing 無し）: 「`テスト直して` → エージェントが場当たりで実行、gates 素通り、同じ依頼で毎回手順が違う」
  - After（routing 有り）: 「`/self-review` へ route → `test-engineering` を読み → Gₑ で証拠 → 同じ手順が再現」
- **原則**: 「概念を説明する前に、変化を見せる」。

### F7【中】境界文書の不一致（public の定義が二つある）

- **何が**: `docs/README.md` は `METHODOLOGY.md` / `PROCESS-PHILOSOPHY.md` を通常の公開文書として並べるが、`docs/PUBLICATION.md` の External 一覧には**含まれない**（`SECURITY.md`・`CHANGELOG.md`・`docs/README.md` も同様）。
- **読者にどう効くか**: コントリビュータ／メンテナが「これは公開物か内部か」を判断できない。`PUBLICATION.md` は境界の**正本**を名乗る以上、網羅性が問われる。
- **証拠**: `docs/PUBLICATION.md:9`（External 列挙に両文書が無い）／`docs/README.md:9-10`（掲載）。
- **改善案**: `PUBLICATION.md` の External 一覧を**網羅**にする（漏れを追記）。または `docs/README.md` の表現を「公開文書」から中立語に。**境界の正本を 1 つに**。

### F8【中】公開 `CHANGELOG.md` が日本語のみ（国際読者への摩擦）

- **何が**: ルートの `CHANGELOG.md` は日本語（言語ポリシー上は「プロジェクト記録」として妥当）。だが公開リポジトリの国際読者には読めない。
- **読者にどう効くか**: 「このプロジェクトは英語圏の利用者を想定していない」というシグナルになる（README は英語主なのに、履歴だけ日本語）。
- **改善案**: 方針は維持でよいが、README の Version 節に「**CHANGELOG は日本語のプロジェクト記録**」と一言添える。余力があれば各版の **1 行英語要約**を先頭に付ける。

### F9【低】文体が名詞化・受動で硬い（"そして誰も読まない文体"）

- **何が**: `reproducible orchestration`、`the done definition`、`is delegated to` など名詞化・受動が目立つ。
- **改善案**: 動詞・二人称・具体に置換。
  - `It provides reproducible orchestration.` → `You get the same steps every time.`
  - `Detailed steps are delegated to skills.` → `Each step's how-to lives in a skill.`
- **基準**: ベストセラーは「あなた」に話しかけ、動詞で語る。

### F10【低】Quick start が最初の成功体験を与えない

- **何が**: README の Quick start は「Open this directory」程度で、**最初の 10 分で何が起きるか**が無い。
- **改善案**: 「**10 分の最初の一歩**」を追加——例: `interpret_intent` に一文を投げて workflow が返る、`/delivery-lite` を 1 回回して `ACTIVE.md` が 1 行進む、まで。
- **原則**: 売れる本は「第 1 章で必ず小さな成功を 1 つ渡す」。

### F11【低】名称だけでは何か分からない

- **何が**: `wawoo-skills` は固有名で、内容を語らない。
- **改善案**: H1 の直下に**固定タグライン**（F5 の固定フレーズと同一）を常設。例: `wawoo-skills — invocation by design for AI coding agents`.

---

## 3. 「もし私がこのキットで“売れる本”を組むなら」——目次案

現在の文書は**リファレンス**（引く辞書）としては完成度が高い。売れる本は**物語**（読む順路）を別に持つ。公開ツリーには次の 2 層を分けることを勧める。

| 層 | 役割 | 現状の対応 | 提案 |
|---|---|---|---|
| **Front matter（読む）** | 3 秒フック → 2 分実例 → 約束 → 読者像 → 最初の一歩 | README（陳列） | README を物語順に再構成（F1/F4/F5/F6/F10） |
| **Manual（引く）** | WARO、D ステージ、gates、ルーティング | METHODOLOGY / PROCESS-PHILOSOPHY / INTENT-ROUTING | 各 §0 を固定文で統一、記号衝突を解消（F2） |
| **Reference（調べる）** | 65 skills / 22 agents / 17 workflows | `CAPABILITIES.md` | 件数はここを正本に（F3） |

**物語の一本道（推奨）**:
1. **Hook**: 「能力はあるのに呼ばれない」を 1 文で。
2. **Story**: 同一依頼の before/after を 2 分で。
3. **Promise**: "invocation by design"（固定フレーズ）。
4. **Proof**: 3 層（Workflow / Skill / Agent）と WARO を**1 つの実例に沿って**説明。
5. **Payoff**: 最初の一歩（F10）と、守られない時の正直な限界（K4）。
6. **Call**: catalog へ。

---

## 4. アクションリスト（優先度付き）

### Quick wins（各 15 分未満・低リスク）
- [ ] **F1**: README 第 1 文を痛み→約束に置換。
- [ ] **F3**: 件数の重複記載を 1 箇所（生成カタログ `CAPABILITIES.md`）へ集約（**現状の値は正確**。将来のドリフト防止）。
- [ ] **F7**: `PUBLICATION.md` の External 一覧に `METHODOLOGY.md`・`PROCESS-PHILOSOPHY.md` を追記。
- [ ] **F8**: README の Version 節に「CHANGELOG は日本語記録」と 1 行。
- [ ] **F11**: H1 直下に固定タグライン。

### Structural（合意が必要・中リスク）
- [ ] **F2**: `L0–L3` の二重定義を改名（儀式 `C0–C3` / ルート `R0–R3`）＋各初出に 1 行注記。影響: `USAGE.md`・`METHODOLOGY.md`・`INTENT-ROUTING.md`・`ROUTER.md`（生成）・`AGENTS.md`。
- [ ] **F5**: 固定フレーズを 1 つ決定し、README＋各 doc §0＋`CAPABILITIES.md` 冒頭で同一文に統一。
- [ ] **F6/F10**: README に「2 分の before/after」と「10 分の最初の一歩」を追加。
- [ ] **F4**: 「向く人／向かない人」表を追加。
- [ ] **F3+CI**: `validate_assets.py` に「文書内の件数 vs 実体」の突合検査を追加（再発防止）。

---

## 5. 付録：検証した事実（Evidence）

実行コマンドと結果（再確認可能）:

```text
$ python3 scripts/validate_assets.py
  WARN: name used as both skill and command (slash vs model): design-review
  WARN: name used as both skill and command (slash vs model): research
  WARN: 13 skills over 4KB budget (see AGENTS §5): code-review, codebase-design, ...
  OK: skills=63 agents=22 commands=16            ← 公開文書の件数と一致（陳腐化なし）
$ cat VERSION                    → 0.6.0

# 誤読注意: `ls .kilo/skills | wc -l` は 65 を返すが、これは
#   非ディレクトリの README.md・ATTRIBUTION.md を含むため。
#   実体（`find -maxdepth 1 -type d` / validate_assets）= 63。
$ grep -rn "63 skill\|(63)\|55 skills\|57 skill" README.md AGENTS.md docs/USAGE.md docs/README.md
AGENTS.md:29:  skills/<name>/SKILL.md   … skills (63)
docs/USAGE.md:15:- Skills: `.kilo/skills/<name>/SKILL.md` (63)     ← 記載は正しい（重複のみが課題）

$ grep -rn "METHODOLOGY\|PROCESS-PHILOSOPHY" docs/PUBLICATION.md
（該当なし → External 一覧に未記載）

$ grep -rln "L0" docs/METHODOLOGY.md docs/INTENT-ROUTING.md
docs/METHODOLOGY.md
docs/INTENT-ROUTING.md   （＝2 文書で別定義の L0–L3 を使用）
```

- **L0–L3 の二重定義**: `docs/METHODOLOGY.md:99-110`（儀式）と `docs/INTENT-ROUTING.md:21-28`（ルーティング）。
- **フックの埋没**: `README.md:3`（陳列）／`README.md:9-11`（真のフック）。
- **§0 一行**: `docs/METHODOLOGY.md:5`、`docs/PROCESS-PHILOSOPHY.md:5`（＝強み K2）。

### 未検証（明示）
- **実際の読者行動**（離脱率・スター数への寄与）は**未検証**の推論。本監査は本文の読みと機械的突合のみに基づく。
- `*.ja.md`（従版）は原則として英主版と同内容と仮定し、差分監査は未実施。
- 拠出 PR への影響試算（工数）は概算で、未確認。
