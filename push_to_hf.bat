@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title Push to Hugging Face Spaces (quangame52/VieNeu-TTS)
cd /d "%~dp0"
echo ==================================================
echo   DAY CODE LEN HUGGING FACE SPACES
echo ==================================================
echo.
echo Remote: https://huggingface.co/spaces/quangame52/VieNeu-TTS
echo.

git push https://huggingface.co/spaces/quangame52/VieNeu-TTS main

echo.
pause
