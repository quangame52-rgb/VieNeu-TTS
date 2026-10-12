@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title VieNeu-TTS OpenAI Speech API
cd /d "%~dp0"
echo ==================================================
echo   KHOI DONG VIENEU-TTS OPENAI-COMPATIBLE API
echo ==================================================
echo.
echo Endpoint: http://127.0.0.1:8000/v1/audio/speech
echo Nhan Ctrl+C de dung.
echo.

.venv\Scripts\python.exe -m apps.openai_speech

pause
