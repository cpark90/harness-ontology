---
status: approved            # 사용자만 approved로 바꾼다
targets: [id:h-lpranging, id:h-techdoc, id:sp-lpranging, id:tool-docgraph]
kind: proposal
---
# 레시피 → 실제 빌드가능 하네스: 재현(materialization) 계층 부재

## 문제 (사용자 보고 + inspection 검증)
사용자가 `recipes/techdoc`를 참고해 "하네스를 구축"해 달라고 했으나 결과는 **repo 전체 clone 후
정리**에 그침. inspection이 `recipes/lpranging`과 실제 하네스 `~/git/agrtls/device_harvest_lp/
lpranging`를 대조한 결과, 이는 우연이 아니라 **구조적 부재** 때문임 — 레시피만으로는 실행 가능한
하네스가 산출될 수 없다.

## 근거 (대조, 실측)
**레시피 = 부품 명세(BoM) 그래프**:
- `recipes/lpranging/lpranging.ttl`(8KB) = 중앙 부품 IRI 재사용 선언 + 도메인 로컬 노드 몇 개 +
  **한 줄 promptText**. `id:sp-lpranging`의 `ho:promptText`는 1문장(~100 토큰,
  `lpranging.ttl:90`). 중앙 `ontology/abox/core/` 전체에 **장문(`"""`) 블록 0개** —
  최장 프롬프트 304자(`system-prompts.ttl`), workflow는 `skos:definition` 1문장(`workflows.ttl:23`).

**실제 하네스 = 파일 트리**:
- `CLAUDE.md` **20KB**(운영 지시), `DESIGN_HARNESS_STANDARD.md` 16.7KB, `CODESTYLE.md` 8.7KB
- `.claude/agents/{developer,vnv,inspection}.md`(역할 정의) + `.claude/agent-memory/`
- `tools/docgraph.py` **32KB**(실제 구현 코드)
- `docs/` scaffold(ARCHITECTURE·CONCEPT·ONTOLOGY·SYSTEM_DESIGN·issues·requirements·research·…)

→ 온톨로지는 하네스의 **"무엇으로 구성되는가(BoM)"**를 담지만, 그 명세에서 **실행 파일 트리를
산출하는 단계도, 그 산출에 필요한 본문 데이터도 없다.** 그래서 "레시피로 하네스 빌드"의 실질적
최선이 clone+정리가 된다(사용자가 관찰한 그대로).

## Gap 분석 (개선 필요 지점)
1. **부품이 라벨+한줄 정의만 저장** — artifact 본문 없음 → 20KB CLAUDE.md·표준문서를 emit 불가.
2. **materialize/build 도구 부재** — `validate.py`(검사)·`retrieve.py`(컨텍스트 투영)는 있으나
   레시피 union → **파일 트리 산출** 도구가 없음.
3. **Tool 노드에 구현 참조 없음** — `id:tool-docgraph`(노드: 라벨/capability/tokenEstimate) ↔
   실제 `tools/docgraph.py`(32KB 코드)가 **미연결**. build가 무엇을 emit/fetch할지 알 수 없음.
4. **멀티에이전트 역할 artifact 미모델링** — 실제 하네스의 `.claude/agents/<role>.md`에 대응하는
   1급 개념 없음(현재는 `pat-orchestrator-workers` + `wf-multiagent` + persona 1개뿐).
5. **표준·docs scaffold 미포착** — DESIGN_HARNESS_STANDARD/CODESTYLE/`docs/` 트리 같은 하네스
   실체의 상당 부분이 온톨로지 밖.

## 권고 개선안 (orchestrator 계획용 · 우선순위)
- **P1 — materialization 계층 (`tools/materialize.py`)**: 검증된 recipe union → 하네스 파일 트리
  렌더. systemPrompt→`CLAUDE.md` 섹션 · 역할→`.claude/agents/<role>.md` · tool→`tools/` ·
  guardrail/workflow/pattern→운영 섹션 · domain→`docs/` scaffold. (retrieve의 projection과
  대칭: retrieve=읽기 투영, materialize=빌드 투영.)
- **P2 — artifact 본문/템플릿 저장**: 노드에 `ho:artifactTemplate`/body(장문, `tokenEstimate`
  유지) 또는 레시피가 템플릿 조각을 가리키게. 어휘 구속(anti-drift)은 그대로.
- **P3 — tool 구현 참조**: `ho:implementationRef`(경로/repo/템플릿) 추가 → build가 코드를
  emit 또는 fetch.
- **P4 — 역할(agent) 1급 모델링**: role → (persona `sp` + tool/guardrail scope + memory policy),
  materialize가 역할별 파일로 emit.
- **P5 — 표준/scaffold 템플릿**: 하네스에 attach 가능한 blueprint 조각(표준문서·docs 트리).

우선 **P1(빌드 도구) + P2/P3(본문·구현 데이터)**가 사용자 요구("실제 하네스가 구축되게")의 핵심.
P4/P5는 멀티에이전트·표준까지 완결하는 후속.

## 범위 / 핸드오프
inspection은 **조사·핸드오프까지**. 실제 설계·어휘 확장·저작·도구 구현은 orchestrator가
노드단위 dispatch brief로 계획해 **developer dispatch**로 수행(orchestrator 직접 저작 아님).
승인 신호 = 사용자가 이 항목 `status: open`→`approved`.
