"""输入重写、长代码分析。"""

from __future__ import annotations

import re

from .config import LANG_CONFIG, MODEL_FAST
from .llm_client import chat_once_nonstream

TB_LINE_RE = re.compile(r'File ".*?", line (\d+)')


def get_line_no_from_traceback(tb: str):
    """从 traceback 中提取行号。"""
    if not tb:
        return None
    ms = TB_LINE_RE.findall(tb)
    return int(ms[-1]) if ms else None


def make_focus_snippet(code: str, line_no: int, context_lines: int = 8):
    """围绕报错行生成带行号片段。"""
    lines = (code or "").splitlines()
    if not line_no or line_no < 1 or line_no > len(lines):
        return None
    s = max(1, line_no - context_lines)
    e = min(len(lines), line_no + context_lines)
    out = []
    for i in range(s, e + 1):
        prefix = ">>" if i == line_no else "  "
        out.append(f"{prefix} {i:04d}: {lines[i - 1]}")
    return "\n".join(out)


def build_user_message(mode: str, code: str, tb: str, question: str, lang: str):
    """根据模式重写用户输入。"""
    code = code or ""
    tb = tb or ""
    question = (question or "").strip()

    fence = LANG_CONFIG[lang]["fence"]
    lang_label = LANG_CONFIG[lang]["label"]
    debug_hint = LANG_CONFIG[lang]["debug_hint"]

    if mode == "Debug":
        if lang == "Python":
            line_no = get_line_no_from_traceback(tb)
            snippet = make_focus_snippet(code, line_no, context_lines=8) if line_no else None
        else:
            snippet = None

        if snippet:
            code_part = "【报错附近代码片段（带行号）】\n" + "```text\n" + snippet + "\n```"
        else:
            code_part = f"【完整代码】\n```{fence}\n" + (code if code.strip() else "(无)") + "\n```"

        return (
            f"请按 {lang_label} 调试模式处理。\n\n"
            f"调试提示：{debug_hint}\n\n"
            "【报错】\n"
            "```text\n" + (tb if tb.strip() else "(无)") + "\n```\n\n"
            + code_part + "\n\n"
            "【我的问题】\n" + (question if question else "请帮我定位问题并修复。")
        )

    if mode == "Explain":
        return (
            f"请按 {lang_label} 讲解模式处理。\n\n"
            "【代码】\n"
            f"```{fence}\n" + (code if code.strip() else "(无)") + "\n```\n\n"
            "【我的问题】\n" + (question if question else f"请逐段解释这段 {lang_label} 代码在做什么。")
        )

    if mode == "Refactor":
        return (
            f"请按 {lang_label} 重构模式处理（不改变功能）。\n\n"
            "【代码】\n"
            f"```{fence}\n" + (code if code.strip() else "(无)") + "\n```\n\n"
            "【我的目标/偏好】\n" + (question if question else f"请对这段 {lang_label} 代码做最小重构，提高可读性。")
        )

    if mode == "Scaffold/Test":
        test_hint = {
            "Python": "请优先生成 pytest 风格测试。",
            "Java": "请优先生成 JUnit 风格测试；如果不确定依赖环境，可先生成测试骨架。",
            "C++": "请优先生成简单断言/测试驱动样例；如有需要可给出 tests/ 占位文件。",
        }[lang]

        return (
            f"请按 {lang_label} 脚手架/测试模式处理。\n\n"
            f"附加要求：{test_hint}\n\n"
            "【项目需求】\n"
            + (question if question else f"请生成一个最小可运行的 {lang_label} 小项目脚手架与测试用例。")
            + "\n\n"
            "【已有代码（可选参考）】\n"
            + f"```{fence}\n" + (code if code.strip() else "(无)") + "\n```\n\n"
            "请严格输出：\n"
            "## 项目结构\n"
            "使用 ```text 展示目录树\n\n"
            "## 核心文件\n"
            "给出 1~3 个最关键文件的代码（带文件名说明）\n\n"
            "## 测试用例\n"
            "给出可运行或可扩展的测试代码\n\n"
            "## 运行说明\n"
            "说明如何运行主程序和测试"
        )

    if mode == "ROCm Doctor":
        return (
            "请按 AMD ROCm 环境问诊模式处理。\n\n"
            "目标：优先判断这是代码问题、环境问题、驱动/权限问题、版本匹配问题，还是日志不足。\n\n"
            "【问题描述】\n"
            + (question if question else "请帮我判断为什么当前 ROCm 环境下程序无法正常使用 GPU。")
            + "\n\n"
            "【相关代码 / 安装命令 / requirements（可选）】\n"
            "```text\n" + (code if code.strip() else "(无)") + "\n```\n\n"
            "【环境信息 / 报错 / 日志】\n"
            "```text\n" + (tb if tb.strip() else "(无)") + "\n```\n\n"
            "优先利用我提供的证据；如果仍不能确认，请在末尾明确列出还缺哪些日志。"
        )

    raise ValueError("mode must be Explain/Debug/Refactor/Scaffold/Test/ROCm Doctor")


def estimate_tokens(text: str) -> int:
    """粗略估算 token 数。"""
    if not text:
        return 0
    return max(1, len(text) // 4)


def split_code_sliding(code: str, lines_per_chunk: int = 80, overlap_lines: int = 12):
    """按行切块，并保留重叠行。"""
    lines = (code or "").splitlines()
    if not lines:
        return []

    chunks = []
    start = 0
    n = len(lines)

    while start < n:
        end = min(n, start + lines_per_chunk)
        chunk_text = "\n".join(lines[start:end])
        chunks.append((start + 1, end, chunk_text))
        if end >= n:
            break
        start = max(0, end - overlap_lines)

    return chunks


def analyze_long_code(mode: str, code: str, question: str, lang: str, *, chunk_model: str = MODEL_FAST):
    """Explain / Refactor 模式下的长代码分块分析。"""
    chunks = split_code_sliding(code, lines_per_chunk=80, overlap_lines=12)
    notes = []

    fence = LANG_CONFIG[lang]["fence"]
    lang_label = LANG_CONFIG[lang]["label"]

    for idx, (start_line, end_line, chunk_text) in enumerate(chunks, start=1):
        if mode == "Explain":
            system = (
                f"你是 {lang_label} 代码讲解助手。用户是初学者。\n"
                "请只分析当前这一块代码，输出不超过 6 条要点。\n"
                "重点写：这块在做什么、关键变量/函数、与前后文可能的关系。"
            )
            user = (
                f"这是第 {idx}/{len(chunks)} 个代码块，行号 {start_line}-{end_line}。\n\n"
                f"```{fence}\n{chunk_text}\n```\n\n"
                f"用户问题：{question or f'请概括这一块 {lang_label} 代码的作用。'}"
            )
        elif mode == "Refactor":
            system = (
                f"你是 {lang_label} 代码重构审查助手。\n"
                "请只分析当前这一块代码，输出不超过 6 条局部问题和建议。\n"
                "重点写：可读性、命名、重复逻辑、函数拆分、风格问题。\n"
                "不要输出完整重构代码，只做局部分析。"
            )
            user = (
                f"这是第 {idx}/{len(chunks)} 个代码块，行号 {start_line}-{end_line}。\n\n"
                f"```{fence}\n{chunk_text}\n```\n\n"
                f"用户目标：{question or f'请找出这一块 {lang_label} 代码值得重构的地方。'}"
            )
        else:
            raise ValueError("analyze_long_code 只用于 Explain / Refactor")

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        note = chat_once_nonstream(chunk_model, messages, num_predict=220, temperature=0.1)
        notes.append(f"[Chunk {idx} | L{start_line}-L{end_line}]\n{note}")

    return "\n\n".join(notes)
