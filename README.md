# 🔐 SecureDoc AI

A role-based document chatbot powered by FastAPI + Claude. Sensitive documents are completely hidden from unauthorized users — at both the UI and AI context level.

---

## Project Structure

```
securedoc/
├── backend/
│   ├── main.py          # FastAPI app, routes, chat logic
│   ├── auth.py          # JWT login, token verification, user DB
│   ├── documents.py     # Document database with role-based access
│   ├── requirements.txt
│   └── .env.example     # Copy to .env and add your API key
├── frontend/
│   └── index.html       # Single-page frontend (served by FastAPI)
├── start.sh             # One-command launcher
└── README.md
```

---

## Quick Start

### 1. Install Python 3.9+
Make sure Python is installed: `python3 --version`

### 2. Set your API key
```bash
cd backend
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-...your key...
```

### 3. Run the app
```bash
# From the securedoc/ root folder:
bash start.sh
```

Then open **http://localhost:8000** in your browser.

---

## Demo Accounts

| Username     | Password      | Role          | Access                          |
|-------------|---------------|---------------|---------------------------------|
| admin       | admin123      | Administrator | All documents                   |
| sarah.hr    | hr2024        | HR Team       | Public + salary/compensation    |
| john.doe    | employee123   | Employee      | Public documents only           |
| jane.smith  | employee123   | Employee      | Public documents only           |

---

## How Access Control Works

1. **Login** → Backend verifies credentials, returns a signed JWT token
2. **Load documents** → `/documents` endpoint filters by user role server-side
3. **Chat** → `/chat` endpoint builds Claude's system prompt using ONLY the docs the user can access
4. **Frontend** → Only shows documents returned by the server (sensitive docs are invisible)

Sensitive documents never touch the frontend or Claude's context for unauthorized users.

---

## Adding Your Own Documents

Edit `backend/documents.py`:

```python
{
    "id": 7,
    "name": "My New Document",
    "icon": "📄",
    "access": "sensitive",           # "public" or "sensitive" (for UI badge)
    "allowed_roles": ["admin"],      # who can see it: admin / hr / public
    "summary": "Short description",
    "content": """Full document text goes here...""",
}
```

---

## Adding Users

Edit `backend/auth.py` in the `USERS` dict:

```python
"new.user": {
    "password": "their-password",
    "role": "hr",              # admin / hr / public
    "display_name": "New User",
},
```

---

## Production Checklist

- [ ] Replace the `USERS` dict in `auth.py` with a real database (PostgreSQL recommended)
- [ ] Replace the `DOCUMENTS` list in `documents.py` with DB queries
- [ ] Change `SECRET_KEY` in `auth.py` to a long random string
- [ ] Use HTTPS (add a reverse proxy like Nginx)
- [ ] Store `ANTHROPIC_API_KEY` in a secrets manager, not a plain `.env`
- [ ] Add rate limiting to the `/chat` endpoint
- [ ] Consider adding pgvector + embeddings for large document sets (RAG)
