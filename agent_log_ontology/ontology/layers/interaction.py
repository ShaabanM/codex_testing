"""Interaction Layer - Agent communication and interfaces."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class InterfaceType(str, Enum):
    """Types of interfaces."""
    
    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"
    ENVIRONMENT = "environment"


class CommunicationProtocol(str, Enum):
    """Communication protocols."""
    
    HTTP = "http"
    WEBSOCKET = "websocket"
    GRPC = "grpc"
    MESSAGE_QUEUE = "message-queue"
    SHARED_MEMORY = "shared-memory"
    CUSTOM = "custom"


class MessageType(str, Enum):
    """Types of messages."""
    
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    COMMAND = "command"
    QUERY = "query"
    UPDATE = "update"
    ERROR = "error"
    ACKNOWLEDGMENT = "acknowledgment"


class InteractionMode(str, Enum):
    """Modes of interaction."""
    
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"
    BATCH = "batch"
    PUBLISH_SUBSCRIBE = "publish-subscribe"


# Interface Components

class Interface(BaseModel):
    """Generic interface definition."""
    
    id: str = Field(..., description="Interface identifier")
    name: str = Field(..., description="Interface name")
    type: InterfaceType = Field(..., description="Interface type")
    protocol: CommunicationProtocol = Field(..., description="Communication protocol")
    endpoint: str = Field(..., description="Interface endpoint")
    capabilities: List[str] = Field(default_factory=list, description="Interface capabilities")
    authentication_required: bool = Field(default=False, description="Whether authentication is required")
    rate_limits: Dict[str, int] = Field(default_factory=dict, description="Rate limits")
    active: bool = Field(default=True, description="Whether interface is active")
    
    class Config:
        extra = "allow"


class HumanInterface(BaseModel):
    """Interface for human interaction."""
    
    interface_id: str = Field(..., description="Base interface ID")
    interaction_modalities: List[str] = Field(..., description="Interaction modalities (text, voice, etc.)")
    language_support: List[str] = Field(default_factory=list, description="Supported languages")
    accessibility_features: List[str] = Field(default_factory=list, description="Accessibility features")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")
    session_management: Dict[str, Any] = Field(default_factory=dict, description="Session configuration")
    feedback_mechanisms: List[str] = Field(default_factory=list, description="Feedback collection methods")
    
    class Config:
        extra = "allow"


class AgentInterface(BaseModel):
    """Interface for agent-to-agent interaction."""
    
    interface_id: str = Field(..., description="Base interface ID")
    supported_agent_types: List[str] = Field(default_factory=list, description="Compatible agent types")
    negotiation_protocols: List[str] = Field(default_factory=list, description="Negotiation protocols")
    coordination_mechanisms: List[str] = Field(default_factory=list, description="Coordination methods")
    trust_model: Dict[str, Any] = Field(default_factory=dict, description="Trust model configuration")
    collaboration_modes: List[str] = Field(default_factory=list, description="Collaboration modes")
    conflict_resolution: Dict[str, Any] = Field(default_factory=dict, description="Conflict resolution rules")
    
    class Config:
        extra = "allow"


class SystemInterface(BaseModel):
    """Interface for system integration."""
    
    interface_id: str = Field(..., description="Base interface ID")
    api_version: str = Field(..., description="API version")
    supported_operations: List[str] = Field(..., description="Supported operations")
    data_formats: List[str] = Field(..., description="Supported data formats")
    security_protocols: List[str] = Field(default_factory=list, description="Security protocols")
    transaction_support: bool = Field(default=False, description="Whether transactions are supported")
    idempotency_keys: bool = Field(default=False, description="Whether idempotency is supported")
    
    class Config:
        extra = "allow"


class EnvironmentInterface(BaseModel):
    """Interface for environment interaction."""
    
    interface_id: str = Field(..., description="Base interface ID")
    sensor_types: List[str] = Field(..., description="Available sensors")
    actuator_types: List[str] = Field(default_factory=list, description="Available actuators")
    environment_model: Dict[str, Any] = Field(default_factory=dict, description="Environment model")
    physical_constraints: Dict[str, Any] = Field(default_factory=dict, description="Physical constraints")
    safety_protocols: List[str] = Field(default_factory=list, description="Safety protocols")
    simulation_support: bool = Field(default=False, description="Whether simulation is supported")
    
    class Config:
        extra = "allow"


# Communication Components

class Message(BaseModel):
    """Generic message structure."""
    
    id: str = Field(..., description="Message identifier")
    type: MessageType = Field(..., description="Message type")
    sender_id: str = Field(..., description="Sender identifier")
    recipient_id: str = Field(..., description="Recipient identifier")
    interface_id: str = Field(..., description="Interface used")
    content: Any = Field(..., description="Message content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Message metadata")
    timestamp: datetime = Field(..., description="Message timestamp")
    correlation_id: Optional[str] = Field(None, description="Correlation ID for tracking")
    reply_to: Optional[str] = Field(None, description="Message being replied to")
    expires_at: Optional[datetime] = Field(None, description="Message expiration")
    
    class Config:
        extra = "allow"


class Conversation(BaseModel):
    """Conversation or interaction session."""
    
    id: str = Field(..., description="Conversation identifier")
    participant_ids: List[str] = Field(..., description="Participant identifiers")
    interface_ids: List[str] = Field(..., description="Interfaces used")
    start_time: datetime = Field(..., description="Conversation start time")
    end_time: Optional[datetime] = Field(None, description="Conversation end time")
    message_count: int = Field(default=0, description="Total messages")
    context: Dict[str, Any] = Field(default_factory=dict, description="Conversation context")
    status: str = Field(default="active", description="Conversation status")
    topic: Optional[str] = Field(None, description="Conversation topic")
    
    class Config:
        extra = "allow"


class InteractionEvent(BaseModel):
    """Significant interaction event."""
    
    id: str = Field(..., description="Event identifier")
    event_type: str = Field(..., description="Event type")
    timestamp: datetime = Field(..., description="Event timestamp")
    interface_id: str = Field(..., description="Interface where event occurred")
    participant_ids: List[str] = Field(..., description="Participants involved")
    description: str = Field(..., description="Event description")
    impact: str = Field(default="low", description="Event impact level")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    
    class Config:
        extra = "allow"


# Protocol Components

class ProtocolSpecification(BaseModel):
    """Specification for interaction protocols."""
    
    id: str = Field(..., description="Protocol identifier")
    name: str = Field(..., description="Protocol name")
    version: str = Field(..., description="Protocol version")
    steps: List[Dict[str, Any]] = Field(..., description="Protocol steps")
    message_formats: Dict[str, Any] = Field(..., description="Message format specifications")
    state_machine: Dict[str, Any] = Field(default_factory=dict, description="Protocol state machine")
    timeouts: Dict[str, float] = Field(default_factory=dict, description="Timeout configurations")
    error_handling: Dict[str, Any] = Field(default_factory=dict, description="Error handling rules")
    
    class Config:
        extra = "allow"


class InteractionPolicy(BaseModel):
    """Policy governing interactions."""
    
    id: str = Field(..., description="Policy identifier")
    name: str = Field(..., description="Policy name")
    interface_types: List[InterfaceType] = Field(..., description="Applicable interface types")
    rules: List[Dict[str, Any]] = Field(..., description="Policy rules")
    permissions: Dict[str, List[str]] = Field(default_factory=dict, description="Permissions")
    restrictions: Dict[str, List[str]] = Field(default_factory=dict, description="Restrictions")
    priority: int = Field(default=0, description="Policy priority")
    active: bool = Field(default=True, description="Whether policy is active")
    
    class Config:
        extra = "allow"


# Monitoring Components

class InteractionMetrics(BaseModel):
    """Metrics for interaction monitoring."""
    
    id: str = Field(..., description="Metrics identifier")
    interface_id: str = Field(..., description="Monitored interface")
    time_window: float = Field(..., description="Metrics window in seconds")
    message_count: int = Field(default=0, description="Messages in window")
    error_count: int = Field(default=0, description="Errors in window")
    average_latency: float = Field(default=0.0, description="Average latency in ms")
    throughput: float = Field(default=0.0, description="Messages per second")
    success_rate: float = Field(default=1.0, description="Success rate (0-1)")
    active_conversations: int = Field(default=0, description="Active conversations")
    
    class Config:
        extra = "allow"


class InteractionSnapshot(BaseModel):
    """Complete interaction state at a point in time."""
    
    timestamp: datetime = Field(..., description="Snapshot timestamp")
    active_interfaces: List[Interface] = Field(default_factory=list, description="Active interfaces")
    ongoing_conversations: List[Conversation] = Field(default_factory=list, description="Ongoing conversations")
    recent_messages: List[Message] = Field(default_factory=list, description="Recent messages")
    interface_metrics: List[InteractionMetrics] = Field(default_factory=list, description="Interface metrics")
    active_policies: List[InteractionPolicy] = Field(default_factory=list, description="Active policies")
    pending_messages: int = Field(default=0, description="Messages pending delivery")
    
    class Config:
        extra = "allow"