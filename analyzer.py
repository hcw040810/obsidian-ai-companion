import json
from openai import OpenAI

from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL

ANALYSIS_PROMPT = """你是一个长期观察用户的 AI 伴侣。请分析以下日记内容，返回 JSON 格式。

要求：
- mood: 主要情绪标签，从以下选择：焦虑/平静/兴奋/低落/愧疚/自信/烦躁/空虚/开心/疲惫
- mood_change: 情绪变化描述（一句话）
- study_state: 学习状态，从以下选择：高效/心流/拖延/摆烂/没学/一般
- stress_source: 压力来源列表（如：考研/论文/人际/家庭/自我评价/经济/健康）
- key_events: 关键事件列表（2-5 条）
- ai_observation: 一句长期观察，要有陪伴感，像朋友一样说话，不要说教，不要用"你应该"这种句式

请严格返回 JSON，不要有其他内容。

日记内容：
{diary_content}

历史摘要（用于发现长期模式，如果没有则忽略）：
{history_summary}"""

WEEKLY_PROMPT = """你是一个长期观察用户的 AI 伴侣。请根据以下一周的日记总结，生成一份周报。

要求返回 JSON 格式：
- mood_distribution: 本周情绪分布（各情绪出现次数）
- overall_mood: 整体情绪评价（一句话）
- study_summary: 学习状态总结
- high_efficiency_days: 高效的日期列表
- low_efficiency_days: 低效的日期列表
- stress_trend: 本周主要压力来源
- ai_weekly_observation: 本周观察（2-3 句话，要有洞察力和陪伴感）
- suggestion: 一条下周建议（不要说教，像朋友提醒）

一周日记总结：
{weekly_summaries}"""


def get_client() -> OpenAI:
    return OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)


def analyze_diary(diary_content: str, history_summary: str = "") -> dict:
    """分析单篇日记，返回结构化结果"""
    client = get_client()
    prompt = ANALYSIS_PROMPT.format(
        diary_content=diary_content,
        history_summary=history_summary or "暂无历史数据",
    )

    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()
    # 尝试提取 JSON（兼容 markdown 代码块包裹的情况）
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)


def generate_weekly_report(weekly_summaries: str) -> dict:
    """生成周报"""
    client = get_client()
    prompt = WEEKLY_PROMPT.format(weekly_summaries=weekly_summaries)

    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)
