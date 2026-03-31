# Streamlit C++ Quiz (150 Questions)

Interactive Streamlit app where students answer **150 C++ questions** from fundamentals (variables, IO, control flow) up to **classes/OOP**, inheritance, templates, and modern C++.

Submissions are optionally logged to **Google Sheets** for instructor review.

## Run locally

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)

### 1) Push to GitHub

Commit and push these files:

- `app.py`
- `questions.py`
- `sheets_logger.py`
- `requirements.txt`
- `.streamlit/config.toml`

### 2) Deploy on Streamlit

- Go to [Streamlit Community Cloud](https://share.streamlit.io)
- Click **New app** → select your GitHub repo + branch
- Set **Main file path** to `app.py`
- Click **Deploy**

## Google Sheets logging (optional)

Logging is optional. If no credentials are configured, the app works normally without logging.

### Setup steps

1. **Create a Google Cloud service account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/) → IAM & Admin → Service Accounts
   - Create a service account and download the JSON key file

2. **Enable APIs**
   - Enable **Google Sheets API** and **Google Drive API** for your project

3. **Create a Google Sheet**
   - Create a new Google Sheet named `cpp_quiz_log` (or any name you like)
   - Share it with the service account email (the `client_email` in the JSON key), giving **Editor** access

4. **Add secrets to Streamlit Cloud**
   - In your Streamlit Cloud app settings → **Secrets**, paste:

```toml
sheet_name = "cpp_quiz_log"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-sa@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

5. **For local testing**, create `.streamlit/secrets.toml` with the same content (do NOT commit this file)

### What gets logged

**`submissions` worksheet** — one row per answer:

| timestamp | student_id | question_id | question_type | topic | difficulty | prompt | user_answer | correct_answer | is_correct |
|---|---|---|---|---|---|---|---|---|---|

**`completions` worksheet** — one row per finished quiz:

| timestamp | student_id | total_questions | correct | incorrect | percentage |
|---|---|---|---|---|---|

## Files

- `app.py` — Streamlit UI (progress, submit/feedback, score, review, shuffle)
- `questions.py` — The 150 questions (MCQ + short answer)
- `sheets_logger.py` — Google Sheets logging (graceful degradation if unconfigured)
- `.streamlit/config.toml` — Streamlit theme & settings
