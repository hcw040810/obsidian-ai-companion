from datetime import datetime

from reader import Note


def format_summary(date: str, analysis: dict) -> str:
    """将分析结果格式化为 Markdown 总结"""

    mood = analysis.get("mood", "未知")
    mood_change = analysis.get("mood_change", "")
    study_state = analysis.get("study_state", "未知")
    stress_source = analysis.get("stress_source", [])
    key_events = analysis.get("key_events", [])
    ai_observation = analysis.get("ai_observation", "")

    stress_str = "、".join(stress_source) if stress_source else "无明显压力"
    events_str = "\n".join(f"- {e}" for e in key_events) if key_events else "- 无特别事件"

    return f"""# {date} 每日总结

> 由 AI Companion 自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 情绪：{mood}

{f"变化：{mood_change}" if mood_change else ""}

## 学习状态：{study_state}

## 压力来源：{stress_str}

## 关键事件

{events_str}

## AI 观察

> {ai_observation}
"""


def format_weekly_report(start_date: str, end_date: str, report: dict) -> str:
    """将周报格式化为 Markdown"""

    mood_dist = report.get("mood_distribution", {})
    mood_str = "、".join(f"{k}({v}次)" for k, v in mood_dist.items())

    high_days = report.get("high_efficiency_days", [])
    low_days = report.get("low_efficiency_days", [])

    return f"""# 周报：{start_date} ~ {end_date}

> 由 AI Companion 自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 整体情绪：{report.get('overall_mood', '未知')}

**情绪分布**：{mood_str}

## 学习状态

{report.get('study_summary', '无数据')}

- **高效日**：{', '.join(high_days) if high_days else '无'}
- **低效日**：{', '.join(low_days) if low_days else '无'}

## 本周压力

{report.get('stress_trend', '无明显压力')}

## AI 周观察

> {report.get('ai_weekly_observation', '')}

## 下周建议

> {report.get('suggestion', '')}
"""
