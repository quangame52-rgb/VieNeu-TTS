@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title VieNeu-TTS Web UI (Public Share)
cd /d "%~dp0"

.venv\Scripts\python.exe start_share.py

pause
