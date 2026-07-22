# vnv 역할 메모리

verification & validation 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/vnv.md`. 검증 노하우를 파일로 추가하고 아래에 한 줄로 인덱스한다.

- composition 결과물의 검증(규격 부합 = `validate.py` PASS)·평가(목적 부합 = `retrieve.py`로
  재검색·capability gap 충족·`HarnessShape` 최소구성) 판정만. 온톨로지·설계 편집 없음.
- 리포트는 `docs/verify/`에. 근거 없는 통과 금지 — 실행한 명령·측정값(도구 출력)을 명시.
- 도구는 `rdflib` 등이 있는 인터프리터로(예: `/usr/bin/python3`). 셸 기본 python3엔 없을 수 있음.

<!-- 학습 인덱스 (한 줄씩) -->
- [webui 검증 재현 절차](webui-smoke.md) — Svelte/Vite+FastAPI web UI 빌드·서버·Docker 스모크, 무결성 sha256 대조, ttl_writer dry 라운드트립, static-missing/dockerignore 결정거리.
- [composition 검증 절차](composition-verify.md) — 새 harness abox 검증 체크리스트; tokenEstimate [지킴] 범위 함정(definition-only는 범위 밖), TBox drift diff, requires→provides 그래프 직접읽기, near-synonym/omit-guardrail 판정.
- [federation 검증 재현 절차](federation-verify.md) — catalog+owl:imports 로딩(D1)·도메인 IRI(D3)·data-repo CI 게이트(D4) 판정; 로더 등가성(HARNESS_CATALOG env+모듈 reload), flat/dangling IRI 스캔, retrieve JSON엔 iri 없음, authored.ttl 의도적 부재 오탐 주의.
- [split+recipe 검증 재현 절차](split-and-recipes-verify.md) — seed.ttl→core/*.ttl 타입별 분할 무손실 증명(HEAD seed vs union instance-triple symdiff 0), recipe-repo compose(임시 central 심링크→검증→rm, union 75), redefinition 0(rdflib subject), all-11-import 판정(결함 아님·anti-rot은 projection 계층).
- [materialize (BUILD projection) 검증 절차](materialize-verify.md) — materialize.py=retrieve의 dual; recipe union 조립(임시 central 심링크→rm), 게이트 refusal(bogus id exit2/non-validating union exit1, out dir 미생성), determinism(diff -r+sha256), template-vs-fallback 구분, most_specific_types reflexive-subClassOf 잠복버그(reason=True) + 로컬 워크어라운드 판정.
- [ODR BIND+Lock 검증 재현 절차](odr-bind-lock-verify.md) — Candidate/implementationCandidate/selectionPolicy(BIND)+materialize lock(③) 판정; property-chain 타입체크(tool-docgraph≠Harness, cand는 hasComponent-reachable, subPropertyOf는 domain-trip으로 틀림), latest-stable/pinned:next cmp, lock 재현(A==B)+tamper 부분쓰기 함정(N1), 심링크는 trap 말고 마지막에 rm, union=83.
- [lpranging faithful-reflection 검증 재현 절차](lpranging-faithful-reflection-verify.md) — recipe가 REAL source harness를 충실 재반영했나(primary axis=cmp-against-source, validate 아님); materialize 산출물 byte-cmp(tools/scaffold identical, agent .md는 render라 byte-differ 정상→sanity-read), synthetic 제거(_v2/lock 부재·direct single ref·central TBox vocab는 유지), CLAUDE.md 6원칙 grep, union=81(83에서 candidate 2 빠짐), pass-with-notes(N1 language-shift/N2 recipe≠full-project/N3 vnv sim tool — 전부 경계한계). + coverage 감사 후속: **core-roles import 회귀 BLOCKER**(central roles.ttl 신설·h-multiagent hasRole 7 core role인데 recipe catalog+lpranging owl:imports가 core-roles 누락→union FAIL→materialize REFUSE; central 자체는 PASS; fix=catalog+import 2줄, 검증됨→P0 dispatch), GAP-A=domain content out-of-model 정당, GAP-B2=.claude/skills 3개 미모델(ho:Instruction 가능·low). → docs/verify/lpranging-coverage.md.
