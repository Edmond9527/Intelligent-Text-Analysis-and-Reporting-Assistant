"""与 Ollama 通信的唯一入口。"""

from __future__ import annotations

import json
from typing import Iterable

import httpx

from .config import OLLAMA


def chat_once_nonstream(
    model: str,
    messages: list[dict],
    *,
    num_predict: int = 220,
    temperature: float = 0.1,
    timeout_s: int = 60,
) -> str:
    """非流式调用，适合长代码分块分析。"""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_ctx": 32768,
            "temperature": temperature,
            "num_predict": num_predict,
        },
        "keep_alive": "30m",
    }

    resp = httpx.post(f"{OLLAMA}/api/chat", json=payload, timeout=timeout_s)
    resp.raise_for_status()
    data = resp.json()
    return (data.get("message") or {}).get("content", "").strip()


def stream_chat_messages(
    model: str,
    messages: list[dict],
    *,
    num_predict: int = 350,
    temperature: float = 0.2,
) -> Iterable[str]:
    """流式输出。"""
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "num_ctx": 32768,
            "temperature": temperature,
            "num_predict": num_predict,
        },
        "keep_alive": "30m",
    }
    timeout = httpx.Timeout(75.0, connect=10.0, read=20.0)

    with httpx.stream("POST", f"{OLLAMA}/api/chat", json=payload, timeout=timeout) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("done"):
                break
            delta = (obj.get("message") or {}).get("content") or ""
            if delta:
                yield delta


def stream_with_fallback(
    primary_model: str,
    fallback_model: str | None,
    messages: list[dict],
    num_predict: int,
    temperature: float,
) -> Iterable[str]:
    """主模型失败时自动切到备用模型。"""
    if fallback_model is None:
        yield f"[model={primary_model}]\n\n"
        yield from stream_chat_messages(primary_model, messages, num_predict=num_predict, temperature=temperature)
        return

    try:
        yield f"[model={primary_model}]\n\n"
        yield from stream_chat_messages(primary_model, messages, num_predict=num_predict, temperature=temperature)
        return
    except Exception as exc:
        yield f"\n\n[WARN] {primary_model} 太慢或失败：{exc}\n"
        yield f"[INFO] 自动切换到 {fallback_model} …\n\n"

    yield f"[model={fallback_model}]\n\n"
    yield from stream_chat_messages(fallback_model, messages, num_predict=num_predict, temperature=temperature)


def chat_once_with_fallback(
    primary_model: str,
    fallback_model: str | None,
    messages: list[dict],
    *,
    num_predict: int = 350,
    temperature: float = 0.2,
    timeout_s: int = 75,
) -> tuple[str, str]:
    """非流式 fallback，返回 (model_used, content)。"""
    try:
        return primary_model, chat_once_nonstream(
            primary_model,
            messages,
            num_predict=num_predict,
            temperature=temperature,
            timeout_s=timeout_s,
        )
    except Exception:
        if fallback_model is None:
            raise
        return fallback_model, chat_once_nonstream(
            fallback_model,
            messages,
            num_predict=num_predict,
            temperature=temperature,
            timeout_s=timeout_s,
        )
