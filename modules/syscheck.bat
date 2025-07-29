@echo off
echo 🩺 [SYS CHECK] Starting SFC scan...

sfc /scannow

echo 🛠 [SYS CHECK] Starting DISM restore...

DISM /Online /Cleanup-Image /RestoreHealth

echo ✅ [SYS CHECK] Completed.
exit /b
