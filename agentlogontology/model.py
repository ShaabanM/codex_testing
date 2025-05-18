from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ObjectKind(Enum):
    """Enumerates high level ontology object types."""

    AGENT = "Agent"
    EVENT = "Event"
    OBSERVATION_STREAM = "ObservationStream"
    OBSERVATION = "Observation"
    PRECEPT = "Precept"
    ENVIRONMENT_CONTEXT = "EnvironmentContext"
    THOUGHT = "Thought"
    PLAN = "Plan"
    POLICY = "Policy"
    KNOWLEDGE_UNIT = "KnowledgeUnit"
    STATE_VARIABLE = "StateVariable"
    ACTION = "Action"
    EXTERNAL_ACTION = "ExternalAction"
    INTERNAL_ACTION = "InternalAction"
    ACTION_RESULT = "ActionResult"
    METRIC_SAMPLE = "MetricSample"
    RISK_SIGNAL = "RiskSignal"
    INTERVENTION_REQUEST = "InterventionRequest"
    POLICY_RULE = "PolicyRule"
    ANOMALY_DETECTOR = "AnomalyDetector"
    ESCALATION_PATH = "EscalationPath"
    HUMAN_FEEDBACK = "HumanFeedback"
    EVAL_RUN = "EvalRun"
    GOAL = "Goal"
    TASK = "Task"
    EPISODE = "Episode"
    RUN = "Run"
    MODEL_VERSION = "ModelVersion"
    AGENT_VERSION = "AgentVersion"


class ActionKind(Enum):
    """Enumerates actions that operate on ontology objects."""

    OBSERVE = "Observe"
    INGEST = "Ingest"
    PARSE = "Parse"
    CONTEXTUALIZE = "Contextualize"
    RETRIEVE = "Retrieve"
    REASON = "Reason"
    PLAN = "Plan"
    SELECT_ACTION = "SelectAction"
    EXECUTE = "Execute"
    MUTATE_STATE = "MutateState"
    WRITE_MEMORY = "WriteMemory"
    ASSESS_OUTCOME = "AssessOutcome"
    MEASURE_METRICS = "MeasureMetrics"
    DETECT_ANOMALY = "DetectAnomaly"
    FLAG_RISK = "FlagRisk"
    REQUEST_INTERVENTION = "RequestIntervention"
    ESCALATE = "Escalate"
    INTERVENE = "Intervene"
    APPROVE = "Approve"
    REJECT = "Reject"
    AMEND = "Amend"
    EVALUATE = "Evaluate"
    UPDATE_POLICY = "UpdatePolicy"
    VERSION = "Version"
    START_RUN = "StartRun"
    COMPLETE_RUN = "CompleteRun"
    REPLAY = "Replay"


@dataclass
class OntologyObject:
    """Base type for all objects in the ontology."""

    object_id: str
    kind: ObjectKind
    state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Action:
    """Represents an action performed on an object."""

    action_id: str
    kind: ActionKind
    target: Optional[str] = None  # object_id of the action target
    params: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None


@dataclass
class Event:
    """Envelope around an action with a timestamp."""

    action: Action
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRun:
    """Represents a sequence of events and objects for one run."""

    run_id: str
    agent: OntologyObject
    objects: Dict[str, OntologyObject] = field(default_factory=dict)
    events: List[Event] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_object(self, obj: OntologyObject) -> None:
        self.objects[obj.object_id] = obj

    def apply_event(self, event: Event) -> None:
        self.events.append(event)
        if event.action.target and event.action.target in self.objects:
            target_obj = self.objects[event.action.target]
            if event.action.result:
                target_obj.state.update(event.action.result)


@dataclass
class AgentLog:
    """Container for multiple runs."""

    runs: List[AgentRun] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
