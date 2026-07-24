# 도구쪽 화이트리스트·경로 glob = 조용한 실패의 온상 (감사법)

`ontology/` 는 초록인데 **도구가 그래프의 일부를 못 보는** 결함 계열. 공통 증상은 에러가 아니라
**조용한 누락**(빈 목록·상위 타입으로 뭉개짐·edge 소실)이다. 이 repo에는 서로 독립인 화이트리스트가
**3개** 있고, 새 어휘를 land할 때마다 전부 갱신 대상인지 따져야 한다.

| 레지스트리 | 위치 | 미등록 시 증상 |
|---|---|---|
| `INSTANCE_CLASSES` | `tools/ontology_lib.py` | 개체가 카운트/reachability/팩에서 증발(추론이 가림) |
| `INSTANCE_LINK_PREDICATES` | 같은 파일 | 노드는 보이는데 **edge만** 안 보임(그래프뷰·전파) |
| `ORDER` / `STRING_PREDS` | `tools/webui/ttl_writer.py` | webui 저장 시 그 술어가 **블록에서 삭제됨** |

## 1. `INSTANCE_CLASSES`: 추론이 결함을 가린다 → 파리티가 유일한 게이트

- 등록 대상은 **asserted leaf 클래스만**. DA-4 **중간 superclass는 절대 넣지 않는다**
  (직접 인스턴스 0 + 추론 타입이라 중복 조회만 늘린다).
- 누락 leaf는 `owlrl` 켜진 경로에선 상위 `ho:HarnessComponent` 타입이 대신 잡아줘서 **안 보인다**.
  ★**불변식 = `len(instance_nodes(load_graph())) == len(instance_nodes(load_graph(reason=False)))`**.
  이 한 줄이 유일한 폭로 수단이다(2026-07 실측: 205 vs 173, leaf 7클래스·32개체 누락).
  차집합 `a - b`를 프린트하면 누락 개체가 바로 나오고, 접두사(`agent-`/`aoi-`/`oa-`/`os-`/`mem-`/
  `scn-`/`fp-`)로 어느 클래스인지 즉시 역추적된다.
- **파급은 MANIFEST의 `type` 표기뿐**: `most_specific_types`가 구체 leaf를 돌려주므로
  `HarnessComponent` → `Agent`/`AreaOfInterest`/`AreaOfObservation`/`ObservationSpace`/`Memory`/
  `TestScenario`/`FailurePolicy`로 정밀해진다. **CLAUDE.md·role md·lock은 byte-identical**
  (렌더러가 타입 문자열을 안 읽음), `individualCount`도 불변(추론 경로는 이미 205였음).
  retrieve 팩도 노드·relevance 동일, **타입 그룹 헤딩만** 세분화된다.
- **before/after 대조는 git 없이**(git 조작 금지): `sys.path.insert(0,'tools')` 후
  `import ontology_lib as l; l.INSTANCE_CLASSES = OLD_SET` 로 **모듈 전역만 monkeypatch**하고
  `import materialize; materialize.main()`. 소비자가 전부 `lib.X`를 호출 시점에 읽으므로 정확히
  옛 동작이 재현된다(`git show HEAD:` 복원보다 싸고, 동시 편집 중인 트리도 오염 안 됨).
  ★대조는 **한 하네스로 부족**: h-multiagent엔 28개체만 물려 있고 `TestScenario`/`FailurePolicy` 4는
  h-harness-factory 쪽 — 7하네스 전수로 돌려야 32 전부가 증명된다.

## 2. DA-4 그룹 디렉토리 이후 **평면 glob은 전부 0건**

`ontology/abox/*.ttl` → 0개(실제 18개는 `abox/core/<group>/<type>.ttl`). 재귀로 고칠 때
`os.path.join(ABOX_DIR, "**", "*.ttl")` + **`recursive=True`**(빠뜨리면 `**`가 `*`처럼 1레벨),
그리고 `sorted()`로 결정적 순서. `**`는 **0개 디렉토리에도 매치**하므로 평면 `abox/authored.ttl`
(webui가 신규 노드를 쓰는 자리)도 계속 잡힌다 — 평면 패턴을 남겨 or-합칠 필요 없음.
- 잔여 취약점: `server.abox_mtimes()`가 **basename을 키로** 쓴다. 지금은 18개 basename이 유일해
  무해하지만, 다른 그룹에 같은 파일명이 생기면 낙관적 잠금이 조용히 뭉개진다(상대경로 키가 정답).

## 3. webui `ORDER` 화이트리스트 = **부분 저장이 곧 데이터 삭제**

`render_block`은 `ORDER`에 있는 술어만 그리고, `_replace_block`이 **블록 전체를 치환**한다 →
목록 밖 술어는 소리 없이 사라진다. 실측(2026-07): 그래프에 존재하나 `ORDER`에 없는 술어 **56종**,
영향 개체 **82/205**. 예: `id:chan-dispatch`를 UI로 저장하면 `channelParticipant`·`channelMedium`·
`involvesUser`·`tagged`·`definition`이 통째로 날아간 2줄 블록이 된다.
서버가 validate FAIL 시 `restore`하므로 **shape이 요구하는 술어만** 우연히 방어되고, 선택 술어는
초록인 채로 유실된다. 감사 스니펫 = 전 개체의 `predicate_objects`를 qname으로 접어 `ORDER` 차집합 카운트.
**확장은 "편집 UI가 무엇을 다뤄야 하는가"라는 범위 결정**이므로 developer가 임의로 넓히지 말 것.

## 4. `tokenEstimate` vs `observedTokenVolume` 계약을 스타일 문서에 못박기

`ONTOLOGYSTYLE §3` 데이터 그룹 순서는 `promptText → observedTokenVolume → tokenEstimate →
salience → maturity`(실 저작 관례와 일치). 여기에 **[지킴] "둘을 섞지 않는다"** 한 줄 —
`tokenEstimate`=노드 자신의 팩 비용 / `observedTokenVolume`=AoO의 런타임 관측량 — 과
**진단 불변식 "`tokenEstimate > DEFAULT_BUDGET`인 노드 0개"**를 같이 적어두면 다음 저작자가
관측량을 되돌려 넣어 팩을 자르는 재발을 막는다.
