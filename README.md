# Streamlit C++ Quiz (100 Questions)

Interactive Streamlit app where the user answers **100 C++ questions** from fundamentals (variables, IO, control flow) up to **classes/OOP** (constructors, access control, inheritance, virtual/override, RAII).

## Run

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)

Streamlit Community Cloud deploys directly from a GitHub repo.

### 1) Put this project on GitHub

- Create a new GitHub repository
- Commit and push these files at the repo root:
  - `app.py`
  - `questions.py`
  - `requirements.txt`

### 2) Deploy on Streamlit

- Go to Streamlit Community Cloud
- Click **New app**
- Select your GitHub repo + branch
- Set **Main file path** to `app.py`
- Click **Deploy**

### 3) Troubleshooting

- **Build fails / missing packages**: ensure everything imported by `app.py` is in `requirements.txt`
- **Python version**: optionally add a `runtime.txt` (example: `python-3.11`)
- **Secrets**: if you later add API keys, store them in Streamlit **Secrets** (not in code)

## Files

- `app.py`: Streamlit UI (progress, submit/feedback, score, review, shuffle).
- `questions.py`: The 100 questions (MCQ + short answer).

