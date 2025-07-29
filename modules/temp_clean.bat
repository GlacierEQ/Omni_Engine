@echo off
echo 🔄 [TEMP CLEAN] Starting temp & cache purge...

del /s /f /q "%TEMP%\*.*" >nul 2>&1
del /s /f /q "C:\Windows\Temp\*.*" >nul 2>&1
rd /s /q "%TEMP%" >nul 2>&1
md "%TEMP%" >nul 2>&1

echo ✅ [TEMP CLEAN] Completed.
exit /b
