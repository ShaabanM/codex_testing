"""State Layer - Agent state management."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class StateType(str, Enum):
    """Types of agent states."""
    
    AGENT = "agent"
    EXECUTION = "execution"
    COGNITIVE = "cognitive"
    PERCEPTUAL = "perceptual"
    HISTORICAL = "historical"


class AgentStatus(str, Enum):
    """Overall agent status."""
    
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    BUSY = "busy"
    PAUSED = "paused"
    ERROR = "error"
    SHUTTING_DOWN = "shutting-down"
    TERMINATED = "terminated"


class ExecutionPhase(str, Enum):
    """Execution phase of the agent."""
    
    PERCEPTION = "perception"
    REASONING = "reasoning"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    LEARNING = "learning"
    IDLE = "idle"


# Core State Components

class AgentState(BaseModel):
    """Overall agent state."""
    
    id: str = Field(..., description="State identifier")
    agent_id: str = Field(..., description="Agent instance ID")
    status: AgentStatus = Field(..., description="Agent status")
    health_score: float = Field(default=1.0, description="Agent health (0-1)")
    uptime: float = Field(..., description="Uptime in seconds")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    active_capabilities: List[str] = Field(default_factory=list, description="Active capability IDs")
    resource_allocation: Dict[str, Any] = Field(default_factory=dict, description="Resource allocation")
    configuration_hash: str = Field(..., description="Configuration hash")
    
    class Config:
        extra = "allow"


class ExecutionState(BaseModel):
    """Current execution state."""
    
    id: str = Field(..., description="State identifier")
    phase: ExecutionPhase = Field(..., description="Current execution phase")
    active_tasks: List[str] = Field(default_factory=list, description="Active task IDs")
    pending_actions: List[str] = Field(default_factory=list, description="Pending action IDs")
    execution_stack: List[Dict[str, Any]] = Field(default_factory=list, description="Execution stack")
    resource_usage: Dict[str, float] = Field(default_factory=dict, description="Current resource usage")
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    bottlenecks: List[str] = Field(default_factory=list, description="Identified bottlenecks")
    
    class Config:
        extra = "allow"


class CognitiveState(BaseModel):
    """Current cognitive state."""
    
    id: str = Field(..., description="State identifier")
    attention_focus: List[str] = Field(default_factory=list, description="Current attention targets")
    working_memory: List[str] = Field(default_factory=list, description="Working memory items")
    active_goals: List[str] = Field(default_factory=list, description="Active goal IDs")
    active_plans: List[str] = Field(default_factory=list, description="Active plan IDs")
    reasoning_depth: int = Field(default=0, description="Current reasoning depth")
    cognitive_load: float = Field(default=0.0, description="Cognitive load (0-1)")
    learning_enabled: bool = Field(default=True, description="Whether learning is enabled")
    exploration_rate: float = Field(default=0.1, description="Exploration vs exploitation rate")
    
    class Config:
        extra = "allow"


class PerceptualState(BaseModel):
    """Current perceptual state."""
    
    id: str = Field(..., description="State identifier")
    active_sensors: List[str] = Field(default_factory=list, description="Active sensor IDs")
    sensor_readings: Dict[str, Any] = Field(default_factory=dict, description="Latest sensor readings")
    observation_buffer: List[str] = Field(default_factory=list, description="Recent observation IDs")
    attention_filters: List[str] = Field(default_factory=list, description="Active filter IDs")
    signal_quality: Dict[str, float] = Field(default_factory=dict, description="Signal quality metrics")
    anomaly_detection_active: bool = Field(default=True, description="Whether anomaly detection is active")
    
    class Config:
        extra = "allow"


class HistoricalState(BaseModel):
    """Historical state information."""
    
    id: str = Field(..., description="State identifier")
    state_history: List[str] = Field(default_factory=list, description="Previous state IDs")
    event_log: List[Dict[str, Any]] = Field(default_factory=list, description="Event history")
    performance_history: List[Dict[str, Any]] = Field(default_factory=list, description="Performance history")
    error_history: List[str] = Field(default_factory=list, description="Error event IDs")
    learning_history: List[str] = Field(default_factory=list, description="Learning event IDs")
    checkpoint_states: List[Dict[str, Any]] = Field(default_factory=list, description="Saved checkpoints")
    
    class Config:
        extra = "allow"


# State Management Components

class StateTransition(BaseModel):
    """Transition between states."""
    
    id: str = Field(..., description="Transition identifier")
    from_state_id: str = Field(..., description="Source state")
    to_state_id: str = Field(..., description="Target state")
    trigger: str = Field(..., description="Transition trigger")
    conditions: List[Dict[str, Any]] = Field(default_factory=list, description="Transition conditions")
    timestamp: datetime = Field(..., description="Transition timestamp")
    duration: float = Field(..., description="Transition duration in seconds")
    success: bool = Field(..., description="Whether transition succeeded")
    side_effects: List[Dict[str, Any]] = Field(default_factory=list, description="Side effects")
    
    class Config:
        extra = "allow"


class StateCheckpoint(BaseModel):
    """Saved state checkpoint."""
    
    id: str = Field(..., description="Checkpoint identifier")
    timestamp: datetime = Field(..., description="Checkpoint timestamp")
    reason: str = Field(..., description="Checkpoint reason")
    state_snapshot: Dict[str, Any] = Field(..., description="Complete state snapshot")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Checkpoint metadata")
    size_bytes: int = Field(..., description="Checkpoint size")
    compression_ratio: float = Field(default=1.0, description="Compression ratio")
    
    class Config:
        extra = "allow"


class StateConstraint(BaseModel):
    """Constraint on agent states."""
    
    id: str = Field(..., description="Constraint identifier")
    name: str = Field(..., description="Constraint name")
    type: str = Field(..., description="Constraint type")
    expression: str = Field(..., description="Constraint expression")
    severity: str = Field(default="warning", description="Violation severity")
    active: bool = Field(default=True, description="Whether constraint is active")
    violation_count: int = Field(default=0, description="Violation count")
    last_violation: Optional[datetime] = Field(None, description="Last violation timestamp")
    
    class Config:
        extra = "allow"


class StateMonitor(BaseModel):
    """State monitoring configuration."""
    
    id: str = Field(..., description="Monitor identifier")
    name: str = Field(..., description="Monitor name")
    monitored_states: List[StateType] = Field(..., description="States to monitor")
    metrics: List[str] = Field(..., description="Metrics to track")
    thresholds: Dict[str, float] = Field(default_factory=dict, description="Alert thresholds")
    sampling_rate: float = Field(default=1.0, description="Sampling rate in Hz")
    alerts_enabled: bool = Field(default=True, description="Whether alerts are enabled")
    
    class Config:
        extra = "allow"


class StateAnalysis(BaseModel):
    """Analysis of state patterns."""
    
    id: str = Field(..., description="Analysis identifier")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    time_window: float = Field(..., description="Analysis window in seconds")
    state_distribution: Dict[str, float] = Field(..., description="Time spent in each state")
    transition_frequency: Dict[str, int] = Field(..., description="Transition frequencies")
    stability_score: float = Field(..., description="State stability (0-1)")
    anomalies_detected: List[Dict[str, Any]] = Field(default_factory=list, description="Detected anomalies")
    recommendations: List[str] = Field(default_factory=list, description="Optimization recommendations")
    
    class Config:
        extra = "allow"


class CompleteState(BaseModel):
    """Complete agent state across all dimensions."""
    
    timestamp: datetime = Field(..., description="State timestamp")
    agent_state: AgentState = Field(..., description="Overall agent state")
    execution_state: ExecutionState = Field(..., description="Execution state")
    cognitive_state: CognitiveState = Field(..., description="Cognitive state")
    perceptual_state: PerceptualState = Field(..., description="Perceptual state")
    historical_summary: Dict[str, Any] = Field(default_factory=dict, description="Historical summary")
    active_constraints: List[StateConstraint] = Field(default_factory=list, description="Active constraints")
    health_indicators: Dict[str, float] = Field(default_factory=dict, description="Health indicators")
    
    class Config:
        extra = "allow"