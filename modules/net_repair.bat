@echo off
echo 🌐 [NET REPAIR] Flushing DNS & resetting network stack...

ipconfig /flushdns
netsh winsock reset
netsh int ip reset

echo ✅ [NET REPAIR] Completed.
exit /b
