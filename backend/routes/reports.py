"""
Report routes — submit fraud reports and look up identifiers.
"""

import json
from fastapi import APIRouter, HTTPException, Query

from schemas import ReportCreate, ReportResponse, SubmitReportResponse, LookupResponse
from database import insert_report, get_reports_by_identifier, get_all_reports, get_report_count_for_identifier
from risk_engine import calculate_risk_score
from gemini_service import analyze_scam_report

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/", response_model=SubmitReportResponse)
async def submit_report(report: ReportCreate):
    """Submit a new fraud/scam report."""

    # Get existing report count for this identifier
    report_count = get_report_count_for_identifier(report.identifier_value)

    # Run AI analysis
    ai_result = await analyze_scam_report(
        description=report.description,
        identifier_type=report.identifier_type,
        identifier_value=report.identifier_value,
    )

    # Calculate risk score
    ai_confidence = ai_result.get("confidence") if ai_result.get("is_scam") else None
    risk = calculate_risk_score(
        identifier_type=report.identifier_type,
        identifier_value=report.identifier_value,
        description=report.description,
        report_count=report_count,
        ai_confidence=ai_confidence,
    )

    # Determine category from AI or fallback
    category = ai_result.get("scam_type", "unknown")
    if category == "unknown" and ai_result.get("is_scam"):
        category = "suspected_scam"

    # Store in database
    report_id = insert_report(
        identifier_type=report.identifier_type,
        identifier_value=report.identifier_value,
        description=report.description,
        category=category,
        risk_score=risk["score"],
        risk_level=risk["level"],
        risk_factors=json.dumps(risk["factors"]),
        ai_analysis=json.dumps(ai_result),
        reporter_name=report.reporter_name,
    )

    return SubmitReportResponse(
        message="Report submitted successfully",
        report_id=report_id,
        risk=risk,
        ai_analysis=ai_result,
    )


@router.get("/", response_model=list[ReportResponse])
async def list_reports(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """List all fraud reports with pagination."""
    reports = get_all_reports(limit=limit, offset=offset)
    return reports


@router.get("/lookup/{identifier}")
async def lookup_identifier(identifier: str):
    """Look up a specific identifier to see if it has been reported."""
    reports = get_reports_by_identifier(identifier)
    report_count = len(reports)

    risk = None
    if report_count > 0:
        # Recalculate aggregate risk based on all reports
        latest = reports[0]
        risk = calculate_risk_score(
            identifier_type=latest["identifier_type"],
            identifier_value=identifier,
            description=latest["description"],
            report_count=report_count,
        )

    return LookupResponse(
        identifier=identifier,
        report_count=report_count,
        risk=risk,
        reports=reports,
    )
