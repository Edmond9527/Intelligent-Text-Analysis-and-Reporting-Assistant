"""ColdCode 核心模块导出。"""

from .cache import CACHE, LAST_OUTPUT
from .config import LANG_CONFIG, MODE_HELP, MODEL_FAST, MODEL_STRONG
from .extractors import extract_first_diff, extract_fixed_code
from .fileflow import apply_fixed_code_to_file, load_text_file, normalize_file_path, restore_backup_file
from .reports import build_prompt_compare_text, build_tech_report, export_markdown_result, export_tech_report
from .service import run_task_once, run_task_stream

__all__ = [
    "CACHE",
    "LAST_OUTPUT",
    "LANG_CONFIG",
    "MODE_HELP",
    "MODEL_FAST",
    "MODEL_STRONG",
    "extract_first_diff",
    "extract_fixed_code",
    "normalize_file_path",
    "load_text_file",
    "apply_fixed_code_to_file",
    "restore_backup_file",
    "build_prompt_compare_text",
    "build_tech_report",
    "export_markdown_result",
    "export_tech_report",
    "run_task_once",
    "run_task_stream",
]
