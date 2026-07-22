# V&V — central per-type split (Phase 1) + harness-recipes payload (Phase 2)

- **역할**: vnv (판정만; ontology/tools/docs 미편집, git 미실행)
- **인터프리터**: `/usr/bin/python3` (rdflib/pyshacl/owlrl 보유)
- **판정 대상**: `ontology/abox/core/*.ttl` (11 units, seed.ttl 대체) + `ontology/harness-ontology.ttl` +
  `ontology/catalog-v001.xml` 재배선 (Phase 1); `staging/harness-recipes/**` (Phase 2)

## Verdict: **pass-with-notes**

6개 검증 항목 전부 그래프 증거로 통과. 결함(fail) 없음. notes는 승격/구조 관련 자문 2건 +
개발자 플래그(all-11 import) 판정.

---

## 1. Central split integrity (Phase 1) — PASS

### 구조 게이트
```
/usr/bin/python3 tools/validate.py
→ loaded graph: 1429 triples (post-reasoning)
  ✓ SHACL  ✓ reachability (all 64 individuals)  ✓ capabilities  ✓ dup-label
  PASS
```

### Triple-equivalence proof (split이 아무것도 잃지 않음)
pre-split union = `git show HEAD:ontology/abox/seed.ttl` (working tree에선 삭제됨),
post-split union = `ontology/abox/core/*.ttl` 11개 parse. `owl:Ontology` 헤더 subject를
제외한 instance triple을 양방향 diff:

| | pre-split (seed.ttl@HEAD) | post-split (11 units) |
|---|---|---|
| total triples | 366 | 386 |
| owl:Ontology 헤더 subject | 1 (`.../data/core`) | 11 (`.../data/core/<type>`) |
| **instance triples** | **364** | **364** |
| **individuals** | **64** | **64** |

- **ONLY-in-pre (lost) = 0, ONLY-in-post (added) = 0** → instance triple 집합 완전 동일.
- 차이는 오직 헤더 triple뿐: pre 2 (1 type + 1 imports) vs post 22 (11×[type+imports]) =
  366 vs 386, 정확히 예상대로. 실제 데이터(64 개체 + 그 data triple)는 triple-단위로 보존.

### 로더 등가성 (catalog+imports vs glob-fallback)
`ontology_lib`을 `sys.modules`에서 제거·reload하여 `HARNESS_CATALOG=/nonexistent`로 glob
fallback을 강제(파일 미수정, env override만):

| path | triples | individuals | symdiff |
|---|---|---|---|
| A catalog+owl:imports (default) | 1429 | 64 | — |
| B glob fallback (`HARNESS_CATALOG=/nonexistent`) | 1429 | 64 | — |
| A ↔ B | | | **raw triple symdiff 0, individual symdiff 0** |

두 로더 경로가 완전히 일치.

### 헤더·root 배선
- 11개 unit 각각 `owl:Ontology` 헤더 보유(위 표), 각 unit은 **schema만** import
  (11개 파일 모두 `owl:imports <.../schema>` 단일 import 확인).
- root `ontology/harness-ontology.ttl`이 11개 core unit + schema + `data/authored`를 모두 import.
- catalog가 11개 `.../data/core/<type>` IRI를 로컬 파일로 매핑.

## 2. Central neutrality preserved — PASS
```
grep -rniE 'uwb|rtls|lpranging|sysdesign|embedded|low-power|lowpower|docgraph|simulator' ontology/abox/core/
→ 0 matches (주석 포함 raw로도 0)
```
도메인 노드가 central로 누출되지 않음.

## 3. Recipe composes + buildable (Phase 2) — PASS
임시 `staging/harness-recipes/central` → repo 심링크 생성 후:
```
cd staging/harness-recipes
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
/usr/bin/python3 central/tools/validate.py
→ loaded graph: 1599 triples
  ✓ SHACL  ✓ reachability (all 75 individuals)  ✓ capabilities  ✓ dup-label
  PASS
```
union **75 = 64 central + 11 local** (dom-sysdesign, c-sysdesign/embedded/lowpower/rtls,
cap-designgraph/simulation, tool-docgraph/simulator, sp-lpranging, h-lpranging). **심링크는
검증 후 제거함** (staging at-rest 심링크 = 0 확인).

### HarnessShape 최소구성 (`id:h-lpranging`) — 충족
hasSystemPrompt 1 (sp-lpranging) · hasWorkflow 1 (wf-multiagent) · usesTool 4
(tool-shell/editor + tool-docgraph/simulator) · hasGuardrail 9 · usesModel 1 (mc-opus) ·
appliesPattern 1 · targetsDomain 1 · addressesTask 2. CLAUDE.md 산문 최소(1 SP + ≥1 WF +
tools + guardrail + ModelConfig) 전부 만족.

### requires → provides (그래프에서 실제 바인딩된 컴포넌트로만 매칭)
| requiresCapability | 제공 컴포넌트 | |
|---|---|---|
| core:cap-fileedit | core:tool-editor | OK |
| core:cap-codeexec | core:tool-shell | OK |
| core:cap-orchestration | core:wf-multiagent | OK |
| core:cap-traceability | core:gr-traceability | OK |
| **id:cap-designgraph** | **id:tool-docgraph** | OK (도메인 cap ← 로컬 tool) |
| **id:cap-simulation** | **id:tool-simulator** | OK (도메인 cap ← 로컬 tool) |

6/6 충족. 도메인 cap 2개는 로컬 tool이, 재사용 core cap 4개는 core 컴포넌트가 제공.
`derivedFrom` = core:h-multiagent (계보).

### 재사용 by IRI (redefinition 0)
recipe 파일 단독 parse → `core:` prefix IRI가 **subject로 등장 = 0** (redefinition 없음).
grep이 잡은 110/111/115/118행은 다중행 object-list의 연속행(직전 행이 콤마로 끝남)이지
subject 선언이 아님을 rdflib로 확증. central 노드는 전부 IRI 참조만.

## 4. Anti-drift — PASS
- **새 `ho:` class/property = 0**: central 11 units + recipe에서 쓰인 `ho:` 용어 전체 −
  TBox(`ontology/tbox/harness.ttl`) 선언 = **공집합**. near-synonym class·untyped edge 없음.
- 새 로컬 concept 연결됨: `id:c-sysdesign skos:topConceptOf core:scheme`, c-embedded/
  lowpower/rtls는 `skos:broader`로 하위 연결 (reachability PASS가 orphan 없음을 재확인).
- 로컬 텍스트 보유 노드 tokenEstimate: tool-docgraph 48, tool-simulator 42, sp-lpranging 100.
  definition-only Capability·prefLabel-only Concept·Domain은 ONTOLOGYSTYLE §1c [지킴] 범위 밖
  (오탐 아님).

## 5. Discoverability — PASS
- **composed union**(recipe catalog+root)에서 도메인 쿼리
  `"low-power UWB ranging RTLS embedded system design harness"` → base 후보 #1
  **"Low-power ranging system-design agent"** (rel 15.3). 도메인 tool/cap/domain 노드 표면화.
- **central-only**에서 동일 쿼리 → base 후보는 중립 "Multi-agent orchestration harness"
  (rel 2.734); 쿼리-에코 헤더행 제외 시 **도메인 노드 0건** 표면화(uwb/rtls/docgraph/
  simulator/design-graph/embedded system design 매치 0). 중립 쿼리
  `"multi-agent orchestrator workers with traceability"` → 중립 파트 정상 표면화.

## 6. Payload hygiene — PASS
- `staging/harness-recipes/` at-rest 심링크 = 0 (임시 central 심링크 제거 확인).
- `/staging/` 루트 `.gitignore` line 9로 ignored.
- recipe `.gitignore`가 `/central/` ignore.
- CI(`.github/workflows/validate.yml`)는 **no-op 아님**: central repo를 `./central`로 checkout,
  `central/requirements.txt` 설치 후 `HARNESS_CATALOG=<repo>/catalog-v001.xml`·
  `HARNESS_ROOT_ONTOLOGY=<recipe IRI>`로 `python3 central/tools/validate.py` 실행(비영 exit
  = 실패). 내가 수동 실행한 composed-union validate와 동일 경로 → PASS.
- Write-tool 잔재 스캔(`</content>`,`<parameter`,`</invoke>`,`<invoke `,`</antml…`) = clean.

---

## 개발자 플래그 판정: "recipe가 core 11 unit 전부 import" (all-of-central)

**판정: 현 central 입도에서 acceptable — 결함 아님, 자문 note.**

- recipe는 9개 unit을 직접 바인딩(guardrails/workflows/patterns/tools/model-configs/
  capabilities/concepts/domains-tasks)하고 `derivedFrom core:h-multiagent`로 harnesses를 끌어옴.
- `core/harnesses`는 **모든** seed harness를 담은 **단일 문서**이고, 그 seed harness들이
  system-prompts·constraints를 포함한 다른 모든 unit을 참조한다. 따라서 harnesses를 import하는
  순간 union이 닫히려면(EdgeTypingShape가 hasSystemPrompt/… object의 타입을 요구, dangling
  ref는 SHACL fail) 나머지 2개(constraints, system-prompts)까지 반드시 import해야 한다.
  즉 **"바인딩한 것만 import"는 derivedFrom 계보 유지 + harnesses 단일문서 구조 하에서 불가능**.
- 대안은 (a) derivedFrom을 버려 harnesses import 회피 → 계보/traceability 손실로 나쁜 트레이드,
  (b) central이 harnesses를 harness별 문서로 재분할하거나 lineage-only stub unit을 제공 →
  **central-side 구조 변경**(recipe 통제 밖).
- context-rot 방어선은 union 크기가 아니라 **projection(retrieve budget-cap) 계층**에 있음
  (golden rule #1). §5 증거대로 composed-union retrieve는 여전히 budget 896/900로 h-lpranging을
  #1로 정확히 project → all-11 import가 런타임 컨텍스트 비용을 만들지 않음(validate-time union
  크기만 커짐). recipe 자체 주석이 이 이유를 정직하게 문서화함.

**결론**: 현재 선택이 옳다. union 최소화가 목표가 되면 central의 harnesses 입도 재분할(또는
lineage-only stub)을 inspection/orchestrator로 라우팅해 다룰 자문 사항이며, 지금은 defect 아님.

## 기타 notes (승격 전 리뷰거리, fail 아님)
- `id:h-lpranging` maturity = `"reviewed"` (tool-simulator/sp-lpranging도 "reviewed",
  tool-docgraph "stable"). CLAUDE.md composition 워크플로 산문은 신규를 `"draft"`로 두고 리뷰
  후 승격 권고. 다만 이는 retired harness를 재구성한 worked-example recipe이고, maturity는
  ONTOLOGYSTYLE [지킴] 강제가 아닌 curation 속성이므로 note로만 남김.
- `data/authored` IRI는 catalog에 매핑되나 `ontology/abox/authored.ttl` 파일은 부재 —
  BFS가 조용히 skip(의도된 optional), union 개체수 불변으로 정상(기존 federation 판정과 동일).

## 재현 명령 요약 (전부 `/usr/bin/python3`)
```
tools/validate.py                                    # Phase1 게이트 (64, PASS)
git show HEAD:ontology/abox/seed.ttl                 # pre-split union 복원
# split_diff.py: instance-triple symdiff 0, 64==64
# loader_equiv.py: HARNESS_CATALOG=/nonexistent reload → symdiff 0
grep -rniE '<domain terms>' ontology/abox/core/      # neutrality = 0
ln -s $(pwd) staging/harness-recipes/central         # 임시 (검증 후 rm)
cd staging/harness-recipes && HARNESS_CATALOG=catalog-v001.xml \
  HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py          # 75, PASS
# recipe_check.py: HarnessShape slots + requires→provides 6/6
# redef_drift.py: core: subject in recipe = 0, undeclared ho: = 0
tools/retrieve.py "<domain query>"                   # central=중립only, union=#1 h-lpranging
```
