"""Enhanced connector for OpenAI agent-traces format with full ontology support."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from ..ontology.enhanced_run import EnhancedAgentRun, EnhancedAgentStep
from ..ontology.layers import (
    AgentInstance,
    AgentType,
    AgentDomain,
    AgentCapability,
    AgentConfiguration,
    AgentMetadata,
    Observation,
    Decision,
    ActionExecution,
    ToolInvocation,
    Message,
    MessageType,
    AgentState,
    AgentStatus,
    ExecutionState,
    ExecutionPhase,
    CompleteState,
    CognitiveState,
    PerceptualState,
    PerceptionSnapshot,
    CognitionSnapshot,
    ActionSnapshot,
    InteractionSnapshot,
    OversightSnapshot,
)


def from_openai_trace_enhanced(trace_json: Dict[str, Any]) -> EnhancedAgentRun:
    """Convert an OpenAI agent-trace to enhanced AgentRun with full ontology."""
    
    # Create agent instance
    agent = _create_agent_instance(trace_json)
    
    # Create initial state
    initial_state = _create_initial_state(agent.id, trace_json)
    
    # Create the run
    run = EnhancedAgentRun(
        id=trace_json.get("id", ""),
        name=f"OpenAI Agent Run {trace_json.get('id', '')}",
        agent=agent,
        start_time=_parse_time(trace_json.get("started_at")),
        end_time=_parse_time(trace_json.get("ended_at")),
        status=_map_status(trace_json.get("status", "completed")),
        initial_state=initial_state,
    )
    
    # Process steps
    for idx, step in enumerate(trace_json.get("steps", [])):
        enhanced_step = _parse_enhanced_step(step, idx, agent.id)
        run.add_step(enhanced_step)
    
    # Calculate run metrics
    run.total_observations = len([s for s in trace_json.get("steps", []) 
                                 if s.get("type") in ["message", "tool"]])
    run.total_actions = len([s for s in trace_json.get("steps", []) 
                            if s.get("type") == "tool"])
    run.total_messages = len([s for s in trace_json.get("steps", []) 
                            if s.get("type") == "message"])
    
    # Set final state
    if run.steps:
        last_step = run.steps[-1]
        if last_step.complete_state:
            run.final_state = last_step.complete_state
    
    return run


def _create_agent_instance(trace_json: Dict[str, Any]) -> AgentInstance:
    """Create an agent instance from trace data."""
    agent_id = trace_json.get("agent_id", trace_json.get("id", "unknown"))
    
    # Infer agent type from trace content
    agent_types = [AgentType.CONVERSATIONAL]
    if any(s.get("type") == "tool" for s in trace_json.get("steps", [])):
        agent_types.append(AgentType.TASK_EXECUTION)
    
    # Create capabilities based on tools used
    capabilities = []
    tools_used = set()
    for step in trace_json.get("steps", []):
        if step.get("type") == "tool":
            tool_name = step.get("tool_name", "")
            if tool_name and tool_name not in tools_used:
                tools_used.add(tool_name)
                capabilities.append(
                    AgentCapability(
                        name=f"tool:{tool_name}",
                        version="1.0.0",
                        enabled=True
                    )
                )
    
    return AgentInstance(
        id=agent_id,
        name=f"OpenAI Agent {agent_id}",
        types=agent_types,
        domains=[AgentDomain.GENERAL],
        capabilities=capabilities,
        configuration=AgentConfiguration(
            model_id=trace_json.get("model", "gpt-4"),
            parameters=trace_json.get("config", {})
        ),
        metadata=AgentMetadata(
            created_at=_parse_time(trace_json.get("started_at")) or datetime.utcnow(),
            created_by="openai",
            version="1.0.0",
            tags=["openai", "trace-import"]
        )
    )


def _create_initial_state(agent_id: str, trace_json: Dict[str, Any]) -> CompleteState:
    """Create initial agent state."""
    timestamp = _parse_time(trace_json.get("started_at")) or datetime.utcnow()
    
    return CompleteState(
        timestamp=timestamp,
        agent_state=AgentState(
            id=f"{agent_id}-state-initial",
            agent_id=agent_id,
            status=AgentStatus.INITIALIZING,
            health_score=1.0,
            uptime=0.0,
            last_activity=timestamp,
            configuration_hash="initial"
        ),
        execution_state=ExecutionState(
            id=f"{agent_id}-exec-initial",
            phase=ExecutionPhase.IDLE,
            active_tasks=[],
            pending_actions=[]
        ),
        cognitive_state=CognitiveState(
            id=f"{agent_id}-cog-initial",
            attention_focus=[],
            working_memory=[],
            active_goals=[],
            active_plans=[]
        ),
        perceptual_state=PerceptualState(
            id=f"{agent_id}-percept-initial",
            active_sensors=[],
            sensor_readings={},
            observation_buffer=[]
        )
    )


def _parse_enhanced_step(
    step: Dict[str, Any], 
    step_number: int,
    agent_id: str
) -> EnhancedAgentStep:
    """Parse a step with full ontology mapping."""
    step_id = step.get("id", f"step-{step_number}")
    timestamp = _parse_time(step.get("timestamp")) or datetime.utcnow()
    
    enhanced_step = EnhancedAgentStep(
        id=step_id,
        name=step.get("type", "unknown"),
        step_number=step_number,
        start_time=timestamp,
        inputs={"original_step": step}
    )
    
    # Map step type to appropriate layer states
    if step.get("type") == "message":
        enhanced_step.perception_state = _create_perception_snapshot_for_message(step, agent_id)
        enhanced_step.interaction_state = _create_interaction_snapshot_for_message(step, agent_id)
        enhanced_step.outputs = {"message_content": step.get("content", "")}
        
    elif step.get("type") == "tool":
        enhanced_step.action_state = _create_action_snapshot_for_tool(step, agent_id)
        enhanced_step.outputs = {"tool_output": step.get("output")}
    
    # Create a basic complete state for the step
    enhanced_step.complete_state = _create_step_state(step, agent_id, timestamp)
    
    return enhanced_step


def _create_perception_snapshot_for_message(
    step: Dict[str, Any],
    agent_id: str
) -> PerceptionSnapshot:
    """Create perception snapshot for a message step."""
    timestamp = _parse_time(step.get("timestamp")) or datetime.utcnow()
    
    # Create observation from message
    observation = Observation(
        id=f"{step.get('id')}-obs",
        processor_id=f"{agent_id}-nlp-processor",
        signal_ids=[f"{step.get('id')}-signal"],
        type="text-message",
        content=step.get("content", ""),
        confidence=1.0,
        timestamp=timestamp,
        metadata={"role": step.get("role", "assistant")}
    )
    
    return PerceptionSnapshot(
        timestamp=timestamp,
        current_observations=[observation],
        processing_queue_size=0
    )


def _create_interaction_snapshot_for_message(
    step: Dict[str, Any],
    agent_id: str
) -> InteractionSnapshot:
    """Create interaction snapshot for a message step."""
    timestamp = _parse_time(step.get("timestamp")) or datetime.utcnow()
    
    # Create message
    message = Message(
        id=step.get("id", ""),
        type=MessageType.RESPONSE if step.get("role") == "assistant" else MessageType.REQUEST,
        sender_id=agent_id if step.get("role") == "assistant" else "user",
        recipient_id="user" if step.get("role") == "assistant" else agent_id,
        interface_id="openai-api",
        content=step.get("content", ""),
        timestamp=timestamp
    )
    
    return InteractionSnapshot(
        timestamp=timestamp,
        recent_messages=[message],
        pending_messages=0
    )


def _create_action_snapshot_for_tool(
    step: Dict[str, Any],
    agent_id: str
) -> ActionSnapshot:
    """Create action snapshot for a tool step."""
    timestamp = _parse_time(step.get("timestamp")) or datetime.utcnow()
    
    # Create tool invocation
    tool_invocation = ToolInvocation(
        id=f"{step.get('id')}-tool",
        tool_name=step.get("tool_name", ""),
        action_execution_id=step.get("id", ""),
        input_parameters=step.get("input", {}),
        output_data=step.get("output"),
        start_time=timestamp,
        end_time=timestamp  # Assuming instant execution for traces
    )
    
    # Create action execution
    action_execution = ActionExecution(
        id=step.get("id", ""),
        action_plan_id=f"{step.get('id')}-plan",
        status="completed",
        start_time=timestamp,
        end_time=timestamp,
        executor_id=agent_id,
        actual_parameters=step.get("input", {}),
        results=step.get("output")
    )
    
    return ActionSnapshot(
        timestamp=timestamp,
        executing_actions=[],
        completed_actions=[action_execution],
        action_queue_size=0
    )


def _create_step_state(
    step: Dict[str, Any],
    agent_id: str,
    timestamp: datetime
) -> CompleteState:
    """Create a complete state for a step."""
    return CompleteState(
        timestamp=timestamp,
        agent_state=AgentState(
            id=f"{agent_id}-state-{step.get('id')}",
            agent_id=agent_id,
            status=AgentStatus.ACTIVE,
            health_score=1.0,
            uptime=0.0,  # Would need to calculate from start
            last_activity=timestamp,
            configuration_hash="active"
        ),
        execution_state=ExecutionState(
            id=f"{agent_id}-exec-{step.get('id')}",
            phase=ExecutionPhase.EXECUTION if step.get("type") == "tool" else ExecutionPhase.PERCEPTION,
            active_tasks=[step.get("id", "")],
            pending_actions=[]
        ),
        cognitive_state=CognitiveState(
            id=f"{agent_id}-cog-{step.get('id')}",
            attention_focus=[step.get("type", "")],
            working_memory=[],
            active_goals=[],
            active_plans=[]
        ),
        perceptual_state=PerceptualState(
            id=f"{agent_id}-percept-{step.get('id')}",
            active_sensors=["openai-api"],
            sensor_readings={"last_input": step.get("content") or step.get("input")},
            observation_buffer=[]
        )
    )


def _map_status(status: str) -> str:
    """Map OpenAI status to our status."""
    status_map = {
        "completed": "completed",
        "failed": "failed",
        "cancelled": "cancelled",
        "running": "running",
    }
    return status_map.get(status, "unknown")


def _parse_time(value: Any) -> Optional[datetime]:
    """Parse time value."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))