powershell
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show("OPRYXX REPAIR DAEMON ACTIVE — Monitoring Repairs...", "OPRYXX: BlackEcho Watcher", "OK", "Information")

Launch it from Opryxx_repair.bat with:
start powershell -Windowstyle Hidden - File status_gui.ps1