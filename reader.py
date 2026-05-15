import os
import re
from dataclasses import dataclass, field
from datetime import datetime

from config import VAULT_PATH


@dataclass
class Note:
    path: str              # 完整路径
    filename: str          # 文件名
    folder: str            # 所属文件夹（如 "01 日记"）
    content: str           # 正文内容
    date: str = ""         # 日期（日记文件才有）
    title: str = ""        # 标题
    timestamps: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


def extract_date(filename: str) -> str | None:
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else None


def extract_title(filename: str) -> str:
    name = filename.removesuffix(".md")
    name = re.sub(r"^\d{4}-\d{2}-\d{2}\s*", "", name)
    return name.strip()


def extract_timestamps(content: str) -> list[str]:
    return re.findall(r"\*\*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\*\*", content)


def extract_wikilinks(content: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def extract_tags(content: str) -> list[str]:
    return re.findall(r"#(\w+)", content)


def scan_vault(vault_path: str = VAULT_PATH) -> list[Note]:
    """扫描整个 Obsidian 仓库，返回所有 .md 文件"""
    notes = []
    if not os.path.isdir(vault_path):
        return notes

    # 跳过的目录
    skip_dirs = {".obsidian", ".claude", ".claudian", "attachments", "附件", "summaries"}

    for root, dirs, files in os.walk(vault_path):
        # 跳过隐藏目录和附件目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, vault_path)
            folder = rel_path.split(os.sep)[0] if os.sep in rel_path else ""

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            note = Note(
                path=filepath,
                filename=filename,
                folder=folder,
                content=content,
                date=extract_date(filename) or "",
                title=extract_title(filename),
                timestamps=extract_timestamps(content),
                wikilinks=extract_wikilinks(content),
                tags=extract_tags(content),
            )
            notes.append(note)

    return notes


def scan_by_folder(folder_name: str, vault_path: str = VAULT_PATH) -> list[Note]:
    """按文件夹扫描"""
    all_notes = scan_vault(vault_path)
    return [n for n in all_notes if n.folder == folder_name]


def get_diaries(vault_path: str = VAULT_PATH) -> list[Note]:
    """获取所有日记，按日期倒序"""
    diaries = [n for n in scan_by_folder("01 日记", vault_path) if n.date]
    diaries.sort(key=lambda n: n.date, reverse=True)
    return diaries


def get_all_content_summary(vault_path: str = VAULT_PATH) -> dict:
    """获取仓库概况"""
    notes = scan_vault(vault_path)
    folders = {}
    for n in notes:
        folder = n.folder or "(根目录)"
        if folder not in folders:
            folders[folder] = []
        folders[folder].append(n)

    return {
        "total_notes": len(notes),
        "folders": {k: len(v) for k, v in folders.items()},
        "notes": notes,
    }
