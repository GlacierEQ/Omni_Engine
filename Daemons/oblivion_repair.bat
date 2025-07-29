@echo off
title OPRYXX: Oblivion Repair Chain [Root-Level Recovery + Echo Sync]
setlocal enabledelayedexpansion

:: 🔐 SET OPRYXX PATH + TIMESTAMP
set OPRYXX_LOG=C:\OPRYXX_LOGS\oblivion
set timestamp=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
mkdir "%OPRYXX_LOG%" >nul 2>&1

:: 🔮 INTRO
echo.
echo ╔════════════════════════════════════════════╗
echo ║      🜏 OPRYXX: Oblivion Repair Chain       ║
echo ║   Rootbearer: The Memory That Remembers    ║
echo ╚════════════════════════════════════════════╝
echo.
echo 🧠 Initiating BlackEcho Stabilization...
echo 🔧 All operations will be logged to:
echo    %OPRYXX_LOG%\repair_%timestamp%.log
echo.

:: 🌌 STEP 1: PURGE TEMP / SYSTEM CACHE
echo 🔄 Purging temp & system cache...
del /s /f /q "%TEMP%\*.*" >> "%OPRYXX_LOG%\repair_%timestamp%.log" 2>&1
del /s /f /q "C:\Windows\Temp\*.*" >> "%OPRYXX_LOG%\repair_%timestamp%.log" 2>&1
rd /s /q "%TEMP%" >> "%OPRYXX_LOG%\repair_%timestamp%.log" 2>&1
md "%TEMP%" >> "%OPRYXX_LOG%\repair_%timestamp%.log" 2>&1

:: ⚙️ STEP 2: SYSTEM FILE SCAN + RESTORE
echo 🩺 Running SFC...
sfc /scannow >> "%OPRYXX_LOG%\repair_%timestamp%.log"

echo 🛠 Running DISM health restore...
DISM /Online /Cleanup-Image /RestoreHealth >> "%OPRYXX_LOG%\repair_%timestamp%.log"

:: 🌐 STEP 3: NETWORK STACK RESET
echo 🌐 Flushing DNS + network reset...
ipconfig /flushdns >> "%OPRYXX_LOG%\repair_%timestamp%.log"
netsh winsock reset >> "%OPRYXX_LOG%\repair_%timestamp%.log"
netsh int ip reset >> "%OPRYXX_LOG%\repair_%timestamp%.log"

:: 🧹 STEP 4: EXPLORER CLEAN
taskkill /f /im explorer.exe >nul
del /f /s /q "%LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db" >> "%OPRYXX_LOG%\repair_%timestamp%.log" 2>&1
start explorer.exe

:: 🧠 STEP 5: MEMORY + PAGEFILE REBUILD
wmic pagefile set AutomaticManagedPagefile=True >> "%OPRYXX_LOG%\repair_%timestamp%.log"

:: 📚 STEP 6: ECHO LOG ENTRY
echo [REPAIR EVENT] Oblivion Repair Chain activated on %date% %time% >> "%OPRYXX_LOG%\blackecho_index.md"
echo [Rootbearer]: GlacierEQ >> "%OPRYXX_LOG%\blackecho_index.md"
echo [Pulse Vector]: FULL SYSTEM RESET >> "%OPRYXX_LOG%\blackecho_index.md"
echo [Echo Status]: Logging successful to %OPRYXX_LOG%\repair_%timestamp%.log >> "%OPRYXX_LOG%\blackecho_index.md"

:: 🌀 STEP 7: CHKDSK QUEUE + SAFE MODE
echo 🧨 CHKDSK enqueued, rebooting into Safe Mode...
echo Y | chkdsk C: /F /R /X >> "%OPRYXX_LOG%\repair_%timestamp%.log"
bcdedit /set {current} safeboot minimal

:: ⏳ WAIT + REBOOT
timeout /t 20
shutdown /r /t 0

endlocal
