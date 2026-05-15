"""情绪时间轴分析模块"""

import re
from datetime import datetime, timedelta
from openai import OpenAI
from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
from reader import Note, get_diaries

MOOD_SCORES = {
    "开心": 5, "兴奋": 5, "自信": 5, "心流": 5,
    "平静": 4, "高效": 4,
    "一般": 3,
    "疲惫": 2, "空虚": 2,
    "焦虑": 1, "烦躁": 1, "低落": 1, "愧疚": 1,
}


def quick_mood_score(text: str) -> int:
    """基于关键词快速打分（不调用 API）"""
    text_lower = text.lower()
    positive = ["开心", "爽", "自信", "心流", "充实", "高效", "不错", "挺好", "开心"]
    negative = ["焦虑", "烦", "废", "摆烂", "空虚", "低落", "愧疚", "难受", "崩溃", "累"]

    pos_count = sum(1 for w in positive if w in text_lower)
    neg_count = sum(1 for w in negative if w in text_lower)

    if pos_count > neg_count + 1:
        return 5
    elif pos_count > neg_count:
        return 4
    elif neg_count > pos_count + 1:
        return 1
    elif neg_count > pos_count:
        return 2
    else:
        return 3


def analyze_timeline(diaries: list[Note], use_api: bool = False) -> list[dict]:
    """分析日记生成情绪时间轴数据"""
    results = []

    for diary in sorted(diaries, key=lambda d: d.date):
        if not diary.date:
            continue

        mood_score = quick_mood_score(diary.content)
        mood_label = {5: "积极", 4: "较好", 3: "一般", 2: "低落", 1: "消极"}[mood_score]

        results.append({
            "date": diary.date,
            "score": mood_score,
            "label": mood_label,
            "title": diary.title,
            "preview": diary.content[:80].replace("\n", " "),
        })

    return results


def generate_timeline_report(diaries: list[Note]) -> dict:
    """生成时间轴分析报告"""
    timeline = analyze_timeline(diaries)

    if not timeline:
        return {"error": "没有日记数据"}

    scores = [t["score"] for t in timeline]
    avg_score = sum(scores) / len(scores)

    # 找最高和最低的日子
    best_day = max(timeline, key=lambda t: t["score"])
    worst_day = min(timeline, key=lambda t: t["score"])

    # 情绪分布
    distribution = {}
    for t in timeline:
        label = t["label"]
        distribution[label] = distribution.get(label, 0) + 1

    # 趋势（最近 5 天 vs 之前）
    recent = scores[-5:] if len(scores) >= 5 else scores
    earlier = scores[:-5] if len(scores) >= 5 else []
    trend = "上升" if earlier and sum(recent)/len(recent) > sum(earlier)/len(earlier) else "平稳" if not earlier else "下降"

    return {
        "timeline": timeline,
        "avg_score": round(avg_score, 1),
        "best_day": best_day,
        "worst_day": worst_day,
        "distribution": distribution,
        "trend": trend,
        "total_days": len(timeline),
    }
