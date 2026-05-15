import os

from config import SUMMARY_DIR


def ensure_summary_dir():
    """确保总结目录存在"""
    os.makedirs(SUMMARY_DIR, exist_ok=True)


def write_daily_summary(date: str, content: str) -> str:
    """写入每日总结文件，返回文件路径"""
    ensure_summary_dir()
    filename = f"{date}-summary.md"
    filepath = os.path.join(SUMMARY_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def write_weekly_report(start_date: str, end_date: str, content: str) -> str:
    """写入周报文件，返回文件路径"""
    ensure_summary_dir()
    filename = f"week-{start_date}-to-{end_date}.md"
    filepath = os.path.join(SUMMARY_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def read_existing_summary(date: str) -> str | None:
    """读取已有的每日总结，如果不存在返回 None"""
    filepath = os.path.join(SUMMARY_DIR, f"{date}-summary.md")
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return None
