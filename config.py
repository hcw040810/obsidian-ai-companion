import os
from dotenv import load_dotenv

load_dotenv()

# Flask session 密钥
SECRET_KEY = os.getenv("SECRET_KEY", "obsidian-ai-companion-default-key")

# mimo API 配置
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://api.mimo.com/v1")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2.5")

# Obsidian 仓库路径 — 优先用环境变量，否则用本地路径
_default_vault = os.path.join(os.path.dirname(__file__), "vault")
VAULT_PATH = os.getenv("VAULT_PATH", _default_vault)

# 如果默认 vault 目录不存在，尝试本地 Obsidian 路径
if not os.path.isdir(VAULT_PATH):
    _local_vault = r"C:\Users\HP\OneDrive\应用\remotely-save\个人"
    if os.path.isdir(_local_vault):
        VAULT_PATH = _local_vault

# 日记目录
DIARY_DIR = os.path.join(VAULT_PATH, "01 日记")

# 总结输出目录
SUMMARY_DIR = os.path.join(DIARY_DIR, "summaries")
