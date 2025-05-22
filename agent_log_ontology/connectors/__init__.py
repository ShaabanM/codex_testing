"""Connectors for converting external agent execution logs to the AgentRun ontology."""

from .openai_traces import from_openai_trace
from .enhanced_openai_traces import from_openai_trace_enhanced

__all__ = ["from_openai_trace", "from_openai_trace_enhanced"]