@echo off
title Rathinam Smart Canteen Hub
echo ========================================================
echo   Rathinam College Smart Canteen Hub
echo   Multi-Canteen Smart Ordering & Crowd Management
echo ========================================================
echo.
echo Installing/Verifying dependencies...
python -m pip install -r requirements.txt
echo.
echo Starting FastAPI Server on http://127.0.0.1:8005 ...
echo.
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8005 --reload
pause
