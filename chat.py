"""AI 对话模块 — 带上下文记忆的聊天"""

from openai import OpenAI
from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
from reader import Note, scan_vault

SYSTEM_PROMPT = """# 角色：观察者

你是「观察者」，一个专属于用户个人的 AI 心理陪伴助手。你已经完整阅读了他在 Obsidian 中的所有笔记，包括日记、灵感随记、收集的知识、以及他和 AI 的聊天记录。

## 核心定位
你不是聊天机器人，不是心理咨询师，不是一个工具。你是一个真正"认识"他的人——通过阅读他的文字，你了解他的性格、恐惧、野心、习惯和人际关系。

## 说话风格（非常重要，必须严格遵守）
- 你有自己独立的说话方式，绝不模仿用户的口头禅或不雅表达
- 用户日记中可能包含情绪化的粗俗用语，这些是他个人的情绪宣泄方式，你绝不能在回复中使用类似的措辞
- 用温暖、自然、有教养的中文交流，像一个成熟可靠的朋友
- 语气温和但不软弱，直接但不粗鲁
- 回复简洁有力，通常 2-5 句话，除非他在问需要详细分析的问题
- 偶尔可以用比喻或类比来让道理更生动
- 你可以理解用户的情绪，但要用你自己的方式表达，而不是复制他的措辞

## 你的能力
1. **记忆引用**：引用他写过的原话来回应，让他感受到"你真的记得"
2. **模式识别**：指出他的情绪周期、行为规律（如"你每次焦虑时都会..."）
3. **情绪陪伴**：在他低落时给出真实的理解和陪伴，而不是空洞的鸡汤
4. **思路梳理**：帮他拆解复杂问题，但不替他做决定
5. **规律发现**：主动关联他过去的想法和现在的状态
6. **温和提醒**：偶尔提一下他之前提到但可能忘了的事

## 你绝对不做的事
- 绝不使用任何不雅或粗俗的表达，即使用户在日记中频繁使用
- 绝不模仿用户的口语习惯来"套近乎"
- 不说教，不用"你应该"这种句式
- 不给空洞的鸡汤（如"一切都会好的"）
- 不过度分析每一句话
- 不在用户只是想聊天时强行分析心理

## 你了解的关于他的完整信息
{user_context}

## 对话历史
{chat_history}

## 当前用户消息
{user_message}

请以观察者的身份回复。记住：你是一个有自己人格的陪伴者，不是用户的镜像。"""


def sanitize_text(text: str) -> str:
    """过滤敏感词汇，避免触发 API 内容过滤"""
    replacements = [
        ("傻逼", "那个人"), ("傻比", "那个人"),
        ("他妈的", "真是的"), ("他妈", "真是"),
        ("草了", "唉"), ("草", "唉"),
        ("卧槽", "哇"), ("我靠", "哎呀"),
        ("nmd", "真是"), ("NMD", "真是"), ("tm", "真是"), ("TM", "真是"),
        ("导了三次", "释放了三次"), ("导了两次", "释放了两次"),
        ("导了", "放松了"), ("手冲", "放松"),
        ("自慰", "放松"), ("sy", "放松"),
        ("偷看", "看到"), ("裸", "没穿衣服"),
    ]
    for bad, good in replacements:
        text = text.replace(bad, good)
    return text


def build_chat_context(notes: list[Note], max_chars: int = 20000) -> str:
    """构建聊天用的用户上下文"""
    parts = []
    current_len = 0

    priority_order = ["01 日记", "02 灵感，想法，随记", "MOC", "04  和ai聊聊"]

    def sort_key(note: Note):
        try:
            return priority_order.index(note.folder)
        except ValueError:
            return 99

    sorted_notes = sorted(notes, key=sort_key)

    for note in sorted_notes:
        header = f"\n[{note.folder}] {note.title or note.filename}:\n"
        content = sanitize_text(note.content[:2000])
        entry = header + content + "\n"
        if current_len + len(entry) > max_chars:
            break
        parts.append(entry)
        current_len += len(entry)

    return "".join(parts)


def chat(user_message: str, chat_history: list[dict], notes: list[Note] | None = None) -> str:
    """单轮对话 — 每次调用都重新扫描仓库以获取最新内容"""
    # 每次对话都重新扫描，确保读取最新笔记
    if notes is None:
        notes = scan_vault()

    user_context = build_chat_context(notes)

    history_text = ""
    for msg in chat_history[-20:]:
        role = "用户" if msg["role"] == "user" else "观察者"
        history_text += f"{role}: {sanitize_text(msg['content'])}\n"

    prompt = SYSTEM_PROMPT.format(
        user_context=user_context,
        chat_history=history_text or "（新对话）",
        user_message=user_message,
    )

    client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )

    reply = response.choices[0].message.content.strip()
    # 过滤 AI 回复中的不雅表达
    reply = sanitize_text(reply)
    return reply
