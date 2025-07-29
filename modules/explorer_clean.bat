@echo off
echo 🧹 [EXPLORER CLEAN] Purging Explorer cache...

taskkill /f /im explorer.exe >nul 2>&1
del /f /s /q "%LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db" >nul 2>&1
start explorer.exe

echo ✅ [EXPLORER CLEAN] Completed.
exit /b
