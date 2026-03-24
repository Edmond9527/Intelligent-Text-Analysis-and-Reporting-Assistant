"""ColdCode 核心配置。"""

from __future__ import annotations

import os

# ===== 模型配置 =====
OLLAMA = os.getenv("COLDCODE_OLLAMA", "http://open-webui-ollama.open-webui:11434")
MODEL_FAST = os.getenv("COLDCODE_MODEL_FAST", "llama3.1:8b")
MODEL_STRONG = os.getenv("COLDCODE_MODEL_STRONG", "qwen3-coder:30b")

# ===== 运行节流 =====
MIN_RUN_INTERVAL = float(os.getenv("COLDCODE_MIN_RUN_INTERVAL", "1.5"))
LONG_CODE_THRESHOLD = int(os.getenv("COLDCODE_LONG_CODE_THRESHOLD", "5000"))

# ===== 语言配置 =====
LANG_CONFIG = {
    "Python": {
        "fence": "python",
        "label": "Python",
        "debug_hint": "重点关注 traceback、函数名、缩进、导入与解释器环境。",
    },
    "Java": {
        "fence": "java",
        "label": "Java",
        "debug_hint": "重点关注类名/文件名一致性、方法签名、分号、访问修饰符、编译错误信息。",
    },
    "C++": {
        "fence": "cpp",
        "label": "C++",
        "debug_hint": "重点关注编译错误、头文件、命名空间、分号、模板/类型不匹配。",
    },
}

MODE_HELP = {
    "Debug": {
        "hint": "适合粘贴代码 + traceback，让模型定位错误、给最小修复步骤、补丁和修复后代码。",
        "question_placeholder": "例如：为什么报错？请帮我给最小修复步骤和 diff",
        "code_placeholder": "粘贴原始代码（将作为补丁应用目标）",
        "tb_placeholder": "粘贴 traceback（没有可留空）",
    },
    "Explain": {
        "hint": "适合让模型按“总览—逐段解释—关键概念—常见坑”讲清楚代码逻辑。",
        "question_placeholder": "例如：请逐段解释这段代码，并说明每个函数的作用",
        "code_placeholder": "粘贴需要讲解的代码",
        "tb_placeholder": "Explain 模式通常不用填 traceback",
    },
    "Refactor": {
        "hint": "适合在不改变功能的前提下，提升代码可读性、命名和结构，并给出 unified diff。",
        "question_placeholder": "例如：请做最小重构，提高可读性，不要改业务逻辑",
        "code_placeholder": "粘贴需要重构的代码",
        "tb_placeholder": "Refactor 模式通常不用填 traceback",
    },
    "Scaffold/Test": {
        "hint": "适合根据需求自动生成最小可运行项目、核心文件与测试用例。",
        "question_placeholder": "例如：请给我一个 Python CLI 计算器项目脚手架和 pytest 测试",
        "code_placeholder": "可选：已有代码或接口定义",
        "tb_placeholder": "可选：已有报错、约束或环境要求",
    },
    "ROCm Doctor": {
        "hint": "适合排查 AMD ROCm / PyTorch / 驱动 / 权限 / 版本兼容问题。建议粘贴 rocminfo、rocm-smi、torch 输出、安装命令和报错日志。",
        "question_placeholder": "例如：为什么我的 PyTorch 在 ROCm 环境下识别不到 GPU？",
        "code_placeholder": "可选：相关脚本、安装命令、requirements 或最小复现代码",
        "tb_placeholder": "粘贴 rocminfo / rocm-smi / torch 输出 / pip list / 报错日志",
    },
}

PROMPT_SYSTEM = {
    "Explain": (
        "你是 ColdCode（讲解模式），面向编程初学者。\n"
        "输出结构：\n"
        "## 总览\n"
        "## 逐段解释\n"
        "## 关键概念（新手友好）\n"
        "## 常见坑（可选）\n"
        "尽量简洁。\n"
    ),
    "Debug": (
        "你是 ColdCode（调试模式），面向编程初学者。\n"
        "输出 Markdown，并严格包含：\n"
        "## 结论\n"
        "## 证据与定位（行号/片段）\n"
        "## 原因解释（面向新手）\n"
        "## 修复步骤（最小可行）\n"
        "## 补丁（unified diff）\n"
        "## 修复后代码\n"
        "如需改代码：必须给出 diff 格式的 unified diff（代码块用 ```diff）。\n"
        "注意：diff 行必须严格以 '+', '-', 或单个空格开头；不要在标记后额外加空格。\n"
    ),
    "Refactor": (
        "你是 ColdCode（重构模式），面向编程初学者。\n"
        "必须输出 diff 格式的 unified diff（代码块用 ```diff）。\n"
        "输出结构：\n"
        "## 改动目标\n"
        "## 主要问题点（简短）\n"
        "## 补丁（unified diff）\n"
        "## 重构后代码（不要加行号）\n"
        "## 可选建议（测试/命名/复杂度）\n"
        "注意：diff 行必须严格以 '+', '-', 或单个空格开头；不要在标记后额外加空格。\n"
    ),
    "Scaffold/Test": (
        "你是 ColdCode（脚手架/测试模式），面向编程初学者。\n"
        "任务：根据用户需求自动生成一个最小可运行的项目脚手架，以及配套测试用例。\n"
        "要求：\n"
        "1) 输出要结构化，尽量直接可用。\n"
        "2) 如果用户没有提供已有代码，就从零生成。\n"
        "3) 如果用户提供了已有代码，则可以在其基础上组织项目结构。\n"
        "4) Python 优先生成 pytest 风格测试；Java 生成 JUnit 风格或占位测试；C++ 生成简单断言/测试驱动样例。\n"
        "输出结构：\n"
        "## 项目结构\n"
        "## 核心文件\n"
        "## 测试用例\n"
        "## 运行说明\n"
    ),
    "ROCm Doctor": (
        "你是 ColdCode（ROCm Doctor 模式），负责排查 AMD ROCm / PyTorch / 驱动 / 环境兼容问题。\n"
        "优先判断：这是代码问题、环境问题、驱动/权限问题、版本匹配问题，还是证据不足。\n"
        "输出 Markdown，并严格包含：\n"
        "## 环境结论\n"
        "## 高概率根因\n"
        "## 兼容性检查清单\n"
        "## 最小修复步骤\n"
        "## 建议执行命令\n"
        "## 如果仍失败，下一步请补充\n"
        "要求：\n"
        "1) 不要伪造版本号、兼容矩阵或系统信息；不确定就明确写“不确定”。\n"
        "2) 优先给最小可执行步骤，而不是大而全教程。\n"
        "3) 如果用户提供了 rocminfo / rocm-smi / pip list / torch 结果，要显式利用这些证据。\n"
    ),
}
