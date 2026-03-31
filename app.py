from __future__ import annotations

import random
import re
from dataclasses import asdict

import streamlit as st
import streamlit.components.v1 as components

from questions import Question, get_questions

COURSE_URL = "https://www.cee.ed.tum.de/ccbe/teaching/master/computation-in-engineering-1/"
MOBILE_BREAKPOINT = 768

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
}

# ── CSS: base styles shared by both modes ────────────────────────────────
_BASE_CSS = """
<style>
    [data-testid="stToolbar"] {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    .stApp { max-width: 100vw; overflow-x: hidden; }
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }

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
    .stProgress > div { width: 100% !important; }
    [data-testid="stMetric"] { text-align: center; padding: 0.4rem; }
    [data-testid="stMetricValue"] { font-size: 1.4rem; }
</style>
"""

# ── Extra CSS injected only on mobile ────────────────────────────────────
_MOBILE_CSS = """
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

# ── JS: detect screen width once, store via query param → session state ──
_SCREEN_WIDTH_JS = """
<script>
(function() {
    const w = window.innerWidth;
    const params = new URLSearchParams(window.parent.location.search);
    const stored = params.get("_sw");
    if (stored !== String(w)) {
        params.set("_sw", w);
        window.parent.history.replaceState(null, "", "?" + params.toString());
        window.parent.location.reload();
    }
})();
</script>
"""


def _detect_mobile() -> bool:
    """Return True when the client screen is narrower than MOBILE_BREAKPOINT."""
    params = st.query_params
    sw = params.get("_sw")
    if sw is not None:
        try:
            return int(sw) < MOBILE_BREAKPOINT
        except ValueError:
            pass
    return False


def _need_width_detection() -> bool:
    return "_sw" not in st.query_params


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


def _init_state(questions: list[Question]) -> None:
    st.session_state.quiz = {
        "order": [q.id for q in questions],
        "idx": 0,
        "answers": {},
        "started": True,
    }


def _get_by_id(questions: list[Question]) -> dict[int, Question]:
    return {q.id: q for q in questions}


def _render_code_snippet(code: str) -> None:
    st.code(code, language="cpp")


def _topic_label(topic: str) -> str:
    return TOPIC_LABELS.get(topic, topic.replace("_", " ").title())


def _difficulty_badge(level: int) -> str:
    label = DIFFICULTY_LABELS.get(level, f"Level {level}")
    stars = "★" * level + "☆" * (5 - level)
    return f"{stars}  {label}"


def _render_settings(questions: list[Question]) -> tuple[bool, bool]:
    """Render quiz settings controls. Returns (shuffle, show_expl)."""
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

    if st.button("Start / Restart", type="primary", use_container_width=True):
        filtered = [
            q
            for q in questions
            if q.topic in selected_topics
            and diff_range[0] <= q.difficulty <= diff_range[1]
        ]
        if not filtered:
            st.warning("No questions match your filters.")
        else:
            if shuffle:
                random.shuffle(filtered)
            _init_state(filtered)
            st.rerun()

    return shuffle, show_expl


# ── Main ─────────────────────────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="C++ Quiz — Computation in Engineering 1",
        page_icon="💻",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Inject base CSS
    st.markdown(_BASE_CSS, unsafe_allow_html=True)

    # Detect screen width on first visit
    if _need_width_detection():
        components.html(_SCREEN_WIDTH_JS, height=0, width=0)

    is_mobile = _detect_mobile()

    if is_mobile:
        st.markdown(_MOBILE_CSS, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────────────────────────
    st.title("C++ Quiz")
    st.caption(
        f"[Computation in Engineering 1]({COURSE_URL}) — TUM School of Engineering and Design  \n"
        "150 questions from variable declarations to templates & move semantics."
    )

    questions = get_questions()
    q_by_id = _get_by_id(questions)

    # ── Settings: sidebar on desktop, inline expander on mobile ──────────
    if is_mobile:
        with st.expander("Settings & Filters", expanded="quiz" not in st.session_state):
            shuffle, show_expl = _render_settings(questions)
    else:
        with st.sidebar:
            st.subheader("Settings & Filters")
            shuffle, show_expl = _render_settings(questions)

    # ── Main area ────────────────────────────────────────────────────────
    if "quiz" not in st.session_state:
        if is_mobile:
            st.info("Open **Settings & Filters** above and press **Start / Restart** to begin.")
        else:
            st.info("Use the **sidebar** to configure settings and press **Start / Restart** to begin.")
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

    key_prefix = f"q{qid}"
    already = answers.get(qid)

    if q.type == "mcq":
        assert q.options is not None
        default_index = 0
        if already and already.get("user_answer") in q.options:
            default_index = q.options.index(already["user_answer"])
        user_choice = st.radio(
            "Select one:",
            q.options,
            index=default_index,
            key=f"{key_prefix}_radio",
        )
        user_answer = user_choice
    else:
        user_answer = st.text_input(
            "Your answer:",
            value=(already.get("user_answer", "") if already else ""),
            key=f"{key_prefix}_text",
            placeholder="Type a C++ statement or snippet…",
        )

    cols = st.columns(3)
    with cols[0]:
        back = st.button("⬅ Back", disabled=(idx == 0), use_container_width=True)
    with cols[1]:
        submit = st.button("Submit", type="primary", use_container_width=True)
    with cols[2]:
        next_btn = st.button("Next ➡", disabled=(qid not in answers), use_container_width=True)

    if back:
        quiz["idx"] = max(0, idx - 1)
        st.rerun()

    if submit:
        if q.type == "mcq":
            correct = user_answer == q.answer
        else:
            correct = _short_answer_matches(user_answer, q.answer)

        quiz["answers"][qid] = {
            "question": asdict(q),
            "user_answer": user_answer,
            "correct": bool(correct),
        }
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
