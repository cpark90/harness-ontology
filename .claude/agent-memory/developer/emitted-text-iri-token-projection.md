# emitted-text IRI-token projection (materialize.py)

**문제 유형**: `skos:definition`/`ho:promptText`가 **두 청중을 겸함** — 저자용 disambiguation
(`id:chan-dispatch`, `ho:appliesPattern` 인용은 anti-drift 장치로 **옳음**; `disambiguation-audit.md`가
의도적으로 심음) vs 실행 에이전트용 산출문서(그 prefix는 해소 불가 = dangling reference).
정합성(validate) 문제가 아니라 **projection contract** 문제. ⇒ **그래프 무변경, emit 시점 해소**.

## 구현 형태 — 사이트별 패치 말고 "그래프 투영" 한 곳
`materialize()` 진입부에서 `IriTokenResolver(g).project(g)` 로 **문자열 리터럴만 해소한 그래프
복사본**을 만들어 그걸 렌더한다(5600 triple 복사 0.04s). 렌더러가 40군데라 per-callsite로 고치면
반드시 새는데(새 렌더러/새 술어), 투영은 **CLAUDE.md 섹션·role `.claude/agents/*.md`·channel
record·skill body·MANIFEST 전부 + 미래 렌더러**까지 자동 커버. 원본 `g`는 불변(라이브러리 호출자 안전).

- `id:<slug>`/`core:<slug>` → 그 개체 `skos:prefLabel`, `ho:<Name>` → `rdfs:label`(없으면 de-camel).
- **`id:`는 네임스페이스 상대적**(중앙 ABox에선 `id:`=core, recipe에선 local domain) ⇒ **slug 기준
  해소**: 유일 매치 우선 → 다중이면 core 우선(결정적) → 없으면 dangling. `core:`는 엄격히 core.
- de-camel은 TBox label 관습 그대로: 대문자 시작(클래스)=단어 대문자 유지 `ExecutionMode`→"Execution
  Mode", 소문자 시작(프로퍼티)=전부 소문자 `appliesPattern`→"applies pattern".
- 정규식 `\b(id|core|ho):[A-Za-z][A-Za-z0-9_-]*` — 이름 없는 맨 mention(``ho:`` 단독)은 참조가 아니라
  **건드리지 않음**. 타입 리터럴(`tokenEstimate` 등 datatype≠xsd:string)은 투영 제외.
- 치환은 **idempotent**(해소된 label엔 토큰 없음) → 여러 경로 중복 적용해도 안전.

## 함정
- **`ho:*Shape`는 `ontology/shapes/`에만 선언**되고 데이터 그래프엔 안 들어옴 → 순진하게 하면 TBox
  정의문의 `ho:ComponentConnectivityShape` 등 4종이 매 빌드 dangling 경고로 뜸(전부 **렌더 안 되는**
  TBox prose). ⇒ ho: 토큰에 label이 없을 때만 **shapes 그래프를 lazy 파싱**해 네임스페이스 실재 확인.
- 투영은 그래프 전체를 훑으므로 경고는 "emit된 텍스트"가 아니라 **graph text 전반** 기준(문구도 그렇게).
- **artifactTemplate 본문은 일부러 해소하지 않는다** — fetch되는 저자 작성 산출물이고, 이 온톨로지가
  주제인 하네스는 `ho:` 용어를 **의도적으로** 지시문에 쓴다(뭉개면 의미 파괴). `{{definition}}` 등
  치환값은 투영 그래프에서 오므로 이미 해소됨. 잔여: techdoc persona 템플릿의 "(ho:artifactTemplate)"
  한 줄은 산출물에 그대로 남음(정책 판단 사항, 결함 아님).

## 증명 방법 (동시 dispatch 환경)
- **baseline을 시간으로 잡지 마라**: 다른 dispatch가 `ontology/`를 편집 중이면 "수정 전 빌드"와
  "수정 후 빌드" 비교가 오염된다. `git show HEAD:tools/materialize.py > scratch/orig.py` 후
  `PYTHONPATH=<repo>/tools /usr/bin/python3 scratch/orig.py <h> --out ...` 로 **같은 시점 온톨로지에
  옛 코드**를 돌려 비교(read-only, git 조작 없음).
- diff 필터 함정: `grep -E "^[-+][^-+]"` 는 마크다운 불릿 삭제줄(`- **X**` → `-- **X**`)을 숨겨
  "1줄만 바뀐 것처럼" 보인다. `diff` 줄번호(`34c34`)로 세라.
- 게이트: 산출 트리 전체 `grep -rE "\b(id|ho|core):[a-zA-Z-]+"` 0 / 2회 실행 `diff -r` 동일 /
  유출 0이던 하네스(h-coding·research·support) 트리 **byte-identical** / validate PASS(205).
- 실제 결과: 4 하네스(h-peer-mesh 19·h-harness-factory 9·h-workspace-synthesis 7·h-multiagent 3
  토큰)만 CLAUDE.md(+channel 정의를 담는 MANIFEST.json) 변경, role/skill/lock 파일 불변.
