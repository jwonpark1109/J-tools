@echo off
title J Tool launcher
title start tool...
title J tools - AutoShutdown
setlocal enabledelayedexpansion

:: setting.txt에서 app 값 읽기
for /f "tokens=1,2 delims==" %%A in (setting.txt) do (
    if /i "%%A"=="app" set app=%%B
)

if not defined app (
    echo no found "setting.txt"
    pause
    exit /b
)

echo Shutdown "%app%"... 0%%
timeout /t 1 >nul
cls

echo Shutdown "%app%"... 28%%
timeout /t 1 >nul
cls

echo Shutdown "%app%"... 56%%
timeout /t 1 >nul

taskkill /f /im "%app%" >nul 2>&1
cls

echo Shutdown "%app%"... 78%%
timeout /t 1 >nul
cls

echo Shutdown "%app%"... 100%%
echo Done sir!
echo Auto Shutdown | by J Tools
pause
