import json
from datetime import datetime
from typing import Any, Dict

from .model import AgentLog, AgentRun, Event


def _datetime_to_iso(dt: datetime) -> str:
    return dt.isoformat() if dt else None


def event_to_dict(event: Event) -> Dict[str, Any]:
    return {
        "event_type": event.event_type,
        "payload": event.payload,
        "timestamp": _datetime_to_iso(event.timestamp),
        "metadata": event.metadata,
    }


def run_to_dict(run: AgentRun) -> Dict[str, Any]:
    return {
        "run_id": run.run_id,
        "agent_name": run.agent_name,
        "events": [event_to_dict(e) for e in run.events],
        "metadata": run.metadata,
    }


def log_to_dict(log: AgentLog) -> Dict[str, Any]:
    return {
        "runs": [run_to_dict(r) for r in log.runs],
        "metadata": log.metadata,
    }


def log_to_json(log: AgentLog) -> str:
    return json.dumps(log_to_dict(log), indent=2)
