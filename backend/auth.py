import jwt
import time
from fastapi import HTTPException

SECRET_KEY = "change-this-to-a-secure-random-secret-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 8

# ── User Database ────────────────────────────────────────
# In production: replace with a real DB (PostgreSQL, etc.)
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "display_name": "Alex Admin",
    },
    "sarah.hr": {
        "password": "hr2024",
        "role": "hr",
        "display_name": "Sarah (HR)",
    },
    "john.doe": {
        "password": "employee123",
        "role": "public",
        "display_name": "John Doe",
    },
    "jane.smith": {
        "password": "employee123",
        "role": "public",
        "display_name": "Jane Smith",
    },
}


def create_token(username: str, role: str) -> str:
    payload = {
        "username": username,
        "role": role,
        "exp": time.time() + (TOKEN_EXPIRY_HOURS * 3600),
        "iat": time.time(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Please log in again.")
