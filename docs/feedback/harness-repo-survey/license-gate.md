# 라이선스 게이트 — 무엇을 어떤 조건으로 반영할 수 있나

우리 반영 방식은 **소스 텍스트의 복사가 아니라 중립 부품으로의 재저작**이지만
(memory: "ontology is a neutral parts library"), 파생물 판단이 갈릴 수 있으므로 소스별로 선을 긋는다.
`revfactory/harness-100` 반영 때 이미 **Apache-2.0 NOTICE + `dct:source` URL** 규약을 세웠고
(`36bd431`), 그 규약을 그대로 확장한다.

## 판정

| repo | license | 판정 | 조건 |
|---|---|---|---|
| `ai-boost/awesome-harness-engineering` | **CC0-1.0** | **채택 가능(무조건)** | 공유 저작권 포기. 그래도 `dct:source`는 남긴다(추적성) |
| `wshobson/agents` | **MIT** | **채택 가능** | NOTICE에 저작권 고지 + `dct:source`. MIT는 파생·상업 이용 허용, 고지만 요구 |
| `VoltAgent/awesome-claude-code-subagents` | **MIT** | **채택 가능** | 위와 동일 |
| `rohitg00/awesome-claude-code-toolkit` | **Apache-2.0** | **채택 가능** | 기존 harness-100과 같은 규약(NOTICE 크레딧) |
| `mattpocock/agent-rules-books` | **MIT** | **조건부 채택** | repo는 MIT지만 **rule의 내용은 서적(Clean Code·DDD·DDIA…)에서 유래**. 문구를 옮기지 말고 **규칙의 취지만** 중립 `ho:Guardrail`로 재저작. 서적 인용문 금지 |
| `tallesborges/agentic-system-prompts` | MIT(편찬물) + "원 프롬프트는 각 창작자 소유" | **구조 관찰만** | 프롬프트 **본문·문구를 옮기지 않는다**. `ho:PromptSection`이 실제로 어떤 절로 나뉘는지 같은 **구조적 사실**만 참조하고, `dct:source`도 개체에 걸지 않는다(부품을 만들지 않으므로) |
| `hesreallyhim/awesome-claude-code` | **CC BY-NC-ND 4.0** | **채택 불가** | **NoDerivatives** — 목록을 변형·재구성한 파생물 배포를 금지한다. 우리 산출물은 공개 repo(central + harness-recipes)라 NonCommercial 조건도 충돌 소지가 있다. 링크 참조조차 부품화의 근거로 쓰지 않는다 |
| leaked system prompt 모음 | 없음 | **채택 불가** | 라이선스 근거 부재 |

## 반영 시 지켜야 할 것 (기존 규약의 연장)
1. **개체마다 `dct:source`** = 원 파일의 GitHub URL(회수일 포함 코멘트). harness-100 pilot에서 쓴 방식 그대로.
2. **NOTICE 갱신**: central repo의 `NOTICE`에 신규 소스별 라이선스·저작권 줄 추가(현재 harness-100
   크레딧만 있음 — recipes repo 쪽). 채택 wave의 완료 조건에 포함한다.
3. **중립화 필수**: 소스의 도메인 특화 이름(`rust-pro`, `nextjs-shadcn-rules` 등)을 그대로 개체로 만들지
   않는다. 이는 라이선스 이전에 **우리 저장 원칙**(중립 부품 라이브러리)의 문제다 — `part-taxonomy.md`가
   harness-100에서 세운 원형화 규율을 재사용한다.
4. **역이용 금지**: 우리가 만든 부품을 소스 repo의 이름으로 표기하지 않는다(귀속은 `dct:source`로만).

## 판단이 필요한 회색지대 (사용자 결정)
`mattpocock/agent-rules-books`는 repo 라이선스는 깨끗하지만 규칙 자체가 유명 서적의 요약이다. 우리가
"취지만 중립 재저작"해도 결국 **서적의 규범을 재배포**하는 셈이라는 해석이 가능하다. 보수적으로는
**이 소스를 빼고**, 같은 취지의 규칙이 필요하면 우리가 직접 근거를 세워 저작하는 편이 안전하다.
inspection 권고는 **보수 노선(제외)** 이며, 채택 여부는 항목에서 결정한다.
