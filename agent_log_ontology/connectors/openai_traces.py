"""Connector for OpenAI agent-traces format."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..ontology.run import AgentMessage, AgentRun, AgentStep, ToolCall


def from_openai_trace(trace_json: Dict[str, Any]) -> AgentRun:
    """Convert an OpenAI agent-trace JSON dict to an :class:`AgentRun`."""

    run = AgentRun(
        id=trace_json.get("id", ""),
        start_time=_parse_time(trace_json.get("started_at")),
        end_time=_parse_time(trace_json.get("ended_at")),
    )

    for step in trace_json.get("steps", []):
        run.steps.append(_parse_step(step))

    return run


def _parse_step(step: Dict[str, Any]) -> AgentStep:
    agent_step = AgentStep(
        id=step.get("id"),
        name=step.get("type"),
        start_time=_parse_time(step.get("timestamp")),
    )
    if step.get("type") == "message":
        agent_step.messages.append(
            AgentMessage(
                id=step.get("id"),
                role=step.get("role", "assistant"),
                content=step.get("content", ""),
                timestamp=_parse_time(step.get("timestamp")),
            )
        )
    elif step.get("type") == "tool":
        agent_step.tool_calls.append(
            ToolCall(
                id=step.get("id"),
                name=step.get("tool_name"),
                input=step.get("input"),
                output=step.get("output"),
                start_time=_parse_time(step.get("timestamp")),
            )
        )
    return agent_step


def _parse_time(value: Any) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
