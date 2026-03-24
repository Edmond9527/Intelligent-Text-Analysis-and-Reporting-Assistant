"""ColdCode 统一编排入口。"""

from __future__ import annotations

import time
from typing import Callable

from .analysis import analyze_long_code, build_user_message, estimate_tokens
from .cache import CACHE, LAST_OUTPUT, make_cache_key
from .config import LONG_CODE_THRESHOLD, MIN_RUN_INTERVAL, MODEL_FAST, MODEL_STRONG
from .extractors import extract_first_diff, extract_fixed_code
from .guards import looks_invalid_text, looks_sensitive
from .llm_client import chat_once_with_fallback, stream_with_fallback
from .prompts import build_messages

LAST_RUN_TS = 0.0

OutputCallback = Callable[[str], None]


def _build_final_user(mode: str, lang: str, code: str, tb: str, q: str) -> str:
    if mode in ("Explain", "Refactor") and estimate_tokens(code) > LONG_CODE_THRESHOLD:
        chunk_notes = analyze_long_code(
            mode=mode,
            code=code,
            question=q,
            lang=lang,
            chunk_model=MODEL_FAST,
        )
        if mode == "Explain":
            return (
                "检测到长代码，已先进行分块分析。\n\n"
                "下面是各代码块的局部摘要：\n"
                f"```text\n{chunk_notes}\n```\n\n"
                f"用户原问题：{q or '请基于这些分块摘要，给出整体解释。'}\n\n"
                "请输出：\n"
                "## 总览\n"
                "## 逐段解释\n"
                "## 关键概念（新手友好）\n"
                "## 常见坑（可选）"
            )
        return (
            "检测到长代码，已先进行分块重构审查。\n\n"
            "下面是各代码块的局部审查摘要：\n"
            f"```text\n{chunk_notes}\n```\n\n"
            f"用户原目标：{q or '请基于这些分块摘要，给出整体重构建议。'}\n\n"
            "请输出：\n"
            "## 改动目标\n"
            "## 主要问题点（简短）\n"
            "## 重构建议（按优先级）\n"
            "## 可选建议（测试/命名/复杂度）\n"
            "如果能给出完整重构后代码，就附上“## 重构后代码”。"
        )
    return build_user_message(mode, code, tb, q, lang)


def _validate_inputs(code: str, tb: str, q: str):
    if not (code.strip() or tb.strip() or q.strip()):
        raise ValueError("请输入至少一项：代码 / 报错 / 问题")
    if looks_sensitive(code) or looks_sensitive(tb) or looks_sensitive(q):
        raise ValueError("检测到疑似敏感信息（如密钥/密码/私钥），请先打码后再提交。")
    if looks_invalid_text(code) or looks_invalid_text(tb) or looks_invalid_text(q):
        raise ValueError("检测到异常输入（可能包含非法控制字符），请清理后再提交。")


def _apply_learning_card(user: str, enabled: bool) -> str:
    if not enabled:
        return user
    return user + (
        "\n\n【附加要求】\n"
        "请在输出末尾追加一个“## 错误成长卡”小节，并固定包含：\n"
        "- 错误类型\n"
        "- 一句话本质\n"
        "- 这次为什么会发生\n"
        "- 下次自检 checklist（3~5条）\n"
        "- 1 个相似练习题\n"
        "- 1 句鼓励反馈\n"
    )


def _finalize_output(
    *,
    final_md: str,
    mode: str,
    model: str,
    num_predict: int,
    temperature: float,
    prompt_ver: str,
    pack: dict,
    user: str,
    learning_card_enabled: bool,
    file_path: str,
) -> dict:
    fixed_code = extract_fixed_code(final_md)
    diff = extract_first_diff(final_md)

    LAST_OUTPUT["md"] = final_md
    LAST_OUTPUT["meta"] = f"mode={mode} model={model} num_predict={num_predict} temp={temperature}"
    LAST_OUTPUT["fixed_code"] = fixed_code
    LAST_OUTPUT["diff"] = diff
    LAST_OUTPUT["prompt_ver"] = prompt_ver
    LAST_OUTPUT["prompt_system"] = pack["system"]
    LAST_OUTPUT["prompt_fewshot"] = pack.get("fewshot", [])
    LAST_OUTPUT["prompt_user"] = user
    LAST_OUTPUT["mode"] = mode
    LAST_OUTPUT["learning_card"] = learning_card_enabled
    if file_path:
        LAST_OUTPUT["loaded_file_path"] = file_path
        LAST_OUTPUT["backup_file_path"] = file_path + ".bak"

    return {
        "md": final_md,
        "meta": LAST_OUTPUT["meta"],
        "diff": diff,
        "fixed_code": fixed_code,
        "prompt_ver": prompt_ver,
        "prompt_system": pack["system"],
        "prompt_fewshot": pack.get("fewshot", []),
        "prompt_user": user,
        "mode": mode,
        "learning_card": learning_card_enabled,
        "file_path": file_path,
        "cache_hit": False,
    }


def run_task_stream(
    *,
    lang: str,
    mode: str,
    model: str,
    prompt_ver: str,
    code: str = "",
    tb: str = "",
    question: str = "",
    file_path: str = "",
    num_predict: int = 350,
    temperature: float = 0.2,
    learning_card: bool = False,
    output_callback: OutputCallback | None = None,
) -> dict:
    """流式主链路，适合 notebook Run 按钮。"""
    global LAST_RUN_TS

    now_ts = time.time()
    if now_ts - LAST_RUN_TS < MIN_RUN_INTERVAL:
        raise ValueError("请求过于频繁，请稍后再试。")
    LAST_RUN_TS = now_ts

    code = code or ""
    tb = tb or ""
    question = question or ""
    file_path = file_path or ""

    _validate_inputs(code, tb, question)

    user = _build_final_user(mode, lang, code, tb, question)
    learning_card_enabled = bool(mode == "Debug" and learning_card)
    user = _apply_learning_card(user, learning_card_enabled)
    if file_path:
        user += f"\n\n【当前工作文件】\n{file_path}"

    messages, pack = build_messages(mode, user, prompt_ver)
    key = make_cache_key(
        model, mode, lang, prompt_ver, code, tb, question, num_predict,
        temperature, file_path=file_path, learning_card=learning_card_enabled,
    )

    if key in CACHE:
        cached = CACHE[key]
        if output_callback:
            output_callback(cached)
        result = _finalize_output(
            final_md=cached,
            mode=mode,
            model=model,
            num_predict=num_predict,
            temperature=temperature,
            prompt_ver=prompt_ver,
            pack=pack,
            user=user,
            learning_card_enabled=learning_card_enabled,
            file_path=file_path,
        )
        result["cache_hit"] = True
        return result

    fallback = MODEL_FAST if model == MODEL_STRONG else None
    acc = []
    for delta in stream_with_fallback(model, fallback, messages, num_predict, temperature):
        acc.append(delta)
        if output_callback:
            output_callback(delta)
    final_md = "".join(acc).strip()

    CACHE[key] = final_md
    return _finalize_output(
        final_md=final_md,
        mode=mode,
        model=model,
        num_predict=num_predict,
        temperature=temperature,
        prompt_ver=prompt_ver,
        pack=pack,
        user=user,
        learning_card_enabled=learning_card_enabled,
        file_path=file_path,
    )


def run_task_once(
    *,
    lang: str,
    mode: str,
    model: str,
    prompt_ver: str,
    code: str = "",
    tb: str = "",
    question: str = "",
    file_path: str = "",
    num_predict: int = 350,
    temperature: float = 0.2,
    learning_card: bool = False,
) -> dict:
    """非流式入口，便于脚本测试。"""
    global LAST_RUN_TS

    now_ts = time.time()
    if now_ts - LAST_RUN_TS < MIN_RUN_INTERVAL:
        raise ValueError("请求过于频繁，请稍后再试。")
    LAST_RUN_TS = now_ts

    code = code or ""
    tb = tb or ""
    question = question or ""
    file_path = file_path or ""

    _validate_inputs(code, tb, question)

    user = _build_final_user(mode, lang, code, tb, question)
    learning_card_enabled = bool(mode == "Debug" and learning_card)
    user = _apply_learning_card(user, learning_card_enabled)
    if file_path:
        user += f"\n\n【当前工作文件】\n{file_path}"

    messages, pack = build_messages(mode, user, prompt_ver)
    key = make_cache_key(
        model, mode, lang, prompt_ver, code, tb, question, num_predict,
        temperature, file_path=file_path, learning_card=learning_card_enabled,
    )

    if key in CACHE:
        cached = CACHE[key]
        result = _finalize_output(
            final_md=cached,
            mode=mode,
            model=model,
            num_predict=num_predict,
            temperature=temperature,
            prompt_ver=prompt_ver,
            pack=pack,
            user=user,
            learning_card_enabled=learning_card_enabled,
            file_path=file_path,
        )
        result["cache_hit"] = True
        return result

    fallback = MODEL_FAST if model == MODEL_STRONG else None
    _used_model, final_md = chat_once_with_fallback(
        model, fallback, messages, num_predict=num_predict, temperature=temperature
    )
    final_md = final_md.strip()
    CACHE[key] = final_md

    return _finalize_output(
        final_md=final_md,
        mode=mode,
        model=model,
        num_predict=num_predict,
        temperature=temperature,
        prompt_ver=prompt_ver,
        pack=pack,
        user=user,
        learning_card_enabled=learning_card_enabled,
        file_path=file_path,
    )
