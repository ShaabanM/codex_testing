"""Tests for the enhanced ontology."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from agent_log_ontology.ontology import (
    EnhancedAgentRun,
    EnhancedAgentStep,
    AgentInstance,
    AgentType,
    AgentDomain,
    AgentCapability,
    AgentConfiguration,
    AgentMetadata,
    AgentState,
    AgentStatus,
    ExecutionState,
    ExecutionPhase,
    CognitiveState,
    PerceptualState,
    CompleteState,
    PerceptionSnapshot,
    CognitionSnapshot,
    ActionSnapshot,
    InteractionSnapshot,
    OversightSnapshot,
    Observation,
    Decision,
    ActionExecution,
    Message,
    MessageType,
    Anomaly,
    AnomalyType,
    RiskLevel,
)
from agent_log_ontology.connectors import from_openai_trace_enhanced


class TestAgentIdentityLayer:
    """Test Agent Identity Layer components."""
    
    def test_agent_instance_creation(self):
        """Test creating an agent instance."""
        agent = AgentInstance(
            id="test-agent-001",
            name="Test Agent",
            types=[AgentType.CONVERSATIONAL, AgentType.TASK_EXECUTION],
            domains=[AgentDomain.CUSTOMER_SUPPORT],
            capabilities=[
                AgentCapability(
                    name="text-processing",
                    version="1.0.0",
                    enabled=True
                )
            ],
            configuration=AgentConfiguration(
                model_id="gpt-4",
                parameters={"temperature": 0.7}
            ),
            metadata=AgentMetadata(
                created_at=datetime.utcnow(),
                created_by="test",
                version="1.0.0",
                tags=["test", "example"]
            )
        )
        
        assert agent.id == "test-agent-001"
        assert AgentType.CONVERSATIONAL in agent.types
        assert len(agent.capabilities) == 1
        assert agent.configuration.model_id == "gpt-4"


class TestPerceptionLayer:
    """Test Perception Layer components."""
    
    def test_observation_creation(self):
        """Test creating an observation."""
        obs = Observation(
            id="obs-001",
            processor_id="nlp-processor",
            signal_ids=["signal-001"],
            type="text-message",
            content="Hello, world!",
            confidence=0.95,
            timestamp=datetime.utcnow()
        )
        
        assert obs.id == "obs-001"
        assert obs.type == "text-message"
        assert obs.confidence == 0.95
    
    def test_perception_snapshot(self):
        """Test creating a perception snapshot."""
        snapshot = PerceptionSnapshot(
            timestamp=datetime.utcnow(),
            current_observations=[
                Observation(
                    id="obs-001",
                    processor_id="processor-001",
                    signal_ids=["signal-001"],
                    type="text",
                    content="test",
                    timestamp=datetime.utcnow()
                )
            ],
            processing_queue_size=5
        )
        
        assert len(snapshot.current_observations) == 1
        assert snapshot.processing_queue_size == 5


class TestCognitionLayer:
    """Test Cognition Layer components."""
    
    def test_decision_creation(self):
        """Test creating a decision."""
        decision = Decision(
            id="decision-001",
            reasoning_ids=["reasoning-001"],
            strategy="optimization",
            options=[
                {"id": "opt1", "score": 0.8},
                {"id": "opt2", "score": 0.6}
            ],
            selected_option={"id": "opt1", "score": 0.8},
            confidence=0.85,
            timestamp=datetime.utcnow()
        )
        
        assert decision.id == "decision-001"
        assert decision.selected_option["id"] == "opt1"
        assert decision.confidence == 0.85


class TestActionLayer:
    """Test Action Layer components."""
    
    def test_action_execution(self):
        """Test creating an action execution."""
        execution = ActionExecution(
            id="exec-001",
            action_plan_id="plan-001",
            status="completed",
            start_time=datetime.utcnow(),
            executor_id="agent-001",
            results={"success": True}
        )
        
        assert execution.id == "exec-001"
        assert execution.status == "completed"
        assert execution.results["success"] is True


class TestStateLayer:
    """Test State Layer components."""
    
    def test_complete_state(self):
        """Test creating a complete state."""
        timestamp = datetime.utcnow()
        state = CompleteState(
            timestamp=timestamp,
            agent_state=AgentState(
                id="state-001",
                agent_id="agent-001",
                status=AgentStatus.ACTIVE,
                health_score=0.95,
                uptime=3600.0,
                last_activity=timestamp,
                configuration_hash="abc123"
            ),
            execution_state=ExecutionState(
                id="exec-state-001",
                phase=ExecutionPhase.REASONING,
                active_tasks=["task-001"]
            ),
            cognitive_state=CognitiveState(
                id="cog-state-001",
                attention_focus=["current-task"],
                active_goals=["goal-001"]
            ),
            perceptual_state=PerceptualState(
                id="percept-state-001",
                active_sensors=["text-sensor"],
                sensor_readings={"last_input": "test"}
            )
        )
        
        assert state.agent_state.status == AgentStatus.ACTIVE
        assert state.execution_state.phase == ExecutionPhase.REASONING
        assert len(state.cognitive_state.active_goals) == 1


class TestInteractionLayer:
    """Test Interaction Layer components."""
    
    def test_message_creation(self):
        """Test creating a message."""
        message = Message(
            id="msg-001",
            type=MessageType.REQUEST,
            sender_id="user-001",
            recipient_id="agent-001",
            interface_id="api-001",
            content="Hello",
            timestamp=datetime.utcnow()
        )
        
        assert message.id == "msg-001"
        assert message.type == MessageType.REQUEST
        assert message.content == "Hello"


class TestOversightLayer:
    """Test Oversight Layer components."""
    
    def test_anomaly_detection(self):
        """Test creating an anomaly."""
        anomaly = Anomaly(
            id="anomaly-001",
            type=AnomalyType.BEHAVIORAL,
            severity=RiskLevel.HIGH,
            detected_at=datetime.utcnow(),
            component="decision-engine",
            description="Unusual decision pattern detected",
            evidence=[{"metric": "decision_time", "value": 15.2, "threshold": 5.0}],
            confidence=0.92
        )
        
        assert anomaly.id == "anomaly-001"
        assert anomaly.severity == RiskLevel.HIGH
        assert anomaly.confidence == 0.92


class TestEnhancedAgentRun:
    """Test the enhanced agent run model."""
    
    def test_enhanced_run_creation(self):
        """Test creating an enhanced agent run."""
        agent = AgentInstance(
            id="agent-001",
            name="Test Agent",
            types=[AgentType.CONVERSATIONAL],
            configuration=AgentConfiguration(),
            metadata=AgentMetadata(
                created_at=datetime.utcnow(),
                created_by="test",
                version="1.0.0"
            )
        )
        
        run = EnhancedAgentRun(
            id="run-001",
            name="Test Run",
            agent=agent,
            start_time=datetime.utcnow()
        )
        
        # Add a step
        step = EnhancedAgentStep(
            id="step-001",
            name="Test Step",
            step_number=1,
            start_time=datetime.utcnow()
        )
        run.add_step(step)
        
        assert run.id == "run-001"
        assert len(run.steps) == 1
        assert run.get_step_by_id("step-001") is not None
    
    def test_enhanced_run_metrics(self):
        """Test calculating run metrics."""
        agent = AgentInstance(
            id="agent-001",
            name="Test Agent",
            types=[AgentType.CONVERSATIONAL],
            configuration=AgentConfiguration(),
            metadata=AgentMetadata(
                created_at=datetime.utcnow(),
                created_by="test",
                version="1.0.0"
            )
        )
        
        run = EnhancedAgentRun(
            id="run-001",
            name="Test Run",
            agent=agent,
            start_time=datetime.utcnow(),
            duration=100.0
        )
        
        # Add steps with durations
        for i in range(3):
            step = EnhancedAgentStep(
                id=f"step-{i}",
                name=f"Step {i}",
                step_number=i,
                start_time=datetime.utcnow(),
                duration=10.0 + i
            )
            run.add_step(step)
        
        metrics = run.calculate_metrics()
        assert metrics["total_steps"] == 3
        assert metrics["average_step_duration"] == 11.0  # (10 + 11 + 12) / 3


class TestEnhancedOpenAIConnector:
    """Test the enhanced OpenAI connector."""
    
    def test_enhanced_connector(self):
        """Test converting OpenAI trace to enhanced ontology."""
        samples_dir = Path(__file__).parent.parent / "samples"
        with open(samples_dir / "openai_example.json") as f:
            trace_data = json.load(f)
        
        # Convert to enhanced ontology
        enhanced_run = from_openai_trace_enhanced(trace_data)
        
        # Verify basic structure
        assert enhanced_run.id == "run_123"
        assert enhanced_run.agent is not None
        assert enhanced_run.agent.types[0] == AgentType.CONVERSATIONAL
        
        # Verify steps were converted
        assert len(enhanced_run.steps) > 0
        
        # Verify layer data is present
        for step in enhanced_run.steps:
            assert step.complete_state is not None
            if step.name == "message":
                assert step.perception_state is not None or step.interaction_state is not None
            elif step.name == "tool":
                assert step.action_state is not None
        
        # Verify metrics
        assert enhanced_run.total_observations > 0
        assert enhanced_run.total_messages >= 0
        assert enhanced_run.total_actions >= 0