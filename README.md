# LegalEase — AI-Powered Legal Document Generator

LegalEase is a local Streamlit + FastAPI application for generating editable legal-document drafts with Google Gemini and exporting them as TXT, DOCX, and PDF.

> Important: LegalEase generates draft legal information, not legal advice. Review generated documents with a qualified legal professional before relying on them.

## Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_generator.py
│   │   └── exporters.py
│   └── assets/
│       └── logo.png              # optional
├── frontend/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_exporters.py
├── .env.example
├── .gitignore
├── requirements.txt
└── run_backend.bat
```

## 1. Requirements

- Python 3.10 or newer
- VS Code
- A Gemini API key for real AI generation

The project uses Google's current `google-genai` Python SDK. The default model is configurable through `GEMINI_MODEL`.

## 2. VS Code setup — Windows

Open the LegalEase folder in VS Code, then open **Terminal → New Terminal**.

### Create virtual environment

```powershell
python -m venv .venv
```

### Activate it

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and set:

```env
GEMINI_API_KEY=YOUR_REAL_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
BACKEND_URL=http://127.0.0.1:8000
```

Do not commit `.env` to Git.

## 4. Run the backend

Terminal 1:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check:

- API: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## 5. Run the frontend

Terminal 2:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Open the URL Streamlit prints, normally:

```text
http://localhost:8501
```

## 6. Use the app

1. Choose a document type.
2. Enter the parties.
3. Enter terms separated by semicolons.
4. Enter the effective date.
5. Optionally upload a logo.
6. Click **Generate Document**.
7. Edit the generated text if needed.
8. Download TXT, DOCX, or PDF.

The API accepts `document_type`, `parties`, `terms`, and `dates`, matching the project specification.

## 7. Run tests

With the virtual environment activated:

```powershell
pytest -q
```

The tests do not require a Gemini API call.

## 8. If Gemini is not configured

The app can still be started and tested. If no API key is configured, the backend returns a clearly marked demo draft instead of pretending that Gemini generated it. Add a real API key to enable live generation.

## 9. Common errors

### `ModuleNotFoundError`

Run:

```powershell
pip install -r requirements.txt
```

and confirm the `.venv` terminal is active.

### PowerShell execution-policy error

Use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### Frontend says backend is unavailable

Start the backend first:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Then start Streamlit in another terminal.

### Gemini error

Check `.env`:

```env
GEMINI_API_KEY=your_actual_key
GEMINI_MODEL=gemini-2.5-flash
```

Restart the backend after changing `.env`.

## 10. API example

```http
POST /generate
Content-Type: application/json
```

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",
  "terms": "Confidential information must be protected; disclosure is limited to authorized personnel; agreement may terminate on written notice",
  "dates": "September 27, 2026"
}
```

## Architecture

```text
Streamlit
   |
   | POST /generate
   v
FastAPI
   |
   v
GeminiDocumentGenerator
   |
   v
Google Gemini API
   |
   v
Generated legal draft
   |
   +--> editable preview
   +--> TXT
   +--> DOCX
   +--> PDF
```
