"""从模型输出里提取 diff 与 fixed code。"""

from __future__ import annotations

import re

DIFF_BLOCK_RE = re.compile(r"```diff\s*\n(.*?)\n```", re.DOTALL)
HUNK_RE = re.compile(r"^@@\s+-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@")

_FIXED_CODE_RE = re.compile(
    r"(?is)(##\s*(修复后代码|重构后代码|核心文件)\s*.*?\n```(?P<lang>[^\n`]*)\n(?P<body>.*?)\n```)"
)
_FENCE_RE = re.compile(r"(?is)\n```(?P<lang>[^\n`]*)\n(?P<body>.*?)\n```")


def extract_fixed_code(md: str) -> str:
    """优先从“修复后代码/重构后代码/核心文件”提取代码。"""
    if not md:
        return ""

    m = _FIXED_CODE_RE.search(md)
    if m:
        lang = (m.group("lang") or "").strip().lower()
        body = (m.group("body") or "").strip("\n\r")
        if "diff" not in lang:
            return body.strip()

    for m2 in _FENCE_RE.finditer("\n" + md):
        lang = (m2.group("lang") or "").strip().lower()
        body = (m2.group("body") or "").strip("\n\r")
        if "diff" in lang:
            continue
        if any(k in body for k in (
            "def ", "class ", "import ", "from ", "if __name__",
            "public class", "public static void main", "System.out.println",
            "#include", "int main(", "std::", "using namespace"
        )):
            return body.strip()

    return ""


def extract_first_diff(md: str) -> str:
    """提取第一个 diff 代码块。"""
    if not md:
        return ""
    m = DIFF_BLOCK_RE.search(md)
    return (m.group(1) or "").strip() if m else ""
