from datetime import datetime
from typing import Any, Dict, List

from .model import (
    Action,
    ActionKind,
    AgentLog,
    AgentRun,
    Event,
    ObjectKind,
    OntologyObject,
)


def _parse_timestamp(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _map_event_type(event_type: str) -> ActionKind:
    mapping = {
        "user_message": ActionKind.OBSERVE,
        "assistant_response": ActionKind.EXECUTE,
        "tool_call": ActionKind.EXECUTE,
        "tool_result": ActionKind.OBSERVE,
    }
    return mapping.get(event_type, ActionKind.EXECUTE)


def _map_object_kind(event_type: str) -> ObjectKind:
    mapping = {
        "user_message": ObjectKind.OBSERVATION,
        "assistant_response": ObjectKind.THOUGHT,
        "tool_call": ObjectKind.EXTERNAL_ACTION,
        "tool_result": ObjectKind.ACTION_RESULT,
    }
    return mapping.get(event_type, ObjectKind.EVENT)


def from_openai_trace(data: Dict[str, Any]) -> AgentLog:
    """Convert OpenAI agent-traces JSON dict into AgentLog."""
    run_id = data.get("trace_id", "unknown")
    agent_name = data.get("agent_name", "agent")

    agent_obj = OntologyObject(object_id=agent_name, kind=ObjectKind.AGENT)
    run = AgentRun(run_id=run_id, agent=agent_obj)
    run.add_object(agent_obj)

    events_data: List[Dict[str, Any]] = data.get("events", [])
    for idx, e in enumerate(events_data):
        e_type = e.get("type", "unknown")
        obj_kind = _map_object_kind(e_type)
        obj_id = e.get("id", f"obj-{idx}")
        obj_state = e.get("payload", {})
        obj = OntologyObject(object_id=obj_id, kind=obj_kind, state=obj_state)
        run.add_object(obj)

        action_kind = _map_event_type(e_type)
        action = Action(
            action_id=f"act-{idx}",
            kind=action_kind,
            target=obj_id,
            params=e.get("payload", {}),
            result=e.get("payload", {}),
        )
        event = Event(
            action=action,
            timestamp=_parse_timestamp(e.get("timestamp")),
            metadata=e.get("metadata", {}),
        )
        run.apply_event(event)
    return AgentLog(runs=[run])
