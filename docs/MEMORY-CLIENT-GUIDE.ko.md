# 메모리: 회상·저장·클라이언트 설정

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## 도구

| MCP | 역할 |
|-----|------|
| `memory_recall` | `docs/memory/` 읽기. 쓰기 금지여도 사용 가능. |
| `memory_save` | 한 건 추가. `WAWOO_MEMORY_READONLY=1`이면 **거부**. 비밀은 항상 거부. |

**정본:** `<kit>/docs/memory/` · `docs/memory/MEMORY-TOOLS.md`

## `WAWOO_MEMORY_READONLY`

| 값 | 동작 | 용도 |
|----|------|------|
| **`1`** (설치 기본) | recall-only | 안전·감사·임의 repo |
| **`0`** | 읽기+쓰기 | 일상 개발·클라이언트 통일 |

**클라이언트 MCP env**. 변경 후 **재시작** (Kilo/Cursor Reload, OpenCode, `paseo daemon restart`).

## 설정 위치

| 클라이언트 | 파일 | 명령 |
|------------|------|------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `install_global.py` **`--memory-writable`** |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `install_opencode.py` **`--memory-writable`** |
| Cursor 사용자 | `~/.cursor/mcp.json` | `install_cursor_global.py` **`--memory-writable`** |
| Cursor 프로젝트 | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --memory-writable` |

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

## 검증

```bash
grep WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

일부 workflow는 `memory_save` 금지 (`compliance-review` 등). `docs/INTENT-ROUTING.md`

**목차:** [GUIDES.ko.md](GUIDES.ko.md)