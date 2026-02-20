"""
Database layer for Fraud Detection System.
Uses SQLite for lightweight, zero-config storage.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fraud_detection.db")


def get_connection() -> sqlite3.Connection:
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS fraud_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier_type TEXT NOT NULL CHECK(identifier_type IN ('phone', 'upi', 'website', 'email', 'other')),
            identifier_value TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT DEFAULT 'unknown',
            risk_score INTEGER DEFAULT 0,
            risk_level TEXT DEFAULT 'LOW',
            risk_factors TEXT DEFAULT '[]',
            ai_analysis TEXT DEFAULT '{}',
            reporter_name TEXT DEFAULT 'Anonymous',
            reported_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_identifier_value ON fraud_reports(identifier_value);
        CREATE INDEX IF NOT EXISTS idx_reported_at ON fraud_reports(reported_at);
        CREATE INDEX IF NOT EXISTS idx_category ON fraud_reports(category);

        CREATE TABLE IF NOT EXISTS lookup_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT NOT NULL UNIQUE,
            result_json TEXT NOT NULL,
            queried_at TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()


def insert_report(
    identifier_type: str,
    identifier_value: str,
    description: str,
    category: str = "unknown",
    risk_score: int = 0,
    risk_level: str = "LOW",
    risk_factors: str = "[]",
    ai_analysis: str = "{}",
    reporter_name: str = "Anonymous",
) -> int:
    """Insert a new fraud report and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO fraud_reports 
        (identifier_type, identifier_value, description, category, risk_score, risk_level, risk_factors, ai_analysis, reporter_name, reported_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (identifier_type, identifier_value.strip().lower(), description, category,
         risk_score, risk_level, risk_factors, ai_analysis, reporter_name, now),
    )

    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id


def get_reports_by_identifier(identifier_value: str) -> list[dict]:
    """Look up all reports for a given identifier."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM fraud_reports WHERE identifier_value = ? ORDER BY reported_at DESC",
        (identifier_value.strip().lower(),),
    )

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_all_reports(limit: int = 50, offset: int = 0) -> list[dict]:
    """Get all reports with pagination."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM fraud_reports ORDER BY reported_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_report_count_for_identifier(identifier_value: str) -> int:
    """Get how many reports exist for a given identifier."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) as cnt FROM fraud_reports WHERE identifier_value = ?",
        (identifier_value.strip().lower(),),
    )

    count = cursor.fetchone()["cnt"]
    conn.close()
    return count


def get_dashboard_stats() -> dict:
    """Get aggregated stats for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total reports
    cursor.execute("SELECT COUNT(*) as total FROM fraud_reports")
    total = cursor.fetchone()["total"]

    # Reports by category
    cursor.execute(
        "SELECT category, COUNT(*) as count FROM fraud_reports GROUP BY category ORDER BY count DESC LIMIT 10"
    )
    by_category = [dict(row) for row in cursor.fetchall()]

    # Reports by identifier type
    cursor.execute(
        "SELECT identifier_type, COUNT(*) as count FROM fraud_reports GROUP BY identifier_type ORDER BY count DESC"
    )
    by_type = [dict(row) for row in cursor.fetchall()]

    # Risk distribution
    cursor.execute(
        "SELECT risk_level, COUNT(*) as count FROM fraud_reports GROUP BY risk_level"
    )
    risk_dist = [dict(row) for row in cursor.fetchall()]

    # Recent 10 reports
    cursor.execute(
        "SELECT id, identifier_type, identifier_value, category, risk_score, risk_level, reported_at FROM fraud_reports ORDER BY reported_at DESC LIMIT 10"
    )
    recent = [dict(row) for row in cursor.fetchall()]

    # Unique identifiers flagged
    cursor.execute("SELECT COUNT(DISTINCT identifier_value) as unique_ids FROM fraud_reports")
    unique_ids = cursor.fetchone()["unique_ids"]

    # High risk count
    cursor.execute("SELECT COUNT(*) as high_risk FROM fraud_reports WHERE risk_level IN ('HIGH', 'CRITICAL')")
    high_risk = cursor.fetchone()["high_risk"]

    conn.close()

    return {
        "total_reports": total,
        "unique_identifiers": unique_ids,
        "high_risk_count": high_risk,
        "by_category": by_category,
        "by_type": by_type,
        "risk_distribution": risk_dist,
        "recent_reports": recent,
    }
