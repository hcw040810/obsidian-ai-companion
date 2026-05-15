"""自然语言搜索模块 — 搜索 Obsidian 笔记"""

from openai import OpenAI
from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
from reader import Note, scan_vault

SEARCH_PROMPT = """你是一个笔记搜索助手。用户会问一个关于自己过去的问题，你需要从笔记中找到相关内容。

用户的问题：{query}

以下是用户的笔记内容：
{notes_content}

请从笔记中找出与问题最相关的内容，返回 JSON 格式：
{{
  "answer": "用 2-3 句话回答用户的问题",
  "relevant_notes": [
    {{
      "title": "笔记标题",
      "date": "日期（如果有）",
      "relevant_excerpt": "最相关的原文片段（50-100字）",
      "relevance": "为什么这篇笔记和问题相关"
    }}
  ],
  "patterns": ["如果发现什么规律或模式，写在这里"]
}}

最多返回 5 篇最相关的笔记。如果找不到相关内容，诚实地说没有找到。"""


def search_notes(query: str, notes: list[Note] | None = None) -> dict:
    """自然语言搜索笔记"""
    if notes is None:
        notes = scan_vault()

    # 构建笔记内容（优先搜索日记和灵感随记）
    priority_order = ["01 日记", "02 灵感，想法，随记", "04  和ai聊聊"]

    def sort_key(note: Note):
        try:
            return priority_order.index(note.folder)
        except ValueError:
            return 99

    sorted_notes = sorted(notes, key=sort_key)

    parts = []
    current_len = 0
    for note in sorted_notes:
        header = f"\n[{note.folder}] {note.title or note.filename} ({note.date or '无日期'}):\n"
        content = note.content[:1500]
        entry = header + content + "\n"
        if current_len + len(entry) > 50000:
            break
        parts.append(entry)
        current_len += len(entry)

    notes_content = "".join(parts)

    client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=[{"role": "user", "content": SEARCH_PROMPT.format(
            query=query,
            notes_content=notes_content,
        )}],
        temperature=0.3,
        max_tokens=3000,
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    import json
    return json.loads(text)
