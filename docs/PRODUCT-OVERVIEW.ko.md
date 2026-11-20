# wawoo-skills: AI 코딩 에이전트용 재현 가능한 workflow
<!-- SEO: Cursor/Kilo/OpenCode용 오픈소스 AI 에이전트 키트 — skill 112, workflow 20, MCP 라우팅으로 동일 요청을 동일 절차로 실행. -->

[English](PRODUCT-OVERVIEW.md) · [日本語](PRODUCT-OVERVIEW.ja.md) · [简体中文](PRODUCT-OVERVIEW.zh-CN.md) · [한국어](PRODUCT-OVERVIEW.ko.md)

## wawoo-skills가 하는 일

AI 에이전트는 스킬을 갖고도 **일관되게 쓰지 못합니다**. wawoo-skills는 **workflow + MCP**로 무엇을 먼저 읽고 어떤 단계를 밟을지 설계해, 같은 요청이 **재현 가능한 결과**를 내도록 합니다.

## 다루는 페인

| # | 페인 | 키트의 답 |
|---|------|-----------|
| 1 | 스킬이 있는데 **산문만으로 진행** | Workflow + `workflow_get`로 입구 고정 |
| 2 | 같은 «버그 수정»도 매번 다른 경로·품질 | `interpret_intent` → **20** workflow 중 하나 |
| 3 | 리뷰·법무·테스트가 **형식만** | 감사 workflow는 `implement` 금지, **증거 게이트** |
| 4 | 스킬 100개를 한꺼번에 → **토큰만 증가** | 후보 → **`skill_get` 하나씩** |
| 5 | 세션 끝나면 결정 소실 | `memory_recall` / `memory_save` + [MEMORY-CLIENT-GUIDE.ko.md](MEMORY-CLIENT-GUIDE.ko.md) |
| 6 | Cursor에서 `/feature-delivery` **무반응** | MCP + `@.kilo/commands/` |
| 7 | 카피·시장·장문 — **어떤 skill?** | [COPY-MARKETING-GUIDE.ko.md](COPY-MARKETING-GUIDE.ko.md) |
| 8 | «완료»만 말하고 재현·산출물 없음 | `change-readiness`, ACTIVE/CONTENT |
| 9 | 감사 중 배포·memory 쓰기 | workflow별 **MCP 허용 목록** |
| 10 | Wiki 지식 미로드 | `memory_recall`, workflow 입구 INDEX |
| 11 | PII·비밀을 외부 API로 | `guard_content` → `mask_pii` |
| 12 | UI 변경에 a11y 증거 없음 | `/ui-delivery` 5b + uplift |
| 13 | principle 전부 읽기 → 컨텍스트 폭발 | 필요한 `principle-*`만 |
| 14 | 클라이언트 설정 불일치 | [CLIENT-INTEGRATION-GUIDE.ko.md](CLIENT-INTEGRATION-GUIDE.ko.md) |

## 제품 특징 (쉬운 말)

| 용어 | 뜻 |
|------|-----|
| Invocation by design | **호출 경로 설계** — `interpret_intent` / `workflow_get` 우선 |
| Progressive disclosure | **전체 카탈로그를 한 번에 넘기지 않음** |
| Phase + exit_criteria | **단계별 완료 기준** 명시 |
| mcp_tools_allow | **이 작업에 허용된 도구만** |
| Gₐ / Gₑ / Gₒ | **승인 / 증거 / 관측 실패** |
| Rails not cage | 레일은 **재현성**; 구현은 에이전트가 작성 |

MCP는 **Python 3 표준 라이브러리만** 사용.

## 키트 구성

| 종류 | 개수 | 정본 |
|------|------|------|
| **Skill** | 112 | `.kilo/CAPABILITIES.md` |
| **Agent** | 23 | 동일 |
| **Workflow** | 20 | `.kilo/commands/*.md` |

## Skill 지도 (요약)

| 분류 | ~ | 예 | workflow 예 |
|------|---|-----|-------------|
| 엔지니어링 | 19 | `implement`, `tdd`, `diagnosing-bugs` | `/delivery-lite` |
| 품질 | 7 | `code-review`, `change-readiness` | `/self-review` |
| UI | 13 | `accessibility-audit`, `frontend-design` | `/ui-delivery` |
| 조사·카피 | 8 | `research`, `viral-hooks` | `/writing`, `/market-plan` |
| 보안·법무 | 6 | `security-review`, `content-guardrail` | `/compliance-review` |
| 운영 | 4+ | `deployment`, `incident-debugging` | `/incident-response` |
| 원칙 | 24 | `principle-*` | 단계별 1~2개 |

워크스페이스 전용: `kiun-*`, `paseo-orchestration` 등 (공개 OSS 제외).

## Workflow 빠른 참조

| 요청 | 시작 |
|------|------|
| 소규모 수정 | `/delivery-lite` |
| UI | `/ui-delivery` |
| 조사 | `/research` |
| 장문·카피 | `/writing` |
| 장애 | `/incident-response` |

## FAQ

### wawoo-skills란?
**AI 코딩 에이전트**용 오픈소스 키트 — skill 112, agent 23, workflow 20, **MCP**(Model Context Protocol) 서버.

### 스킬을 한꺼번에 넣는 것과 차이?
**점진적 공개**: 카탈로그 → 후보 → 단계마다 `skill_get`으로 하나씩.

### MCP는?
**Model Context Protocol**. Python 표준 라이브러리만으로 동작하는 소형 서버.

### pip 추가 설치?
불필요.

## 다음

1. [GUIDES.ko.md](GUIDES.ko.md)  
2. [CLIENT-INTEGRATION-GUIDE.ko.md](CLIENT-INTEGRATION-GUIDE.ko.md)  
3. `.kilo/CAPABILITIES.md` — **전체 skill 이름**