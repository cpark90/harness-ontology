# federation: owl:imports + catalog loader, IRI sub-namespace migration

`docs/federation-design.md` (D1–D4) 구현 시 배운 것. 원문 근거: `docs/feedback/inquiries/benchmark.md`.

## 로더를 glob → owl:imports+catalog로 (D1)
- `tools/ontology_lib.py`가 진입점. `load_graph()`는 `catalog-v001.xml`(루트, Protégé
  OASIS 포맷: `<uri name="<IRI>" uri="<상대경로>"/>`)를 파싱해 IRI→로컬파일 맵을 만들고,
  루트 온톨로지 IRI(`.../ontology`, `ontology/harness-ontology.ttl`)에서 `owl:imports`를
  BFS로 따라가며 각 파일 1회 parse. import closure = union.
- **fallback 필수**: catalog/root 없으면 기존 `ontology/**/*.ttl` glob으로 폴백해야
  partial checkout·webui가 안 깨진다. `_load_via_imports`가 아무것도 못 읽으면 `_load_via_glob`.
- shapes는 절대 import 안 함(검증 전용). imports 경로·glob 둘 다 `shapes/` skip.
- 각 abox 파일 상단(prefix 다음)에 자기 `owl:Ontology` 헤더 선언: 문서 IRI `.../data/<domain>`,
  `owl:imports <.../schema>` (+다른 도메인 참조하면 그 `.../data/<x>`도). rdflib.parse는
  owl:imports를 자동 fetch 안 하니 네트워크 걱정 없음 — catalog로 수동 해석.
- **검증법**: `_load_via_imports`와 `_load_via_glob`의 (reason=False) triple 수가 같아야
  union 동일. 여기선 둘 다 514.
- **D4 CI 재사용**: env override 추가(`HARNESS_CATALOG`, `HARNESS_ROOT_ONTOLOGY`)로 data repo가
  자기 catalog+root로 중앙 validate.py를 union 위에서 돌린다. shapes는 `lib.ONT_DIR`(중앙)에서 옴.

## IRI 도메인 서브네임스페이스 마이그레이션 (D3)
- entity IRI = `.../id/<domain>/<slug>`, `core`는 중앙 예약. 문서(ontology) IRI `.../data/<domain>`
  와 **별개**(표준 OWL).
- **text-surgical 핵심**: 노드 본문 안 건드리고 **prefix 바인딩만** 바꾼다. 자기 도메인
  `@prefix id: <.../id/<domain>/>`; 다른 도메인 참조는 prefix 하나 더(`@prefix core: <.../id/core/>`)
  선언 후 그 참조들만 `core:`로 치환. 두 prefix가 같은 ns 가리키면 union에서 같은 IRI로 병합돼
  cross-domain edge 성립(reachability/SHACL/capability 다 union 위에서 통과).
- seed(중앙)는 prefix 한 줄만 바꾸면 전체 core화(본문 0줄 수정). 파생 abox(lpranging)만
  core 참조들을 골라 `core:`로(usesTool/hasGuardrail/usesModel/requiresCapability/derivedFrom/
  tagged c-safety/topConceptOf scheme 등). grep으로 잔여 `id:<core-slug>` 없음 확인.
- retrieve node.id는 full IRI라 마이그 후 `.../id/lpranging/...`로 바뀜 — 랭킹은 그대로.

## tools 하드코딩된 flat id/ 베이스
- `ontology_lib.ID`(prefix 바인딩용, 직렬화 cosmetic), `tools/webui/server.py:ID_NS`,
  `tools/webui/ttl_writer.py:_HEADER`, `frontend/.../RetrievePanel.svelte:ID_NS`가 `.../id/`를 가정.
  webui는 `core` 도메인 저작으로 통일(ID_NS/_HEADER를 `.../id/core/`로). ttl_writer의 surgical
  writer는 `id:<slug>` qname **텍스트**로 블록 매칭 → prefix 선언만 바뀌면 기존 노드 편집 그대로 동작.
  타 도메인 노드는 full IRI로 표시(flat 경로 read-only, webui 도메인 선택 UX는 follow-up).

## 물리적 repo split (lpranging pilot — 중앙에서 도메인 externalize)
- **data-repo payload** = `<domain>.ttl`(abox 그대로 복사, owl:Ontology 헤더·schema+core imports 유지)
  + `catalog-v001.xml` + `.github/workflows/validate.yml`(`docs/ci/data-repo-validate.yml` 템플릿) +
  `README.md`(clone central→union validate 안내) + `LICENSE`(Apache-2.0, 중앙과 동일) + `.gitignore`(`/central/`).
- **data-repo catalog**: `central/` 상대경로로 중앙 IRI 해석 — `.../schema`→`central/ontology/tbox/harness.ttl`,
  `.../data/core`→`central/ontology/abox/seed.ttl`, `.../data/<domain>`→`<domain>.ttl`. root(`.../ontology`)·
  authored 엔트리는 넣지 않음(union은 data 문서 IRI의 import closure). 로컬 검증은 `central` 심링크로 대체.
- **proof**: `HARNESS_CATALOG=<payload>/catalog HARNESS_ROOT_ONTOLOGY=.../data/<domain> /usr/bin/python3
  <central>/tools/validate.py` → PASS. shapes는 항상 `lib.ONT_DIR`(중앙 checkout). data-repo union은
  중앙의 해당 abox 파일 삭제와 무관하게 self-contained(자기 `<domain>.ttl` 사용).
- **중앙 transition(한 번에, broken 상태 없이)**: abox 파일 삭제 + catalog 엔트리 제거 + root owl:imports 제거.
  glob fallback도 파일이 없어졌으니 같은 schema+core로 수렴(bogus HARNESS_CATALOG로 강제 확인:
  `id/lpranging/` 노드 부재·individual 수 일치). core/seed는 중앙 유지.
- **full 연합 union 재구성 문서화 필수**: split이 도메인을 연합 검증에서 조용히 빠뜨리면 안 됨.
  canonical recipe = data-repo에서 central을 `central/`로 clone 후 data-repo catalog로 중앙 validate.py 실행
  (=CI가 하는 것). `docs/federation-design.md`에 "Composing the full federated union" 절로 남김.
- **개수**: lpranging = 21 individuals(dom1+task2+cap2+concept6+pat1+tool2+wf1+gr4+sp1+h1). core = 41.
  union = 62. (초기 추정 "42 core"는 off-by-one; 실측 41.)

## 물리적 split 안전순서 (중요 — data-loss 회피)
- **split(중앙에서 abox 삭제)은 외부 repo가 durably push된 뒤에만.** lpranging은 초기 커밋 이후
  세션에서 저작돼 **git 이력에 없었음** → 중앙에서 삭제하면 세션 scratchpad(ephemeral)에만 남아
  별도 inspection 세션이 접근 불가 = data loss. 교정: 중앙 파일 복원(central form: `.../data/<domain>`
  헤더, imports schema+core, `.../id/<domain>/`, cross-ref은 `core:`) + catalog 엔트리 + root
  owl:imports 재추가. GATE: validate 62 individuals PASS, retrieve #1, imports/glob 두 로더 동수(514/62).
- **payload는 durable 경로 `staging/<domain>-data-repo/`로** (scratchpad 금지, inspection 온디스크 인계).
  중앙 `.gitignore`에 `/staging/` 추가(다른 repo 소유물 — 중앙에 커밋 금지). payload 안 재귀
  `central` 심링크는 durable본에 두지 않음 — 로컬 proof 시에만 `ln -sfn <repo> central`로 임시 생성 후
  `rm`. proof는 env override(`HARNESS_CATALOG`+`HARNESS_ROOT_ONTOLOGY`)로 union PASS 확인.
- **docs는 "PENDING"으로**: split을 "executed/removed from central"로 적지 말 것 — 중앙이 아직
  도메인을 보유. federation-design.md Migration·"Composing the full union"절 + catalog/root NOTE 동기화.

## 함정
- **Write 툴이 파일 끝에 `</content>`(가끔 `</invoke>`)를 흘림** — Write 후 `grep -n '</content>\|</invoke>'`
  로 확인하고 `sed -i '/^<\/content>$/d; /^<\/invoke>$/d'`로 제거. TTL이면 parse가 EOF 에러로 잡아줌.
