import threading
import streamlit as st
import plotly.graph_objects as go

from config import VAULT_PATH
from reader import scan_vault, get_all_content_summary, get_diaries
from analyzer import analyze_diary
from summarizer import format_summary
from writer import write_daily_summary, read_existing_summary
from profile import generate_profile
from chat import chat
from timeline import generate_timeline_report

st.set_page_config(page_title="Obsidian AI Companion", page_icon="🧠", layout="wide")

# ---- 模块级后台任务（跨 rerun 存活）----
_tasks = {}

def start_task(tid, func, *args):
    _tasks[tid] = {"s": "running", "r": None, "e": None}
    def w():
        try:
            _tasks[tid]["r"] = func(*args)
            _tasks[tid]["s"] = "done"
        except Exception as ex:
            _tasks[tid]["e"] = str(ex)
            _tasks[tid]["s"] = "error"
    threading.Thread(target=w, daemon=True).start()

def get_task(tid):
    return _tasks.get(tid, {"s": "idle", "r": None, "e": None})

# ---- 初始化 ----
if "notes" not in st.session_state:
    st.session_state.notes = scan_vault()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

notes = st.session_state.notes
summary = get_all_content_summary()

# ---- 侧边栏 ----
with st.sidebar:
    st.title("🧠 观察者")
    st.caption("你的个人 AI 伴侣")
    st.divider()
    st.markdown(f"**笔记总数**：{summary['total_notes']} 篇")
    for f, c in summary["folders"].items():
        st.caption(f"📁 {f}: {c} 篇")

# ---- 标签页 ----
tabs = st.tabs(["💬 对话", "👤 人格画像", "📊 日记分析", "📈 情绪时间轴", "🗂️ 仓库概览"])

# ==================== 对话 ====================
with tabs[0]:
    st.subheader("和观察者聊聊")

    for msg in st.session_state.chat_history:
        st.markdown(f"**{'你' if msg['role'] == 'user' else '观察者'}**：{msg['content']}")

    # 检查后台回复
    ct = get_task("chat")
    if ct["s"] == "done" and ct["r"]:
        st.session_state.chat_history.append({"role": "assistant", "content": ct["r"]})
        _tasks.pop("chat", None)
        st.rerun()
    elif ct["s"] == "running":
        st.caption("💭 思考中... 你可以先去其他标签页")
    elif ct["s"] == "error":
        st.error(f"回复失败：{ct['e']}")
        _tasks.pop("chat", None)

    user_input = st.text_input("说点什么...", key="chat_input")
    if st.button("发送", key="send_chat") and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        start_task("chat", chat, user_input, list(st.session_state.chat_history), notes)
        st.rerun()

    if st.session_state.chat_history and st.button("清空对话", key="clear_chat"):
        st.session_state.chat_history = []
        _tasks.pop("chat", None)
        st.rerun()

# ==================== 人格画像 ====================
with tabs[1]:
    st.subheader("你的人格画像")

    pt = get_task("profile")
    if pt["s"] == "idle":
        if st.button("生成人格画像", key="gen_profile"):
            start_task("profile", generate_profile, notes)
            st.rerun()
    elif pt["s"] == "running":
        st.info("⏳ 人格画像正在后台生成中...你可以先去其他标签页")
    elif pt["s"] == "error":
        st.error(f"生成失败：{pt['e']}")
        _tasks.pop("profile", None)
    elif pt["s"] == "done":
        p = pt["r"]
        st.markdown(f"#### {p.get('name', '用户')}")
        st.markdown(f"**身份**：{p.get('age_context', '未知')}")
        st.markdown(f"**写作风格**：{p.get('writing_style', '未知')}")
        st.divider()
        st.markdown("#### 最关心的主题")
        for x in p.get("core_topics", []):
            st.markdown(f"- {x}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 人格特征")
            for x in p.get("personality_traits", []):
                st.markdown(f"- {x}")
        with c2:
            st.markdown("#### 优势")
            for x in p.get("strengths", []):
                st.markdown(f"- {x}")
        st.divider()
        st.markdown("#### 情绪模式")
        ep = p.get("emotional_patterns", {})
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**主要情绪**")
            for x in ep.get("dominant_emotions", []):
                st.markdown(f"- {x}")
        with c2:
            st.markdown("**情绪触发点**")
            for x in ep.get("triggers", []):
                st.markdown(f"- {x}")
        with c3:
            st.markdown("**应对方式**")
            for x in ep.get("coping_mechanisms", []):
                st.markdown(f"- {x}")
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 价值观与信念")
            for x in p.get("values_and_beliefs", []):
                st.markdown(f"- {x}")
        with c2:
            st.markdown("#### 成长方向")
            for x in p.get("growth_areas", []):
                st.markdown(f"- {x}")
        st.divider()
        st.markdown("#### 人际关系")
        rel = p.get("relationships", {})
        st.markdown(f"**社交风格**：{rel.get('social_style', '未知')}")
        for x in rel.get("key_people", []):
            st.markdown(f"- {x}")
        st.divider()
        st.markdown("#### 一段话总结")
        st.info(p.get("one_paragraph_summary", ""))

# ==================== 日记分析 ====================
with tabs[2]:
    st.subheader("日记分析")
    diaries = get_diaries()
    if not diaries:
        st.warning("未找到日记")
    else:
        dates = [d.date for d in diaries]
        sel = st.selectbox("选择日期", dates, key="diary_sel")
        entry = next((d for d in diaries if d.date == sel), None)
        if entry:
            st.markdown("#### 日记原文")
            st.text_area("", value=entry.content, height=300, disabled=True, key=f"txt_{sel}")

            tid = f"diary_{sel}"
            dt = get_task(tid)
            if dt["s"] == "idle":
                if st.button("分析这篇日记", key=f"analyze_{sel}"):
                    history = ""
                    for d in diaries[:5]:
                        if d.date != sel:
                            s = read_existing_summary(d.date)
                            if s:
                                history += f"\n--- {d.date} ---\n{s}\n"
                    start_task(tid, analyze_diary, entry.content, history)
                    st.rerun()
            elif dt["s"] == "running":
                st.info("⏳ 正在分析中...你可以先去其他标签页")
            elif dt["s"] == "error":
                st.error(f"分析失败：{dt['e']}")
            elif dt["s"] == "done":
                result = dt["r"]
                write_daily_summary(sel, format_summary(sel, result))
                st.markdown(f"**情绪**：{result.get('mood', '未知')}")
                if result.get("mood_change"):
                    st.markdown(f"**变化**：{result['mood_change']}")
                st.markdown(f"**学习状态**：{result.get('study_state', '未知')}")
                if result.get("stress_source"):
                    st.markdown(f"**压力来源**：{'、'.join(result['stress_source'])}")
                if result.get("key_events"):
                    st.markdown("**关键事件**：")
                    for e in result["key_events"]:
                        st.markdown(f"- {e}")
                if result.get("ai_observation"):
                    st.info(f"💡 {result['ai_observation']}")

            existing = read_existing_summary(sel)
            if existing:
                with st.expander("已有分析结果"):
                    st.markdown(existing)

# ==================== 情绪时间轴 ====================
with tabs[3]:
    st.subheader("情绪时间轴")
    diaries = get_diaries()

    tt = get_task("timeline")
    if tt["s"] == "idle":
        if st.button("生成情绪时间轴", key="gen_timeline"):
            start_task("timeline", generate_timeline_report, diaries)
            st.rerun()
    elif tt["s"] == "running":
        st.info("⏳ 正在生成时间轴...你可以先去其他标签页")
    elif tt["s"] == "error":
        st.error(f"生成失败：{tt['e']}")
    elif tt["s"] == "done":
        report = tt["r"]
        if "error" in report:
            st.warning(report["error"])
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("总天数", f"{report['total_days']} 天")
            c2.metric("平均情绪", f"{report['avg_score']}/5")
            c3.metric("整体趋势", report["trend"])
            c4.metric("最好的一天", report["best_day"]["date"])
            st.divider()
            td = report["timeline"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[x["date"] for x in td], y=[x["score"] for x in td],
                mode="lines+markers", line=dict(width=3), marker=dict(size=10),
            ))
            fig.update_layout(title="情绪波动", yaxis=dict(range=[0.5, 5.5], dtick=1), height=350)
            fig.update_xaxes(fixedrange=True)
            fig.update_yaxes(fixedrange=True)
            st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False, "displayModeBar": False})
            st.divider()
            st.markdown("#### 情绪分布")
            dist = report["distribution"]
            df = go.Figure()
            df.add_trace(go.Bar(x=list(dist.keys()), y=list(dist.values()),
                                marker_color=["#ff6b6b", "#ffd93d", "#a8dadc", "#457b9d", "#1d3557"]))
            df.update_layout(height=300)
            df.update_xaxes(fixedrange=True)
            df.update_yaxes(fixedrange=True)
            st.plotly_chart(df, use_container_width=True, config={"displayModeBar": False})
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 最好的一天")
                b = report["best_day"]
                st.markdown(f"**{b['date']}** - {b['title']}")
                st.caption(b["preview"])
            with c2:
                st.markdown("#### 最低的一天")
                w = report["worst_day"]
                st.markdown(f"**{w['date']}** - {w['title']}")
                st.caption(w["preview"])
            with st.expander("详细数据"):
                for x in td:
                    e = {"积极": "🟢", "较好": "🔵", "一般": "⚪", "低落": "🟡", "消极": "🔴"}[x["label"]]
                    st.markdown(f"{e} **{x['date']}** ({x['label']}) - {x['title']}")

# ==================== 仓库概览 ====================
with tabs[4]:
    st.subheader("Obsidian 仓库概览")
    st.markdown(f"**路径**：`{VAULT_PATH}`")
    st.markdown(f"**笔记总数**：{summary['total_notes']} 篇")
    for folder, count in summary["folders"].items():
        with st.expander(f"📁 {folder} ({count} 篇)"):
            for note in [n for n in notes if n.folder == folder]:
                preview = note.content[:100].replace("\n", " ")
                st.markdown(f"**{note.title or note.filename}**")
                st.caption(preview + ("..." if len(note.content) > 100 else ""))
