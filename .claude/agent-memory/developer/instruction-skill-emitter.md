# Instruction(skill/slash-command) 반영 + materialize emitter

GAP-B2(source `.claude/skills/` 미반영) 종결. Claude-Code SKILL = 이름있는 on-demand 절차.

## 핵심: 스키마 무수정으로 끝났다
- `ho:Instruction`(⊑HarnessComponent) 클래스 + `ho:hasInstruction`(⊑hasComponent, range Instruction)
  둘 다 **이미 TBox에 있었고**, `HO.Instruction`도 이미 `ontology_lib.INSTANCE_CLASSES`에,
  `HO.hasInstruction`도 relation set에 등록돼 있었음(0 instance였을 뿐). → 새 property/클래스
  발명 금지(drift). 중앙 96 불변. **감사부터**: audit가 "class 있음 0 instance"라 하면 진짜
  TBox/lib를 grep해 확인 — 없다고 가정하고 property 추가하지 말 것.
- 네이밍 prefix = `ins-`(ONTOLOGYSTYLE 표), 술어순 `hasInstruction`→`hasExample`.

## 모델링 (도메인특정 → recipe LOCAL)
- 소스 skill이 도메인특정(docgraph를 이 설계 문서망에 굴림)이라 recipe(`id/lpranging/`)에 저작,
  중앙 아님. 각 `ho:Instruction`: `skos:prefLabel`(class 내 유일) + `skos:notation`(=invocation
  name=trigger, 예 "check-docs") + `skos:definition`(what) + `ho:artifactTemplate`(vendored body
  경로) + `ho:tokenEstimate`(vendored 본문 기준, byte/4 rough) + `ho:maturity`.
- `skos:notation`은 온톨로지 어디에도 안 쓰였지만 표준 SKOS라 validate 통과(ho: 아니라 drift 아님).
- 본문 substantial(2~2.7KB) → **byte-identical vendor**: `recipes/lpranging/skills/<name>/SKILL.md`로
  `cp -p`+`cmp` 확인, `ho:artifactTemplate`이 그 상대경로. 소스 레이아웃이 dir-per-skill
  (`.claude/skills/<name>/SKILL.md`)이라 그대로 미러.
- harness에 `ho:hasInstruction id:ins-... , ...` 배선(non-orphan, hasComponent 롤업).

## Emitter (materialize.py 7b절, roles/channels 쌍둥이)
- `instruction_name(g,ins)`= `skos:notation` 우선, 없으면 IRI tail `ins-` strip.
- `emit_instructions`: `hasInstruction` IRI-sort, `.claude/skills/<name>/SKILL.md`로.
  artifactTemplate 있으면 **shutil.copyfile(byte-identical)** — render_from_template은
  rstrip+placeholder라 vendor엔 안 씀. 없으면 `_render_instruction_fallback`(frontmatter
  name+definition + promptText body). sources에 tmpl append.
- build_claude_md에 `instructions` param + `## Skills`섹션(if instructions 가드, 없으면 생략).
  MANIFEST `skills` 배열(instruction/label/name/definition/skillFile/vendoredFrom). CLI 리포트 라인.
- `_iter_components`가 이미 hasInstruction 포함 → components/token 카운트 자동, Skills섹션·배열은 additive.

## 게이트
- 중앙 validate 96 불변(스키마·lib 무수정). core grep 0 leakage.
- recipe compose(central 심링크→repo root, `HARNESS_CATALOG=catalog-v001.xml`+root IRI env,
  repo-root cwd) PASS 113→**116**(+3 skill). materialize: skills byte-identical to SOURCE,
  Skills섹션+MANIFEST 배열. 2런 diff -r IDENTICAL. 회귀=h-multiagent(skill-less) 여전히
  materialize+`## Skills`0+skills[]+`.claude/skills`디렉토리 부재. 심링크는 실행후 `rm`(payload symlink-free).
