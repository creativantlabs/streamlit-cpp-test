"""
Google Sheets logger for the C++ quiz app.

Reads credentials from Streamlit secrets (st.secrets["gcp_service_account"]).
Expects a sheet with two worksheets:
  - "submissions"  : one row per question submission
  - "completions"  : one row per finished quiz attempt

If the worksheets don't exist they are created automatically.
If credentials are missing the logger silently does nothing (graceful degradation).
"""
from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

_client = None
_sheet = None
_available: bool | None = None


def _is_available() -> bool:
    global _available
    if _available is not None:
        return _available
    try:
        _ = st.secrets["gcp_service_account"]
        _available = True
    except (KeyError, FileNotFoundError):
        _available = False
    return _available


def _get_sheet():
    global _client, _sheet
    if _sheet is not None:
        return _sheet
    if not _is_available():
        return None

    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=scopes,
    )
    _client = gspread.authorize(creds)
    _sheet = _client.open(st.secrets.get("sheet_name", "cpp_quiz_log"))
    return _sheet


def _get_or_create_worksheet(name: str, headers: list[str]):
    sheet = _get_sheet()
    if sheet is None:
        return None
    try:
        ws = sheet.worksheet(name)
    except Exception:
        ws = sheet.add_worksheet(title=name, rows=1000, cols=len(headers))
        ws.append_row(headers)
    return ws


_SUBMISSION_HEADERS = [
    "timestamp",
    "student_id",
    "question_id",
    "question_type",
    "topic",
    "difficulty",
    "prompt",
    "user_answer",
    "correct_answer",
    "is_correct",
]

_COMPLETION_HEADERS = [
    "timestamp",
    "student_id",
    "total_questions",
    "correct",
    "incorrect",
    "percentage",
]


def log_submission(
    student_id: str,
    question_id: int,
    question_type: str,
    topic: str,
    difficulty: int,
    prompt: str,
    user_answer: str,
    correct_answer: str,
    is_correct: bool,
) -> None:
    if not _is_available():
        return
    try:
        ws = _get_or_create_worksheet("submissions", _SUBMISSION_HEADERS)
        if ws is None:
            return
        ws.append_row(
            [
                datetime.now(timezone.utc).isoformat(),
                student_id,
                question_id,
                question_type,
                topic,
                difficulty,
                prompt[:200],
                user_answer,
                correct_answer,
                str(is_correct),
            ],
            value_input_option="RAW",
        )
    except Exception:
        pass


def log_completion(
    student_id: str,
    total: int,
    correct: int,
) -> None:
    if not _is_available():
        return
    try:
        ws = _get_or_create_worksheet("completions", _COMPLETION_HEADERS)
        if ws is None:
            return
        pct = round(correct / total * 100, 1) if total else 0.0
        ws.append_row(
            [
                datetime.now(timezone.utc).isoformat(),
                student_id,
                total,
                correct,
                total - correct,
                pct,
            ],
            value_input_option="RAW",
        )
    except Exception:
        pass
