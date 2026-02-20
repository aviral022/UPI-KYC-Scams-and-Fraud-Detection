"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Request Models ──────────────────────────────────────────────

class ReportCreate(BaseModel):
    identifier_type: str = Field(
        ..., description="Type of identifier", 
        pattern="^(phone|upi|website|email|other)$"
    )
    identifier_value: str = Field(..., min_length=2, max_length=500, description="The scam identifier (phone number, UPI ID, URL, etc.)")
    description: str = Field(..., min_length=10, max_length=5000, description="Description of the scam")
    reporter_name: str = Field(default="Anonymous", max_length=100, description="Name of the reporter")


class AnalysisRequest(BaseModel):
    message: str = Field(..., min_length=5, max_length=5000, description="Suspicious message or content to analyze")
    identifier_type: Optional[str] = Field(default=None, description="Optional identifier type for context")
    identifier_value: Optional[str] = Field(default=None, description="Optional identifier value for context")


class LookupRequest(BaseModel):
    identifier: str = Field(..., min_length=2, max_length=500, description="Identifier to look up")


# ── Response Models ─────────────────────────────────────────────

class RiskResult(BaseModel):
    score: int = Field(..., ge=0, le=100)
    level: str
    factors: list[str] = []


class AIAnalysisResult(BaseModel):
    is_scam: bool = False
    confidence: float = 0.0
    scam_type: str = "unknown"
    explanation: str = ""
    advice: str = ""
    error: Optional[str] = None


class ReportResponse(BaseModel):
    id: int
    identifier_type: str
    identifier_value: str
    description: str
    category: str
    risk_score: int
    risk_level: str
    risk_factors: str
    ai_analysis: str
    reporter_name: str
    reported_at: str


class SubmitReportResponse(BaseModel):
    message: str
    report_id: int
    risk: RiskResult
    ai_analysis: AIAnalysisResult


class LookupResponse(BaseModel):
    identifier: str
    report_count: int
    risk: Optional[RiskResult] = None
    reports: list[ReportResponse] = []


class DashboardStats(BaseModel):
    total_reports: int = 0
    unique_identifiers: int = 0
    high_risk_count: int = 0
    by_category: list[dict] = []
    by_type: list[dict] = []
    risk_distribution: list[dict] = []
    recent_reports: list[dict] = []
