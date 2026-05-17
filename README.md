# 观察者 — Obsidian AI Companion

一个基于 Obsidian 笔记的 AI 心理陪伴助手。它会阅读你在 Obsidian 中的所有笔记（日记、灵感、随记等），通过 AI 分析你的情绪模式、行为规律，成为一个真正"认识"你的陪伴者。

## 功能

- **AI 对话** — 基于你的完整笔记上下文进行深度对话，能引用你写过的原话
- **日记分析** — 自动分析日记的情绪、学习状态、压力来源
- **情绪时间轴** — 可视化你的情绪变化趋势
- **人格画像** — 从笔记中提炼你的性格特征和行为模式
- **笔记搜索** — 智能搜索所有笔记内容
- **考研驾驶舱** — 番茄钟、任务管理、每日学习计划和复盘

## 数据源支持

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **Obsidian 插件连接** | 通过 Local REST API 插件直连本地 Obsidian | 电脑/手机（同一局域网） |
| **文件夹上传** | 在网页中上传 Obsidian 文件夹 | 任何设备 |
| **默认仓库** | 使用项目内置的示例 vault | 演示/测试 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
```

需要配置：
- `MIMO_API_KEY` — AI 模型的 API Key

### 3. 启动

```bash
python server.py
```

打开 http://localhost:5000

## 连接 Obsidian（推荐）

1. 在 Obsidian 中安装社区插件 **"Local REST API"**
2. 启用插件的 HTTP 服务器（设置 → Local REST API → Enable HTTP server）
3. 复制插件设置中的 API Key
4. 在网页的连接界面中填入地址和 Key

默认地址：`http://127.0.0.1:27123`

### 手机使用

手机和电脑连接同一 WiFi，在连接界面填入电脑的局域网 IP：

```
http://192.168.x.x:27123
```

## 部署到 Render

项目已配置 `render.yaml`，可以直接部署：

1. Fork 本仓库
2. 在 [Render](https://render.com) 创建 Web Service
3. 连接你的 GitHub 仓库
4. 设置环境变量 `MIMO_API_KEY`
5. 部署

注意：Render 免费版会在闲置 15 分钟后休眠，首次访问需等待 50 秒左右冷启动。

## 项目结构

```
obsidian-ai-companion/
├── server.py          # Flask 后端主文件，所有 API 路由
├── chat.py            # AI 对话模块
├── analyzer.py        # 日记情绪分析
├── profile.py         # 人格画像生成
├── search.py          # 笔记搜索
├── timeline.py        # 情绪时间轴
├── reader.py          # Obsidian 笔记读取器
├── writer.py          # 日记总结写入
├── summarizer.py      # 内容摘要
├── config.py          # 配置管理
├── templates/
│   └── index.html     # 前端单页应用
├── vault/             # 示例 Obsidian 仓库
├── requirements.txt   # Python 依赖
├── Procfile           # Render/Heroku 部署配置
├── render.yaml        # Render 服务配置
└── .env.example       # 环境变量模板
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/summary` | GET | 仓库概况（笔记数量、文件夹） |
| `/api/vault` | GET | 笔记列表（按文件夹分组） |
| `/api/diaries` | GET | 日记列表 |
| `/api/diary/<date>` | GET | 指定日期日记内容 |
| `/api/chat` | POST | AI 对话 |
| `/api/diary/analyze` | POST | 日记情绪分析 |
| `/api/profile/generate` | POST | 生成人格画像 |
| `/api/timeline/generate` | POST | 生成情绪时间轴 |
| `/api/search` | POST | 搜索笔记 |
| `/api/upload` | POST | 上传 Obsidian 文件夹 |
| `/api/upload/status` | GET | 上传状态检查 |
| `/api/study/tasks` | GET/POST | 考研任务管理 |
| `/api/study/pomodoro` | GET/POST | 番茄钟记录 |
| `/api/study/schedule` | POST | AI 学习计划 |

## 技术栈

- **后端**: Python + Flask + OpenAI SDK
- **前端**: 原生 HTML/CSS/JS（单文件）
- **AI**: mimo API（兼容 OpenAI 格式）
- **部署**: Render / Gunicorn

## License

MIT
