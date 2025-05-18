"""Agent Log Ontology package."""

from .ontology.run import AgentRun
from .connectors.openai_traces import from_openai_trace

__all__ = ["AgentRun", "from_openai_trace"]
