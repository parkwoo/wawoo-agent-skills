<p align="center">
  <img src="assets/wawoo-skills-logo.png" width="128" alt="wawoo-skills 로고" />
</p>

<h1 align="center">wawoo-skills 사용 가이드</h1>

<p align="center">
  <strong>설치, 설정, 사용 가이드.</strong>
</p>

<p align="center">
  <a href="USAGE.md">English</a> ·
  <a href="USAGE.ja.md">日本語</a> ·
  <a href="USAGE.zh-CN.md">简体中文</a> ·
  <a href="USAGE.ko.md">한국어</a>
</p>

<p align="center">
  <a href="../README.ko.md">README로 돌아가기</a> ·
  <a href="https://github.com/parkwoo/wawoo-skills">GitHub</a>
</p>

> 이 문서는 **설치, 설정, 문제 해결**에 중점을 둡니다. `wawoo-skills`가 무엇이고 왜 필요한지에 대한 자세한 내용은 [`README.ko.md`](../README.ko.md)를 참조하세요.

**대상**: `wawoo-skills`를 처음 도입하는 개발자. 약 10분 내에 설치 및 실행이 가능합니다.

**지원**: Kilo, Cursor, OpenCode, Codex, Claude Code, Paseo — Python 3 표준 라이브러리만 사용합니다.

## 빠른 시작 (먼저 보기)

1.  Python 3 확인 — [§0 사전 조건](#s0)
2.  클라이언트별 연결 — [§2 클라이언트별 연결](#s2) (**Kilo / Cursor가 가장 간단**)
3.  검증 — `python3 scripts/validate_assets.py` 실행 후 `OK`가 나오면 완료

나머지(MCP 매개변수, 메모리 설정, 문제 해결)는 아래 목차에서 필요할 때 참조하세요.

> **설정을 변경해야 하나요?** 작업 언어, 이미지 생성 키, 메모리, 라우팅 튜닝, 설치 대상은 모두 [**§9 설정 목록**](#s9)에 있습니다.

## 목차

- [0. 사전 조건: Python 3](#s0)
- [1. 무엇이 설치되나](#s1)
  - [1.1 세 가지 구성 요소: 찾는 방법](#s1-1)
  - [1.2 워크플로 구조](#s1-2)
  - [1.3 의도 라우팅(Intent Routing)](#s1-3)
  - [1.4 직접 추가하기 (skill / agent / workflow)](#s1-4)
- [2. 클라이언트별 연결 (Kilo / Cursor / OpenCode / Codex / Paseo)](#s2)
  - [2.1 Kilo (CLI / Kilo Code)](#s2-1)
  - [2.2 OpenCode](#s2-2)
  - [2.3 Cursor](#s2-3)
  - [2.4 Paseo (OpenCode 내장, 다른 클라이언트와 다름)](#s2-4)
  - [2.5 Codex (OpenAI Codex CLI / 확장)](#s2-5)
  - [2.6 Claude Code (Anthropic CLI)](#s2-6)
- [3. MCP 서비스](#s3)
- [4. 메모리(memory) 설정](#s4)
  - [4.1 도구가 하는 일](#s4-1)
  - [4.2 `WAWOO_MEMORY_READONLY` (읽기 전용 / 쓰기 가능)](#s4-2)
  - [4.3 클라이언트별 설정 위치](#s4-3)
  - [4.4 확인 방법](#s4-4)
  - [4.5 워크플로도 제한](#s4-5)
  - [4.6 다른 프로젝트에서](#s4-6)
- [5. 호출 순서 (MCP 도구 체인)](#s5)
  - [5.1 흔한 시나리오: 한 번의 작업 → 어떤 워크플로](#s5-1)
- [6. 유지보수와 검증](#s6)
- [7. 주의사항 (의존성, 키, 제한)](#s7)
- [8. 문제 해결 (FAQ)](#s8)
- [9. 설정 목록 (환경 변수와 설정)](#s9)
  - [9.1 핵심 (거의 필수)](#s9-1)
  - [9.2 작업 언어 (3단계 정책)](#s9-2)
  - [9.3 이미지 생성](#s9-3)
  - [9.4 Google Modern Web Guidance](#s9-4)
  - [9.5 의도 라우팅 (고급, 보통 변경 불필요)](#s9-5)
  - [9.6 설치와 CI](#s9-6)
  - [9.7 문서 검토 스크립트 (선택)](#s9-7)
  - [9.8 외부 전제](#s9-8)
  - [9.9 설정 파일 비교](#s9-9)

<a id="s0"></a>

## 0. 사전 조건: Python 3

-   **Python 3(표준 라이브러리만)**: MCP 서비스와 유지보수 스크립트는 표준 라이브러리만 사용하므로, 추가 패키지가 필요 없습니다.
-   `PATH`에 `python3`가 있어야 합니다(Windows는 `python`). 확인: `python3 --version` → `3.x`.
    -   macOS: `xcode-select --install`; Linux: `apt install python3` 등; Windows: https://www.python.org/downloads/ 에서 설치하고 **"Add python.exe to PATH"**를 체크하세요.
-   MCP는 `python3`로 실행합니다(`kilo.json`, `.cursor/mcp.json`). 만약 명령 이름이 다르다면(`python` / `py`), 각 설정의 `command`를 실제 명령으로 변경하세요.
-   네트워크나 `.env` 파일은 필요 없습니다(MCP는 stdio를 통해 통신합니다).

<a id="s1"></a>

## 1. 무엇이 설치되나

요약: **스킬은 「무엇을 할 줄 아는가」, 역할은 「누구의 관점에서 보는가」, 워크플로는 「어떤 순서로, 무엇을 완료로 간주할 것인가」입니다.**

<a id="s1-1"></a>

### 1.1 세 가지 구성 요소: 찾는 방법

스킬 / 역할 / 워크플로의 정의는 [README의 「용어」](../README.ko.md)를 참조하세요. 여기서는 **찾는 방법**만 다룹니다:

| 분류 | 찾는 방법 |
|---|---|
| 스킬 skills | `skill_search` / `.kilo/CAPABILITIES.md` |
| 역할 agents | `agent_get` |
| 워크플로 workflows | `workflow_get` |
| MCP 서비스 | `python3 mcp/server.py` |

<a id="s1-2"></a>

### 1.2 워크플로 구조

**12개 워크플로 목록은 [README「12개 워크플로」](../README.ko.md)에 있습니다.** 여기서는 구조만 설명합니다 — 각 워크플로에는:

-   **단계(phase)**: 목표 / 담당 역할 / 사용하는 스킬 / `exit_criteria`; `workflow_get {name, phase}`로 단계별 확인.
-   **게이트(gate)**: 승인, 증거, 실패 관찰; **검토 계열 워크플로는 읽기 전용**이며(구현 단계 없음).
-   **완료 조건(exit_criteria)**: 이 조건이 충족되지 않으면 완료로 간주되지 않습니다.

**`implement` 단계가 없는 워크플로**(`/design-review`, `/compliance-review`, `/release-review`, `/research`, `/status-report` 등)는 구현 단계로 진행되지 않습니다. 코드를 수정해야 한다면 `/delivery-lite`, `/feature-delivery`, `/ui-delivery`, `/incident-response`, `/self-improve` 중 하나로 전환하세요.

<a id="s1-3"></a>

### 1.3 의도 라우팅(Intent Routing)

**워크플로 선택 순서**(명시적 → 로컬 어휘 → 학습된 → 모델 점수)는 [README](../README.ko.md)를 참조하세요. 여기서는 **선택된 워크플로의 관리**를 다룹니다:

-   **도구 게이트**: 해당 워크플로의 **허용 도구 목록**(`mcp_tools_allow`)으로 MCP 도구를 제한합니다 — 감사 계열은 읽기 도구만 사용하며, 구현 단계는 없습니다.
-   **세션 게이트**: 호출 간에 「지금 어느 워크플로인지」를 기억합니다; `WAWOO_INTENT_RESUME=1`이면 재시작 후 복원되며, `WAWOO_INTENT_CLIENT`로 다중 클라이언트 충돌을 방지합니다.
-   **마무리**: `workflow_clear`로 현재 세션 게이트를 해제합니다.
-   **라우팅 재정의**: `/name`을 직접 사용하거나, `interpret_intent`에 `scoring`을 전달합니다. **잘못 선택되거나 찾을 수 없는 경우**: [§8 문제 해결](#s8) (대개 MCP를 재시작하지 않은 경우).

<a id="s1-4"></a>

### 1.4 직접 추가하기 (skill / agent / workflow)

-   **skill**: `.kilo/skills/<name>/SKILL.md`를 생성합니다; `name`은 디렉터리명과 같아야 하고, 엔트리는 4KB 이하, 상세 내용은 `references/`에 작성합니다.
-   **agent**: `.kilo/agents/<name>.md`를 생성합니다(`mode: primary|subagent`, 권한은 필요에 따라).
-   **workflow**: `.kilo/commands/<name>.md`를 생성합니다(frontmatter: `description` / `agent` / `replay`).
-   그다음: `python3 scripts/validate_assets.py` → `python3 scripts/gen_capabilities.py` → **MCP / Kilo 재시작**(명령은 시작 시 캐시됨).

<a id="s2"></a>

## 2. 클라이언트별 연결 (Kilo / Cursor / OpenCode / Codex / Paseo)

<a id="s2-1"></a>

### 2.1 Kilo (CLI / Kilo Code)

0.  **먼저 로그인**: `kilo auth login`(provider 선택 후 로그인). Paseo에서 Kilo를 실행하기 전에도 로그인이 필요합니다.
1.  이 저장소 디렉터리를 열면 됩니다(`.kilo/` 자동 발견; MCP는 `kilo.json`으로 활성화).
2.  워크플로는 `/feature-delivery`와 같은 슬래시 명령으로 실행하며, 스킬은 모델이 선택하거나 직접 지정할 수 있습니다.

**전역 설치**(모든 프로젝트에서 사용, 재실행 가능):

```bash
python3 scripts/install_global.py --dry-run     # 변경 미리보기
python3 scripts/install_global.py               # 적용(기본 미러: 잉여 파일 삭제)
python3 scripts/install_global.py --no-delete   # 잉여 파일 보존
python3 scripts/install_global.py --memory-writable   # memory_save 허용
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py   # 대상 지정
```

-   **세 가지를 수행합니다**: ① MCP 등록(절대 경로 `python3` + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`); ② `ROUTER.md` 생성 후 **절대 경로**로 `instructions`에 등록; ③ 기본 역할을 `wawoo-auto`로 설정(`--default-agent` / `--no-default-agent`로 변경).
-   Kilo의 `instructions`는 **절대 경로여야** 합니다(상대 경로는 주입되지 않습니다).
-   **적용 후 Kilo를 재시작해야 합니다**(agents / commands / instructions는 시작 시 캐시; VS Code: Reload Window).

<a id="s2-2"></a>

### 2.2 OpenCode

`opencode.json`에 로컬 stdio MCP로 추가:

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

-   한 번에 설치: `python3 scripts/install_opencode.py`(기본 읽기 전용); 쓰기 허용은 `--memory-writable` 옵션을 사용합니다.
-   OpenCode는 **네이티브 슬래시 명령 / 스킬 실행을 지원하지 않습니다**. 항상 MCP를 통해 `interpret_intent` → `workflow_get` → `skill_get` 순서로 실행됩니다.

<a id="s2-3"></a>

### 2.3 Cursor

1.  디렉터리를 엽니다(`AGENTS.md`와 `.cursor/rules`를 읽음).
2.  **Settings → MCP**에서 `wawoo-skills`를 활성화합니다(`.cursor/mcp.json`).

```bash
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace   # MCP만 설치(프로젝트 mcp.json 덮어씀)
python3 scripts/install_cursor_global.py                                     # 사용자 레벨 ~/.cursor(기존 mcp.json에 병합)
# memory_save 허용:
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace --memory-writable
```

**Cursor의 제한 사항:**

-   슬래시 명령(`/feature-delivery` 등) **동작 안 함**;
-   **에이전트 전환 없음**(`@.kilo/agents/<role>.md`를 읽어 직접 역할 적용);
-   **`SKILL.md`를 자동 발견/실행하지 않음**.

**MCP가 없을 때 폴백**: `@.kilo/CAPABILITIES.md`에서 후보 선택 → `@.kilo/skills/<name>/SKILL.md` 읽기 → 절차 수행; 워크플로는 `@.kilo/commands/<name>.md`.

<a id="s2-4"></a>

### 2.4 Paseo (OpenCode 내장, 다른 클라이언트와 다름)

Paseo는 **멀티 에이전트 IDE**로, OpenCode를 내장하고 에이전트를 자체 **daemon**(백그라운드 서비스) 안에서 실행합니다:

-   **설정**: **동일한** `~/.config/opencode/opencode.json`을 사용합니다(MCP `wawoo-skills`가 여기에 연결); 설치는 `python3 scripts/install_opencode.py`를 사용합니다.
-   **먼저 로그인**: Paseo가 `kilo` / `cursor`를 실행하기 전에 해당 CLI에서 먼저 로그인해야 합니다(Kilo는 `kilo auth login`), 그렇지 않으면 실행되지 않습니다.
-   **재시작 규칙**: 환경 변수나 MCP를 변경하면 다음 명령을 사용합니다.
    ```bash
    paseo daemon stop && paseo daemon start     # 완전 전환
    # 또는: paseo daemon restart                 # worker만 재시작
    ```
    **daemon 재시작은 그것이 띄운 세션도 함께 재시작합니다.**
-   **독립 프로세스**: VS Code의 Kilo 확장, Cursor 데스크톱, 독립 터미널의 opencode/kilo/cursor는 **daemon의 영향을 받지 않습니다**.
-   **플러그인은 별개**: Paseo 자체 플러그인 스킬(`npx skills add getpaseo/paseo`)은 이 키트와 무관합니다; MCP와 daemon만 맞추면 함께 쓸 수 있습니다.

<a id="s2-5"></a>

### 2.5 Codex (OpenAI Codex CLI / 확장)

Codex는 `AGENTS.md`를 읽고 스킬을 로드하며 MCP를 지원합니다(`~/.codex/config.toml`). 이 키트를 stdio MCP로 추가:

```toml
[mcp_servers.wawoo-skills]
command = "python3"
args = ["/abs/path/to/wawoo-skills/mcp/server.py"]
env = { WAWOO_SKILLS_ROOT = "/abs/path/to/wawoo-skills", WAWOO_MEMORY_READONLY = "1" }
```

-   스킬 디렉터리는 `.agents/skills/`를 가리킵니다(`.kilo/skills/` 내용을 넣을 경우).
-   Codex는 현재 **수동 설정**이 필요하며, 이 저장소는 원클릭 스크립트를 제공하지 않습니다. Codex는 `/skills`, `$skill` 호출과 MCP(`codex mcp add ...`)를 지원합니다.

<a id="s2-6"></a>

### 2.6 Claude Code (Anthropic CLI)

Claude Code는 MCP, `CLAUDE.md`, `.claude/skills/`, `.claude/commands/`(네이티브 슬래시 명령)를 지원합니다.

```bash
claude mcp add wawoo-skills \
  --env WAWOO_SKILLS_ROOT=/abs/path/to/wawoo-skills \
  --env WAWOO_MEMORY_READONLY=1 \
  -- python3 /abs/path/to/wawoo-skills/mcp/server.py
```

-   **스킬**: `.kilo/skills`를 `.claude/skills`로 복사하거나 심볼릭 링크합니다.
-   **워크플로**: `.kilo/commands/*.md`를 `.claude/commands/`로 복사합니다(네이티브 슬래시 명령).
-   **계약**: `AGENTS.md`와 `CLAUDE.md` 중 **하나만** 사용하며, 동시에 만들지 마세요.
-   **서브에이전트**: `Agent`(`subagent_type`)를 사용하며, `swarm` / `reflect` 병렬 실행이 가능합니다.

> **Pi 등 기타 MCP 클라이언트**: stdio MCP를 지원하면 동일한 `python3 mcp/server.py`로 연결할 수 있습니다. 스킬 디렉터리는 클라이언트 규칙(예: `.pi/skills/`)을 따릅니다. 서브에이전트 확장이 있으면 `swarm` / `reflect`는 병렬, 없으면 순차 실행(둘 다 지원).

<a id="s3"></a>

## 3. MCP 서비스

이 키트의 기능은 **로컬 MCP 서비스**로 노출됩니다(stdio: 로컬 프로세스 통신, 클라이언트가 자동 실행, 포트 불필요).

```bash
python3 mcp/server.py          # 보통 클라이언트가 실행
python3 scripts/e2e_flows.py   # 계약 / E2E 스모크
```

자주 쓰는 도구: `capabilities`, `skill_search`, `skill_get`, `workflow_get`, `agent_get`, `memory_recall`, `memory_save`; 의도 라우팅: `interpret_intent` → `workflow_get` → … → `workflow_clear`; 하위 작업: `delegate_subtask`.

<a id="s4"></a>

## 4. 메모리(memory) 설정

### 4.1 도구가 하는 일

| MCP 도구 | 역할 |
|---|---|
| `memory_recall` | `docs/memory/`(INDEX + 주제 파일)에서 과거 결정을 읽습니다. **읽기 전용 모드에서도 사용 가능.** |
| `memory_save` | 결정을 추가합니다(INDEX + 주제 파일, 템플릿 `docs/memory/TEMPLATE.md`). **`WAWOO_MEMORY_READONLY=1`이면 거부**; 키는 어떤 경우에도 거부됩니다. |

메모리의 **원본 소스(Source of Truth)**은 `<kit>/docs/memory/`의 Markdown 파일입니다; 클라이언트 내장 메모리와 충돌하면 **파일을 우선**합니다(`docs/memory/MEMORY-TOOLS.md` 참고).

### 4.2 `WAWOO_MEMORY_READONLY` (읽기 전용 / 쓰기 가능)

| 값 | 효과 | 언제 |
|---|---|---|
| **`1`**(설치 기본) | **읽기 전용**: `memory_save` 오류, `memory_recall` 정상 | 아무 프로젝트에 MCP 등록; 감사/컴플라이언스 세션; 에이전트가 키트에 쓰는 것을 원치 않을 때 |
| **`0`** | **읽기/쓰기 가능**: `WAWOO_SKILLS_ROOT/docs/memory/`에 기록 허용 | 키트 저장소 또는 동일한 `docs/memory/` 레이아웃 작업 공간 |

MCP 서비스는 **시작 시** 클라이언트 설정의 환경 변수를 읽습니다 — **파일만 변경하는 것으로는 부족하며, 클라이언트 재시작이 필수입니다**(Kilo Reload, Cursor Reload, OpenCode 재시작, Paseo 내장 OpenCode는 `paseo daemon restart`).

### 4.3 클라이언트별 설정 위치

| 클라이언트 | 설정 파일 | 권장 명령(재실행 가능) |
|---|---|---|
| Kilo(전역) | `~/.config/kilo/kilo.jsonc` → `mcp.wawoo-skills.environment` | `python3 scripts/install_global.py`(기본 `1`) 또는 `--memory-writable`(`0`) |
| OpenCode(터미널 또는 **Paseo 내장**) | `~/.config/opencode/opencode.json` → `mcp.wawoo-skills.environment` | `python3 scripts/install_opencode.py` 또는 `--memory-writable` |
| Cursor(사용자) | `~/.cursor/mcp.json` → `mcpServers.wawoo-skills.env` | `python3 scripts/install_cursor_global.py`(다른 MCP 병합) + `--memory-writable` |
| Cursor(프로젝트) | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root>` + `--memory-writable`(덮어씀, 수동 병합 필요) |

**수동 조각**(아무 클라이언트, 경로만 수정):

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

선택: `WAWOO_MEMORY_ROOT`로 디렉터리 변경(기본 `<kit>/docs/memory`).

### 4.4 확인 방법

```bash
grep -A2 WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep -A2 WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep -A2 WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

그다음 **클라이언트를 재시작**하고 테스트 세션에서 `memory_save`를 한 번 호출하여 확인합니다.

### 4.5 워크플로도 제한

`READONLY=0`이어도 일부 워크플로는 `memory_save`를 **금지**합니다(예: `/compliance-review`).

### 4.6 다른 프로젝트에서

`docs/memory/INDEX.example.md`를 `docs/memory/INDEX.md`로 복사하면 동일한 메모리 메커니즘을 사용할 수 있습니다.

<a id="s5"></a>

## 5. 호출 순서 (MCP 도구 체인)

1.  **워크플로** 선택(진입점); 애매하면 MCP `interpret_intent`를 사용합니다.
2.  **목록 / MCP**로 후보를 선택합니다(전부를 읽지 않기).
3.  필요한 **skill**만 엽니다.
4.  워크플로의 **출력 형식과 게이트**(승인, 증거)에 따라 실행합니다.
5.  시작 전 `memory_recall`, 결정 후 `memory_save`를 수행합니다.

> **고정은 기본 구조, 단계는 조정 가능.** 불필요한 단계는 건너뛰고, 순서가 틀리면 재배열, 우선순위가 바뀌면 조정, 방향이 틀리면 범위 변경이나 중단, 서로 독립적인 하위 작업은 동시에. 이 조정은 시스템이 증거에 따라 **자동**으로 합니다; 언제든 개입할 수 있지만 수동 편성은 필요 없습니다.

<a id="s5-1"></a>

### 5.1 흔한 시나리오: 한 번의 작업 → 어떤 워크플로

| 하고 싶은 일 | 한마디 | 실행되는 것 |
|---|---|---|
| 버그 수정 | 「이 버그 고쳐줘」 | `/self-review`: 먼저 재현, 수정, 증거와 함께 완료 |
| 작은 기능 추가 | 「설정 페이지 추가해줘」 | `/delivery-lite`: 계획 → 구현 → 검증, `ACTIVE.md`에 기록 |
| 브랜치 리뷰 | 「이 브랜치 리뷰해줘」 | `/self-review`: 표준·스펙 두 축 병행 리뷰 |
| 릴리스 준비 | 「릴리스 준비해줘」 | `/release-review`: 법무 / 개인정보 / 버전 / 보안 읽기 전용 게이트 |
| 조사 후 결정 | 「X 조사하고 결론 내줘」 | `/research`: 조사 → 제품 발견 → 스펙화 |
| 페이지 재작업 | 「홈페이지 다시 만들어줘」 | `/ui-delivery`: 설계 → 구현 → 접근성 확인 |
| 장애 대응 | 「프로덕션에서 에러 나요」 | `/incident-response`: 먼저 증거 → 완화 → 회고 |

<a id="s6"></a>

## 6. 유지보수와 검증

```bash
python3 scripts/validate_assets.py    # 자산 검증(name=dir, 참조, 중복, JSON)
python3 scripts/gen_capabilities.py   # 능력 목록 재생성(직접 편집 금지)
python3 scripts/e2e_flows.py          # MCP 계약 / E2E 스모크
```

<a id="s7"></a>

## 7. 주의사항 (의존성, 키, 제한)

-   **이슈 트래커가 필요한 스킬**: `to-spec`, `to-tickets`, `triage`는 먼저 설정(GitHub Issues 등) 후 `setup-matt-pocock-skills`를 실행해야 합니다.
-   **이미지 생성**: `imagegen-frontend-mobile`은 프롬프트만 제공합니다; 실제 이미지는 `fal-gen`(`FAL_KEY`) 또는 `openrouter-gen`(`OPENROUTER_API_KEY`)을 통해 생성됩니다.
-   **Cursor**의 제한 사항은 §2.3을 참조하세요.

> [!WARNING]
> **키를 커밋하지 마세요**: API key / token / `.env` 파일을 저장소에 커밋하지 마세요; `memory_save`는 키를 거부합니다.

<a id="s8"></a>

## 8. 문제 해결 (FAQ)

| 증상 | 처리 |
|---|---|
| `memory_save` 오류(readonly 언급) | `WAWOO_MEMORY_READONLY`를 `0`으로 바꾸고 **클라이언트 재시작**(§4.2) |
| 설정을 바꿨는데 MCP가 그대로 | 클라이언트 재시작; Paseo는 `paseo daemon stop && paseo daemon start` |
| `python3`를 찾을 수 없음 / 명령 이름이 다름 | 각 설정의 `command`를 실제 명령(`python` / `py`)으로 |
| Kilo 라우팅 설명이 적용 안 됨 | `instructions`는 **절대 경로**여야 함(§2.1) |
| 설치 확인 | `python3 scripts/validate_assets.py`에서 `OK` |

<a id="s9"></a>

## 9. 설정 목록 (환경 변수와 설정)

먼저 결론: **대부분은 2개만 설정**하면 됩니다 — `WAWOO_SKILLS_ROOT`(키트 경로)와 `WAWOO_MEMORY_READONLY`(메모리 쓰기 여부).

### 9.1 핵심 (거의 필수)

| 변수 | 역할 | 기본 | 설정 방법 |
|---|---|---|---|
| `WAWOO_SKILLS_ROOT` | 키트 루트의 절대 경로 | `server.py`의 두 단계 위 | 클라이언트 MCP의 `environment` / `env`; 원클릭 스크립트가 자동 기록 |
| `WAWOO_MEMORY_READONLY` | `1`=읽기 전용(저장 불가), `0`=쓰기 가능 | 설치 스크립트 기본 `1` | `install_*.py --memory-writable`, 또는 설정 수동 편집([§4](#s4)) |
| `WAWOO_MEMORY_ROOT` | 메모리 디렉터리 | `<kit>/docs/memory` | 다른 곳에 둘 때 |

### 9.2 작업 언어 (3단계 정책)

기본: **코드 = 영어; 엔지니어링 기록과 응답 = 프로젝트 작업 언어(이 키트 = 일본어); 설명 문서 = 영어 주 + 일본어 부**.

**변경(프로젝트마다 1회):**

1.  `AGENTS.md` §1(권위 계약) 수정;
2.  `.kilo/skills/language-policy/SKILL.md`의 「(wawoo-skills: Japanese)」 두 곳 동기화;
3.  라우팅 설명 재생성: `python3 scripts/gen_router.py`;
4.  이 문서의 언어 설명도 일치시키기.

> 「문서 전체를 어떤 언어로」 바꾸려면 `README.<lang>.md` / `docs/USAGE.<lang>.md`를 해당 언어로 만드세요(이 키트에는 `en / ja / zh-CN / ko`가 있습니다).

### 9.3 이미지 생성

실제 이미지를 만들려면 key를 설정해야 합니다; `imagegen-frontend-mobile`은 프롬프트만 작성하고 모델을 호출하지 않습니다.

| 기능 | 필요한 key | 위치 | 설명 |
|---|---|---|---|
| `fal-gen`(실제 이미지, fal.ai) | `FAL_KEY`(형식 `key_id:secret`) | `.kilo/skills/fal-gen/.env`(`.env.example` 복사) | **커밋/출력 금지**; 기본 가장 저렴한 모델 `flux/schnell` |
| `openrouter-gen`(실제 이미지, OpenRouter) | `OPENROUTER_API_KEY`(형식 `sk-or-v1-...`) | `.kilo/skills/openrouter-gen/.env`(`.env.example` 복사) | 기본 `google/gemini-2.5-flash-image`; `OPENROUTER_IMAGE_MODEL`로 변경; 더 저렴한 `google/gemini-3.1-flash-lite-image` 가능 |
| `imagegen-frontend-mobile` | 불필요 | — | **프롬프트만 제공**, 모델 호출 없음 |

-   선택: `FAL_BASE_URL`로 fal.ai 엔드포인트를 지정할 수 있습니다.
-   두 이미지 스킬은 **매니페스트(manifest)**로 일괄 생성하며, 이미 있는 파일은 자동으로 건너뜁니다(재실행 안전): 먼저 `--dry-run`으로 확인 후 생성합니다(이미지 생성은 비용 발생).

> [!WARNING]
> **키를 절대 저장소에 쓰지 마세요**(`.env`도 커밋 금지). 키는 로컬 `.env`에만 두고, `.gitignore`에 의해 무시되는지 확인하세요(이 저장소는 `.env` / `.env.*` 무시, `.env.example`만 유지).

### 9.4 Google Modern Web Guidance

**무엇인가**: Google이 만든 「현대 웹을 어떻게 만드는가」 온라인 가이드(약 262편).

**무엇을 해결하나**: AI 지식은 낡을 수 있습니다. 웹을 만들 때 최신 방식을 필요할 때 조회하고, 버려야 할 오래된 방식도 찾아 줍니다.

**어떻게 쓰나**: 한마디 하면 됩니다; 에이전트가 `modern-web-guidance-bridge`로 검색(`mwg_search`)하고 가져옵니다(`mwg_retrieve`). 가이드는 저장소에 복사하지 않습니다.

**전제**: Node.js와 네트워크 필요; 오프라인이면 `WAWOO_MWG_DISABLE=1`로 끄기.

**기존 규범과 충돌 시**: 제품 규범 / Vercel 우선.

### 9.5 의도 라우팅 (고급, 보통 변경 불필요)

`interpret_intent`가 「워크플로 자동 선택」을 담당합니다; 아래는 그 매칭 세부에만 영향을 주며 **보통 변경하지 않습니다**.

| 변수 | 역할 | 기본 |
|---|---|---|
| `WAWOO_INTENT_LEARN_DB` | 학습된 트리거 저장소 | `data/intent_learned.db` |
| `WAWOO_INTENT_SESSION` | 세션 게이트 상태 파일 | `<root>/data/intent_session.json` |
| `WAWOO_INTENT_RESUME` | `1`이면 재시작 후 게이트 복원 | 꺼짐 |
| `WAWOO_INTENT_CLIENT` | 클라이언트별 파일, 게이트 충돌 방지 | 비어 있음 |
| `WAWOO_INTENT_SOCKET` | 상주 `intent_receiver.py`의 socket | 비어 있음 |
| `WAWOO_INTENT_LEXICAL` / `_THRESHOLD` / `_MARGIN` / `_MIN_TOKENS` / `_MAX_ABSTAIN` / `_DEBUG` | 어휘 라우팅 스위치·임계값·디버그 | `mcp/README.md` 참고 |

### 9.6 설치와 CI

설치와 CI에만 영향을 미치며, 일상 사용에는 영향이 없습니다.

| 변수 / 인자 | 역할 |
|---|---|
| `KILO_GLOBAL_DIR` | `install_global.py` 대상 디렉터리(기본 `~/.config/kilo`) |
| `CURSOR_API_KEY` | Cursor CLI **무인 CI** 전용(로컬은 보통 `agent login`) |

### 9.7 문서 검토 스크립트 (선택)

선택 사항; 스크립트 검토 전용이며, 메인 흐름에는 참여하지 않습니다.

`scripts/audit_docs_dual.py` / `scripts/openrouter_doc_audit.py`는 OpenRouter로 문서를 검토합니다:

-   `OPENROUTER_API_KEY`(필수)
-   `OPENROUTER_DOC_MODEL`(기본 `google/gemini-2.5-flash`)
-   `OPENROUTER_QWEN_MODEL`(기본 `qwen/qwen3-30b-a3b`)

### 9.8 외부 전제

이슈 트래커가 필요한 3개 스킬: `to-spec`, `to-tickets`, `triage`(`scripts/readiness.json` 참고). 한 번 설정: `setup-matt-pocock-skills`.

### 9.9 설정 파일 비교

클라이언트별 설정 파일 위치; **변경 후 클라이언트 재시작**.

| 클라이언트 / 용도 | 파일 |
|---|---|
| Kilo | `~/.config/kilo/kilo.jsonc`(프로젝트 내 `kilo.json`) |
| Cursor(사용자 / 프로젝트) | `~/.cursor/mcp.json` / `<workspace>/.cursor/mcp.json` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` |
| Codex | `~/.codex/config.toml` |
| 이미지 key | `.kilo/skills/fal-gen/.env`, `.kilo/skills/openrouter-gen/.env`(**커밋 금지**) |
