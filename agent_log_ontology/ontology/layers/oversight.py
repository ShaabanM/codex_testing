"""Oversight Layer - Monitoring, anomaly detection, and human-in-the-loop control."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class AnomalyType(str, Enum):
    """Types of anomalies."""
    
    BEHAVIORAL = "behavioral"
    PERFORMANCE = "performance"
    RESOURCE = "resource"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    DATA_QUALITY = "data-quality"
    SYSTEM = "system"


class RiskLevel(str, Enum):
    """Risk levels."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class InterventionType(str, Enum):
    """Types of interventions."""
    
    HUMAN_REVIEW = "human-review"
    AUTOMATIC_CORRECTION = "automatic-correction"
    PAUSE_EXECUTION = "pause-execution"
    ROLLBACK = "rollback"
    PARAMETER_ADJUSTMENT = "parameter-adjustment"
    CAPABILITY_RESTRICTION = "capability-restriction"
    SHUTDOWN = "shutdown"


class AuditLevel(str, Enum):
    """Audit logging levels."""
    
    FULL = "full"
    DETAILED = "detailed"
    SUMMARY = "summary"
    MINIMAL = "minimal"
    NONE = "none"


# Anomaly Detection Components

class Anomaly(BaseModel):
    """Detected anomaly."""
    
    id: str = Field(..., description="Anomaly identifier")
    type: AnomalyType = Field(..., description="Anomaly type")
    severity: RiskLevel = Field(..., description="Anomaly severity")
    detected_at: datetime = Field(..., description="Detection timestamp")
    component: str = Field(..., description="Component where anomaly detected")
    description: str = Field(..., description="Anomaly description")
    evidence: List[Dict[str, Any]] = Field(..., description="Supporting evidence")
    confidence: float = Field(..., description="Detection confidence (0-1)")
    false_positive_probability: float = Field(default=0.0, description="False positive probability")
    related_anomalies: List[str] = Field(default_factory=list, description="Related anomaly IDs")
    
    class Config:
        extra = "allow"


class AnomalyDetector(BaseModel):
    """Anomaly detection configuration."""
    
    id: str = Field(..., description="Detector identifier")
    name: str = Field(..., description="Detector name")
    type: str = Field(..., description="Detection algorithm type")
    monitored_components: List[str] = Field(..., description="Components to monitor")
    detection_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Detection rules")
    thresholds: Dict[str, float] = Field(default_factory=dict, description="Detection thresholds")
    baseline: Dict[str, Any] = Field(default_factory=dict, description="Normal behavior baseline")
    sensitivity: float = Field(default=0.5, description="Detection sensitivity (0-1)")
    active: bool = Field(default=True, description="Whether detector is active")
    
    class Config:
        extra = "allow"


# Risk Assessment Components

class Risk(BaseModel):
    """Identified risk."""
    
    id: str = Field(..., description="Risk identifier")
    name: str = Field(..., description="Risk name")
    description: str = Field(..., description="Risk description")
    level: RiskLevel = Field(..., description="Risk level")
    probability: float = Field(..., description="Risk probability (0-1)")
    impact: float = Field(..., description="Risk impact (0-1)")
    risk_score: float = Field(..., description="Combined risk score (0-1)")
    affected_components: List[str] = Field(..., description="Affected components")
    mitigation_options: List[Dict[str, Any]] = Field(default_factory=list, description="Mitigation options")
    monitoring_required: bool = Field(default=True, description="Whether monitoring is required")
    
    class Config:
        extra = "allow"


class RiskAssessment(BaseModel):
    """Risk assessment results."""
    
    id: str = Field(..., description="Assessment identifier")
    timestamp: datetime = Field(..., description="Assessment timestamp")
    scope: str = Field(..., description="Assessment scope")
    identified_risks: List[Risk] = Field(..., description="Identified risks")
    overall_risk_level: RiskLevel = Field(..., description="Overall risk level")
    recommendations: List[str] = Field(..., description="Risk mitigation recommendations")
    next_assessment: Optional[datetime] = Field(None, description="Next assessment scheduled")
    
    class Config:
        extra = "allow"


# Performance Monitoring Components

class PerformanceMetric(BaseModel):
    """Performance metric definition."""
    
    id: str = Field(..., description="Metric identifier")
    name: str = Field(..., description="Metric name")
    category: str = Field(..., description="Metric category")
    value: float = Field(..., description="Current value")
    unit: str = Field(..., description="Metric unit")
    baseline: float = Field(..., description="Baseline value")
    threshold_warning: float = Field(..., description="Warning threshold")
    threshold_critical: float = Field(..., description="Critical threshold")
    trend: str = Field(default="stable", description="Metric trend")
    
    class Config:
        extra = "allow"


class PerformanceReport(BaseModel):
    """Performance monitoring report."""
    
    id: str = Field(..., description="Report identifier")
    timestamp: datetime = Field(..., description="Report timestamp")
    time_window: float = Field(..., description="Report window in seconds")
    metrics: List[PerformanceMetric] = Field(..., description="Performance metrics")
    efficiency_score: float = Field(..., description="Overall efficiency (0-1)")
    bottlenecks: List[str] = Field(default_factory=list, description="Identified bottlenecks")
    optimization_opportunities: List[str] = Field(default_factory=list, description="Optimization opportunities")
    comparison_to_baseline: Dict[str, float] = Field(default_factory=dict, description="Baseline comparison")
    
    class Config:
        extra = "allow"


# Audit and Compliance Components

class AuditEvent(BaseModel):
    """Audit log event."""
    
    id: str = Field(..., description="Event identifier")
    timestamp: datetime = Field(..., description="Event timestamp")
    event_type: str = Field(..., description="Event type")
    actor_id: str = Field(..., description="Actor identifier")
    action: str = Field(..., description="Action performed")
    target: str = Field(..., description="Action target")
    result: str = Field(..., description="Action result")
    details: Dict[str, Any] = Field(default_factory=dict, description="Event details")
    compliance_tags: List[str] = Field(default_factory=list, description="Compliance tags")
    immutable: bool = Field(default=True, description="Whether event is immutable")
    
    class Config:
        extra = "allow"


class ComplianceCheck(BaseModel):
    """Compliance verification."""
    
    id: str = Field(..., description="Check identifier")
    name: str = Field(..., description="Check name")
    regulation: str = Field(..., description="Regulation or policy")
    timestamp: datetime = Field(..., description="Check timestamp")
    passed: bool = Field(..., description="Whether check passed")
    violations: List[Dict[str, Any]] = Field(default_factory=list, description="Found violations")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    remediation_required: bool = Field(default=False, description="Whether remediation needed")
    
    class Config:
        extra = "allow"


# Human-in-the-Loop Components

class HumanReviewRequest(BaseModel):
    """Request for human review."""
    
    id: str = Field(..., description="Request identifier")
    timestamp: datetime = Field(..., description="Request timestamp")
    urgency: RiskLevel = Field(..., description="Request urgency")
    reason: str = Field(..., description="Review reason")
    context: Dict[str, Any] = Field(..., description="Review context")
    decision_options: List[Dict[str, Any]] = Field(..., description="Available decisions")
    timeout: Optional[float] = Field(None, description="Timeout in seconds")
    assigned_to: Optional[str] = Field(None, description="Assigned reviewer")
    status: str = Field(default="pending", description="Review status")
    
    class Config:
        extra = "allow"


class HumanIntervention(BaseModel):
    """Human intervention record."""
    
    id: str = Field(..., description="Intervention identifier")
    request_id: str = Field(..., description="Review request ID")
    reviewer_id: str = Field(..., description="Reviewer identifier")
    timestamp: datetime = Field(..., description="Intervention timestamp")
    decision: str = Field(..., description="Intervention decision")
    rationale: str = Field(..., description="Decision rationale")
    actions_taken: List[Dict[str, Any]] = Field(..., description="Actions taken")
    override_automated: bool = Field(default=False, description="Whether automated action was overridden")
    feedback_to_system: Dict[str, Any] = Field(default_factory=dict, description="Feedback for learning")
    
    class Config:
        extra = "allow"


class EscalationPolicy(BaseModel):
    """Policy for escalating issues."""
    
    id: str = Field(..., description="Policy identifier")
    name: str = Field(..., description="Policy name")
    triggers: List[Dict[str, Any]] = Field(..., description="Escalation triggers")
    escalation_levels: List[Dict[str, Any]] = Field(..., description="Escalation hierarchy")
    notification_channels: List[str] = Field(..., description="Notification methods")
    auto_escalate_timeout: float = Field(..., description="Auto-escalation timeout")
    active: bool = Field(default=True, description="Whether policy is active")
    
    class Config:
        extra = "allow"


# Intervention Components

class InterventionAction(BaseModel):
    """Automated intervention action."""
    
    id: str = Field(..., description="Action identifier")
    type: InterventionType = Field(..., description="Intervention type")
    trigger: str = Field(..., description="Intervention trigger")
    timestamp: datetime = Field(..., description="Intervention timestamp")
    target_component: str = Field(..., description="Target component")
    parameters: Dict[str, Any] = Field(..., description="Intervention parameters")
    expected_outcome: str = Field(..., description="Expected outcome")
    actual_outcome: Optional[str] = Field(None, description="Actual outcome")
    success: Optional[bool] = Field(None, description="Whether intervention succeeded")
    rollback_available: bool = Field(default=False, description="Whether rollback is available")
    
    class Config:
        extra = "allow"


# Oversight Summary

class OversightSnapshot(BaseModel):
    """Complete oversight state at a point in time."""
    
    timestamp: datetime = Field(..., description="Snapshot timestamp")
    active_anomalies: List[Anomaly] = Field(default_factory=list, description="Active anomalies")
    current_risks: List[Risk] = Field(default_factory=list, description="Current risks")
    performance_summary: Dict[str, float] = Field(default_factory=dict, description="Performance summary")
    pending_reviews: List[HumanReviewRequest] = Field(default_factory=list, description="Pending reviews")
    recent_interventions: List[InterventionAction] = Field(default_factory=list, description="Recent interventions")
    compliance_status: Dict[str, bool] = Field(default_factory=dict, description="Compliance status")
    oversight_health: float = Field(..., description="Oversight system health (0-1)")
    recommendations: List[str] = Field(default_factory=list, description="Oversight recommendations")
    
    class Config:
        extra = "allow"