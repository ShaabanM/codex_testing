"""CLI for converting logs to the ontology."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .connectors.openai_traces import from_openai_trace


def _print_tree(step, indent=0):
    prefix = " " * indent
    print(f"{prefix}- {step.name or 'step'} ({step.id})")
    for msg in step.messages:
        print(f"{prefix}  message[{msg.role}]: {msg.content}")
    for call in step.tool_calls:
        print(f"{prefix}  tool[{call.name}]")
    for sub in step.sub_steps:
        _print_tree(sub, indent + 2)


def main(path: str) -> None:
    data = json.loads(Path(path).read_text())
    run = from_openai_trace(data)
    print(run.json(indent=2))
    print("\nTree:")
    for step in run.steps:
        _print_tree(step, 2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m agent_log_ontology <path>")
        raise SystemExit(1)
    main(sys.argv[1])
