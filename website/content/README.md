# 官网展示数据（SSOT）

## `home-copy.zh.json`

首页标题、段落导语、区块标题等**可变文案**（不含统计数字）。

另含 `stats_subline`（馆藏区桥接句）、`how_cards[]`（`#how` 六张卡标题与正文）。

页面加载后由 `main.js` 写入带 `data-kit-copy-text` 的节点，并同步 subline / how 卡片。

## `site-metrics.json`

首页 hero 信任条、统计行、meta description、部分正文中的**可变数字**由此文件提供。

| 字段 | 用途 |
|------|------|
| `release_version` | 信任条 `v*`、页脚版本 |
| `counts.*` | 技能 / 角色 / 工作流 / 客户端等数量 |
| `labels_zh.*` | 统计行中文标签 |
| `meta_description_zh` | `<meta name="description">`（`{skills}` 等占位符） |
| `copy_zh.*` | 含数字的句式（如阶段数 + 工作流数） |

修改后刷新浏览器即可（`main.js` 会 `fetch` 本 JSON）。无 JavaScript 时 HTML 内保留与 JSON 相同的默认数字作降级。

正本对照：`README.zh-CN.md` · `VERSION` · `.kilo/CAPABILITIES.md`（改库存时建议四处一起核对）。