
---

## ✅ Backend: `backend/README.md`

```markdown
# ⚙️ AI Leaders AGI Tracker – Backend (FastAPI + SQLite)

This backend handles the API and scraping logic for the AI Leaders Tracker app.

It:
- Serves `/api/leaders` via FastAPI
- Scrapes daily quotes from Google News via RSS + newspaper3k
- Falls back to hardcoded quotes when needed
- Stores data in a SQLite DB (or PostgreSQL for production)

---

## 🔗 Live API Endpoint
https://ai-leaders-backend.onrender.com/api/leaders

---

## 📦 Stack

- FastAPI
- SQLite (for dev) / PostgreSQL (recommended for production)
- Feedparser + Newspaper3k for article summaries

---

## 🔧 Setup Instructions

### 1. Install dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate
pip install -r requirements.txt
