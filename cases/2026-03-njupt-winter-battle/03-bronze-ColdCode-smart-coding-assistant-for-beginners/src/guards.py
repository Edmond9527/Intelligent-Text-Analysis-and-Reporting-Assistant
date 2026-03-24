"""输入清洗与安全检查。"""

from __future__ import annotations

import re

SENSITIVE_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"(?i)api[_-]?key\s*=",
    r"(?i)secret\s*=",
    r"(?i)password\s*=",
    r"(?i)token\s*=",
    r"-----BEGIN .* PRIVATE KEY-----",
]


def looks_sensitive(text: str) -> bool:
    """检测疑似敏感信息。"""
    if not text:
        return False
    return any(re.search(p, text) for p in SENSITIVE_PATTERNS)


def looks_invalid_text(text: str) -> bool:
    """粗略检测非法控制字符。"""
    if not text:
        return False
    bad = 0
    for ch in text:
        o = ord(ch)
        if o < 32 and ch not in ("\n", "\r", "\t"):
            bad += 1
    return bad > 5
