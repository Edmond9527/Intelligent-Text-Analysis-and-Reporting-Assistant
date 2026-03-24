"""Prompt 对比、导出与技术报告骨架。"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

from .cache import LAST_OUTPUT
from .config import OLLAMA, MODEL_FAST, MODEL_STRONG
from .prompts import PROMPT_VERSIONS, PROMPT_BANK


def build_prompt_compare_text(mode: str) -> str:
    """生成当前模式下 v0-v3 的 prompt 对比文本。"""
    parts = []
    for ver in PROMPT_VERSIONS:
        pack = PROMPT_BANK[ver][mode]
        parts.append(f"# {ver}\n\n## system\n```text\n{pack['system']}\n```")
        if pack.get("fewshot"):
            parts.append("## fewshot\n```json\n" + json.dumps(pack["fewshot"], ensure_ascii=False, indent=2) + "\n```")
        else:
            parts.append("## fewshot\n无")
    return "\n\n".join(parts)


def build_tech_report(current_mode: str = "", current_prompt_ver: str = "", learning_card: bool | None = None) -> str:
    """生成技术文档骨架。"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt_intro = {
        "v0": "朴素提示：只给出基础任务描述。",
        "v1": "结构化提示：加入固定输出格式约束。",
        "v2": "Few-shot 提示：加入示例对话，提高输出稳定性。",
        "v3": "工程化提示：强调信息不足不编造、敏感信息提醒、输出更可落地。",
    }

    current_prompt_ver = current_prompt_ver or LAST_OUTPUT.get("prompt_ver", "")
    current_mode = current_mode or LAST_OUTPUT.get("mode", "")
    learning_card_enabled = LAST_OUTPUT.get("learning_card") if learning_card is None else learning_card
    current_prompt_desc = prompt_intro.get(current_prompt_ver, "未记录")

    fewshot_text = "无"
    if LAST_OUTPUT.get("prompt_fewshot"):
        fewshot_text = "```json\n" + json.dumps(LAST_OUTPUT["prompt_fewshot"], ensure_ascii=False, indent=2) + "\n```"

    return f"""# ColdCode：基于 ROCm 的代码辅助编程专家系统技术文档

## 1. 项目概述
本项目围绕“代码辅助编程专家”主题开发，定位为一个面向初学者、兼顾工程使用场景的智能编程助手。
在原始 Explain / Debug / Refactor / Scaffold-Test 四模式之外，系统进一步补充了两个更适合比赛展示的亮点：
1. 面向 AMD ROCm / PyTorch 的 **ROCm Doctor 环境问诊**
2. 面向初学者学习闭环的 **错误成长卡**

同时，系统提供 **Prompt Lab**，可直接对比当前模式在不同 Prompt 版本下的差异，方便展示 Prompt Engineering 迭代过程。

## 2. 开发环境
- 运行环境：JupyterLab / Notebook（Python 3.12+）
- 大模型服务：Ollama 内网 API
- 模型地址：`{OLLAMA}`
- 快速模型：`{MODEL_FAST}`
- 高质量模型：`{MODEL_STRONG}`
- 当前导出时间：{now}

## 3. 功能设计
### 3.1 Explain 模式
对代码进行逐段讲解，面向初学者输出“总览—逐段解释—关键概念—常见坑”。

### 3.2 Debug 模式
结合 traceback 与代码片段分析报错原因，输出结论、定位、修复步骤与修复后代码。

### 3.3 Refactor 模式
对代码进行可读性与可维护性分析，并给出重构建议与重构后代码。

### 3.4 Scaffold/Test 模式
根据用户给出的项目需求，自动生成项目目录结构、核心文件脚手架代码与测试用例。

### 3.5 ROCm Doctor 模式
针对 AMD ROCm / PyTorch / 环境兼容问题进行结构化问诊，重点区分“代码错误”和“环境错误”，输出兼容性检查清单、最小修复步骤与建议执行命令。

### 3.6 错误成长卡
当 Debug 模式开启“错误成长卡”后，系统会在修复结果末尾追加：
- 错误类型
- 一句话本质
- 本次发生原因
- 下次自检 checklist
- 相似练习题
- 鼓励式反馈

### 3.7 Prompt Lab
系统支持直接查看当前模式下的 Prompt v0-v3 差异，便于演示：
- 朴素提示
- 结构化提示
- few-shot 提示
- 工程化提示

### 3.8 文件级工作流
系统支持输入文件路径并直接读取源码到代码框，在 Jupyter 内形成轻量的“读文件—修改—写回—恢复备份”闭环。

### 3.9 结果导出
系统支持导出：
- 单次运行结果 Markdown
- Prompt 迭代日志 `prompt_log.md`
- 技术文档骨架 `tech_report.md`

## 4. Prompt Engineering 迭代过程
### 4.1 v0
{prompt_intro["v0"]}

### 4.2 v1
{prompt_intro["v1"]}

### 4.3 v2
{prompt_intro["v2"]}

### 4.4 v3
{prompt_intro["v3"]}

## 5. 最近一次运行配置
- 当前模式：`{current_mode}`
- 当前 Prompt 版本：`{current_prompt_ver}`
- 版本说明：{current_prompt_desc}
- 错误成长卡：`{'开启' if learning_card_enabled else '关闭'}`

### 5.1 当前 System Prompt
```text
{LAST_OUTPUT.get("prompt_system", "").strip()}
```

### 5.2 当前 Few-shot
{fewshot_text}

### 5.3 当前 User Input
```text
{LAST_OUTPUT.get("prompt_user", "").strip()}
```

## 6. 错误处理与系统稳健性设计
1. 空输入检查：若代码、报错、问题三者均为空，则直接阻止发送请求。
2. 流式输出：使用 Ollama `/api/chat` 接口进行流式响应，提升交互体验。
3. 模型降级（Fallback）：当高质量模型响应过慢、超时或失败时，系统自动切换到快速模型。
4. 缓存机制（Cache）：相同输入与参数组合命中缓存后，可直接复用结果。
5. Undo / Backup 机制：应用修复后代码到代码框后可 Undo；应用到真实文件前会自动创建 `.bak` 备份，并支持恢复。
6. 请求频率限制：限制连续 Run 的最小时间间隔。
7. 敏感内容与非法输入检查：拦截疑似密钥、密码、私钥以及异常控制字符内容。

## 7. 长代码处理策略
当 Explain / Refactor 模式下输入代码较长时，系统采用：
- Chunking：按行切块
- Sliding Window：相邻代码块保留重叠行
- Local Analysis：先对每个代码块单独分析
- Final Merge：最后将各块摘要统一汇总生成整体回答

## 8. 最近一次运行结果示例
### 8.1 最近一次输出
{LAST_OUTPUT.get("md", "").strip()}

## 9. 总结
当前版本已经形成“代码解释—调试—重构—脚手架生成—ROCm 环境问诊—文件写回—Prompt 可视化比较”的完整演示闭环，适合在比赛答辩中直接展示。
"""


def export_markdown_result(target_dir: str | Path = ".") -> tuple[Path, Path]:
    """导出本次结果和 prompt 日志。"""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    md = LAST_OUTPUT.get("md", "").strip()
    if not md:
        raise ValueError("没有可导出的内容，请先 Run 一次。")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = target_dir / f"report_{ts}.md"
    result_file.write_text(md, encoding="utf-8")

    log_name = target_dir / "prompt_log.md"
    with log_name.open("a", encoding="utf-8") as f:
        f.write("\n\n---\n")
        f.write(f"## {datetime.datetime.now().isoformat(timespec='seconds')}\n")
        f.write(f"- mode: {LAST_OUTPUT.get('mode', '')}\n")
        f.write(f"- prompt_version: {LAST_OUTPUT.get('prompt_ver','')}\n")
        f.write(f"- learning_card: {LAST_OUTPUT.get('learning_card', False)}\n\n")
        f.write("### System Prompt\n")
        f.write("```text\n" + (LAST_OUTPUT.get("prompt_system", "")) + "\n```\n\n")
        if LAST_OUTPUT.get("prompt_fewshot"):
            f.write("### Few-shot\n")
            f.write("```json\n" + json.dumps(LAST_OUTPUT["prompt_fewshot"], ensure_ascii=False, indent=2) + "\n```\n\n")
        f.write("### User Input\n")
        f.write("```text\n" + (LAST_OUTPUT.get("prompt_user", "")) + "\n```\n\n")
        f.write("### Model Output\n")
        f.write(LAST_OUTPUT.get("md", "") + "\n")
    return result_file, log_name


def export_tech_report(target_dir: str | Path = ".") -> Path:
    """导出技术文档骨架。"""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    out = target_dir / "tech_report.md"
    out.write_text(build_tech_report(), encoding="utf-8")
    return out
