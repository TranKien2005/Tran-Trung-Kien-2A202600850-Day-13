from __future__ import annotations

import hashlib
import re

PII_PATTERNS: dict[str, str] = {
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "phone_vn": r"(?:\+84|0)[ \.-]?\d{3}[ \.-]?\d{3}[ \.-]?\d{3,4}", # Matches 090 123 4567, 090.123.4567, etc.
    "cccd": r"\b\d{12}\b",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    # Passport: Vietnamese format B/C followed by 7–8 digits (e.g., B1234567, C12345678)
    "passport": r"\b[BC]\d{7,8}\b",
    # Vietnamese address: keyword + proper noun (capitalized word or digit-based address)
    "address_vn": r"(?:s\u1ed1 \d+[,\s]+)?(?:\d+\s+)?(?:(?:ph\u1ed1|\u0111\u01b0\u1eddng|ng\u00f5|ph\u01b0\u1eddng|qu\u1eadn|huy\u1ec7n|t\u1ec9nh|th\u00e0nh ph\u1ed1|x\u00e3|th\u1ecb tr\u1ea5n)\s+[\w\u00c0-\u1ef9][\w\u00c0-\u1ef9\s]{1,40})",
}


def scrub_text(text: str) -> str:
    safe = text
    for name, pattern in PII_PATTERNS.items():
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def summarize_text(text: str, max_len: int = 80) -> str:
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12]
