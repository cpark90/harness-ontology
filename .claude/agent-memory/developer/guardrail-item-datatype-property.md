# Guardrail item as a new TBox datatype property (user-authorized vocab ext)

맥락: harness 규칙의 세부(예: 언어 규칙의 artifact별 언어)를 별도 first-class 노드가 아니라
**guardrail의 item/field**로 붙이라는 요청. anti-drift상 새 `ho:` 발명은 금지지만, 사용자가
명시 인가하면 예외 — 단 **같은 변경에서 연결**해 drift가 아님을 보인다.

## 패턴 (TBox datatype property 1개 + ABox 값)
- TBox `ontology/tbox/harness.ttl` Datatype properties 절에 추가. `ho:promptText` 스타일 모방:
  `a owl:DatatypeProperty ; rdfs:domain <해당 컴포넌트클래스> ; rdfs:range xsd:string ;
  rdfs:label ... ; skos:definition ...`. domain을 좁혀 두면 의미가 명확.
  예: `ho:languageCondition` domain `ho:Guardrail` range `xsd:string`.
- ABox: 대상 노드에 값을 **한 프레디킷 여러 리터럴**(콤마 구분)로. artifact class 하나당 item 하나.
  기존 트리플(prefLabel/promptText/tokenEstimate/maturity/tagged)은 보존, predicate order는
  §3(데이터는 promptText→tokenEstimate 앞쪽). 값은 영어(§1d 그래프 데이터 값).
- promptText도 세부를 담게 다듬으면 tokenEstimate 재산정(리터럴 커진 만큼 상향, rough OK).

## shapes
- guardrail/컴포넌트 NodeShape에 `sh:closed true`가 **없으면** shapes 손대지 않는다 —
  열린 shape는 미선언 프레디킷을 자동 허용. 이 repo shapes엔 closed 없음(2026-07 기준).
  closed였다면 그 shape의 허용 목록에 새 프레디킷만 추가(새 hard requirement·기존 완화 금지).

## 중앙 노드 enrich = recipe 자동 반영
- recipe(예: lpranging)가 `core:gr-lang`을 **IRI로 재사용**(`ho:hasGuardrail core:gr-lang`)하면,
  중앙 guardrails.ttl을 enrich하는 것만으로 recipe union에도 그대로 나타남(별도 recipe 편집 불요).
- 확인: staging catalog의 `central/`을 이 repo로 심링크 → `HARNESS_CATALOG=... 
  HARNESS_ROOT_ONTOLOGY=.../recipes/<name> /usr/bin/python3 tools/validate.py` PASS, 그리고
  대상 노드에 새 프레디킷 값이 union에 들어왔는지 확인 → **심링크 삭제**. 개체수는 불변
  (property/triple만 추가). 중앙 단독 validate도 PASS·개체수 동일.
