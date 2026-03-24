"""Prompt 版本与消息构造。"""

from __future__ import annotations

from .config import PROMPT_SYSTEM

PROMPT_VERSIONS = ["v0", "v1", "v2", "v3"]

PROMPT_BANK = {
    "v0": {
        "Debug": {
            "system": "你是编程助手，帮用户定位报错并给出修复建议。",
            "fewshot": [],
        },
        "Explain": {"system": "你是编程老师，解释用户代码。", "fewshot": []},
        "Refactor": {"system": "你是代码重构助手，给出改进建议。", "fewshot": []},
        "Scaffold/Test": {
            "system": "你是项目脚手架生成助手，请根据需求生成目录结构和测试用例。",
            "fewshot": [],
        },
        "ROCm Doctor": {
            "system": "你是 AMD ROCm 环境问诊助手，帮用户判断 GPU 不可用、驱动、PyTorch 或环境兼容问题。",
            "fewshot": [],
        },
    },
    "v1": {
        "Debug": {
            "system": PROMPT_SYSTEM["Debug"] + "\n额外要求：必须严格按标题输出，不要漏标题。",
            "fewshot": [],
        },
        "Explain": {"system": PROMPT_SYSTEM["Explain"], "fewshot": []},
        "Refactor": {"system": PROMPT_SYSTEM["Refactor"], "fewshot": []},
        "Scaffold/Test": {
            "system": PROMPT_SYSTEM["Scaffold/Test"] + "\n额外要求：必须严格按标题输出，不要漏标题。",
            "fewshot": [],
        },
        "ROCm Doctor": {
            "system": PROMPT_SYSTEM["ROCm Doctor"] + "\n额外要求：必须严格按标题输出，不要漏标题。",
            "fewshot": [],
        },
    },
    "v2": {
        "Debug": {
            "system": PROMPT_SYSTEM["Debug"],
            "fewshot": [
                {"role": "user", "content": "import httpx 报错：ModuleNotFoundError: No module named 'httpx'"},
                {"role": "assistant", "content": "原因：缺少依赖或环境不一致。最小修复：在当前解释器执行 pip install httpx，然后重启 kernel。"},
            ],
        },
        "Explain": {"system": PROMPT_SYSTEM["Explain"], "fewshot": []},
        "Refactor": {"system": PROMPT_SYSTEM["Refactor"], "fewshot": []},
        "Scaffold/Test": {
            "system": PROMPT_SYSTEM["Scaffold/Test"],
            "fewshot": [
                {
                    "role": "user",
                    "content": "请为一个 Python 命令行计算器生成项目脚手架和 pytest 测试。"
                },
                {
                    "role": "assistant",
                    "content": "## 项目结构\n```text\ncalculator/\n  main.py\n  calculator.py\n  tests/\n    test_calculator.py\n```\n\n## 核心文件\n```python\n# calculator.py\n\ndef add(a, b):\n    return a + b\n```\n\n## 测试用例\n```python\n# tests/test_calculator.py\nfrom calculator import add\n\ndef test_add():\n    assert add(1, 2) == 3\n```\n\n## 运行说明\n使用 pytest 运行测试。"
                },
            ],
        },
        "ROCm Doctor": {
            "system": PROMPT_SYSTEM["ROCm Doctor"],
            "fewshot": [
                {
                    "role": "user",
                    "content": "我在 Ubuntu + ROCm 环境里运行 torch.cuda.is_available() 返回 False，rocminfo 能看到 GPU，帮我判断可能原因。"
                },
                {
                    "role": "assistant",
                    "content": "## 环境结论\n更像是 Python / PyTorch 与 ROCm 运行时之间的匹配问题，而不是 GPU 完全不可见。\n\n## 高概率根因\n1. 安装了 CPU 版或 CUDA 版 PyTorch，而不是 ROCm 版。\n2. 当前 Python 环境与执行 rocminfo 的系统环境不是同一个。\n3. 相关库路径或权限设置不完整。\n\n## 兼容性检查清单\n- 检查 torch 版本字符串是否带 ROCm 标识\n- 检查 python 与 pip 是否来自同一环境\n- 检查 rocm-smi / rocminfo 是否在当前用户下可用\n\n## 最小修复步骤\n先确认 PyTorch 构建版本，再确认当前解释器与 pip 指向一致。\n\n## 建议执行命令\n```bash\npython -c \"import torch; print(torch.__version__); print(torch.version.hip); print(torch.cuda.is_available())\"\nwhich python\npython -m pip show torch\n```\n\n## 如果仍失败，下一步请补充\n补充 python 输出、pip show torch 和完整报错日志。"
                },
            ],
        },
    },
    "v3": {
        "Debug": {
            "system": PROMPT_SYSTEM["Debug"] + (
                "\n工程约束：\n"
                "1) 信息不足不要编造，说明需要补充什么。\n"
                "2) 如果用户粘贴疑似密钥/密码，提醒打码。\n"
                "3) 可以在内部逐步推理，但不要输出推理过程，只输出结论与步骤。\n"
            ),
            "fewshot": [],
        },
        "Explain": {"system": PROMPT_SYSTEM["Explain"], "fewshot": []},
        "Refactor": {"system": PROMPT_SYSTEM["Refactor"], "fewshot": []},
        "Scaffold/Test": {
            "system": PROMPT_SYSTEM["Scaffold/Test"] + (
                "\n工程约束：\n"
                "1) 信息不足不要编造，需求不明确时按“最小可运行项目”生成。\n"
                "2) 目录结构要清晰、文件命名要合理。\n"
                "3) 测试用例应覆盖核心功能而不是只写空壳。\n"
                "4) 可以在内部逐步推理，但不要输出推理过程，只输出结果。\n"
            ),
            "fewshot": [],
        },
        "ROCm Doctor": {
            "system": PROMPT_SYSTEM["ROCm Doctor"] + (
                "\n工程约束：\n"
                "1) 不确定的版本关系不要编造，明确写“需要进一步核实”。\n"
                "2) 先给最小排查路径，再给扩展建议。\n"
                "3) 优先区分“代码错误”和“环境错误”。\n"
                "4) 可以在内部逐步推理，但不要输出推理过程，只输出结果。\n"
            ),
            "fewshot": [],
        },
    },
}


def build_messages(mode: str, user_text: str, prompt_ver: str):
    """根据模式和版本构造 message 列表。"""
    pack = PROMPT_BANK[prompt_ver][mode]
    msgs = [{"role": "system", "content": pack["system"]}]
    msgs.extend(pack.get("fewshot", []))
    msgs.append({"role": "user", "content": user_text})
    return msgs, pack
