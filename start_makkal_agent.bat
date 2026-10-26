@echo off
title Makkal Agent - Meta AI Hackathon 2026
color 0A
cls
echo ==============================================================================
echo    Makkal Agent (makkal-agent-ai) - Meta AI Developer Hackathon 2026
echo    Autonomous Multimodal Citizen Action Agent for Tamil Nadu
echo    Powered by: Muse Spark, Muse Wonder, SAM 3.1 & Muse Voice
echo ==============================================================================
echo.

cd /d "%~dp0"

echo [*] Starting Makkal Agent Server on http://127.0.0.1:8001 ...
echo [*] Press CTRL+C to stop the server anytime.
echo.

start http://127.0.0.1:8001
"D:\api\arcreel\.venv\Scripts\uvicorn.exe" app:app --host 127.0.0.1 --port 8001 --reload

pause
