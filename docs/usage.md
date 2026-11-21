---
title: wawoo-skills 使用说明
description: 装好、配好、用得顺。
hide:
  - title
  - navigation
---

<div class="kit-doc-hero" markdown="1">

**wawoo-skills 使用说明**

装好、配好、用得顺。

<div class="kit-doc-langs">
  <a href="/en/docs/usage/">English</a>
  <span aria-hidden="true">·</span>
  <a href="/ja/docs/usage/">日本語</a>
  <span aria-hidden="true">·</span>
  <strong>简体中文</strong>
</div>

<div class="kit-doc-links">
  <a href="https://github.com/parkwoo/wawoo-agent-skills/blob/master/README.zh-CN.md">返回 README</a>
  <span aria-hidden="true">·</span>
  <a href="https://github.com/parkwoo/wawoo-agent-skills">GitHub</a>
</div>

</div>

!!! info "这份文档讲什么"
    只讲**怎么装、怎么配、怎么排错**。要了解「这是什么、为什么用」，见 [GitHub 上的 README.zh-CN](https://github.com/parkwoo/wawoo-agent-skills/blob/master/README.zh-CN.md)。

## 最短路径（先看这个） {#usage-quickstart}（先看这个）

1. 确认有 Python 3 —— [§0 前提](#s0)
2. 按你的客户端接入 —— [§2 各客户端接入](#s2)（**Kilo / Cursor 最简单**，照命令跑即可）
3. 验证 —— 运行 `python3 scripts/validate_assets.py`，出现 `OK` 就成了

其余（各端 MCP 参数、记忆开关、排错）按需查下面的目录。

> **要设开关？** 工作语言、图片生成 key、记忆、路由调优、安装目标……都在 [**§9 设定一览**](#s9)。

## 0. 前提：Python 3（标准库即可） {#s0} {#s0}
- **Python 3（只用标准库）**：MCP 服务与维护脚本都只用标准库，**不需要额外安装包**。
- 需要 `PATH` 上有 `python3`（Windows 为 `python`）。检查：`python3 --version` 返回 `3.x` 即可。
  - macOS：缺就 `xcode-select --install`；Linux：`apt install python3` 等；Windows：从 https://www.python.org/downloads/ 安装并勾选 **"Add python.exe to PATH"**。
- MCP 用 `python3` 作为启动命令（`kilo.json`、`.cursor/mcp.json`）。若你机器上叫别的名字（`python` / `py`），把对应配置里的 `command` 改成真实命令。
- 不需要联网、不需要 `.env`（MCP 走 stdio）。

## 1. 装的是什么 {#s1}
一句话：**技能是「会什么」，角色是「谁来看」，工作流是「按什么顺序做、做到什么算完」。**
### 1.1 三类资产：怎么查 {#s1-1}
技能 / 角色 / 工作流的定义见 [README 的「名词表」](../README.zh-CN.md)。这里只讲**怎么查**：

| 类别 | 怎么查 |
|---|---|
| 技能 skills | `skill_search` / `.kilo/CAPABILITIES.md` |
| 角色 agents | `agent_get` |
| 工作流 workflows | `workflow_get` |
| MCP 服务 | `python3 mcp/server.py` |

### 1.2 工作流长什么样 {#s1-2}
**12 条工作流的清单见 [README「12 条工作流」](../README.zh-CN.md)。** 这里只讲它们的结构——每条都有：

- **阶段（phase）**：目标 / 负责角色 / 用到的技能 / `exit_criteria`；用 `workflow_get {name, phase}` 可逐段查看。
- **闸门（gate）**：批准、证据、失败观察；**审查类只读**（没有 implement 阶段）。
- **完成条件（exit_criteria）**：没达标就不算完成。

**没有 `implement` 阶段的流程**（如 `/design-review`、`/compliance-review`、`/release-review`、`/research`、`/status-report`）不会进入实现阶段；要改代码，切到 `/delivery-lite`、`/feature-delivery`、`/ui-delivery`、`/incident-response` 或 `/self-improve`。

### 1.3 意图路由（router） {#s1-3}
**选流程的顺序**（显式 → 本地词法 → 已学习 → 模型评分）见 [README](../README.zh-CN.md)。这里讲**选完之后怎么管**：

- **工具闸门**：按该工作流的**允许工具清单**（`mcp_tools_allow`）限定 MCP 工具——审计类只给读工具，也没有 implement 阶段。
- **会话门禁**：跨调用记住「现在在哪条流程」；`WAWOO_INTENT_RESUME=1` 可在重启后恢复，`WAWOO_INTENT_CLIENT` 避免多客户端串台。
- **收尾**：`workflow_clear` 清掉当前会话门禁。
- **想覆盖路由**：直接写 `/name`；或调 `interpret_intent` 时带 `scoring`。**路由选错 / 查不到**：见 [§8 排错](#s8)（多为没重启 MCP）。

### 1.4 自己加一个（skill / agent / workflow）

- **skill**：建 `.kilo/skills/<name>/SKILL.md`；`name` 必须等于目录名，入口 ≤4KB，细节进 `references/`。
- **agent**：建 `.kilo/agents/<name>.md`（`mode: primary|subagent`，权限按需）。
- **workflow**：建 `.kilo/commands/<name>.md`（frontmatter：`description` / `agent` / `replay`）。
- 然后：`python3 scripts/validate_assets.py` → `python3 scripts/gen_capabilities.py` → **重启 MCP / Kilo**（命令在启动时缓存）。

## 2. 各客户端接入（Kilo / Cursor / OpenCode / Codex / Paseo） {#s2}
### 2.1 Kilo（CLI / Kilo Code） {#s2-1}
0. **先登录**：`kilo auth login`（选择 provider 完成登录）。Paseo 拉起 Kilo 前也需要先登录，否则会拉不起来。
1. 打开本仓库目录即可（自动发现 `.kilo/`；MCP 由 `kilo.json` 启用）。
2. 工作流用 `/feature-delivery` 等斜杠命令；技能由模型自行选择或显式引用。

**全局安装**（在所有项目里可用，可重复跑）：

```bash
python3 scripts/install_global.py --dry-run     # 预览改动
python3 scripts/install_global.py               # 应用（默认镜像：删除多余文件）
python3 scripts/install_global.py --no-delete   # 保留多余文件
python3 scripts/install_global.py --memory-writable   # 允许 memory_save
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py   # 指定目标
```

- **它会做三件事**：① 写入 MCP（绝对路径的 `python3` + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`）；② 生成 `ROUTER.md`，并以**绝对路径**注册到 `instructions`；③ 把默认角色设为 `wawoo-auto`（`--default-agent` / `--no-default-agent` 可改）。
- Kilo 的 `instructions` **必须是绝对路径**（相对路径不会被注入运行时上下文）。
- **改完要重启 Kilo 才生效**（agents / commands / instructions 在服务启动时缓存；VS Code：Reload Window）。

### 2.2 OpenCode {#s2-2}
`opencode.json` 里把本套件加成本地 stdio MCP：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "/abs/path/to/wawoo-skills/mcp/server.py"],
      "enabled": true,
      "environment": {
        "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
        "WAWOO_MEMORY_READONLY": "1"
      }
    }
  }
}
```

- 一键安装：`python3 scripts/install_opencode.py`（默认只读）；要可写加 `--memory-writable`。
- OpenCode **没有原生斜杠命令 / 技能执行**，一律走 MCP：`interpret_intent` → `workflow_get` → `skill_get`。

### 2.3 Cursor {#s2-3}
1. 打开目录（会读 `AGENTS.md` 和 `.cursor/rules`）。
2. 在 **Settings → MCP** 里启用 `wawoo-skills`（`.cursor/mcp.json`）。

```bash
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace   # 只装 MCP（会覆盖项目 mcp.json）
python3 scripts/install_cursor_global.py                                     # 用户级 ~/.cursor（合并进 mcp.json）
# 允许 memory_save：
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace --memory-writable
```

**Cursor 的限制：**

- 斜杠命令（`/feature-delivery` 等）**不生效**；
- **没有 agent 切换**（读 `@.kilo/agents/<role>.md` 自己套用角色）；
- **不会自动发现 / 自动启动 `SKILL.md`**。

**没有 MCP 时的兜底**：看 `@.kilo/CAPABILITIES.md` 选候选 → 读 `@.kilo/skills/<name>/SKILL.md` → 按步骤做；工作流读 `@.kilo/commands/<name>.md`。

### 2.4 Paseo（内置 OpenCode，与别家不同） {#s2-4}
Paseo 是**多智能体 IDE**，内置 OpenCode，智能体跑在它自己的 **daemon**（后台服务）里：

- **配置**：沿用**同一份** `~/.config/opencode/opencode.json`（MCP `wawoo-skills` 就接这里）；安装用 `python3 scripts/install_opencode.py`。
- **先登录**：Paseo 拉起 `kilo` / `cursor` 前，先在对应 CLI 登录（Kilo 用 `kilo auth login`），否则会拉不起来。
- **重启语义**：改环境变量或 MCP 后要
  ```bash
  paseo daemon stop && paseo daemon start     # 彻底切换
  # 或：paseo daemon restart                  # 只重启 worker
  ```
  **daemon 重启会一并重启它自己启动的会话。**
- **独立进程**：VS Code 的 Kilo 扩展、Cursor 桌面、独立终端里的 opencode/kilo/cursor **不受** daemon 影响。
- **插件是两回事**：Paseo 自带插件技能（`npx skills add getpaseo/paseo`）与本套件互不相干；MCP 与 daemon 配好即可并用。

### 2.5 Codex（OpenAI Codex CLI / 扩展） {#s2-5}
Codex 读 `AGENTS.md`、加载技能、并支持 MCP（配置在 `~/.codex/config.toml`）。把本套件加成一个 stdio MCP：

```toml
[mcp_servers.wawoo-skills]
command = "python3"
args = ["/abs/path/to/wawoo-skills/mcp/server.py"]
env = { WAWOO_SKILLS_ROOT = "/abs/path/to/wawoo-skills", WAWOO_MEMORY_READONLY = "1" }
```

- 技能目录指向 `.agents/skills/`（如需把 `.kilo/skills/` 的内容放进去）。
- 目前 Codex 需**手动配置**，本仓未提供一键脚本。Codex 支持 `/skills`、`$skill` 调用与 MCP（`codex mcp add ...`）。

### 2.6 Claude Code（Anthropic CLI） {#s2-6}
Claude Code 支持 MCP、`CLAUDE.md`、`.claude/skills/`、`.claude/commands/`（原生斜杠命令）。

```bash
claude mcp add wawoo-skills \
  --env WAWOO_SKILLS_ROOT=/abs/path/to/wawoo-skills \
  --env WAWOO_MEMORY_READONLY=1 \
  -- python3 /abs/path/to/wawoo-skills/mcp/server.py
```

- **技能**：把 `.kilo/skills` 复制或软链到 `.claude/skills`。
- **工作流**：把 `.kilo/commands/*.md` 复制到 `.claude/commands/`（有原生斜杠命令）。
- **契约**：`AGENTS.md` 与 `CLAUDE.md` **二选一**，不要同时建。
- **子代理**：用 `Agent`（`subagent_type`），`swarm` / `reflect` 可正常并行。

> **Pi 等其它 MCP 客户端**：只要支持 stdio MCP，用同一 `python3 mcp/server.py` 即可；技能目录按客户端约定（如 `.pi/skills/`）。有子代理扩展时 `swarm` / `reflect` 并行；没有时按顺序执行（两种都支持）。

## 3. MCP 服务 {#s3}
本套件的能力通过一个**本地 MCP 服务**暴露（stdio：本地进程通信，客户端自动拉起，不用开端口）。

```bash
python3 mcp/server.py          # 一般由客户端拉起
python3 scripts/e2e_flows.py   # 契约 / E2E 冒烟
```

常用工具：`capabilities`、`skill_search`、`skill_get`、`workflow_get`、`agent_get`、`memory_recall`、`memory_save`；意图路由：`interpret_intent` → `workflow_get` → … → `workflow_clear`；子任务：`delegate_subtask`。

## 4. 记忆（memory）设定 {#s4}
### 4.1 工具做什么

| MCP 工具 | 作用 |
|---|---|
| `memory_recall` | 从 `docs/memory/`（INDEX + 主题文件）读既往决定。**只读模式下也能用。** |
| `memory_save` | 追加一条决定（写进 INDEX + 主题文件，模板 `docs/memory/TEMPLATE.md`）。**`WAWOO_MEMORY_READONLY=1` 时被拒绝**；密钥任何情况下都拒绝。 |

记忆的**唯一正本**是 `<kit>/docs/memory/` 下的 Markdown；与客户端内置记忆冲突时，**以文件为准**（见 `docs/memory/MEMORY-TOOLS.md`）。

### 4.2 `WAWOO_MEMORY_READONLY`（只读 / 可写）

| 值 | 效果 | 什么时候用 |
|---|---|---|
| **`1`**（安装默认） | **只读**：`memory_save` 报错，`memory_recall` 照常 | MCP 注册在任意项目；审计 / 合规会话；不希望 agent 往 kit 里写东西 |
| **`0`** | **可读可写**：允许写进 `WAWOO_SKILLS_ROOT/docs/memory/` | 在 kit 仓库或镜像同一 `docs/memory/` 布局的工作区日常开发 |

MCP 服务**启动时**从客户端配置的 env 读取它——**只改文件不够，必须重启客户端**（Kilo Reload、Cursor Reload、OpenCode 重启、Paseo 内置 OpenCode 需 `paseo daemon restart`）。

### 4.3 各客户端在哪里设

| 客户端 | 配置文件 | 推荐命令（可重复跑） |
|---|---|---|
| Kilo（全局） | `~/.config/kilo/kilo.jsonc` → `mcp.wawoo-skills.environment` | `python3 scripts/install_global.py`（默认 `1`）或 `--memory-writable`（`0`） |
| OpenCode（终端或 **Paseo 内置**） | `~/.config/opencode/opencode.json` → `mcp.wawoo-skills.environment` | `python3 scripts/install_opencode.py` 或 `--memory-writable` |
| Cursor（用户） | `~/.cursor/mcp.json` → `mcpServers.wawoo-skills.env` | `python3 scripts/install_cursor_global.py`（会合并其它 MCP）+ `--memory-writable` |
| Cursor（项目） | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root>` + `--memory-writable`（会覆盖，需自行合并） |

**手动片段**（任意客户端，改路径即可）：

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

可选：`WAWOO_MEMORY_ROOT` 覆盖目录（默认 `<kit>/docs/memory`）。

### 4.4 改完怎么验证

```bash
grep -A2 WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep -A2 WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep -A2 WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

然后**重启客户端**，在测试会话里调一次 `memory_save` 确认。

### 4.5 工作流也会限制

即使 `READONLY=0`，某些工作流也**禁止** `memory_save`（如 `/compliance-review`）。

### 4.6 在别的项目里用

把 `docs/memory/INDEX.example.md` 复制成你的 `docs/memory/INDEX.md`，即可用同一套记忆机制。

## 5. 调用顺序（MCP 工具链） {#s5}
1. 选**工作流**（入口）；不确定就用 MCP `interpret_intent`。
2. 用**目录 / MCP**选候选（别整份读）。
3. 只打开需要的 **skill**。
4. 按工作流的**输出格式与闸门**（批准、证据）执行。
5. 开工前 `memory_recall`，有决定后 `memory_save`。

> **固定的只有骨架，步骤可以边做边调。** 没必要的一步可跳过、顺序不对可重排、优先级变了可调整、方向错了可改范围或中止，互不影响的子任务可同时做。这些由系统根据证据**自动**完成；你也可以随时插话，但不需要手动编排。

### 5.1 常见场景：你说一句，它走哪条 {#s5-1}
| 你想做的事 | 你说一句 | 会走哪条 |
|---|---|---|
| 修一个 bug | 「修一下这个 bug」 | `/self-review`：先复现，再改，带上证据才算完成 |
| 加一个小功能 | 「加一个设置页」 | `/delivery-lite`：计划 → 实现 → 验证，进度写进 `ACTIVE.md` |
| 评审一个分支 | 「review 这个分支」 | `/self-review`：标准、规格两条线并行评审 |
| 准备一次发布 | 「准备发布包」 | `/release-review`：法务 / 隐私 / 版本 / 安全只读闸门 |
| 查资料再决策 | 「调研 X，再给结论」 | `/research`：先调研 → 产品发现 → 成规格 |
| 重做一个页面 | 「把首页重做」 | `/ui-delivery`：设计 → 实现 → 可访问性核对 |
| 处理线上故障 | 「线上报错了」 | `/incident-response`：先取证、再缓解、再复盘 |

## 6. 维护与校验 {#s6}
```bash
python3 scripts/validate_assets.py    # 资产校验（name=dir、引用、重复、JSON）
python3 scripts/gen_capabilities.py   # 重新生成能力清单（勿手改）
python3 scripts/e2e_flows.py          # MCP 契约 / E2E 冒烟
```

## 7. 注意事项（依赖 / 密钥 / 限制） {#s7}
- **需要 issue tracker 的技能**：`to-spec`、`to-tickets`、`triage` 需先配置（如 GitHub Issues），跑一次 `setup-matt-pocock-skills`。
- **图像生成**：`imagegen-frontend-mobile` 只给提示词；要真正出图用 `fal-gen`（`FAL_KEY`）或 `openrouter-gen`（`OPENROUTER_API_KEY`）。
- **Cursor** 的限制见 §2.3。

> [!WARNING]
> **不要提交密钥**：不要把 API key / token / `.env` 提交进仓库；`memory_save` 会拒绝密钥。

## 8. 排错（FAQ） {#s8}
| 现象 | 处理 |
|---|---|
| `memory_save` 报错（提到 readonly） | 把 `WAWOO_MEMORY_READONLY` 设为 `0` 并**重启客户端**（§4.2） |
| 改了配置但 MCP 没变化 | 重启客户端；Paseo 用 `paseo daemon stop && paseo daemon start` |
| 找不到 `python3` / 命令名不同 | 把各配置里的 `command` 改成真实命令（`python` / `py`） |
| Kilo 的 routing 说明没生效 | `instructions` 必须是**绝对路径**（§2.1） |
| 想确认装好了 | `python3 scripts/validate_assets.py` 出现 `OK` |

## 9. 设定一览（环境变量与配置） {#s9}
先说结论：**多数人只需要设 2 个**——`WAWOO_SKILLS_ROOT`（套件路径）和 `WAWOO_MEMORY_READONLY`（记忆是否可写）。下面把其余开关也列全，按需取用。

### 9.1 核心（几乎必设）

| 变量 | 作用 | 默认 | 怎么设 |
|---|---|---|---|
| `WAWOO_SKILLS_ROOT` | 套件根目录的绝对路径 | `server.py` 的上两级 | 客户端 MCP 的 `environment` / `env`；一键脚本会自动写入 |
| `WAWOO_MEMORY_READONLY` | `1`=只读（不能保存），`0`=可写 | 安装脚本默认 `1` | `install_*.py --memory-writable`，或手改配置（见 [§4](#s4)） |
| `WAWOO_MEMORY_ROOT` | 记忆目录 | `<kit>/docs/memory` | 想放别处时设它 |

### 9.2 工作语言（三层政策）

默认：**代码 = 英语；工程记录与助手回复 = 项目工作语言（本套件 = 日语）；对外说明文档 = 英语主 + 日语副**。

**改法（每个项目改一次）：**

1. 改 `AGENTS.md` §1（权威契约）；
2. 同步 `.kilo/skills/language-policy/SKILL.md` 里两处「(wawoo-skills: Japanese)」；
3. 重新生成路由说明：`python3 scripts/gen_router.py`；
4. 让本文件的语言说明与之一致。

> 想换「整篇文档用哪种语言」，就相应产出 `README.<lang>.md` / `docs/USAGE.<lang>.md`（本套件已有 `en / ja / zh-CN / ko`）。

### 9.3 图片生成

要**真正出图**就配 key；`imagegen-frontend-mobile` 只写提示词、不调用模型。

| 能力 | 需要的 key | 放哪 | 说明 |
|---|---|---|---|
| `fal-gen`（真正出图，fal.ai） | `FAL_KEY`（格式 `key_id:secret`） | `.kilo/skills/fal-gen/.env`（从 `.env.example` 复制） | **不要提交、不要回显**；默认最便宜模型 `flux/schnell` |
| `openrouter-gen`（真正出图，OpenRouter） | `OPENROUTER_API_KEY`（格式 `sk-or-v1-...`） | `.kilo/skills/openrouter-gen/.env`（从 `.env.example` 复制） | 默认 `google/gemini-2.5-flash-image`；可用 `OPENROUTER_IMAGE_MODEL` 改；更便宜可换 `google/gemini-3.1-flash-lite-image` |
| `imagegen-frontend-mobile` | 不需要 | — | **只产出提示词**，不调用模型 |

- 可选：`FAL_BASE_URL` 指定 fal.ai 端点。
- 两个出图 skill 都用一份**清单（manifest）**批量生成，已有文件会自动跳过（可安全重跑）：先 `--dry-run`，确认后再生成（出图要花钱）。

> [!WARNING]
> **永远不要把 key 写进仓库**（`.env` 也不要提交）。密钥只放本地 `.env`，并确认它已被 `.gitignore` 忽略（本仓已忽略 `.env` / `.env.*`，只保留 `.env.example`）。

### 9.4 Google Modern Web Guidance

**这是什么**：Google 写的一套「现代网页怎么做」的在线指南（约 262 篇）。

**解决什么**：AI 的知识会过时。做网页时，它可以按需去查最新写法，也能帮你找出该淘汰的旧写法。

**怎么用**：说一句需求就行；助手会用 `modern-web-guidance-bridge` 去搜（`mwg_search`）和取（`mwg_retrieve`），指南本身不复制进仓库。

**前提**：需要 Node.js 和网络；离线就设 `WAWOO_MWG_DISABLE=1` 关掉。

**和现有规范冲突时**：以你的产品规范 / Vercel 为准。

### 9.5 意图路由（进阶，通常不用改）

`interpret_intent` 负责「自动选流程」；下面这些只影响它的匹配细节，**通常不用改**。

| 变量 | 作用 | 默认 |
|---|---|---|
| `WAWOO_INTENT_LEARN_DB` | 学到的触发词库 | `data/intent_learned.db` |
| `WAWOO_INTENT_SESSION` | 会话门禁状态文件 | `<root>/data/intent_session.json` |
| `WAWOO_INTENT_RESUME` | `1` 时重启后恢复门禁 | 关 |
| `WAWOO_INTENT_CLIENT` | 按客户端分文件，避免门禁串台 | 空 |
| `WAWOO_INTENT_SOCKET` | 常驻 `intent_receiver.py` 的 socket | 空 |
| `WAWOO_INTENT_LEXICAL` / `_THRESHOLD` / `_MARGIN` / `_MIN_TOKENS` / `_MAX_ABSTAIN` / `_DEBUG` | 词法路由的开关、阈值与调试 | 见 `mcp/README.md` |

### 9.6 安装与 CI

只影响安装与 CI，不影响日常使用。

| 变量 / 参数 | 作用 |
|---|---|
| `KILO_GLOBAL_DIR` | `install_global.py` 的目标目录（默认 `~/.config/kilo`） |
| `CURSOR_API_KEY` | 仅 Cursor CLI **无人值守 CI** 使用（本地一般用 `agent login`） |

### 9.7 文档审校脚本（可选）

可选；只用于脚本审校，不参与主流程。

`scripts/audit_docs_dual.py` / `scripts/openrouter_doc_audit.py` 用 OpenRouter 做文档审校：

- `OPENROUTER_API_KEY`（必需）
- `OPENROUTER_DOC_MODEL`（默认 `google/gemini-2.5-flash`）
- `OPENROUTER_QWEN_MODEL`（默认 `qwen/qwen3-30b-a3b`）

### 9.8 外部前提

需要 issue tracker 的 3 个技能：`to-spec`、`to-tickets`、`triage`（见 `scripts/readiness.json`）。配置一次：`setup-matt-pocock-skills`。

### 9.9 配置文件对照

各端配置文件在哪；**改完要重启客户端**。

| 客户端 / 用途 | 文件 |
|---|---|
| Kilo | `~/.config/kilo/kilo.jsonc`（项目内 `kilo.json`） |
| Cursor（用户 / 项目） | `~/.cursor/mcp.json` / `<workspace>/.cursor/mcp.json` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` |
| Codex | `~/.codex/config.toml` |
| 图片 key | `.kilo/skills/fal-gen/.env`、`.kilo/skills/openrouter-gen/.env`（**勿提交**） |
