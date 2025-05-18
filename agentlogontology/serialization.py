import json
from datetime import datetime
from typing import Any, Dict

from .model import Action, AgentLog, AgentRun, Event, OntologyObject


def _datetime_to_iso(dt: datetime) -> str:
    return dt.isoformat() if dt else None


def object_to_dict(obj: OntologyObject) -> Dict[str, Any]:
    return {
        "object_id": obj.object_id,
        "kind": obj.kind.value,
        "state": obj.state,
        "metadata": obj.metadata,
    }


def action_to_dict(action: Action) -> Dict[str, Any]:
    return {
        "action_id": action.action_id,
        "kind": action.kind.value,
        "target": action.target,
        "params": action.params,
        "result": action.result,
    }


def event_to_dict(event: Event) -> Dict[str, Any]:
    return {
        "timestamp": _datetime_to_iso(event.timestamp),
        "action": action_to_dict(event.action),
        "metadata": event.metadata,
    }


def run_to_dict(run: AgentRun) -> Dict[str, Any]:
    return {
        "run_id": run.run_id,
        "agent": object_to_dict(run.agent),
        "objects": [object_to_dict(o) for o in run.objects.values()],
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
