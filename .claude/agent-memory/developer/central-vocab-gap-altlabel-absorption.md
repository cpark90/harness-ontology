# 코퍼스 GAP을 중앙에 반영할 때 — altLabel 흡수·host 배선·예산 보정

harness-100 Phase 0.6 (`docs/plans/dispatch-central-vocab-gap.md`) 저작 dispatch의 재사용 지식.
관측 속성값을 **전부 신규 개체로 만들지 않고** 중립 부품 라이브러리를 유지하는 실무 절차.

## 1. ★altLabel 흡수는 byte-identity SAFE — 이게 분류②를 싸게 만든다

`grep -n altLabel tools/*.py` → **`retrieve.py:85` 한 곳뿐**(검색 텍스트 조립). `materialize.py`는
`skos:altLabel`을 **절대 렌더하지 않는다**. 따라서 이미 여러 harness에 bound된 노드
(`gr-cite`·`gr-grounding`·`gr-scale-modes`·`role-vnv`·`role-design`…)에 altLabel을 **몇 개든 추가해도
emit 산출물은 전부 불변**이다. 즉 "근사 동의어 개체 신설" 대신 "기존 개체에 altLabel"이라는
anti-drift 수단은 **파급 0**이다 — 주저할 이유가 없다. (반대로 `skos:definition`/`prefLabel` 수정은
CLAUDE.md·agents/*.md를 바꾼다. 그래서 중립 sibling 신설이 정답인 경우가 많다.)

한 노드에 altLabel 여러 개는 콤마 리스트로: `skos:altLabel "a" , "b" ;` (prefLabel과 같은 줄이
길어지면 다음 줄로 내려 4칸 들여쓰기 — 지역 컨벤션 유지).

## 2. byte-identity 불변식의 **정확한** 서술 — `harness.lock.json`은 예외다

`harness.lock.json`의 `spec.individualCount`는 **union 전체 개체 수**라서 그래프가 커지면
**모든 harness에서** 205→223처럼 바뀐다. 배선을 아무리 잘해도 고정할 수 없다.
⇒ 불변식은 "산출물 전부 byte-identical"이 아니라 **"lock의 union 카운터를 뺀 모든 emit 파일이
byte-identical"** 로 서술·증명해야 한다. 증명 레시피(git 없이, baseline을 먼저 뽑아둠):

```bash
for h in ...; do
  a=$(cd base/$h && find . -type f ! -name harness.lock.json | sort | xargs md5sum | md5sum)
  b=$(cd after/$h && find . -type f ! -name harness.lock.json | sort | xargs md5sum | md5sum)
done   # + diff base/$h/harness.lock.json after/$h/harness.lock.json 로 카운터만 바뀐 것도 함께 제시
```

## 3. `ho:tokenEstimate` — brief의 "필수"보다 **지역 컨벤션이 우선**

이 repo에서 tokenEstimate를 다는 클래스는 **텍스트 리터럴을 실제로 지닌 것뿐**이다:
Guardrail(promptText)·TestScenario·FailurePolicy·SystemPrompt·Tool·Workflow.
**Role·Concept·Channel은 definition만 있으므로 안 단다**(기존 8 Role·35 Concept·6 Channel 전부 0건).
신규 6 Role에만 붙이면 오히려 일관성이 깨진다. 브리프가 "필수"라 해도 §1(일관성 최우선)이 이긴다.

값 보정은 **peer 실측 비율**로 (감으로 쓰지 말 것):
- Guardrail: `declared / promptText단어수` ≈ **1.25~1.5** (gr-absolute-paths 1.53, gr-graceful-fallback 1.26)
- FailurePolicy: `declared / (definition+condition+strategy 단어수)` ≈ **1.1~1.2**
- 진단 불변식(§3): tokenEstimate가 기본 예산(900)을 넘는 노드는 0개여야 한다 — 저작 후 rdflib로 확인.

## 4. 정의가 얼어 있는 sibling과의 disambiguation은 **한쪽에만** 쓴다

`role-implementer` vs `role-developer`처럼 기존 노드 definition을 못 고칠 때(수정=CLAUDE.md 변경),
"Distinguished from id:role-developer, which is this repository's own concrete authoring agent …"를
**신규 노드 쪽에만** 넣는다. emit 진입부가 `id:`/`ho:` 토큰을 prefLabel로 해소하므로
산출 문서에서는 "Distinguished from **Developer agent**, …"로 읽힌다 — 저자용 IRI를 그대로 써도 된다.

## 5. host 배선 — 신규 중립 부품은 라이브러리 carrier에만

Role·Guardrail·FailurePolicy는 전부 ⊑HarnessComponent → harness 배선 없으면 SHACL orphan FAIL.
`ho:hasFailurePolicy`는 Harness 직결이라 특히 host 필수. 용도별 carrier가 이미 3개 있다:
- `h-workspace-synthesis` = **팀 구성 부품**(worker 원형 role, 팀 규율 guardrail, 도메인 무관 error row)
- `h-harness-factory` = **메타/방법론 부품**(복잡도·저작·검증 거버넌스, 메타 workflow)
- `h-peer-mesh` = peer 채널
harness 블록 술어 순서(지역): `…hasGuardrail → usesModel → hasRole → hasChannel → hasTestScenario →
hasFailurePolicy → appliesPattern → hasExecutionMode → requiresCapability → tagged → derivedFrom → maturity`.

## 6. 저빈도 원형은 **`ho:salience`로 내린다** (기본값을 알고 써야 함)

`retrieve.py:131` → `prior = 0.5 + (salience if present else **0.4**)`. 즉 **미기재 = 0.4**이므로
"우선순위 낮게"는 반드시 **0.4 미만**을 명시해야 효과가 있다(`role-tester`에 0.25).

## 7. 중앙 성장 후엔 **staging recipe closure 8종도 재검증**

`staging/harness-recipes/`에서 recipe별로:
`HARNESS_CATALOG=catalog-<recipe>.xml`(전용 catalog가 있으면 그것, 없으면 `catalog-v001.xml`) +
`HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<recipe>` → 중앙 `validate.py`.
새 unit 파일을 만들지 않았다면 catalog·imports 무변경이라 전부 PASS여야 한다(실제로 8/8 PASS).

## 8. 저작하지 않은 것을 반드시 보고한다

분류③(도메인 특수)은 "누락"이 아니라 **결정**이다: domain-specialist role, compliance/security/a11y/
l10n 원칙 문장, TestScenario prompt 실체, extending skill 209종, 도메인 scale-mode 라벨, Task 100종.
재사용을 시도했다가 못 쓴 기존 개체와 그 이유(= 근사 동의어 방어의 증거)도 같이 남긴다.
