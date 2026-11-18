# 集成：Paseo、Google、pstack

[English](INTEGRATIONS.md) · [简体中文](INTEGRATIONS.zh-CN.md) · [日本語](INTEGRATIONS.ja.md) · [한국어](INTEGRATIONS.ko.md)

公开套件**正式对接**的外部能力（非项目私有 skill）。

## Paseo

[Paseo](https://github.com/getpaseo/paseo) 内置 **OpenCode**，与本套件的 `install_opencode.py` 配置一致。

- 配置：`~/.config/opencode/opencode.json`
- 安装：`python3 scripts/install_opencode.py --memory-writable`（可选）
- 改环境变量后：`paseo daemon restart`
- 详见 [CLIENT-INTEGRATION-GUIDE.zh-CN.md](CLIENT-INTEGRATION-GUIDE.zh-CN.md)

## Google

- **Modern Web Guidance**：`modern-web-guidance-bridge` + MCP `mwg_search` / `mwg_retrieve`（`npx modern-web-guidance`，不落库）
- **design-md**：Stitch 格式设计文档（Google Labs  lineage，技能目录 Apache-2.0）
- UI 走 `/ui-delivery`；见 [SKILL-UPLIFT-PILOT.md](SKILL-UPLIFT-PILOT.md)

## pstack

- MIT 吸收：**`principle-*`** 与 `blast-radius` 等验证类 skill
- 许可：`LICENSES/pstack-MIT.txt` · [ATTRIBUTION.md](../.kilo/skills/ATTRIBUTION.md)
- 不要一次读完所有 principle；用 `ask-matt` 或 workflow 点名

**索引：** [GUIDES.zh-CN.md](GUIDES.zh-CN.md)