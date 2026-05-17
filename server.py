"""Flask 后端 — 提供 API 接口"""
import threading
import uuid
import json
import os
import shutil
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, session
from config import VAULT_PATH, SECRET_KEY
from reader import scan_vault, get_all_content_summary, get_diaries
from analyzer import analyze_diary
from summarizer import format_summary
from writer import write_daily_summary, read_existing_summary
from profile import generate_profile
from chat import chat
from timeline import generate_timeline_report
from search import search_notes

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---- 考研驾驶舱数据持久化 ----
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
STUDY_TASKS_FILE = os.path.join(DATA_DIR, "study_tasks.json")
POMODORO_LOG_FILE = os.path.join(DATA_DIR, "pomodoro_log.json")

# 用户上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 全局数据
_default_notes = scan_vault()
_default_summary = get_all_content_summary()
tasks = {}  # tid -> {"s": status, "r": result, "e": error}
chat_history = []


def get_user_vault_path():
    """获取当前用户的仓库路径"""
    sid = session.get("vault_session")
    if sid:
        user_vault = os.path.join(UPLOAD_DIR, sid)
        if os.path.isdir(user_vault):
            return user_vault
    return VAULT_PATH


def get_user_notes():
    """获取当前用户的笔记"""
    return scan_vault(get_user_vault_path())


def get_user_summary():
    """获取当前用户的仓库概况"""
    return get_all_content_summary(get_user_vault_path())


def start_bg(func, *args):
    """启动后台任务，返回 task_id"""
    tid = str(uuid.uuid4())[:8]
    tasks[tid] = {"s": "running", "r": None, "e": None}
    def w():
        try:
            tasks[tid]["r"] = func(*args)
            tasks[tid]["s"] = "done"
        except Exception as ex:
            tasks[tid]["e"] = str(ex)
            tasks[tid]["s"] = "error"
    threading.Thread(target=w, daemon=True).start()
    return tid


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary")
def api_summary():
    s = get_user_summary()
    return jsonify({
        "total": s["total_notes"],
        "folders": s["folders"],
        "vault_path": get_user_vault_path(),
    })


@app.route("/api/debug")
def api_debug():
    """Debug endpoint to check vault contents"""
    vault_path = get_user_vault_path()
    vault_exists = os.path.isdir(vault_path)
    vault_contents = os.listdir(vault_path) if vault_exists else []
    diary_dir = os.path.join(vault_path, "01 日记")
    diary_exists = os.path.isdir(diary_dir)
    diary_files = os.listdir(diary_dir) if diary_exists else []
    return jsonify({
        "vault_path": vault_path,
        "vault_exists": vault_exists,
        "vault_contents": vault_contents[:20],
        "diary_dir": diary_dir,
        "diary_exists": diary_exists,
        "diary_files": diary_files[:10],
        "total_notes": get_user_summary()["total_notes"],
    })


@app.route("/api/vault")
def api_vault():
    folders = {}
    for n in get_user_notes():
        f = n.folder or "(根目录)"
        if f not in folders:
            folders[f] = []
        folders[f].append({"title": n.title or n.filename, "preview": n.content[:120].replace("\n", " "), "date": n.date})
    return jsonify(folders)


@app.route("/api/diaries")
def api_diaries():
    diaries = get_diaries(get_user_vault_path())
    return jsonify([{"date": d.date, "title": d.title, "content": d.content[:500]} for d in diaries])


@app.route("/api/diary/<date>")
def api_diary(date):
    diaries = get_diaries(get_user_vault_path())
    entry = next((d for d in diaries if d.date == date), None)
    if not entry:
        return jsonify({"error": "not found"}), 404
    existing = read_existing_summary(date)
    return jsonify({"date": entry.date, "title": entry.title, "content": entry.content, "existing_summary": existing})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    msg = data.get("message", "")
    notes_ctx = data.get("notes_context")  # 前端从 Obsidian 传来的笔记内容
    if not msg:
        return jsonify({"error": "empty message"}), 400
    chat_history.append({"role": "user", "content": msg})
    fresh_notes = get_user_notes()
    tid = start_bg(chat, msg, list(chat_history), fresh_notes, notes_ctx)
    return jsonify({"task_id": tid})


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """手动刷新仓库数据"""
    s = get_user_summary()
    return jsonify({"ok": True, "total": s["total_notes"]})


@app.route("/api/chat/history")
def api_chat_history():
    return jsonify(chat_history)


@app.route("/api/chat/clear", methods=["POST"])
def api_chat_clear():
    chat_history.clear()
    return jsonify({"ok": True})


@app.route("/api/profile/generate", methods=["POST"])
def api_profile_gen():
    tid = start_bg(generate_profile, get_user_notes())
    return jsonify({"task_id": tid})


@app.route("/api/diary/analyze", methods=["POST"])
def api_diary_analyze():
    data = request.json
    date = data.get("date", "")
    content = data.get("content")  # 前端直接传内容（Obsidian 模式）
    if content:
        # Obsidian 模式：使用前端传来的日记内容
        tid = start_bg(analyze_diary, content, "")
        return jsonify({"task_id": tid})
    diaries = get_diaries(get_user_vault_path())
    entry = next((d for d in diaries if d.date == date), None)
    if not entry:
        return jsonify({"error": "not found"}), 404
    history = ""
    for d in diaries[:5]:
        if d.date != date:
            s = read_existing_summary(d.date)
            if s:
                history += f"\n--- {d.date} ---\n{s}\n"
    tid = start_bg(analyze_diary, entry.content, history)
    return jsonify({"task_id": tid})


@app.route("/api/timeline/generate", methods=["POST"])
def api_timeline_gen():
    diaries = get_diaries(get_user_vault_path())
    tid = start_bg(generate_timeline_report, diaries)
    return jsonify({"task_id": tid})


@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "empty query"}), 400
    tid = start_bg(search_notes, query, get_user_notes())
    return jsonify({"task_id": tid})


# ==================== 仓库上传 API ====================

@app.route("/api/upload/status")
def api_upload_status():
    """检查用户是否已上传仓库"""
    sid = session.get("vault_session")
    has_upload = False
    note_count = 0
    if sid:
        user_vault = os.path.join(UPLOAD_DIR, sid)
        if os.path.isdir(user_vault):
            has_upload = True
            note_count = len([f for f in os.listdir(user_vault) if f.endswith(".md")])
    return jsonify({
        "uploaded": has_upload,
        "session_id": sid,
        "note_count": note_count,
        "default_vault": VAULT_PATH,
    })


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """接收用户上传的 Obsidian 仓库文件"""
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "没有文件"}), 400

    # 生成或复用 session id
    sid = session.get("vault_session")
    if not sid:
        sid = str(uuid.uuid4())[:8]
        session["vault_session"] = sid

    user_vault = os.path.join(UPLOAD_DIR, sid)

    # 如果已有旧数据，先清除
    if os.path.isdir(user_vault):
        shutil.rmtree(user_vault)
    os.makedirs(user_vault, exist_ok=True)

    saved = 0
    for f in files:
        # webkitdirectory 会把相对路径放在 filename 里
        rel_path = f.filename
        if not rel_path.endswith(".md"):
            continue
        # 跳过 .obsidian 等隐藏目录
        parts = rel_path.replace("\\", "/").split("/")
        if any(p.startswith(".") for p in parts):
            continue
        path = os.path.join(user_vault, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f.save(path)
        saved += 1

    return jsonify({"ok": True, "count": saved, "session_id": sid})


@app.route("/api/upload/reset", methods=["POST"])
def api_upload_reset():
    """清除上传数据，重新开始"""
    sid = session.get("vault_session")
    if sid:
        user_vault = os.path.join(UPLOAD_DIR, sid)
        if os.path.isdir(user_vault):
            shutil.rmtree(user_vault)
        session.pop("vault_session", None)
    return jsonify({"ok": True})


# ==================== 快速记录 API ====================

FOLDER_MAP = {
    "日记": "01 日记",
    "灵感": "02 灵感，想法，随记",
    "待办": "02 灵感，想法，随记",
    "知识": "03 收集知识（未查证）",
}


@app.route("/api/notes/classify", methods=["POST"])
def api_classify_note():
    """AI 自动分类笔记内容"""
    data = request.json
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "empty content"}), 400

    def _classify():
        from openai import OpenAI
        from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
        prompt = f"""判断以下文字属于哪个分类，只返回 JSON。

分类选项：
- 日记：情绪、感受、今日记录、心情
- 灵感：想法、创意、随记、观点
- 待办：任务、计划、要做的事
- 知识：学到的东西、收集的信息、笔记

文字内容：
{content[:500]}

只返回 JSON：{{"category": "分类名", "title": "建议标题（10字以内）"}}"""

        client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
        resp = client.chat.completions.create(
            model=MIMO_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100,
        )
        text = resp.choices[0].message.content.strip()
        # 清理 markdown 代码块
        if "```" in text:
            parts = text.split("```")
            text = parts[1] if len(parts) > 1 else parts[0]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        # 提取 JSON
        import re
        m = re.search(r'\{[^}]+\}', text)
        if m:
            text = m.group()
        result = json.loads(text)
        valid_cats = ["日记", "灵感", "待办", "知识"]
        if result.get("category") not in valid_cats:
            result["category"] = "灵感"
        if not result.get("title"):
            result["title"] = content[:10].replace("\n", " ")
        return result

    tid = start_bg(_classify)
    return jsonify({"task_id": tid})


@app.route("/api/notes/create", methods=["POST"])
def api_create_note():
    """创建新笔记"""
    data = request.json
    content = data.get("content", "").strip()
    title = data.get("title", "").strip()
    category = data.get("category", "灵感")

    if not content:
        return jsonify({"error": "empty content"}), 400

    vault_path = get_user_vault_path()
    folder_name = FOLDER_MAP.get(category, "02 灵感，想法，随记")
    folder_path = os.path.join(vault_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # 生成文件名
    today = date.today().isoformat()
    if not title:
        # 从内容取前 20 个字作为标题
        title = content.replace("\n", " ")[:20].strip()
        if not title:
            title = "未命名"

    if category == "日记":
        filename = f"{today}  {title}.md"
    else:
        filename = f"{title}.md"

    # 避免重名
    filepath = os.path.join(folder_path, filename)
    counter = 1
    while os.path.exists(filepath):
        if category == "日记":
            filename = f"{today}  {title} ({counter}).md"
        else:
            filename = f"{title} ({counter}).md"
        filepath = os.path.join(folder_path, filename)
        counter += 1

    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}\n")

    return jsonify({"ok": True, "filename": filename, "folder": folder_name, "path": filepath})


@app.route("/api/dashboard")
def api_dashboard():
    """今日概览数据"""
    vault_path = get_user_vault_path()
    notes = scan_vault(vault_path)
    diaries = [n for n in notes if n.date and n.folder == "01 日记"]
    diaries.sort(key=lambda n: n.date, reverse=True)

    today_str = date.today().isoformat()
    today_note = next((d for d in diaries if d.date == today_str), None)

    # 本周记了多少天
    from datetime import timedelta
    week_ago = (date.today() - timedelta(days=7)).isoformat()
    this_week_dates = [d.date for d in diaries if d.date >= week_ago]
    streak = len(set(this_week_dates))

    # 最新日记
    latest = diaries[0] if diaries else None

    return jsonify({
        "today": today_str,
        "total_notes": len(notes),
        "total_diaries": len(diaries),
        "week_streak": streak,
        "has_today_diary": today_note is not None,
        "latest_diary": {
            "date": latest.date,
            "title": latest.title,
            "preview": latest.content[:150].replace("\n", " "),
        } if latest else None,
    })


@app.route("/api/task/<tid>")
def api_task(tid):
    t = tasks.get(tid)
    if not t:
        return jsonify({"s": "not_found"}), 404
    if t["s"] == "done":
        r = t["r"]
        # 如果是聊天回复，加入历史
        if tid in [k for k, v in tasks.items() if v.get("r") and isinstance(v["r"], str) and len(v["r"]) > 10]:
            if r and isinstance(r, str) and not any(m["content"] == r for m in chat_history if m["role"] == "assistant"):
                chat_history.append({"role": "assistant", "content": r})
        # 如果是日记分析，写入总结
        return jsonify({"s": t["s"], "r": r})
    return jsonify({"s": t["s"], "e": t.get("e")})


# ==================== 考研驾驶舱 API ====================

@app.route("/api/study/tasks", methods=["GET"])
def api_study_tasks():
    return jsonify(load_json(STUDY_TASKS_FILE, []))


@app.route("/api/study/tasks", methods=["POST"])
def api_study_add_task():
    data = request.json
    tasks_list = load_json(STUDY_TASKS_FILE, [])
    task = {
        "id": str(uuid.uuid4())[:8],
        "title": data.get("title", ""),
        "category": data.get("category", "其他"),  # 数学/英语/政治/专业课/其他
        "priority": data.get("priority", "medium"),  # high/medium/low
        "status": "pending",  # pending/done/skipped
        "created": datetime.now().isoformat(),
        "completed_at": None,
    }
    tasks_list.append(task)
    save_json(STUDY_TASKS_FILE, tasks_list)
    return jsonify(task)


@app.route("/api/study/tasks/<task_id>", methods=["PUT"])
def api_study_update_task(task_id):
    data = request.json
    tasks_list = load_json(STUDY_TASKS_FILE, [])
    for t in tasks_list:
        if t["id"] == task_id:
            if "status" in data:
                t["status"] = data["status"]
                if data["status"] == "done":
                    t["completed_at"] = datetime.now().isoformat()
            if "title" in data:
                t["title"] = data["title"]
            if "category" in data:
                t["category"] = data["category"]
            if "priority" in data:
                t["priority"] = data["priority"]
            save_json(STUDY_TASKS_FILE, tasks_list)
            return jsonify(t)
    return jsonify({"error": "not found"}), 404


@app.route("/api/study/tasks/<task_id>", methods=["DELETE"])
def api_study_delete_task(task_id):
    tasks_list = load_json(STUDY_TASKS_FILE, [])
    tasks_list = [t for t in tasks_list if t["id"] != task_id]
    save_json(STUDY_TASKS_FILE, tasks_list)
    return jsonify({"ok": True})


@app.route("/api/study/pomodoro", methods=["POST"])
def api_pomodoro_log():
    data = request.json
    log = load_json(POMODORO_LOG_FILE, [])
    entry = {
        "id": str(uuid.uuid4())[:8],
        "task_title": data.get("task_title", ""),
        "category": data.get("category", ""),
        "duration_min": data.get("duration_min", 25),
        "started_at": data.get("started_at", datetime.now().isoformat()),
        "completed": data.get("completed", True),
        "mood": data.get("mood", ""),  # 高效/一般/低效
        "note": data.get("note", ""),
    }
    log.append(entry)
    save_json(POMODORO_LOG_FILE, log)
    return jsonify(entry)


@app.route("/api/study/pomodoro", methods=["GET"])
def api_pomodoro_history():
    log = load_json(POMODORO_LOG_FILE, [])
    today = date.today().isoformat()
    today_log = [e for e in log if e.get("started_at", "").startswith(today)]
    total_min = sum(e.get("duration_min", 0) for e in today_log if e.get("completed"))
    by_category = {}
    for e in today_log:
        if e.get("completed"):
            cat = e.get("category", "其他")
            by_category[cat] = by_category.get(cat, 0) + e.get("duration_min", 0)
    return jsonify({
        "today_count": len(today_log),
        "today_minutes": total_min,
        "by_category": by_category,
        "entries": today_log,
        "all_count": len(log),
    })


@app.route("/api/study/schedule", methods=["POST"])
def api_study_schedule():
    """AI 根据当前状态生成今日学习计划"""
    data = request.json
    energy = data.get("energy", "一般")  # 高/一般/低
    mood = data.get("mood", "一般")  # 好/一般/差
    available_hours = data.get("available_hours", 8)
    goals = data.get("goals", [])  # 长期目标
    tasks_list = load_json(STUDY_TASKS_FILE, [])
    pending = [t for t in tasks_list if t["status"] == "pending"]

    prompt = f"""你是一个考研学习教练。根据学生当前状态，生成今日学习计划。

当前状态：
- 精力水平：{energy}
- 情绪状态：{mood}
- 可用学习时间：{available_hours} 小时

长期目标：
{json.dumps(goals, ensure_ascii=False) if goals else "未设置"}

待完成任务：
{json.dumps([{"title": t["title"], "category": t["category"], "priority": t["priority"]} for t in pending[:10]], ensure_ascii=False)}

请返回 JSON 格式：
{{
  "schedule": [
    {{"time": "08:00-09:30", "task": "任务名", "category": "类别", "reason": "为什么安排在这个时间"}},
    ...
  ],
  "tips": "今日学习建议（1-2句话）",
  "energy_note": "根据精力水平的建议"
}}

规则：
- 精力低时安排简单任务（政治选择题、英语阅读），不安排高强度数学
- 上午精力最高时安排最难的任务
- 每 90 分钟休息一次
- 总时长不超过可用时间"""

    def _generate():
        from openai import OpenAI
        from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
        client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
        resp = client.chat.completions.create(
            model=MIMO_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=2000,
        )
        text = resp.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        return json.loads(text)

    tid = start_bg(_generate)
    return jsonify({"task_id": tid})


@app.route("/api/study/review", methods=["POST"])
def api_study_review():
    """AI 生成每日学习复盘"""
    pomodoro_log = load_json(POMODORO_LOG_FILE, [])
    today = date.today().isoformat()
    today_log = [e for e in pomodoro_log if e.get("started_at", "").startswith(today)]
    tasks_list = load_json(STUDY_TASKS_FILE, [])
    today_done = [t for t in tasks_list if (t.get("completed_at") or "").startswith(today)]

    prompt = f"""你是一个考研学习教练。根据今天的学习数据，生成每日复盘。

今日番茄钟记录：
{json.dumps(today_log, ensure_ascii=False)}

今日完成的任务：
{json.dumps([{"title": t["title"], "category": t["category"]} for t in today_done], ensure_ascii=False)}

请返回 JSON 格式：
{{
  "summary": "一句话总结今天的学习",
  "strengths": ["做得好的方面"],
  "improvements": ["可以改进的方面"],
  "tomorrow_suggestion": "明天的建议",
  "mood_analysis": "根据学习数据分析情绪状态",
  "score": 7
}}"""

    def _generate():
        from openai import OpenAI
        from config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
        client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)
        resp = client.chat.completions.create(
            model=MIMO_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1500,
        )
        text = resp.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        return json.loads(text)

    tid = start_bg(_generate)
    return jsonify({"task_id": tid})


if __name__ == "__main__":
    print(f"启动服务器... http://localhost:5000")
    print(f"Vault: {VAULT_PATH}")
    print(f"笔记: {_default_summary['total_notes']} 篇")
    app.run(host="0.0.0.0", port=5000, debug=False)
