"""Enhanced Agent Run - Comprehensive agent execution model integrating all layers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .layers import (
    # Identity
    AgentInstance,
    # Perception
    PerceptionSnapshot,
    # Cognition
    CognitionSnapshot,
    # Action
    ActionSnapshot,
    # State
    CompleteState,
    # Interaction
    InteractionSnapshot,
    # Oversight
    OversightSnapshot,
)


class EnhancedAgentStep(BaseModel):
    """Enhanced agent step with full ontology support."""
    
    # Core identification
    id: str = Field(..., description="Step identifier")
    name: str = Field(..., description="Step name")
    step_number: int = Field(..., description="Step sequence number")
    parent_step_id: Optional[str] = Field(None, description="Parent step for nested steps")
    
    # Temporal information
    start_time: datetime = Field(..., description="Step start time")
    end_time: Optional[datetime] = Field(None, description="Step end time")
    duration: Optional[float] = Field(None, description="Step duration in seconds")
    
    # Layer snapshots at this step
    perception_state: Optional[PerceptionSnapshot] = Field(None, description="Perception state")
    cognition_state: Optional[CognitionSnapshot] = Field(None, description="Cognition state")
    action_state: Optional[ActionSnapshot] = Field(None, description="Action state")
    complete_state: Optional[CompleteState] = Field(None, description="Complete agent state")
    interaction_state: Optional[InteractionSnapshot] = Field(None, description="Interaction state")
    oversight_state: Optional[OversightSnapshot] = Field(None, description="Oversight state")
    
    # Step-specific data
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Step inputs")
    outputs: Dict[str, Any] = Field(default_factory=dict, description="Step outputs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Step metadata")
    
    # Nested steps
    sub_steps: List[EnhancedAgentStep] = Field(default_factory=list, description="Sub-steps")
    
    class Config:
        extra = "allow"


class EnhancedAgentRun(BaseModel):
    """Enhanced agent run with comprehensive ontology support."""
    
    # Core identification
    id: str = Field(..., description="Run identifier")
    name: str = Field(..., description="Run name")
    description: Optional[str] = Field(None, description="Run description")
    
    # Agent information
    agent: AgentInstance = Field(..., description="Agent instance")
    
    # Temporal information
    start_time: datetime = Field(..., description="Run start time")
    end_time: Optional[datetime] = Field(None, description="Run end time")
    duration: Optional[float] = Field(None, description="Run duration in seconds")
    
    # Execution status
    status: str = Field(default="running", description="Run status")
    success: Optional[bool] = Field(None, description="Whether run succeeded")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Initial conditions
    initial_state: Optional[CompleteState] = Field(None, description="Initial agent state")
    initial_goals: List[str] = Field(default_factory=list, description="Initial goal IDs")
    initial_context: Dict[str, Any] = Field(default_factory=dict, description="Initial context")
    
    # Final state
    final_state: Optional[CompleteState] = Field(None, description="Final agent state")
    achieved_goals: List[str] = Field(default_factory=list, description="Achieved goal IDs")
    final_context: Dict[str, Any] = Field(default_factory=dict, description="Final context")
    
    # Execution steps
    steps: List[EnhancedAgentStep] = Field(default_factory=list, description="Execution steps")
    
    # Aggregate metrics
    total_observations: int = Field(default=0, description="Total observations processed")
    total_decisions: int = Field(default=0, description="Total decisions made")
    total_actions: int = Field(default=0, description="Total actions executed")
    total_messages: int = Field(default=0, description="Total messages exchanged")
    total_anomalies: int = Field(default=0, description="Total anomalies detected")
    total_interventions: int = Field(default=0, description="Total interventions")
    
    # Performance summary
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    resource_usage: Dict[str, Any] = Field(default_factory=dict, description="Resource usage")
    
    # Oversight summary
    risk_events: List[str] = Field(default_factory=list, description="Risk event IDs")
    compliance_checks: List[str] = Field(default_factory=list, description="Compliance check IDs")
    human_reviews: List[str] = Field(default_factory=list, description="Human review IDs")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Run tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        extra = "allow"
    
    def add_step(self, step: EnhancedAgentStep) -> None:
        """Add a step to the run."""
        self.steps.append(step)
        
    def get_step_by_id(self, step_id: str) -> Optional[EnhancedAgentStep]:
        """Get a step by ID (searches recursively)."""
        def search_steps(steps: List[EnhancedAgentStep]) -> Optional[EnhancedAgentStep]:
            for step in steps:
                if step.id == step_id:
                    return step
                if step.sub_steps:
                    found = search_steps(step.sub_steps)
                    if found:
                        return found
            return None
        
        return search_steps(self.steps)
    
    def get_timeline(self) -> List[Dict[str, Any]]:
        """Get a timeline of all events in the run."""
        events = []
        
        def extract_events(step: EnhancedAgentStep, depth: int = 0) -> None:
            events.append({
                "timestamp": step.start_time,
                "type": "step_start",
                "step_id": step.id,
                "step_name": step.name,
                "depth": depth
            })
            
            if step.end_time:
                events.append({
                    "timestamp": step.end_time,
                    "type": "step_end",
                    "step_id": step.id,
                    "step_name": step.name,
                    "depth": depth
                })
            
            for sub_step in step.sub_steps:
                extract_events(sub_step, depth + 1)
        
        for step in self.steps:
            extract_events(step)
        
        return sorted(events, key=lambda x: x["timestamp"])
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate aggregate metrics from the run."""
        metrics = {
            "total_steps": len(self.steps),
            "total_duration": self.duration or 0,
            "average_step_duration": 0,
            "max_nesting_depth": 0,
            "success_rate": 0,
        }
        
        # Calculate average step duration
        step_durations = []
        
        def collect_durations(steps: List[EnhancedAgentStep]) -> None:
            for step in steps:
                if step.duration:
                    step_durations.append(step.duration)
                if step.sub_steps:
                    collect_durations(step.sub_steps)
        
        collect_durations(self.steps)
        
        if step_durations:
            metrics["average_step_duration"] = sum(step_durations) / len(step_durations)
        
        # Calculate max nesting depth
        def get_max_depth(steps: List[EnhancedAgentStep], current_depth: int = 0) -> int:
            if not steps:
                return current_depth
            max_depth = current_depth
            for step in steps:
                if step.sub_steps:
                    depth = get_max_depth(step.sub_steps, current_depth + 1)
                    max_depth = max(max_depth, depth)
            return max_depth
        
        metrics["max_nesting_depth"] = get_max_depth(self.steps, 1)
        
        # Add provided metrics
        metrics.update(self.performance_metrics)
        
        return metrics