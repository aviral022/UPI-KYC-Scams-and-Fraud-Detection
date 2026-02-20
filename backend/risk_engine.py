"""
Risk Scoring Engine for Fraud Detection.
Calculates a 0-100 risk score based on multiple factors.
"""

import re
from typing import Optional


# ── Known Scam Patterns (India-specific) ───────────────────────

SCAM_KEYWORDS = [
    "otp", "kyc", "aadhar", "aadhaar", "pan card", "lottery", "prize",
    "winner", "congratulations", "urgent", "verify", "suspend",
    "blocked", "link", "click here", "rupees", "lakhs", "crore",
    "transfer", "upi", "paytm", "phonepe", "gpay", "google pay",
    "loan approved", "credit card", "insurance", "refund", "cashback",
    "job offer", "work from home", "earn money", "investment",
    "trading", "bitcoin", "crypto", "forex", "stock tips",
    "customs", "courier", "parcel", "fedex", "police", "cbi",
    "narcotics", "arrest", "warrant", "legal action",
    "whatsapp", "telegram", "bank", "rbi", "sbi", "hdfc", "icici",
    "account", "password", "pin", "cvv", "expire",
    "free", "offer", "limited time", "act now", "immediately",
    "sextortion", "video", "compromise", "blackmail",
]

SCAM_PHONE_PREFIXES = [
    "+91 140",  # Known spam prefix
    "140",       # TRAI-tagged telemarketing
]

SUSPICIOUS_UPI_PATTERNS = [
    r".*paytm.*@.*",     # Impersonating Paytm
    r".*rbi.*@.*",       # Impersonating RBI
    r".*sbi.*@.*",       # Impersonating SBI
    r".*refund.*@.*",    # Refund scam
    r".*lucky.*@.*",     # Lottery scam
    r".*winner.*@.*",    # Prize scam
    r".*support.*@.*",   # Fake support
    r".*helpdesk.*@.*",  # Fake helpdesk
]


def _keyword_score(description: str) -> tuple[int, list[str]]:
    """Score based on scam keywords found in description."""
    description_lower = description.lower()
    found: list[str] = []

    for keyword in SCAM_KEYWORDS:
        if keyword in description_lower:
            found.append(keyword)

    if not found:
        return 0, []

    # More keywords = higher score, max 30
    score = min(len(found) * 5, 30)
    return score, [f"Contains scam keywords: {', '.join(found[:5])}{'...' if len(found) > 5 else ''}"]


def _identifier_pattern_score(identifier_type: str, identifier_value: str) -> tuple[int, list[str]]:
    """Score based on identifier pattern analysis."""
    factors: list[str] = []
    scores: list[int] = []
    value = identifier_value.strip().lower()

    if identifier_type == "phone":
        scores, factors = _check_phone(value)
    elif identifier_type == "upi":
        scores, factors = _check_upi(value)
    elif identifier_type == "website":
        scores, factors = _check_website(value)
    elif identifier_type == "email":
        scores, factors = _check_email(value)

    return min(sum(scores), 25), factors


def _check_phone(value: str) -> tuple[list[int], list[str]]:
    """Check phone number for spam indicators."""
    scores: list[int] = []
    factors: list[str] = []
    for prefix in SCAM_PHONE_PREFIXES:
        if value.startswith(prefix.lower().replace(" ", "")):
            scores.append(15)
            factors.append(f"Phone number starts with known spam prefix: {prefix}")
            break
    if value.startswith("+") and not value.startswith("+91"):
        scores.append(10)
        factors.append("International number (non-Indian)")
    return scores, factors


def _check_upi(value: str) -> tuple[list[int], list[str]]:
    """Check UPI ID for suspicious patterns."""
    scores: list[int] = []
    factors: list[str] = []
    for pattern in SUSPICIOUS_UPI_PATTERNS:
        if re.match(pattern, value):
            scores.append(15)
            factors.append("UPI ID matches suspicious pattern")
            break
    if re.match(r"^[a-z0-9]{10,}@", value):
        scores.append(5)
        factors.append("UPI ID appears randomly generated")
    return scores, factors


def _check_website(value: str) -> tuple[list[int], list[str]]:
    """Check website URL for suspicious patterns."""
    scores: list[int] = []
    factors: list[str] = []
    if not value.startswith("http"):
        value = "http://" + value
    suspicious_tlds = [".xyz", ".top", ".buzz", ".club", ".icu", ".tk", ".ml", ".ga"]
    for tld in suspicious_tlds:
        if tld in value:
            scores.append(15)
            factors.append(f"Uses suspicious domain extension: {tld}")
            break
    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl", "is.gd", "rebrand.ly"]
    for shortener in shorteners:
        if shortener in value:
            scores.append(10)
            factors.append("Uses URL shortener (often used for phishing)")
            break
    return scores, factors


def _check_email(value: str) -> tuple[list[int], list[str]]:
    """Check email for impersonation patterns."""
    scores: list[int] = []
    factors: list[str] = []
    if re.search(r"(bank|sbi|hdfc|icici|rbi|govt|gov)", value) and \
       re.search(r"@(gmail|yahoo|hotmail|outlook)", value):
        scores.append(20)
        factors.append("Email impersonates official entity using free email service")
    return scores, factors


def _report_frequency_score(report_count: int) -> tuple[int, list[str]]:
    """Score based on how many times this identifier has been reported."""
    if report_count == 0:
        return 0, []
    elif report_count == 1:
        return 5, ["Previously reported once"]
    elif report_count <= 3:
        return 15, [f"Reported {report_count} times before"]
    elif report_count <= 10:
        return 20, [f"Frequently reported ({report_count} times)"]
    else:
        return 25, [f"Heavily reported ({report_count} times) — likely confirmed scam"]


def _ai_confidence_score(ai_confidence: Optional[float]) -> tuple[int, list[str]]:
    """Score based on AI analysis confidence."""
    if ai_confidence is None:
        return 0, []

    if ai_confidence >= 0.9:
        return 20, [f"AI highly confident this is a scam ({ai_confidence:.0%})"]
    elif ai_confidence >= 0.7:
        return 15, [f"AI moderately confident this is a scam ({ai_confidence:.0%})"]
    elif ai_confidence >= 0.5:
        return 10, [f"AI suspects this may be a scam ({ai_confidence:.0%})"]
    elif ai_confidence >= 0.3:
        return 5, [f"AI sees some suspicious signals ({ai_confidence:.0%})"]
    else:
        return 0, [f"AI considers this low risk ({ai_confidence:.0%})"]


def _determine_level(score: int) -> str:
    """Map numeric score to risk level."""
    if score >= 75:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 25:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_risk_score(
    identifier_type: str,
    identifier_value: str,
    description: str,
    report_count: int = 0,
    ai_confidence: Optional[float] = None,
) -> dict:
    """
    Calculate a comprehensive risk score (0-100).
    
    Returns:
        {
            "score": int (0-100),
            "level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
            "factors": [str, ...]
        }
    """
    total_score = 0
    all_factors = []

    # Factor 1: Keyword analysis (max 30)
    kw_score, kw_factors = _keyword_score(description)
    total_score += kw_score
    all_factors.extend(kw_factors)

    # Factor 2: Identifier pattern (max 25)
    id_score, id_factors = _identifier_pattern_score(identifier_type, identifier_value)
    total_score += id_score
    all_factors.extend(id_factors)

    # Factor 3: Report frequency (max 25)
    freq_score, freq_factors = _report_frequency_score(report_count)
    total_score += freq_score
    all_factors.extend(freq_factors)

    # Factor 4: AI confidence (max 20)
    ai_score, ai_factors = _ai_confidence_score(ai_confidence)
    total_score += ai_score
    all_factors.extend(ai_factors)

    # Clamp to 0-100
    total_score = min(max(total_score, 0), 100)
    level = _determine_level(total_score)

    if not all_factors:
        all_factors.append("No significant risk factors detected")

    return {
        "score": total_score,
        "level": level,
        "factors": all_factors,
    }
