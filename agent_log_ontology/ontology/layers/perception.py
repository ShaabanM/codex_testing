"""Perception Layer - Agent input processing and observation."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class SensorType(str, Enum):
    """Types of sensors for agent perception."""
    
    TEXT_INPUT = "text-input"
    DOCUMENT_INPUT = "document-input"
    API_INPUT = "api-input"
    DATABASE_INPUT = "database-input"
    FILE_SYSTEM_INPUT = "file-system-input"
    NETWORK_INPUT = "network-input"
    ENVIRONMENT_STATE = "environment-state"
    AGENT_STATE = "agent-state"
    USER_FEEDBACK = "user-feedback"
    SYSTEM_METRICS = "system-metrics"


class SignalType(str, Enum):
    """Types of raw signals from sensors."""
    
    TEXT = "text"
    NUMERIC = "numeric"
    BINARY = "binary"
    STRUCTURED = "structured"
    UNSTRUCTURED = "unstructured"
    TIME_SERIES = "time-series"
    EVENT = "event"


class ProcessingType(str, Enum):
    """Types of signal processing."""
    
    NLP = "nlp"
    OCR = "ocr"
    PARSING = "parsing"
    FILTERING = "filtering"
    AGGREGATION = "aggregation"
    NORMALIZATION = "normalization"
    FEATURE_EXTRACTION = "feature-extraction"
    PATTERN_RECOGNITION = "pattern-recognition"


class Sensor(BaseModel):
    """Sensor that captures raw input."""
    
    id: str = Field(..., description="Sensor identifier")
    name: str = Field(..., description="Sensor name")
    type: SensorType = Field(..., description="Sensor type")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Sensor configuration")
    active: bool = Field(default=True, description="Whether sensor is active")
    sampling_rate: Optional[float] = Field(None, description="Sampling rate in Hz")
    filters: List[str] = Field(default_factory=list, description="Applied filters")
    
    class Config:
        extra = "allow"


class RawSignal(BaseModel):
    """Raw signal from a sensor."""
    
    id: str = Field(..., description="Signal identifier")
    sensor_id: str = Field(..., description="Source sensor")
    type: SignalType = Field(..., description="Signal type")
    data: Any = Field(..., description="Raw signal data")
    timestamp: datetime = Field(..., description="Signal timestamp")
    quality: float = Field(default=1.0, description="Signal quality (0-1)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Signal metadata")
    
    class Config:
        extra = "allow"


class SignalProcessor(BaseModel):
    """Processes raw signals into observations."""
    
    id: str = Field(..., description="Processor identifier")
    name: str = Field(..., description="Processor name")
    processing_types: List[ProcessingType] = Field(..., description="Processing capabilities")
    input_signal_types: List[SignalType] = Field(..., description="Accepted signal types")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Processor configuration")
    
    class Config:
        extra = "allow"


class Observation(BaseModel):
    """Processed observation from signals."""
    
    id: str = Field(..., description="Observation identifier")
    processor_id: str = Field(..., description="Source processor")
    signal_ids: List[str] = Field(..., description="Source signals")
    type: str = Field(..., description="Observation type")
    content: Any = Field(..., description="Observation content")
    confidence: float = Field(default=1.0, description="Observation confidence (0-1)")
    timestamp: datetime = Field(..., description="Observation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Observation metadata")
    
    class Config:
        extra = "allow"


class Process(BaseModel):
    """Process that generates observations."""
    
    id: str = Field(..., description="Process identifier")
    name: str = Field(..., description="Process name")
    processor_id: str = Field(..., description="Associated processor")
    input_signals: List[str] = Field(default_factory=list, description="Input signal IDs")
    output_observations: List[str] = Field(default_factory=list, description="Output observation IDs")
    sub_processes: List[Process] = Field(default_factory=list, description="Sub-processes")
    status: str = Field(default="active", description="Process status")
    
    class Config:
        extra = "allow"


class ContextFilter(BaseModel):
    """Filters observations based on context."""
    
    id: str = Field(..., description="Filter identifier")
    name: str = Field(..., description="Filter name")
    criteria: Dict[str, Any] = Field(..., description="Filter criteria")
    priority: int = Field(default=0, description="Filter priority")
    active: bool = Field(default=True, description="Whether filter is active")
    
    class Config:
        extra = "allow"


class PerceptionSnapshot(BaseModel):
    """Complete perception state at a point in time."""
    
    timestamp: datetime = Field(..., description="Snapshot timestamp")
    active_sensors: List[Sensor] = Field(default_factory=list, description="Active sensors")
    recent_signals: List[RawSignal] = Field(default_factory=list, description="Recent signals")
    current_observations: List[Observation] = Field(default_factory=list, description="Current observations")
    active_filters: List[ContextFilter] = Field(default_factory=list, description="Active filters")
    processing_queue_size: int = Field(default=0, description="Signals awaiting processing")
    
    class Config:
        extra = "allow"