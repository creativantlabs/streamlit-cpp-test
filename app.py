from __future__ import annotations

import random
import re

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from questions import Question, get_questions
from sheets_logger import is_enabled as logging_enabled, log_completion, log_submission

MOBILE_BREAKPOINT = 768
MAX_STUDENT_ID_LEN = 64
ANONYMOUS_ID = "anonymous"

DIFFICULTY_LABELS = {1: "Beginner", 2: "Easy", 3: "Intermediate", 4: "Hard", 5: "Advanced"}
TOPIC_LABELS = {
    "variables": "Variables",
    "types": "Types & Literals",
    "io": "Input / Output",
    "const": "Const",
    "operators": "Operators",
    "syntax": "Syntax",
    "strings": "Strings",
    "stl": "STL Containers",
    "control_flow": "Control Flow",
    "loops": "Loops",
    "functions": "Functions",
    "standard_library": "Standard Library",
    "arrays": "Arrays",
    "pointers": "Pointers",
    "references": "References",
    "memory": "Memory Management",
    "oop": "OOP / Classes",
    "modern_cpp": "Modern C++",
    "exceptions": "Exceptions",
    "templates": "Templates",
    "namespaces": "Namespaces",
    "libraries": "Libraries & Linking",
    "flowcharts": "Flowcharts",
}

_HIDE_CHROME_CSS = """
<style>
    [data-testid="stToolbar"] {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    .stButton > button {
        min-height: 48px; font-size: 1rem; border-radius: 10px;
        padding: 0.5rem 1rem; touch-action: manipulation;
    }
    .stRadio > div[role="radiogroup"] > label {
        padding: 0.6rem 0.4rem; min-height: 44px;
        display: flex; align-items: center; font-size: 1rem; cursor: pointer;
    }
    .stTextInput > div > div > input {
        font-size: 1rem; min-height: 44px; padding: 0.5rem;
    }
    pre {
        overflow-x: auto !important; -webkit-overflow-scrolling: touch;
        font-size: 0.85rem; max-width: 100%;
    }
    [data-testid="stMetric"] { text-align: center; padding: 0.4rem; }
    [data-testid="stMetricValue"] { font-size: 1.4rem; }
</style>
"""

_MOBILE_HIDE_SIDEBAR_CSS = """
<style>
    section[data-testid="stSidebar"],
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 0.5rem !important;
        max-width: 100% !important;
    }
    h1 { font-size: 1.5rem !important; }
    h3 { font-size: 1.1rem !important; }
    .stRadio > div[role="radiogroup"] > label {
        font-size: 0.95rem; padding: 0.5rem 0.3rem;
    }
    [data-testid="stMetricValue"] { font-size: 1.2rem; }
    pre { font-size: 0.78rem; }
</style>
"""


# ── Helpers ──────────────────────────────────────────────────────────────

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _short_answer_matches(user_answer: str, expected: str) -> bool:
    ua = _norm(user_answer)
    ex = _norm(expected)
    if not ua:
        return False
    strip_tokens = lambda t: re.sub(r"[;(){}\[\],]", "", t)
    return ua == ex or strip_tokens(ua) == strip_tokens(ex)


def _clean_student_id(raw: str) -> str:
    return re.sub(r"\s+", " ", raw.strip())[:MAX_STUDENT_ID_LEN]


def _init_state(questions: list[Question], student_id: str) -> None:
    # Drop answer widgets left over from a previous attempt so a restart starts blank.
    for key in [k for k in st.session_state if re.fullmatch(r"q\d+_(radio|text)", str(k))]:
        del st.session_state[key]
    st.session_state.quiz = {
        "order": [q.id for q in questions],
        "idx": 0,
        "answers": {},
        "started": True,
        "student_id": student_id or ANONYMOUS_ID,
        "completion_logged": False,
    }


def _get_by_id(questions: list[Question]) -> dict[int, Question]:
    return {q.id: q for q in questions}


def _render_code_snippet(code: str) -> None:
    st.code(code, language="cpp")


def _render_flowchart(dot: str) -> None:
    st.graphviz_chart(dot)


def _render_visual(kind: str, content: str) -> None:
    if kind == "dot":
        _render_flowchart(content)
    else:
        _render_code_snippet(content)


def _render_option_visuals(q: Question) -> None:
    """Show every option's diagram/code under its label (A, B, C, ...)."""
    assert q.options is not None and q.option_visuals is not None
    for label, content in zip(q.options, q.option_visuals):
        st.markdown(f"**{label}**")
        _render_visual(q.visual_kind, content)


def _topic_label(topic: str) -> str:
    return TOPIC_LABELS.get(topic, topic.replace("_", " ").title())


def _difficulty_badge(level: int) -> str:
    label = DIFFICULTY_LABELS.get(level, f"Level {level}")
    stars = "★" * level + "☆" * (5 - level)
    return f"{stars}  {label}"


def _render_settings(questions: list[Question]) -> tuple[bool, bool, list[str], tuple[int, int], str]:
    """Render ID + filter controls. Returns (shuffle, show_expl, topics, diff_range, student_id)."""
    required = logging_enabled()
    student_id = _clean_student_id(
        st.text_input(
            "Student ID" if required else "Student ID (optional)",
            max_chars=MAX_STUDENT_ID_LEN,
            key="student_id_input",
            help="Your answers are logged under this ID for instructor review." if required else None,
        )
    )
    shuffle = st.toggle("Shuffle questions", value=False)
    show_expl = st.toggle("Show explanation after submit", value=True)

    topics = sorted({q.topic for q in questions})
    selected_topics = st.multiselect(
        "Filter by topic",
        options=topics,
        default=topics,
        format_func=_topic_label,
    )
    diff_range = st.slider("Difficulty range", 1, 5, (1, 5))

    st.caption("For short-answer questions, minor whitespace and punctuation differences are tolerated.")
    return shuffle, show_expl, selected_topics, diff_range, student_id


def _start_quiz(
    questions: list[Question],
    *,
    shuffle: bool,
    selected_topics: list[str],
    diff_range: tuple[int, int],
    student_id: str,
) -> None:
    if logging_enabled() and not student_id:
        st.warning("Please enter your Student ID before starting.")
        return
    filtered = [
        q
        for q in questions
        if q.topic in selected_topics and diff_range[0] <= q.difficulty <= diff_range[1]
    ]
    if not filtered:
        st.warning("No questions match your filters.")
        return
    if shuffle:
        random.shuffle(filtered)
    _init_state(filtered, student_id)
    st.rerun()


def _detect_mobile() -> bool:
    """Use JS to read window.innerWidth once and cache in session state."""
    if "screen_width" not in st.session_state:
        width = streamlit_js_eval(js_expressions="window.innerWidth", key="screen_width_js")
        if width is not None:
            st.session_state.screen_width = int(width)
        else:
            return False  # still waiting for JS result
    return st.session_state.screen_width < MOBILE_BREAKPOINT


# ── Main ─────────────────────────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="C++ Quiz — Computation in Engineering 1",
        page_icon="💻",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(_HIDE_CHROME_CSS, unsafe_allow_html=True)

    is_mobile = _detect_mobile()

    if is_mobile:
        st.markdown(_MOBILE_HIDE_SIDEBAR_CSS, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────────────────────────
    st.title("C++ Practice and Revision Questions")
    questions = get_questions()
    st.caption(
        f"{len(questions)} questions from variable declarations to templates, "
        "pointers, namespaces, the standard library and flowcharts."
    )
    q_by_id = _get_by_id(questions)

    # ── Settings: sidebar on PC, inline expander on mobile ───────────────
    if is_mobile:
        with st.expander("Settings & Filters", expanded="quiz" not in st.session_state):
            shuffle, show_expl, selected_topics, diff_range, student_id = _render_settings(questions)
    else:
        with st.sidebar:
            st.subheader("Settings & Filters")
            shuffle, show_expl, selected_topics, diff_range, student_id = _render_settings(questions)

    # ── Start / Restart (always visible) ─────────────────────────────────
    start_label = "Restart Quiz" if "quiz" in st.session_state else "Start Quiz"
    if is_mobile:
        if st.button(start_label, type="primary", use_container_width=True):
            _start_quiz(
                questions, shuffle=shuffle, selected_topics=selected_topics,
                diff_range=diff_range, student_id=student_id,
            )
    else:
        with st.sidebar:
            st.divider()
            if st.button(start_label, type="primary", use_container_width=True):
                _start_quiz(
                questions, shuffle=shuffle, selected_topics=selected_topics,
                diff_range=diff_range, student_id=student_id,
            )

    # ── Main area ────────────────────────────────────────────────────────
    if "quiz" not in st.session_state:
        if is_mobile:
            st.info("Open **Settings & Filters** above, then press **Start Quiz**.")
        else:
            st.info("Use the **sidebar** to configure settings and press **Start Quiz**.")
        return

    quiz = st.session_state.quiz
    order: list[int] = quiz["order"]
    idx: int = quiz["idx"]
    answers: dict[int, dict] = quiz["answers"]

    total = len(order)

    # ── Finished ─────────────────────────────────────────────────────────
    if idx >= total:
        correct = sum(1 for a in answers.values() if a.get("correct") is True)
        pct = correct / total * 100 if total else 0

        if not quiz.get("completion_logged"):
            quiz["completion_logged"] = True
            log_completion(quiz["student_id"], total, correct)

        st.success("Quiz finished!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{correct} / {total}")
        col2.metric("Percentage", f"{pct:.0f}%")
        col3.metric("Incorrect", f"{total - correct}")

        with st.expander("Review all answers", expanded=False):
            for qid in order:
                q = q_by_id[qid]
                a = answers.get(qid, {})
                is_correct = a.get("correct", False)
                icon = "✅" if is_correct else "❌"
                st.markdown(
                    f"### {icon} Q{qid}. {_topic_label(q.topic)}  \n"
                    f"*{_difficulty_badge(q.difficulty)}*"
                )
                st.write(q.prompt)
                if q.code_snippet:
                    _render_code_snippet(q.code_snippet)
                if q.flowchart:
                    _render_flowchart(q.flowchart)
                if q.option_visuals and q.options:
                    _render_option_visuals(q)
                st.write(f"**Your answer:** {a.get('user_answer', '') or '—'}")
                st.write(f"**Correct answer:** {q.answer}")
                st.caption(q.explanation)
                st.divider()
        return

    # ── Current question ─────────────────────────────────────────────────
    qid = order[idx]
    q = q_by_id[qid]

    progress = idx / total
    st.progress(progress, text=f"Question {idx + 1} of {total}")

    st.markdown(
        f"### Q{idx + 1}.  {_topic_label(q.topic)}\n"
        f"*{_difficulty_badge(q.difficulty)}*"
    )
    st.write(q.prompt)

    if q.code_snippet:
        _render_code_snippet(q.code_snippet)
    if q.flowchart:
        _render_flowchart(q.flowchart)
    if q.option_visuals and q.options:
        _render_option_visuals(q)

    key_prefix = f"q{qid}"
    already = answers.get(qid)
    locked = already is not None  # the first submitted answer is final

    if q.type == "mcq":
        assert q.options is not None
        # No preselected option: Submit stays disabled until the student picks one.
        # (Widget state is dropped when leaving a question, so restore a locked answer explicitly.)
        locked_index = q.options.index(already["user_answer"]) if locked and already["user_answer"] in q.options else None
        user_answer = st.radio(
            "Select one:",
            q.options,
            index=locked_index,
            key=f"{key_prefix}_radio",
            disabled=locked,
        )
    else:
        user_answer = st.text_input(
            "Your answer:",
            value=already["user_answer"] if locked else "",
            key=f"{key_prefix}_text",
            placeholder="Type a C++ statement or snippet…",
            disabled=locked,
        )
    has_input = bool(user_answer and str(user_answer).strip())

    cols = st.columns(3)
    with cols[0]:
        back = st.button("⬅ Back", disabled=(idx == 0), use_container_width=True)
    with cols[1]:
        submit = st.button(
            "Submitted" if locked else "Submit",
            type="primary",
            use_container_width=True,
            disabled=locked or not has_input,
        )
    with cols[2]:
        next_btn = st.button("Next ➡", disabled=(qid not in answers), use_container_width=True)

    if back:
        quiz["idx"] = max(0, idx - 1)
        st.rerun()

    if submit and not locked:
        if q.type == "mcq":
            correct = user_answer == q.answer
        else:
            correct = _short_answer_matches(user_answer, q.answer)

        quiz["answers"][qid] = {"user_answer": user_answer, "correct": bool(correct)}
        log_submission(
            student_id=quiz["student_id"],
            question_id=qid,
            question_type=q.type,
            topic=q.topic,
            difficulty=q.difficulty,
            prompt=q.prompt,
            user_answer=str(user_answer),
            correct_answer=q.answer,
            is_correct=bool(correct),
        )
        st.rerun()

    if qid in answers:
        a = answers[qid]
        if a.get("correct"):
            st.success("Correct!")
        else:
            st.error("Incorrect.")
        if show_expl:
            st.markdown(f"**Answer:** `{q.answer}`")
            st.info(q.explanation)

    if next_btn:
        quiz["idx"] = idx + 1
        st.rerun()


if __name__ == "__main__":
    main()
