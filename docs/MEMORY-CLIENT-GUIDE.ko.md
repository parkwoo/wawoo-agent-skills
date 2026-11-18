# 메모리: 회상·저장·클라이언트 설정

[English](MEMORY-CLIENT-GUIDE.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## 이 키트의 memory

팀 **결정·실수**를 `docs/memory/` Markdown에 저장합니다. 작업 전 **`memory_recall`**, 결정 후 **`memory_save`**(쓰기 허용 시).

클라이언트 내장 대화 메모리와 **다릅니다**. 충돌 시 **`docs/memory/` 우선**. [`memory/MEMORY-TOOLS.md`](memory/MEMORY-TOOLS.md)

## MCP 도구

| 도구 | 역할 |
|------|------|
| `memory_recall` | `INDEX.md`·topic 읽기. **쓰기 금지여도 가능** |
| `memory_save` | [`memory/TEMPLATE.md`](memory/TEMPLATE.md)에 1건 추가. `WAWOO_MEMORY_READONLY=1`이면 **거부** |

## `WAWOO_MEMORY_READONLY`

| 값 | 동작 | 용도 |
|----|------|------|
| **`1`** | **recall-only** | 설치 기본·감사 |
| **`0`** | 읽기+쓰기 | `docs/memory/`에 결정 저장 |

**MCP environment**에 설정 후 **클라이언트 재시작**.

## 첫 설정

1. **wawoo-skills** clone·절대 경로  
2. install 시 **`--memory-writable`** ([CLIENT-INTEGRATION-GUIDE.ko.md](CLIENT-INTEGRATION-GUIDE.ko.md))  
3. `grep WAWOO_MEMORY_READONLY`  
4. **`memory_save`** 테스트  

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

**목차:** [GUIDES.ko.md](GUIDES.ko.md)