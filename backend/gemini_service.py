"""
Gemini API integration for AI-powered scam analysis.
Uses Google's Generative AI SDK to analyze suspicious content.
"""

import os
import json
import re
from typing import Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# ── Configuration ──────────────────────────────────────────────

GEMINI_MODEL = "gemini-1.5-flash"

SYSTEM_PROMPT = """You are an expert fraud and scam analyst specializing in Indian scams and cybercrimes. 
Your job is to analyze suspicious messages, phone numbers, UPI IDs, websites, and emails to determine if they are part of a scam.

You are deeply familiar with common Indian scam patterns including:
- UPI fraud (fake refund requests, QR code scams, collect requests)
- KYC update scams (fake bank/Paytm/PhonePe KYC messages)
- OTP theft (social engineering to steal one-time passwords)
- Fake job/work-from-home offers
- Lottery/prize scams
- Loan approval scams
- Customs/courier parcel scams
- Digital arrest scams (fake police/CBI/narcotics threats)
- Investment/trading/crypto scams
- Sextortion and blackmail schemes
- Fake customer care numbers
- SIM swap fraud
- Aadhaar/PAN card misuse threats

Analyze the given content and respond ONLY with a valid JSON object (no markdown, no code fences) in this exact format:
{
    "is_scam": true/false,
    "confidence": 0.0 to 1.0,
    "scam_type": "category name",
    "explanation": "detailed explanation of why this is or is not a scam",
    "advice": "what the person should do"
}
"""


def _configure_api():
    """Configure the Gemini API with the environment key."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True


def _parse_response(text: str) -> dict:
    """Parse Gemini response text into structured dict."""
    # Try to extract JSON from the response
    text = text.strip()

    # Remove markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        result = json.loads(text)
        return {
            "is_scam": bool(result.get("is_scam", False)),
            "confidence": float(result.get("confidence", 0.0)),
            "scam_type": str(result.get("scam_type", "unknown")),
            "explanation": str(result.get("explanation", "")),
            "advice": str(result.get("advice", "")),
            "error": None,
        }
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return {
            "is_scam": False,
            "confidence": 0.0,
            "scam_type": "unknown",
            "explanation": text[:500],
            "advice": "Could not parse AI response. Please try again.",
            "error": f"Parse error: {str(e)}",
        }


async def analyze_scam_report(
    description: str,
    identifier_type: Optional[str] = None,
    identifier_value: Optional[str] = None,
) -> dict:
    """
    Analyze a potential scam using Gemini AI.
    
    Returns:
        {
            "is_scam": bool,
            "confidence": float (0-1),
            "scam_type": str,
            "explanation": str,
            "advice": str,
            "error": str | None
        }
    """
    # Check if genai is available
    if not GENAI_AVAILABLE:
        return {
            "is_scam": False,
            "confidence": 0.0,
            "scam_type": "unknown",
            "explanation": "AI analysis unavailable — google-generativeai package not installed.",
            "advice": "Install the package: pip install google-generativeai",
            "error": "google-generativeai not installed",
        }

    # Check API key
    if not _configure_api():
        return {
            "is_scam": False,
            "confidence": 0.0,
            "scam_type": "unknown",
            "explanation": "AI analysis unavailable — no API key configured.",
            "advice": "Set the GEMINI_API_KEY environment variable to enable AI analysis.",
            "error": "No GEMINI_API_KEY set",
        }

    # Build user prompt
    user_prompt = f"Analyze the following for potential scam/fraud:\n\n"
    if identifier_type and identifier_value:
        user_prompt += f"Identifier Type: {identifier_type}\n"
        user_prompt += f"Identifier Value: {identifier_value}\n\n"
    user_prompt += f"Content/Description:\n{description}"

    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )

        response = model.generate_content(user_prompt)
        return _parse_response(response.text)

    except Exception as e:
        return {
            "is_scam": False,
            "confidence": 0.0,
            "scam_type": "unknown",
            "explanation": f"AI analysis failed: {str(e)}",
            "advice": "The AI service is temporarily unavailable. Risk score is based on pattern matching only.",
            "error": str(e),
        }
