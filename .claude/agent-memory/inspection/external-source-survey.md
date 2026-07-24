# 외부 소스 repo 조사·라이선스 게이트 (inspection)

harness 관련 외부 repo를 온톨로지 반영 후보로 조사할 때의 절차와 함정. 산출 위치는
`docs/feedback/<survey>/` + 결정 앵커 항목(기존 `harness-100-augmentation`·`revfactory-harness-reflection`과
같은 형식: item 1편 + companion 여러 편).

## 라이선스는 API 배지를 믿지 말고 LICENSE 본문을 읽는다
`gh api repos/<r>` 의 `.license.spdx_id`가 **NOASSERTION**이면 판정 불가지 "없음"이 아니다. 실제로
같은 NOASSERTION 3건이 **CC0-1.0 / CC BY-NC-ND-4.0 / MIT**로 전부 달랐다. 확인:
`gh api repos/<r>/contents/LICENSE --jq .content | base64 -d | head -4`
- **CC BY-NC-ND = 채택 불가**(NoDerivatives). 큐레이션 목록에서 흔하다 — 별 수가 많다고 안전하지 않다.
- repo 라이선스가 깨끗해도 **내용의 출처**가 따로일 수 있다(서적 요약 rule, 유출 system prompt).
  편찬물 라이선스는 원저작물에 미치지 않는다.
- 실측 한 줄: `gh api repos/<r> --jq '"\(.license.spdx_id)\t\(.stargazers_count)\t\(.size)KB\t\(.pushed_at[0:10])"'`

## 조사 깊이를 정직하게 표시한다
README·디렉토리 구조까지만 봤으면 "수확 추정"은 **추정**이라고 문서에 쓴다. 파일 전수 정독 없이
개체 수를 약속하면 이후 wave가 그 숫자에 묶인다.

## 수확의 우선순위 = 우리 얇은 축
부품 수가 아니라 **우리 그래프에서 얇은 축**(측정: `grep -rhoE 'a ho:[A-Za-z]+' ontology/abox/core | sort | uniq -c`)에
대응하는 소스가 값지다. 그리고 부품보다 **축의 목록**(예: harness-engineering의 12 design primitives)이
커버리지 감사 기준으로 더 쓸모 있다 — 저작 0으로 GAP을 찾아낸다.

## 관련
[[federation-lockstep]] (반영 wave마다 recipe federate 게이트), [[refresh-and-git-baseline]].
