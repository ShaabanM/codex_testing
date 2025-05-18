from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Event:
    """Generic event in an agent execution log."""

    event_type: str
    payload: Dict[str, Any]
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRun:
    """Represents a sequence of events for one agent run."""

    run_id: str
    agent_name: str
    events: List[Event] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentLog:
    """Container for one or more agent runs."""

    runs: List[AgentRun] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
