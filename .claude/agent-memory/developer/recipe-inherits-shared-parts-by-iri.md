# recipe가 공유 파트를 IRI로 상속 (derivedFrom ≠ component inheritance)

## 문제
recipe harness(id:h-lpranging)가 템플릿 core:h-multiagent를 `ho:derivedFrom`으로 참조해도
템플릿이 가진 `ho:hasChannel`/`ho:hasRole` 등의 컴포넌트 edge를 **자동으로 갖지 않는다**.
derivedFrom은 lineage/provenance 표시일 뿐, RDFS/OWL 컴포넌트 상속이 아니다. 따라서 실 소스
하네스가 조정 채널을 쓰면 recipe도 명시적으로 그 edge를 실어야 충실(faithful) 반영이 된다.

## 해법
- recipe ttl의 harness 개체에 `ho:hasChannel core:chan-agent-user,
  core:chan-orchestrator-inspection, core:chan-dispatch ;` 를 직접 추가.
- **공유 중립 파트는 로컬 개체로 저작하지 않는다** — `core:` IRI로 REUSE. recipe가 중앙 root
  온톨로지(`.../ontology`)를 owl:imports 하므로 채널 개체 + 그 participant Role은 union에 이미
  존재(추가 개체 0). 로컬 chan-* 개체를 만들면 중복/drift.
- 술어 순서: h-multiagent seed 관례를 따라 `hasRole → hasChannel → appliesPattern` 사이에 삽입
  (ONTOLOGYSTYLE §4는 hasRole/hasChannel을 명시 안 하지만 seed abox 관례가 SoT).

## materialize 거동
채널 전용 emitter는 아직 없다. `ho:hasChannel ⊑ ho:hasComponent`라 채널이 harness로 roll-up
→ `MANIFEST.json` 컴포넌트 인벤토리엔 뜨지만(label "…channel") 전용 artifact 파일은 미생성.
이는 정상("no emitter yet"). materialize는 그대로 성공 + 2런 byte-identical 결정성 유지.

## 게이트
- 중앙 validate: 새 중앙 개체 0이므로 개체수 불변(예: 77) PASS.
- recipe compose: staging/harness-recipes에 `central` 심링크 → repo root(`ln -sfn ../../ central`),
  `HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name>
  /usr/bin/python3 central/tools/validate.py` (cwd=staging/harness-recipes, 상대 catalog 함정).
  edge만 추가·새 개체 0 → union 개체수 불변(94). 실행 후 `rm -f central`.
- staging/ 는 git-ignored → central-untouched 자동 충족(git check-ignore로 확인).
- 채널 resolve 확인: load_graph 후 hasChannel objects + channelParticipant 쿼리.
