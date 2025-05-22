"""Agent Identity Layer - Core agent identification and configuration."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Types of agents in the system."""
    
    CONVERSATIONAL = "conversational"
    TASK_EXECUTION = "task-execution"
    REASONING = "reasoning"
    LEARNING = "learning"
    HYBRID = "hybrid"
    GENERAL = "general"
    DELIBERATIVE = "deliberative"
    REACTIVE = "reactive"


class AgentDomain(str, Enum):
    """Domains where agents operate."""
    
    CUSTOMER_SUPPORT = "customer-support"
    FINANCE = "finance"
    SOFTWARE_DEVELOPMENT = "software-development"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    GENERAL = "general"


class AgentCapability(BaseModel):
    """Individual capability of an agent."""
    
    name: str = Field(..., description="Capability name")
    version: str = Field(default="1.0.0", description="Capability version")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Capability parameters")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Capability constraints")
    enabled: bool = Field(default=True, description="Whether capability is enabled")


class AgentConfiguration(BaseModel):
    """Agent configuration settings."""
    
    model_id: Optional[str] = Field(None, description="Model identifier")
    model_version: Optional[str] = Field(None, description="Model version")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters")
    resource_limits: Dict[str, Any] = Field(default_factory=dict, description="Resource constraints")
    security_settings: Dict[str, Any] = Field(default_factory=dict, description="Security configuration")
    feature_flags: Dict[str, bool] = Field(default_factory=dict, description="Feature toggles")


class AgentMetadata(BaseModel):
    """Agent metadata and tracking information."""
    
    created_at: datetime = Field(..., description="Agent creation timestamp")
    created_by: str = Field(..., description="Creator identifier")
    version: str = Field(..., description="Agent version")
    description: Optional[str] = Field(None, description="Agent description")
    tags: List[str] = Field(default_factory=list, description="Agent tags")
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    license: Optional[str] = Field(None, description="License information")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata")


class AgentInstance(BaseModel):
    """Core agent instance representation."""
    
    id: str = Field(..., description="Unique agent instance identifier")
    name: str = Field(..., description="Agent name")
    types: List[AgentType] = Field(..., description="Agent types")
    domains: List[AgentDomain] = Field(default_factory=list, description="Agent domains")
    capabilities: List[AgentCapability] = Field(default_factory=list, description="Agent capabilities")
    configuration: AgentConfiguration = Field(..., description="Agent configuration")
    metadata: AgentMetadata = Field(..., description="Agent metadata")
    parent_agent_id: Optional[str] = Field(None, description="Parent agent for hierarchical agents")
    child_agent_ids: List[str] = Field(default_factory=list, description="Child agents")
    
    class Config:
        extra = "allow"