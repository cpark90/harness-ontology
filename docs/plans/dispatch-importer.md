# Dispatch brief — P1: 코퍼스 importer (`tools/import_corpus.py`) + 파일럿 5 재생성 대조

> 작성: orchestrator (2026-07-25, 자율 루프). 상위: `docs/plans/harness-100-scaleup-plan.md` §6 P1 ·
> 근거: `docs/feedback/harness-100/recipe-roadmap.md` §4 · `docs/plans/harness-100-attribute-inventory.md` M3.
> 실행: **developer dispatch (opus)**. 선행: P0-b land 완료(`5084827`/`d9ebf0c`) — catalog는 이제 glob 생성이라
> importer가 catalog를 직접 안 건드려도 된다(`recipes/*/`에 dir만 만들면 `gen_recipe_catalog.py`가 잡는다).

## ★이 증분의 경계 (매우 중요)
**importer 도구 완성 + 파일럿 5 재생성 대조(수용 시험)까지**가 이번 범위다. **대량 임포트(대표 35 recipe 실제 저작)는
하지 않는다** — 그건 별도 증분이고 D2(리뷰 깊이) 결정이 선행돼야 한다. 이번엔 **도구가 옳게 동작함을 증명**하는 데까지.
이유: 도구(코드)는 되돌릴 수 있지만 35 recipe 대량 저작은 훨씬 큰 비가역 작업이라 분리한다.

## 배경
코퍼스 100개는 구조적으로 균일(`.claude/CLAUDE.md` + `agents/*.md`[name/description frontmatter + body] +
`skills/*/skill.md`). ~90%가 기계 변환 가능하나 100× 손저작은 drift를 부른다. importer가 그 기계 부분을 담당한다.
**파일럿 5개(`03`·`16`·`21`·`31`·`46`)는 이미 손저작·검증됐다** — 이것이 importer의 **oracle**이다.

## 설계 — importer 계약 (roadmap §4 + 인벤토리 M3)
`tools/import_corpus.py <corpus-harness-dir> [--out recipes/<name>/]` — 코퍼스 하네스 하나를 draft recipe TTL로.

### SHOULD (기계적·결정적 — importer가 한다)
- `.claude/` walk → skeleton `id:h-<name>`(recipe-local `id:` 도메인 = `<name>`, §2a 규약).
- `agents/<x>.md` → `id:role-<x>`(`ho:Role`, prefLabel=name, definition=description) + `id:sp-role-<x>`
  (`ho:SystemPrompt`, `rolePersona`). **persona body는 vendor 금지** — 외부 `ho:artifactTemplate` 참조로
  (recipes-design §refs). 하네스에 `hasRole`로 바인딩.
- `skills/*/skill.md` → `id:ins-<x>`(`ho:Instruction`); orchestrator(슬래시 트리거) vs extending 판별,
  extending이면 대상 agent를 `ho:augmentsRole`로 기록(다중 타깃 가능).
- `ho:tokenEstimate` = 텍스트 wc 기반(기존 recipe 관례의 비율 재사용).
- `ho:maturity "draft"` 일괄. 하네스에 `derivedFrom core:h-multiagent`.
- **execMode**: 코퍼스 전량 Agent Team이므로 `hasExecutionMode core:mode-agent-teams`(§1F).

### MUST NOT (판단성 — importer가 하면 안 되고, draft 후 developer 리뷰가 채운다)
- **어휘 신설 금지**: `Concept`/`Capability`/`Guardrail`/`Domain`을 새로 만들지 않는다. 기존 `core:` IRI **바인딩만**.
  신규 도메인 concept가 필요해 보이면 **flag**로 표시(Golden Rule #2) — 저작 금지.
- **capability 충족 추측 금지**: `requiresCapability`를 붙였는데 그것을 `providesCapability`하는 컴포넌트가 없으면
  **hard stop**(미충족을 무음으로 넘기지 않는다). 
- **tool/model 의미 배정 금지**: 인벤토리 M3 확인 — agent frontmatter에 `tools:`도 `model:`도 **0/489**다.
  즉 어떤 tool을 `roleTool`로 줄지는 **판단**이다. importer는 배정하지 말고 flag만.
- **guardrail 의미 배정 금지**: 어떤 원칙 문장이 어떤 `core:gr-*`에 대응하는지는 판단.
- 본문 vendor(persona/instruction 본문을 TTL에 인라인) 금지 — 외부 ref만.

## ★수용 시험 (importer의 oracle — 이번 증분의 핵심 산출)
**파일럿 5개를 importer로 재생성**해 기존 손저작 recipe와 대조하라. 목적은 "importer가 옳은가"의 증명이다.
- **기계적 부분 일치**: role skeleton(name/description)·systemprompt 참조 구조·instruction·tokenEstimate 산정·
  execMode·maturity가 손저작과 **일치**해야 한다.
- **불일치를 두 종류로 분류**하라:
  - **① importer 결함** — 기계적으로 재현 가능한데 importer가 틀림 → importer를 고친다.
  - **② 사람이 넣은 판단성 결정** — MUST NOT 영역(tool/guardrail/capability 배정, 어휘 선택) → 자동화 대상이 **아님**이
    맞다. 이 목록이 곧 **"recipe당 사람이 해야 하는 일"의 실측 명세**이며, D2(리뷰 깊이) 결정과 35× 리뷰 비용 추정의 근거다.
- **이 대조가 통과(=①이 0이거나 전부 수정됨, ②가 목록화됨)하기 전에는 다른 코퍼스에 돌리지 마라.**
- 재생성 산출은 **스크래치에** 두고 기존 파일럿 recipe를 덮어쓰지 마라(대조용). recipe TTL 5개를 실제로 바꾸지 않는다.

## 완료 게이트
```bash
# 파일럿 재생성(스크래치) 후 기존과 대조
for r in 03-newsletter-engine 16-fullstack-webapp 21-code-reviewer 31-ml-experiment 46-product-manager; do
  /usr/bin/python3 tools/import_corpus.py /home/cpark/git/harness-100/en/<r-dir> --out <scratch>/$r
done
# 생성물이 최소 validate를 통과하는 draft인지(per-recipe closure, 신규 dir이면 gen_recipe_catalog로 catalog에 반영해 검증)
/usr/bin/python3 tools/validate.py     # 중앙 무변경 PASS @223
```
- importer는 **결정적**(같은 입력 → 같은 TTL). 2회 실행 diff 0.
- 코퍼스 `/home/cpark/git/harness-100`는 **읽기 전용**.

## 금지
- 중앙 `ontology/**` 편집 금지 · 기존 파일럿 recipe TTL **덮어쓰기 금지**(대조 무결성) · `docs/**` 편집 금지 ·
  **git 조작 금지**(inspection 전담). 신규 파일은 `tools/import_corpus.py`(+테스트/스크래치).

## 반환 보고
① importer 위치·CLI·계약 구현(SHOULD/MUST NOT 각각 어떻게) ② 파일럿 5 재생성 대조 결과 — **①결함 목록(수정함)
+ ②판단성 결정 목록(recipe당 몇 건)** ③ flag된 것(신규 도메인 concept·미충족 capability 등) ④ 결정성 증거
⑤ 이 도구로 35 임포트 시 예상되는 recipe당 사람 작업량(②에서 추정) ⑥ GAP.

종료 전 `.claude/agent-memory/developer/`에 재사용 지식을 남겨라(기존 보존).
