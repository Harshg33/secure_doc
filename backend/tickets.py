import csv
import re
from datetime import datetime
from pathlib import Path

TICKETS_FILE = Path(__file__).parent / "tickets.csv"
FIELDNAMES = ["id", "timestamp", "username", "role", "question", "answer", "sources", "thumbs_up"]

# Fuzzy threshold — only used if no exact match found
FUZZY_THRESHOLD = 0.40


# ── File helpers ──────────────────────────────────────────

def _ensure_file():
    if not TICKETS_FILE.exists():
        with open(TICKETS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def _next_id() -> int:
    rows = load_all_tickets()
    return max((int(r["id"]) for r in rows), default=0) + 1


def load_all_tickets() -> list[dict]:
    _ensure_file()
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_ticket(username: str, role: str, question: str, answer: str, sources: list) -> dict:
    """Append a new Q&A ticket to the CSV."""
    _ensure_file()
    ticket = {
        "id": _next_id(),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "role": role,
        "question": question,
        "answer": answer,
        "sources": str(sources),
        "thumbs_up": 0,
    }
    with open(TICKETS_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(ticket)
    return ticket


def mark_thumbs_up(ticket_id: int) -> bool:
    """Increment thumbs_up for a ticket by ID."""
    rows = load_all_tickets()
    updated = False
    for row in rows:
        if int(row["id"]) == ticket_id:
            row["thumbs_up"] = int(row["thumbs_up"]) + 1
            updated = True
            break
    if updated:
        _rewrite(rows)
    return updated


def _rewrite(rows: list[dict]):
    _ensure_file()
    with open(TICKETS_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(rows)


# ── Matching ──────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Lowercase, strip punctuation and extra spaces."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def _tokenize(text: str) -> set:
    """Keyword set — removes common stopwords."""
    stopwords = {
        "the","a","an","is","are","was","were","what","how","why","when",
        "where","who","which","do","does","did","can","could","would","should",
        "i","my","me","we","our","you","your","it","its","in","on","at","to",
        "of","for","and","or","not","be","been","have","has","had","tell","show",
        "give","get","any","all","this","that","these","those","about","please"
    }
    return {w for w in _normalize(text).split() if w not in stopwords and len(w) > 2}


def _jaccard(q1: str, q2: str) -> float:
    """Jaccard similarity between keyword sets of two strings."""
    t1, t2 = _tokenize(q1), _tokenize(q2)
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


def find_cached_answer(question: str, role: str) -> dict | None:
    """
    Two-stage cache lookup for a positively-rated answer:

    Stage 1 — Exact match:
        Normalize both questions and compare directly.
        If identical → return immediately (score = 1.0).

    Stage 2 — Fuzzy match:
        Jaccard keyword similarity across all liked tickets.
        Return best match only if score >= FUZZY_THRESHOLD.

    Only considers tickets with thumbs_up >= 1 and the same role.
    """
    rows = load_all_tickets()

    # Filter: liked tickets for this role only
    candidates = [
        r for r in rows
        if int(r.get("thumbs_up", 0)) >= 1 and r.get("role") == role
    ]

    if not candidates:
        return None

    q_norm = _normalize(question)

    # ── Stage 1: Exact match ──────────────────────────────
    for ticket in candidates:
        if _normalize(ticket["question"]) == q_norm:
            print(f"Cache EXACT match for: {question[:60]}", flush=True)
            return _hit(ticket, score=1.0, match_type="exact")

    # ── Stage 2: Fuzzy match ──────────────────────────────
    best_score = 0.0
    best_ticket = None

    for ticket in candidates:
        score = _jaccard(question, ticket["question"])
        if score > best_score:
            best_score = score
            best_ticket = ticket

    if best_score >= FUZZY_THRESHOLD and best_ticket:
        print(f"Cache FUZZY match (score={best_score:.2f}) for: {question[:60]}", flush=True)
        return _hit(best_ticket, score=round(best_score, 2), match_type="fuzzy")

    return None


def _hit(ticket: dict, score: float, match_type: str) -> dict:
    return {
        "answer": ticket["answer"],
        "sources": ticket["sources"],
        "from_cache": True,
        "cache_score": score,
        "match_type": match_type,
        "ticket_id": int(ticket["id"]),
    }


# ── Stats ─────────────────────────────────────────────────

def get_stats() -> dict:
    rows = load_all_tickets()
    total = len(rows)
    liked = sum(1 for r in rows if int(r.get("thumbs_up", 0)) >= 1)
    by_role: dict = {}
    for r in rows:
        role = r.get("role", "unknown")
        by_role[role] = by_role.get(role, 0) + 1
    return {
        "total_tickets": total,
        "liked_tickets": liked,
        "by_role": by_role,
        "cache_hit_eligible": liked,
    }
