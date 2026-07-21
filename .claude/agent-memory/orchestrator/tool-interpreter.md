# 도구 실행 인터프리터

`tools/validate.py`·`retrieve.py`는 `rdflib`/`pyshacl`/`owlrl`를 import한다. 이 의존성은
**모든 `python3`에 있지 않다** — 이 머신의 셸 기본 `python3`(anaconda `oto` env)에는 없어
`ModuleNotFoundError: No module named 'rdflib'`로 실패한다. `/usr/bin/python3`에는 셋 다
설치돼 있다(rdflib 7.6.0). baseline `/usr/bin/python3 tools/validate.py` = PASS 확인됨.

**어떻게 적용**: 도구를 `python3 tools/validate.py`로 실행했다 실패하면 인터프리터 문제다.
`/usr/bin/python3 tools/validate.py`처럼 의존성이 있는 인터프리터로 재실행한다. 리포트·메모리
에는 실제 실행한 명령을 그대로 적는다. (CLAUDE.md는 "plain python3"라 하지만 이는 그 셋이
기본 python3에 깔린 환경 전제 — 이 머신에선 어긋난다.)
