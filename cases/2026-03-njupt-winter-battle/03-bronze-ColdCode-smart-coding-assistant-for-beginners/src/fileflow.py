"""文件加载、写回与恢复。"""

from __future__ import annotations

from pathlib import Path


def normalize_file_path(p: str) -> str:
    return str(Path((p or "").strip()).expanduser()) if (p or "").strip() else ""


def load_text_file(path: str) -> dict:
    norm = normalize_file_path(path)
    if not norm:
        raise ValueError("请先输入文件路径。")

    p = Path(norm)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在：{path}")
    if p.is_dir():
        raise IsADirectoryError(f"该路径是目录，不是文件：{path}")

    text = p.read_text(encoding="utf-8")
    backup_path = str(p) + ".bak"
    return {
        "path": str(p),
        "content": text,
        "backup_path": backup_path if Path(backup_path).exists() else "",
        "backup_exists": Path(backup_path).exists(),
    }


def apply_fixed_code_to_file(path: str, fixed_code: str) -> dict:
    norm = normalize_file_path(path)
    if not norm:
        raise ValueError("目标文件路径不能为空。")
    if not fixed_code.strip():
        raise ValueError("没有可写回的修复后代码。")

    p = Path(norm)
    if not p.exists():
        raise FileNotFoundError(f"目标文件不存在：{path}")
    if p.is_dir():
        raise IsADirectoryError(f"该路径是目录，不是文件：{path}")

    original = p.read_text(encoding="utf-8")
    backup = Path(str(p) + ".bak")
    backup.write_text(original, encoding="utf-8")

    final_text = fixed_code + ("\n" if fixed_code and not fixed_code.endswith("\n") else "")
    p.write_text(final_text, encoding="utf-8")

    return {
        "path": str(p),
        "backup_path": str(backup),
        "content": final_text,
    }


def restore_backup_file(path: str) -> dict:
    norm = normalize_file_path(path)
    if not norm:
        raise ValueError("请先指定文件路径。")

    p = Path(norm)
    backup = Path(str(p) + ".bak")
    if not backup.exists():
        raise FileNotFoundError(f"未找到备份文件：{backup}")

    restored = backup.read_text(encoding="utf-8")
    p.write_text(restored, encoding="utf-8")
    return {
        "path": str(p),
        "backup_path": str(backup),
        "content": restored,
    }
