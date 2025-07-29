@echo off
echo 🧬 [PAGEFILE RESET] Reconfiguring virtual memory management...

wmic pagefile set AutomaticManagedPagefile=True

echo ✅ [PAGEFILE RESET] Completed.
exit /b
