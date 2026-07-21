.PHONY: install validate retrieve

install:
	pip install --user -r requirements.txt

# Gate: reasoning + SHACL + reachability + capability + dedup
validate:
	python3 tools/validate.py

# Usage: make retrieve Q="an agent that fixes bugs and runs tests"
retrieve:
	python3 tools/retrieve.py "$(Q)" $(if $(BUDGET),--budget $(BUDGET),)
