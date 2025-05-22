"""Action Layer - Agent planning and execution."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Types of actions an agent can take."""
    
    EXTERNAL = "external"  # Actions affecting external environment
    INTERNAL = "internal"  # Actions affecting agent's internal state
    SOCIAL = "social"      # Actions involving other agents
    META = "meta"          # Actions about actions (planning, monitoring)


class ActionCategory(str, Enum):
    """Categories of actions."""
    
    COMMUNICATION = "communication"
    COMPUTATION = "computation"
    DATA_MANIPULATION = "data-manipulation"
    RESOURCE_ACCESS = "resource-access"
    TOOL_USE = "tool-use"
    DECISION_MAKING = "decision-making"
    LEARNING = "learning"
    MONITORING = "monitoring"


class ActionStatus(str, Enum):
    """Status of an action."""
    
    PLANNED = "planned"
    VALIDATED = "validated"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"


class ExecutionMode(str, Enum):
    """How an action is executed."""
    
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    CONDITIONAL = "conditional"
    ITERATIVE = "iterative"


# Action Planning Components

class ActionPlan(BaseModel):
    """Planned action with details."""
    
    id: str = Field(..., description="Action plan identifier")
    name: str = Field(..., description="Action name")
    type: ActionType = Field(..., description="Action type")
    category: ActionCategory = Field(..., description="Action category")
    description: str = Field(..., description="Action description")
    goal_id: Optional[str] = Field(None, description="Associated goal")
    plan_id: Optional[str] = Field(None, description="Parent plan")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    preconditions: List[Dict[str, Any]] = Field(default_factory=list, description="Action preconditions")
    expected_effects: List[Dict[str, Any]] = Field(default_factory=list, description="Expected effects")
    priority: int = Field(default=0, description="Action priority")
    deadline: Optional[datetime] = Field(None, description="Action deadline")
    
    class Config:
        extra = "allow"


class ActionSequence(BaseModel):
    """Sequence of actions to be executed."""
    
    id: str = Field(..., description="Sequence identifier")
    name: str = Field(..., description="Sequence name")
    action_ids: List[str] = Field(..., description="Ordered action IDs")
    execution_mode: ExecutionMode = Field(..., description="Execution mode")
    dependencies: Dict[str, List[str]] = Field(default_factory=dict, description="Action dependencies")
    branching_conditions: List[Dict[str, Any]] = Field(default_factory=list, description="Conditional branches")
    loop_conditions: List[Dict[str, Any]] = Field(default_factory=list, description="Loop conditions")
    
    class Config:
        extra = "allow"


class ActionValidation(BaseModel):
    """Validation result for an action."""
    
    id: str = Field(..., description="Validation identifier")
    action_id: str = Field(..., description="Validated action")
    timestamp: datetime = Field(..., description="Validation timestamp")
    is_valid: bool = Field(..., description="Whether action is valid")
    validation_checks: List[Dict[str, Any]] = Field(..., description="Validation checks performed")
    violations: List[str] = Field(default_factory=list, description="Validation violations")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    
    class Config:
        extra = "allow"


# Action Execution Components

class ActionExecution(BaseModel):
    """Execution record of an action."""
    
    id: str = Field(..., description="Execution identifier")
    action_plan_id: str = Field(..., description="Executed action plan")
    status: ActionStatus = Field(..., description="Execution status")
    start_time: datetime = Field(..., description="Execution start time")
    end_time: Optional[datetime] = Field(None, description="Execution end time")
    duration: Optional[float] = Field(None, description="Execution duration in seconds")
    executor_id: str = Field(..., description="Executor component ID")
    actual_parameters: Dict[str, Any] = Field(default_factory=dict, description="Actual parameters used")
    results: Any = Field(None, description="Execution results")
    side_effects: List[Dict[str, Any]] = Field(default_factory=list, description="Observed side effects")
    resource_usage: Dict[str, Any] = Field(default_factory=dict, description="Resource consumption")
    
    class Config:
        extra = "allow"


class ToolInvocation(BaseModel):
    """Tool or API invocation."""
    
    id: str = Field(..., description="Invocation identifier")
    tool_name: str = Field(..., description="Tool name")
    tool_version: Optional[str] = Field(None, description="Tool version")
    action_execution_id: str = Field(..., description="Parent action execution")
    input_parameters: Dict[str, Any] = Field(..., description="Tool input")
    output_data: Any = Field(None, description="Tool output")
    status_code: Optional[int] = Field(None, description="Status code")
    error_message: Optional[str] = Field(None, description="Error message")
    start_time: datetime = Field(..., description="Invocation start time")
    end_time: Optional[datetime] = Field(None, description="Invocation end time")
    
    class Config:
        extra = "allow"


class CommunicationAction(BaseModel):
    """Communication with external entities."""
    
    id: str = Field(..., description="Communication identifier")
    action_execution_id: str = Field(..., description="Parent action execution")
    sender_id: str = Field(..., description="Sender identifier")
    recipient_id: str = Field(..., description="Recipient identifier")
    channel: str = Field(..., description="Communication channel")
    message_type: str = Field(..., description="Message type")
    content: Any = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Communication timestamp")
    acknowledgment_required: bool = Field(default=False, description="Whether acknowledgment is required")
    acknowledgment_received: Optional[bool] = Field(None, description="Whether acknowledgment was received")
    
    class Config:
        extra = "allow"


# Action Types

class ExternalAction(BaseModel):
    """Action affecting external environment."""
    
    id: str = Field(..., description="Action identifier")
    execution_id: str = Field(..., description="Execution record ID")
    target_system: str = Field(..., description="Target system")
    operation: str = Field(..., description="Operation performed")
    environment_changes: List[Dict[str, Any]] = Field(default_factory=list, description="Environment changes")
    reversible: bool = Field(..., description="Whether action is reversible")
    reversal_action_id: Optional[str] = Field(None, description="Reversal action if reversible")
    
    class Config:
        extra = "allow"


class InternalAction(BaseModel):
    """Action affecting agent's internal state."""
    
    id: str = Field(..., description="Action identifier")
    execution_id: str = Field(..., description="Execution record ID")
    component_affected: str = Field(..., description="Internal component affected")
    state_changes: Dict[str, Any] = Field(..., description="State changes")
    configuration_updates: Dict[str, Any] = Field(default_factory=dict, description="Configuration updates")
    
    class Config:
        extra = "allow"


class SocialAction(BaseModel):
    """Action involving other agents."""
    
    id: str = Field(..., description="Action identifier")
    execution_id: str = Field(..., description="Execution record ID")
    interaction_type: str = Field(..., description="Type of interaction")
    other_agent_ids: List[str] = Field(..., description="Other agents involved")
    protocol: str = Field(..., description="Interaction protocol")
    negotiation_state: Optional[Dict[str, Any]] = Field(None, description="Negotiation state if applicable")
    outcome: Optional[str] = Field(None, description="Interaction outcome")
    
    class Config:
        extra = "allow"


class MetaAction(BaseModel):
    """Action about actions (planning, monitoring)."""
    
    id: str = Field(..., description="Action identifier")
    execution_id: str = Field(..., description="Execution record ID")
    meta_type: str = Field(..., description="Type of meta-action")
    target_actions: List[str] = Field(..., description="Actions being managed")
    adjustments_made: List[Dict[str, Any]] = Field(default_factory=list, description="Adjustments made")
    optimization_metrics: Dict[str, float] = Field(default_factory=dict, description="Optimization metrics")
    
    class Config:
        extra = "allow"


class ActionSnapshot(BaseModel):
    """Complete action state at a point in time."""
    
    timestamp: datetime = Field(..., description="Snapshot timestamp")
    planned_actions: List[ActionPlan] = Field(default_factory=list, description="Planned actions")
    executing_actions: List[ActionExecution] = Field(default_factory=list, description="Currently executing")
    completed_actions: List[ActionExecution] = Field(default_factory=list, description="Recently completed")
    failed_actions: List[ActionExecution] = Field(default_factory=list, description="Recently failed")
    action_queue_size: int = Field(default=0, description="Actions awaiting execution")
    resource_utilization: Dict[str, float] = Field(default_factory=dict, description="Resource usage")
    
    class Config:
        extra = "allow"