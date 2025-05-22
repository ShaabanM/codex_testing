"""Cognition Layer - Agent reasoning, knowledge, and metacognition."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ReasoningType(str, Enum):
    """Types of reasoning approaches."""
    
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    PROBABILISTIC = "probabilistic"
    FUZZY = "fuzzy"
    RULE_BASED = "rule-based"
    CASE_BASED = "case-based"
    MODEL_BASED = "model-based"


class DecisionStrategy(str, Enum):
    """Decision-making strategies."""
    
    OPTIMIZATION = "optimization"
    SATISFICING = "satisficing"
    HEURISTIC = "heuristic"
    MULTI_CRITERIA = "multi-criteria"
    GAME_THEORETIC = "game-theoretic"
    CONSENSUS = "consensus"


class KnowledgeType(str, Enum):
    """Types of knowledge in the system."""
    
    DECLARATIVE = "declarative"
    PROCEDURAL = "procedural"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    TACIT = "tacit"
    EXPLICIT = "explicit"


class LearningType(str, Enum):
    """Types of learning mechanisms."""
    
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    FEDERATED = "federated"
    CONTINUAL = "continual"
    ONE_SHOT = "one-shot"
    ZERO_SHOT = "zero-shot"


# Reasoning Engine Components

class Reasoning(BaseModel):
    """A reasoning process or inference."""
    
    id: str = Field(..., description="Reasoning identifier")
    type: ReasoningType = Field(..., description="Reasoning type")
    inputs: List[str] = Field(..., description="Input observation IDs")
    premises: List[Dict[str, Any]] = Field(default_factory=list, description="Reasoning premises")
    inference_steps: List[Dict[str, Any]] = Field(default_factory=list, description="Inference steps")
    conclusion: Any = Field(..., description="Reasoning conclusion")
    confidence: float = Field(default=1.0, description="Confidence in conclusion (0-1)")
    timestamp: datetime = Field(..., description="Reasoning timestamp")
    
    class Config:
        extra = "allow"


class Decision(BaseModel):
    """A decision made by the agent."""
    
    id: str = Field(..., description="Decision identifier")
    reasoning_ids: List[str] = Field(..., description="Supporting reasoning")
    strategy: DecisionStrategy = Field(..., description="Decision strategy")
    options: List[Dict[str, Any]] = Field(..., description="Considered options")
    selected_option: Dict[str, Any] = Field(..., description="Selected option")
    criteria: Dict[str, float] = Field(default_factory=dict, description="Decision criteria")
    confidence: float = Field(default=1.0, description="Decision confidence (0-1)")
    timestamp: datetime = Field(..., description="Decision timestamp")
    justification: Optional[str] = Field(None, description="Decision justification")
    
    class Config:
        extra = "allow"


class Goal(BaseModel):
    """Agent goal representation."""
    
    id: str = Field(..., description="Goal identifier")
    name: str = Field(..., description="Goal name")
    description: str = Field(..., description="Goal description")
    priority: int = Field(default=0, description="Goal priority")
    parent_goal_id: Optional[str] = Field(None, description="Parent goal")
    sub_goal_ids: List[str] = Field(default_factory=list, description="Sub-goals")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Goal constraints")
    success_criteria: Dict[str, Any] = Field(..., description="Success criteria")
    status: str = Field(default="active", description="Goal status")
    progress: float = Field(default=0.0, description="Goal progress (0-1)")
    
    class Config:
        extra = "allow"


class Plan(BaseModel):
    """Execution plan for achieving goals."""
    
    id: str = Field(..., description="Plan identifier")
    goal_ids: List[str] = Field(..., description="Target goals")
    steps: List[Dict[str, Any]] = Field(..., description="Plan steps")
    dependencies: Dict[str, List[str]] = Field(default_factory=dict, description="Step dependencies")
    resources_required: Dict[str, Any] = Field(default_factory=dict, description="Required resources")
    estimated_duration: Optional[float] = Field(None, description="Estimated duration in seconds")
    confidence: float = Field(default=1.0, description="Plan confidence (0-1)")
    alternatives: List[str] = Field(default_factory=list, description="Alternative plan IDs")
    
    class Config:
        extra = "allow"


class RiskAssessment(BaseModel):
    """Risk assessment for decisions and plans."""
    
    id: str = Field(..., description="Assessment identifier")
    target_id: str = Field(..., description="Decision or plan ID")
    target_type: str = Field(..., description="Target type (decision/plan)")
    risk_factors: List[Dict[str, Any]] = Field(..., description="Identified risks")
    probability: float = Field(..., description="Risk probability (0-1)")
    impact: float = Field(..., description="Risk impact (0-1)")
    mitigation_strategies: List[Dict[str, Any]] = Field(default_factory=list, description="Mitigation strategies")
    
    class Config:
        extra = "allow"


# Knowledge Engine Components

class KnowledgeItem(BaseModel):
    """Individual piece of knowledge."""
    
    id: str = Field(..., description="Knowledge identifier")
    type: KnowledgeType = Field(..., description="Knowledge type")
    content: Any = Field(..., description="Knowledge content")
    source: str = Field(..., description="Knowledge source")
    confidence: float = Field(default=1.0, description="Knowledge confidence (0-1)")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_accessed: datetime = Field(..., description="Last access timestamp")
    access_count: int = Field(default=0, description="Access count")
    tags: List[str] = Field(default_factory=list, description="Knowledge tags")
    
    class Config:
        extra = "allow"


class Memory(BaseModel):
    """Memory storage and retrieval."""
    
    id: str = Field(..., description="Memory identifier")
    type: str = Field(..., description="Memory type")
    content: Any = Field(..., description="Memory content")
    importance: float = Field(default=0.5, description="Memory importance (0-1)")
    timestamp: datetime = Field(..., description="Memory timestamp")
    decay_rate: float = Field(default=0.0, description="Memory decay rate")
    associations: List[str] = Field(default_factory=list, description="Associated memory IDs")
    
    class Config:
        extra = "allow"


class LearningEvent(BaseModel):
    """Learning event or update."""
    
    id: str = Field(..., description="Learning event identifier")
    type: LearningType = Field(..., description="Learning type")
    trigger: str = Field(..., description="Learning trigger")
    input_data: Any = Field(..., description="Learning input")
    learned_content: Any = Field(..., description="What was learned")
    knowledge_updates: List[str] = Field(default_factory=list, description="Updated knowledge IDs")
    performance_delta: Optional[float] = Field(None, description="Performance change")
    timestamp: datetime = Field(..., description="Learning timestamp")
    
    class Config:
        extra = "allow"


class Context(BaseModel):
    """Current context for cognition."""
    
    id: str = Field(..., description="Context identifier")
    active_goals: List[str] = Field(default_factory=list, description="Active goal IDs")
    relevant_knowledge: List[str] = Field(default_factory=list, description="Relevant knowledge IDs")
    recent_memories: List[str] = Field(default_factory=list, description="Recent memory IDs")
    environmental_factors: Dict[str, Any] = Field(default_factory=dict, description="Environmental context")
    temporal_context: Dict[str, Any] = Field(default_factory=dict, description="Time-based context")
    social_context: Dict[str, Any] = Field(default_factory=dict, description="Social context")
    
    class Config:
        extra = "allow"


# Metacognition Components

class SelfAssessment(BaseModel):
    """Self-monitoring assessment."""
    
    id: str = Field(..., description="Assessment identifier")
    target_component: str = Field(..., description="Component being assessed")
    metrics: Dict[str, float] = Field(..., description="Assessment metrics")
    performance_rating: float = Field(..., description="Performance rating (0-1)")
    identified_issues: List[Dict[str, Any]] = Field(default_factory=list, description="Identified issues")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    timestamp: datetime = Field(..., description="Assessment timestamp")
    
    class Config:
        extra = "allow"


class Uncertainty(BaseModel):
    """Uncertainty representation."""
    
    id: str = Field(..., description="Uncertainty identifier")
    source: str = Field(..., description="Uncertainty source")
    type: str = Field(..., description="Uncertainty type")
    magnitude: float = Field(..., description="Uncertainty magnitude (0-1)")
    reducible: bool = Field(..., description="Whether uncertainty is reducible")
    reduction_strategies: List[str] = Field(default_factory=list, description="Reduction strategies")
    impact_on_decisions: List[str] = Field(default_factory=list, description="Affected decision IDs")
    
    class Config:
        extra = "allow"


class ErrorEvent(BaseModel):
    """Error or failure event."""
    
    id: str = Field(..., description="Error identifier")
    error_type: str = Field(..., description="Error type")
    severity: str = Field(..., description="Error severity")
    component: str = Field(..., description="Component where error occurred")
    description: str = Field(..., description="Error description")
    root_cause: Optional[str] = Field(None, description="Root cause analysis")
    recovery_action: Optional[str] = Field(None, description="Recovery action taken")
    timestamp: datetime = Field(..., description="Error timestamp")
    
    class Config:
        extra = "allow"


class CognitionSnapshot(BaseModel):
    """Complete cognition state at a point in time."""
    
    timestamp: datetime = Field(..., description="Snapshot timestamp")
    active_reasoning: List[Reasoning] = Field(default_factory=list, description="Active reasoning processes")
    recent_decisions: List[Decision] = Field(default_factory=list, description="Recent decisions")
    current_goals: List[Goal] = Field(default_factory=list, description="Current goals")
    active_plans: List[Plan] = Field(default_factory=list, description="Active plans")
    knowledge_stats: Dict[str, int] = Field(default_factory=dict, description="Knowledge statistics")
    learning_rate: float = Field(default=0.0, description="Current learning rate")
    uncertainty_level: float = Field(default=0.0, description="Overall uncertainty (0-1)")
    
    class Config:
        extra = "allow"