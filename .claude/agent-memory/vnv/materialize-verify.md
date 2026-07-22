# materialize.py (BUILD projection) 검증 재현 절차 + 함정

`tools/materialize.py`는 retrieve의 dual = validated harness → 파일트리(CLAUDE.md +
MANIFEST.json). 전부 `/usr/bin/python3`. 판정: `docs/verify/materialize-and-language.md`.

## 재현 (recipe union을 materialize)
- h-techdoc 등 recipe 노드는 central 64에 없다 → **recipe union**을 조립해야 한다:
  `ln -sfn "$(pwd)" staging/harness-recipes/central` (임시 심링크), `cd staging/harness-recipes`,
  `HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=…/recipes/techdoc
  /usr/bin/python3 central/tools/materialize.py h-techdoc --out <scratch>`. **끝나면 `rm -f central`**
  (staging at-rest 심링크=0 hygiene). lib.ROOT는 tools 파일 위치 기준(심링크 통해 repo root),
  template base #1=lib.ROOT #2=catalog dir. `ho:artifactTemplate "tools/materialize_templates/…"`는
  repo-root 상대라 base#1로 central에서 해소.
- CLAUDE.md 섹션 고정순: overview / Persona(hasSystemPrompt+promptText, template 있으면 render) /
  Operating rules(hasGuardrail, languageCondition은 sub-bullet) / Process(hasWorkflow+appliesPattern) /
  Model(usesModel). MANIFEST: components(concrete type)/capabilityBindings(requires→provides)/
  derivedFrom/templateSources/tokenEstimate, sort_keys+IRI정렬 → determinism.

## 게이트/결정성 증명
- **게이트는 load/resolve/write보다 먼저** `validate.run_structured()` 실행. 두 refusal 증명:
  bogus id→exit2(union valid, resolve 실패), non-validating union→exit1. 둘 다 **out dir 미생성** 확인.
  invalid union 쉽게 만들기: scratch root가 schema+core/harnesses만 import → harness가 참조하는
  컴포넌트 미해소 → SHACL fail.
- determinism: 2회 → `diff -r` IDENTICAL + sha256 동일.
- template render vs fallback 구분: persona.md.tmpl에 고정 tail줄("rendered from a template
  fragment")이 있어 그 줄 존재=template경로, 부재=graph-data fallback.

## 함정 — ontology_lib.most_specific_types 잠복버그 (central-side)
- `load_graph(reason=True)`면 OWL RL이 reflexive `rdfs:subClassOf`(Tool subClassOf Tool)를
  materialize → `most_specific_types`의 superclass-drop 루프가 **자기 self-edge로 자신을 discard**,
  항상 fallback(all types) 반환. `mst[0]`=알파벳순 `HarnessComponent`(abstract). 그래서
  materialize `_component_type`가 HarnessComponent를 걸러내고 [0] 취하는 **로컬 워크어라운드** 필요.
- 이 버그는 **pre-existing**, materialize 변경물 아님. 모든 caller 영향(validate.py dup-label=benign,
  retrieve/webui `types`=noisy). 중앙 fix = `if sup != t: specific.discard(sup)` (self-edge guard).
  로컬 워크어라운드는 least-privilege 상 이번 increment엔 적정 → pass-with-notes, 중앙 fix는
  orchestrator/developer 라우팅. 로컬 방식은 HarnessComponent만 벗겨 중간계층 3-level엔 부족.
- 판정: pass-with-notes. 6항목 전부 통과, note=위 central 잠복버그 1건뿐.

## increment 2 — P4 roles / P3 implementationRef / P5 scaffold (verdict: pass)
- **New TBox**: `ho:Role` (subClassOf HarnessComponent) + 7 props (hasRole,
  rolePersona/roleTool/roleGuardrail/roleMemoryPolicy, implementationRef, scaffold).
  Drift check that matters: (a) `ho:hasRole rdfs:subPropertyOf ho:hasComponent` →
  roles reachable+SHACL-valid with **NO new shape** (prove: `git diff <init> HEAD --
  ontology/shapes/harness-shapes.ttl` empty AND union validates with roles). (b)
  `ho:scaffold` has **no rdfs:domain** (else OWL RL mistypes the Harness/Domain it
  hangs on as a component → orphan-shape trip); `grep rdfs:domain` in the scaffold
  block hits only the *definition string* text, not a real predicate — check with
  `grep -E "^\s+rdfs:domain"`.
- **Neutrality**: roles live in the recipe, central abox stays 64; grep core/ for
  hasRole|implementationRef|role-|scaffold = 0. retrieve.py ignores build-only props.
- **Full-tree materialize** (lpranging union, symlink dance): tree = CLAUDE.md
  (+`## Roles`) / MANIFEST / `.claude/agents/{developer,vnv,inspection}.md` /
  `tools/<copied>.py` / scaffold files. Verify copied code **byte-identical**:
  `cmp` + `sha256sum` vs source `~/git/agrtls/device_harvest_lp/lpranging/tools/
  docgraph.py` (32560B) & `reference/sim_grid_reservation.py` (11309B). Role scopes
  in agent files must be **strict subsets** of harness usesTool/hasGuardrail
  (least-privilege) — cross-check each roleTool/roleGuardrail against the harness.
  MANIFEST gains roles/implementations(status resolved|stub)/scaffold.
- **implementationRef portability**: lpranging uses **absolute** source paths
  (resolve only on this box). Judged **pass, non-blocking**: documented trade-off,
  fails *safe* (unresolvable → `tools/<base>.ref` stub, no crash), build-only so no
  neutrality/validation impact; portable fix = ship code in recipe + repo-relative
  ref (recipe-authoring follow-up, not a defect).
- **Regression**: role-less central `h-multiagent` still emits only CLAUDE.md+MANIFEST
  (manifest gains empty roles/impl/scaffold keys — additive/benign); techdoc still builds.
  Gate still refuses bogus id (exit2) / non-validating union (exit1), out dir never made.
