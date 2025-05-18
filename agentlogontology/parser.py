from datetime import datetime
from typing import Any, Dict, List

from .model import AgentLog, AgentRun, Event


def _parse_timestamp(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def from_openai_trace(data: Dict[str, Any]) -> AgentLog:
    """Convert OpenAI agent-traces JSON dict into AgentLog."""
    run_id = data.get("trace_id", "unknown")
    agent_name = data.get("agent_name", "agent")

    events_data: List[Dict[str, Any]] = data.get("events", [])
    events = []
    for e in events_data:
        events.append(
            Event(
                event_type=e.get("type", "unknown"),
                payload=e.get("payload", {}),
                timestamp=_parse_timestamp(e.get("timestamp")),
                metadata=e.get("metadata", {}),
            )
        )
    run = AgentRun(run_id=run_id, agent_name=agent_name, events=events)
    return AgentLog(runs=[run])
