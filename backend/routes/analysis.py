"""
Analysis routes — quick AI-powered scam analysis without saving a report.
"""

from fastapi import APIRouter
from schemas import AnalysisRequest, AIAnalysisResult
from gemini_service import analyze_scam_report

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/", response_model=AIAnalysisResult)
async def analyze_content(request: AnalysisRequest):
    """Analyze suspicious content using AI without creating a report."""
    result = await analyze_scam_report(
        description=request.message,
        identifier_type=request.identifier_type,
        identifier_value=request.identifier_value,
    )
    return AIAnalysisResult(**result)
