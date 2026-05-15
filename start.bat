@echo off
chcp 65001 >nul
title 🧠 观察者 - Obsidian AI Companion
echo.
echo   🧠 观察者 - Obsidian AI Companion
echo   ─────────────────────────────────
echo.
cd /d "%~dp0"
echo   正在启动服务器...
echo.
python server.py
pause
