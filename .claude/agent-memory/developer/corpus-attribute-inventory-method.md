# 코퍼스 전수 속성 인벤토리 — 방법과 함정 (harness-100 Phase 0.5)

100개 외부 하네스 코퍼스의 **속성값 공간을 실측하고 중앙 어휘와 대조(GAP)** 하는 분석 dispatch를
수행했을 때의 재사용 지식. 산출물: `docs/plans/harness-100-attribute-inventory.md`.

## 1. 컨텍스트를 태우지 않고 100개를 읽는 법

- **파일 전문 로드 금지.** `scan.py`(스크래치패드) 한 번으로 904 파일을 파싱해 `facts.json`
  중간 산출물을 만들고, 이후 모든 집계는 그 JSON에서만 한다. 정독은 표본 2~3개.
- 저장할 필드: frontmatter dict, 섹션 헤딩 리스트, bullet 리스트, 표 행, word count, 산출물 경로.
  **body 원문은 orchestrator skill만** 저장(표 파싱이 필요해서). agent body는 필요할 때 재오픈.
- 산출물이 커지면 `git status`에 남지 않도록 반드시 스크래치패드에 둔다(브리프 밖 경로 금지).

## 2. 셸 grep 함정 (실제로 물림)

- `grep -r --include=*.md .` 에서 **`--include` 패턴을 따옴표로 감싸지 않으면** cwd에 `README.md`가
  있을 때 셸이 `--include=README.md`로 전개해 **조용히 1파일만** 검사한다. 항상 `--include='*.md'`.
- `grep -rl` 출력에 `./` 접두사가 붙는지 아닌지는 호출 형태에 따라 다르다 → `cut -d/ -f1`이 맞는지
  **먼저 5줄 찍어 확인**하고 센다. (안 하면 "1/100 harnesses" 같은 헛수치가 나온다.)

## 3. 기계번역 코퍼스의 파싱 원칙

외부 영문 코퍼스는 헤딩 문자열이 10종 이상으로 변형된다(`Workflow`/`workflow`/`flow`/
`data before as`/`inthisbefore setup`). 따라서:
- **1차 근거 = 표 헤더 + 본문 시그널**(`SendMessage`, `_workspace/`, `Depends On`, `🔴`),
  **2차 = 헤딩 정규식 패밀리**. 헤딩만 믿으면 10~25%가 조용히 누락된다.
- 표 헤더를 `tuple(cells)`로 Counter에 넣어 빈도순으로 보면 **템플릿 구조가 바로 드러난다**
  (`agent/file/role/type` 96, `error type/strategy` 95, `order/task/owner/dependencies/deliverable` 33…).

## 4. GAP 판정을 정직하게 하는 3분류

관측값마다 **① 신규 개체 / ② 기존 개체의 altLabel로 흡수 / ③ 도메인 특수라 중앙 금지**를 붙인다.
- ③의 판별 기준(실측 가능): **인스턴스 재사용률**. extending skill 209종 중 2회 등장 6종·3회 0종
  → 재사용률 ≈0 → ③. 반대로 role 원형은 이름은 429종 unique여도 원형으로 접으면 14종에 78/489가
  몰린다 → ①.
- ②를 적극적으로 써야 한다. 근사 동의어 개체 신설이 이 repo가 막는 drift 그 자체다.
- **definition을 읽고 판정하라, label로 하지 마라.** 예: `core:role-developer`의 prefLabel은
  "Developer agent"라 implementer 원형에 맞아 보이지만 definition은 "authors the **ontology nodes**
  assigned in a brief" — repo 전용이라 중립이 아니다. `role-orchestrator`도 "performs no
  substantive work itself"라 코퍼스의 planner 워커와 정반대.
- Guardrail은 `skos:definition`이 아니라 **`ho:promptText`** 에 내용이 있다(rdflib로 뽑을 때 주의).

## 5. TBox 확장 후보는 "우회 가능성"까지 적어야 한다

"담을 클래스가 없다"고 보고하기 전에 **기존 어휘로의 우회를 실제로 설계해 보고**, 왜 무리인지를
같이 적는다. 예(scale mode): 모드마다 Workflow를 만들고 `stepByRole`로 활성 역할을 표현하는 우회는
가능하지만 (a) recipe당 5~7 workflow로 비대해지고 (b) "어떤 요청 패턴이 이 모드를 켜는가"를 담을
술어가 없다(`ho:triggerPhrase`는 definition에 Harness+Instruction 전용으로 명시). 이렇게 써야
orchestrator가 (i)신설 (ii)적용범위 확장 (iii)명시적 미표현 중에서 고를 수 있다.

## 6. coverage-driven 선정은 "우주"를 먼저 고정한다

한 개의 커버리지 %는 의미가 없다. 최소 3개 우주로 나눠 각각 실측:
- **U1 구조·중립값**(중앙이 담아야 할 축) → 이게 100%가 목표.
- **U2 중간층**(이름 어휘 등) → 부분 커버가 정상.
- **U3 순수 도메인 payload** → 커버 안 되는 게 **옳다**(③이므로).

★ 실측 결과의 교훈: **U1은 매우 빨리 포화한다**(harness-100은 파일럿 5개→15개에서 100%).
그러니 "N개 선정"의 근거를 구조 커버리지로만 정당화하면 N이 15로 붕괴한다. 카테고리 비례 쿼터·
도메인 어휘 예시 같은 **다른 축의 근거**를 명시해야 정직하다. greedy는 쿼터를 강제한 뒤
`3×|newU1| + 2×|newU2| + 1×|newU3|` 점수로, tie-break는 번호 오름차순(결정적)으로.

## 7. 부산물로 나오는 강한 신호들 (보고 가치 높음)

- **바인딩 누락 vs 어휘 GAP 구분**: 소스가 거의 전수 제공하는데 이미 land된 recipe에는 0건인 축을
  찾아라(여기선 `hasExecutionMode`·`TestScenario`·`FailurePolicy`가 8 recipe 전체에서 0). 이는
  TBox/ABox 문제가 아니라 **coverage-audit 미이행**이며, 스케일업 전에 되돌아가야 할 지점이다.
- **변이가 0인 축**을 찾아라(여기선 실행 topology가 100/100 `Agent Team`). 계획이 그 축의 "판별"을
  게이트로 넣고 있다면 판별할 것이 없다고 알려야 한다.
- **소스에 아예 없는 정보**를 찾아라(agent frontmatter에 `tools:`·`model:` 0/489). 매핑 표가 그걸
  "소스→노드"로 적고 있으면 그건 기계 변환이 아니라 **판단성 결정**이므로 importer 계약을 고쳐야 한다.
