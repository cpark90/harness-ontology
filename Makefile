.PHONY: install validate determinism retrieve

install:
	pip install --user -r requirements.txt

# Gate: reasoning + SHACL + reachability + capability + dedup
validate:
	python3 tools/validate.py

# Gate: the same request must project the same context pack in every process
# (read-projection counterpart of materialize's byte-identity guarantee).
determinism:
	python3 tools/check_determinism.py

# Usage: make retrieve Q="an agent that fixes bugs and runs tests"
retrieve:
	python3 tools/retrieve.py "$(Q)" $(if $(BUDGET),--budget $(BUDGET),)
