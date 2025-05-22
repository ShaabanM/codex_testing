"""Pydantic models for agent runs."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class AgentMessage(BaseModel, extra="allow"):
    """A message exchanged during agent execution."""

    id: Optional[str] = None
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ToolCall(BaseModel, extra="allow"):
    """A call to an external tool."""

    id: Optional[str] = None
    name: Optional[str] = None
    input: Optional[Dict[str, object]] = None
    output: Optional[Dict[str, object]] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class AgentError(BaseModel, extra="allow"):
    """Error information."""

    message: str
    code: Optional[str] = None
    timestamp: Optional[datetime] = None


class AgentStep(BaseModel, extra="allow"):
    """A single step within a run."""

    id: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    messages: List[AgentMessage] = Field(default_factory=list)
    tool_calls: List[ToolCall] = Field(default_factory=list)
    sub_steps: List["AgentStep"] = Field(default_factory=list)
    error: Optional[AgentError] = None


class AgentRun(BaseModel, extra="allow"):
    """Top-level run of an agent."""

    id: str
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    steps: List[AgentStep] = Field(default_factory=list)
    metadata: Dict[str, object] = Field(default_factory=dict)
