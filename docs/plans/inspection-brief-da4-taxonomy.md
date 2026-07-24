# Inspection 브리프 — DA-4 taxonomy + ABox 레이아웃 재조직 증분 (6b563a0 이후)

> 작성: orchestrator (2026-07-23). 실행: **inspection 세션**. 직전 land(`4b31b59`, central @185, disambiguation DA-1/DA-2까지)의 **다음 증분**: DA-4(TBox 상위 taxonomy) + REORG-1/2(ABox 파일 레이아웃을 taxonomy에 맞춰 재조직). **개체 수 185 불변**(순수 재부모화/이동/split — 의미 무변경).

## 미커밋 델타 (~39파일: TBox + 파일 이동/split + catalog + docs + agent-memory)
### 1. DA-4 — TBox 상위 taxonomy (`ontology/tbox/harness.ttl`)
중간 superclass 11 신설 + 22 HC leaf + 7 비-comp leaf 재부모화. HC 하위 9(Behavioral/Observational/Operational/State/Organization/Process/Verification/Assembly/Substrate) + 비-comp 2(SpecConcept/InformationSpace). `HarnessComponent` 직결 subclass=9(중간만).

### 2. REORG-1 — 중앙 ABox 파일 → DA-4 그룹 디렉토리 (파일 이동/split)
- 이동(git rename): `ontology/abox/core/<type>.ttl` → `ontology/abox/core/<group>/<type>.ttl`. 12 그룹 디렉토리(assembly/behavioral/information-space/observational/operational/organization/process/spec/state/substrate/vocab/wholes). 평면 잔재 0.
- **grab-bag split → 신규 4유닛**: roles→(organization/roles + observational/observation + state/memory) · domains-tasks→(spec/domains-tasks + information-space/information-space) · harnesses→(wholes/harnesses + assembly/assembly-sections). 개체 IRI 불변(`id:core/` 위치독립).
- federation: `catalog-v001.xml`(root, 13경로 갱신 + 4신규) · `ontology/harness-ontology.ttl`(owl:imports +4) · `ONTOLOGYSTYLE.md §4`(그룹 레이아웃 규칙).

### 3. REORG-2 — recipe catalog 동기화 + stale 문서
- `staging/harness-recipes/catalog-v001.xml`: central 13경로 그룹화 + 4신규 + **pilot 5줄 공유 consolidate**(inc3의 대기 catalog 통합도 해소).
- live 구조문서: `docs/federation-design.md`·`docs/recipes-design.md`·`docs/ci/data-repo-validate.yml` 평면→그룹 경로.

### 4. 부수: docs/plans(`disambiguation-audit.md §G`·`abox-taxonomy-reorg.md`·이 브리프) + agent-memory 노트.

## 검증 증거 (land 전 재확인)
- 중앙 `/usr/bin/python3 tools/validate.py` → **PASS 185**(3 로더 경로: imports+catalog / glob fallback / 명시 env 전부). tools 하드코딩 경로 0(이동 투명).
- `ls ontology/abox/core/*.ttl` → **0**(전부 그룹 디렉토리). `grep -c "rdfs:subClassOf ho:HarnessComponent" tbox/harness.ttl` → **9**(중간만).
- recipe federate(공유 catalog, per-recipe closure): 5 pilot 전부 PASS(200/203/205/205/205) + lpranging/techdoc/contract-demo PASS.
- materialize h-multiagent byte-identity(DA-4·이동은 emit 무관). 판정: dev 자기검증 + orchestrator validate/구조/federate 확인(순수 구조 refactor, 저위험). 별도 vnv 판정 원하면 orchestrator 요청.

## 실행 (git rename 다수 — `git add -A`가 이동 포착)
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # PASS 185
git add -A                                     # 파일 이동/split을 rename+add로 포착
git commit -m "Taxonomy: 11 intermediate superclasses (DA-4) + ABox files regrouped into DA-4 group dirs (reorg)

- DA-4: MAS-aligned intermediate superclasses group flat HarnessComponent/non-component leaves
- REORG: abox/core/<type>.ttl -> abox/core/<group>/<type>.ttl; roles/domains-tasks/harnesses grab-bags split into observation/memory/information-space/assembly-sections units; catalog + root imports + ONTOLOGYSTYLE synced
- 185 individuals invariant (pure re-parent/move/split, no semantic change)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## 레시피 repo(harness-recipes) push — catalog 그룹경로 동기화
이미 published된 recipe repo의 `catalog-v001.xml`도 central 그룹 경로로 갱신 필요(중앙 push 후):
```bash
DST=/home/cpark/git/harness-recipes; cd "$DST" && git pull
# catalog-v001.xml: central/ontology/abox/core/<type>.ttl → <group>/<type>.ttl + 신규 4유닛 (staging 갱신본 참조)
git clone https://github.com/cpark90/harness-ontology.git central
for R in 21-code-reviewer 16-fullstack-webapp 31-ml-experiment 03-newsletter-engine 46-product-manager; do
  HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/$R /usr/bin/python3 central/tools/validate.py; done  # PASS
rm -rf central; git add -A && git commit && git push
```
(inc3 pilot 5 recipe가 아직 published repo에 없으면 함께 push — `inspection-brief-CONSOLIDATED` 그룹4 참조. 이미 land됐으면 catalog 경로만.)

## 완료 보고 (inspection → orchestrator, append)
- [ ] 중앙 push @185 taxonomy+reorg (commit ____) / CI green
- [ ] recipes repo catalog 그룹경로 동기화 (commit ____) / CI green
