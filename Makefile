.PHONY: test fmt lint

fmt:
	black agent_log_ontology

lint:
	ruff check agent_log_ontology

test:
	./pytest

