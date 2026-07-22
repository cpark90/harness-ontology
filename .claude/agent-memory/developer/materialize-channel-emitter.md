# materialize channel emitter (EMIT counterpart of ho:Channel)

materialize 증분: `ho:hasChannel`(⊑hasComponent)로 롤업만 되고 전용 emitter가 없던 채널을
roles와 쌍둥이 패턴으로 투영(EMIT). 코드는 `tools/materialize.py`.

- **단일 소스 helper** `channel_record(g, chan)` → `{iri,label,definition,participants[],
  involvesUser,medium}`을 CLAUDE.md 섹션과 MANIFEST 배열 **양쪽이 공유**(consistency).
  participants=`ho:channelParticipant`(→Role) IRI-sort, 각 `{iri,label}`.
- **boolean 읽기 함정**: `ho:involvesUser`는 xsd:boolean Literal. `bool(Literal)`는 truthy
  오판 위험→`involves.toPython()` 후 bool, None이면 False.
- **CLAUDE.md** `## Coordination channels` 섹션은 `## Roles` 바로 뒤, roles와 동일하게
  `if channels:` 가드(채널 없으면 섹션 통째 생략). build_claude_md 시그니처에 channels 추가,
  materialize()에서 `_sorted(g.objects(h, HO.hasChannel))`로 계산해 전달.
- **MANIFEST** `channels` 배열을 build_manifest에 추가(components에 묻히지 않게 first-class).
  roles/implementations 스타일 미러. 없으면 `[]`.
- 결정성: 채널 IRI-sort + 참가자 IRI-sort, 무타임스탬프 → 2런 diff -r IDENTICAL.
- **순수 EMIT 추가**: TBox/shapes/ABox 무수정, 그래프가 이미 모델한 것만 투영. 중앙 validate 96 불변.
- 게이트 gotcha: brief가 예시로 든 `h-techdoc`는 recipe(중앙 스토어에 없음). 채널 없는 회귀
  테스트는 중앙 harness 중 hasChannel 없는 것(h-coding/h-research/h-support)으로. h-multiagent는
  hasChannel 있음. lpranging recipe는 staging central 심링크+HARNESS_CATALOG/ROOT_ONTOLOGY env로.
