---
name: wawoo-oss-boundary
description: wawoo-skills 是公开 OSS — 只能放通用、产品无关、英文的 skill/agent/workflow/MCP；私人・项目级・本地化的东西一律放内部 workspace/skills（或项目仓）。新增/修改前先判定边界。内部运用。
---

# wawoo-skills（OSS）公开边界

**一句话**：`/home/git/wawoo-skills` = 公开开源 kit：**通用、产品无关、英文**。私人 / 项目级 / 本地化资产只放内部 `/home/git/workspace/skills`（或对应项目仓）。

## 可以放（通用）

- 与具体公司/项目无关的 skill / agent / workflow / MCP。
- 通用工程实践（`principle-*`、评审、测试、发布、合规等）。
- 第三方 OSS 资产（保留 `LICENSE` / `NOTICE` / `ATTRIBUTION`）。

## 不能放（私人 / 项目级 / 本地化）

- 公司项目名/代号：`nextwave*`、`kiun*`、`co-taro*`、`medibridge`、`rokuyo` 等。
- 内部 URL / 主机 / IP / 端口 / 凭证；`repo-docs/`、vault、私有路径。
- 项目专属 agent / command / workflow（如 `platform-*`、`kiun-*`）。
- 把某种语言/区域写死的本地化政策作为默认。
- 私人 Git 身份、账号、环境变量、本机绝对路径。
- 非英文内容（公开仓要求英文；既定的双语 `*.ja.md` 例外）。

## 新增 / 修改前检查

1. 判定：通用能力还是本项目专用？**不确定 → 放内部**。
2. `grep -rliE "nextwave|kiun|co-taro|medibridge|rokuyo|platform-ops"` 应为空。
3. 英文（除既定双语 `.ja.md`）。
4. 第三方资产：`LICENSE` / `NOTICE` / `ATTRIBUTION` + `.publish-allowlist`。
5. 跑 `python3 scripts/validate_assets.py` 与 `python3 scripts/e2e_flows.py`。
6. `internal/`、私有文档、个人规则不得进入公开树（`.publish-allowlist` 守门）。

## 放错地方时

从 wawoo-skills 删除并移到 `/home/git/workspace/skills`；更新 `ATTRIBUTION` / `CAPABILITIES`；必要时 bump 版本并重新发布。
