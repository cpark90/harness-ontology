# composition (new-harness) 검증 재현 절차 + 함정

새 harness abox 파일 하나가 저작됐을 때의 V&V 표준 체크리스트.

## 재현 명령 (전부 `/usr/bin/python3`)
- 구조 게이트: `tools/validate.py` → `PASS`. 4섹션(SHACL / reachability / capability / dup-label) 캡처.
- 발견성: `tools/retrieve.py "<원 request>" --format json` → 대상 harness가 seeds 상위(이상적 #1)인지.
  2차 쿼리로 컴포넌트(workflow/pattern)도 뜨는지 스팟체크.
- 그래프 직접질의(rdflib, tbox+seed+새파일 parse): HarnessShape 슬롯 카운트, requires→provides는
  **harness에 실제 바인딩된 컴포넌트의 providesCapability**로만 매칭(개발자 주장 말고 그래프에서 읽기).

## 판정 함정 / 요령
- **tokenEstimate [지킴] 범위(ONTOLOGYSTYLE §1c:75-76)**: 필수 대상은 **promptText 지닌
  SystemPrompt/Instruction/Guardrail/Example + Tool/Workflow**뿐. `skos:definition`만 가진
  Task/Capability/DesignPattern/Harness/Domain/Concept은 **범위 밖** — 없어도 결함 아님.
  seed.ttl도 동일(Task 0/4, DesignPattern 0/3, Harness 0/3만 tokenEstimate 보유). 순진하게
  "definition=text니까 tokenEstimate 필요"로 잡으면 오탐.
- **TBox drift 체크**: 새 파일에서 쓰인 `ho:` 술어/타입 집합 - TBox 선언 집합 = 공집합이어야.
  프로그램으로 diff. 하나라도 남으면 near-synonym class/untyped edge 신설(=drift) 의심.
- **"omit한 guardrail" 평가 시** 먼저 그 노드가 seed에 **실재하는지** 확인. 없으면 "omit"=신설
  안 함(anti-drift 준수)이지 누락 아님. 있는데 안 붙였으면 validation 판단거리.
- **near-synonym guardrail**: prefLabel + promptText 스코프로 판별(예: gr-traceability=결정/기록
  수명주기 vs gr-nodestruct=쉘 파괴명령 안전 → 별개). validate dup-label은 동일 label만 잡음.
- **derivedFrom**은 실제 존재하는 template(보통 Harness) 가리키는지 타입까지 확인.

판정 리포트: `docs/verify/lpranging-sysdesign.md` (pass-with-notes: 구조/shape/drift/rot 전부 통과,
notes=모델 tier sonnet vs 템플릿 opus, 피드백루프 미모델링 — draft 승격 전 리뷰거리).
