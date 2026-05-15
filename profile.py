"""构建用户综合人格画像"""

from openai import OpenAI
from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
from reader import Note, scan_vault

PROFILE_PROMPT = """你是一个深度观察者。请根据以下这个人的全部 Obsidian 笔记内容，为他构建一份综合人格画像。

要求返回 JSON 格式：

{{
  "name": "（如果笔记中提到名字就写，否则写「用户」）",
  "age_context": "年龄/身份背景（如大学生、考研党等）",
  "core_topics": ["他最关心的 5-8 个主题"],
  "personality_traits": ["5-8 个人格特征描述"],
  "emotional_patterns": {{
    "dominant_emotions": ["主要情绪"],
    "triggers": ["常见情绪触发点"],
    "coping_mechanisms": ["他的应对方式"]
  }},
  "values_and_beliefs": ["他看重的东西"],
  "relationships": {{
    "key_people": ["提到的重要人物及关系"],
    "social_style": "社交风格描述"
  }},
  "growth_areas": ["他想成长/改变的方面"],
  "strengths": ["他的优势/闪光点"],
  "writing_style": "写作风格描述（口语化/文艺/简洁等）",
  "one_paragraph_summary": "用一段话总结这个人，要像一个真正了解他的朋友那样说"
}}

全部笔记内容：
{all_content}
"""


def build_context(notes: list[Note], max_chars: int = 60000) -> str:
    """将所有笔记拼接成上下文，限制总长度"""
    parts = []
    current_len = 0

    for note in notes:
        header = f"\n\n=== [{note.folder}] {note.title or note.filename} ===\n"
        entry = header + note.content
        if current_len + len(entry) > max_chars:
            remaining = max_chars - current_len
            if remaining > 100:
                parts.append(entry[:remaining] + "\n...[截断]")
            break
        parts.append(entry)
        current_len += len(entry)

    return "".join(parts)


def generate_profile(notes: list[Note] | None = None) -> dict:
    """生成综合人格画像"""
    if notes is None:
        notes = scan_vault()

    context = build_context(notes)

    client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=[{"role": "user", "content": PROFILE_PROMPT.format(all_content=context)}],
        temperature=0.3,
        max_tokens=4000,
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    import json
    return json.loads(text)
