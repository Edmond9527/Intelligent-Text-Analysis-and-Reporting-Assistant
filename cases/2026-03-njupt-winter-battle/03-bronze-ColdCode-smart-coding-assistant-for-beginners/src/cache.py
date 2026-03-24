"""缓存与最近一次输出状态。"""

from __future__ import annotations

import hashlib
import json

CACHE = {}
LAST_OUTPUT = {
    "md": "",
    "meta": "",
    "diff": "",
    "fixed_code": "",
    "prev_code": "",
    "prompt_ver": "",
    "prompt_system": "",
    "prompt_fewshot": [],
    "prompt_user": "",
    "loaded_file_path": "",
    "backup_file_path": "",
    "last_apply_target": "code_box",
    "mode": "",
    "learning_card": False,
}


def make_cache_key(
    model,
    mode,
    lang,
    prompt_ver,
    code,
    tb,
    q,
    num_predict,
    temperature,
    file_path="",
    learning_card=False,
):
    raw = json.dumps(
        {
            "model": model,
            "mode": mode,
            "lang": lang,
            "prompt_ver": prompt_ver,
            "code": code,
            "tb": tb,
            "q": q,
            "num_predict": num_predict,
            "temperature": temperature,
            "file_path": file_path,
            "learning_card": learning_card,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
