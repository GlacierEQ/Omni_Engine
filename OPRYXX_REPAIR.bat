:: OPRYXX_REPAIR 3.0+ Supernova Edition
@echo off
setlocal enabledelayedexpansion

:: === CONFIGURE PATHS ===
set "DOCUMENTS=%USERPROFILE%\Documents"
set "DOWNLOADS=%USERPROFILE%\Downloads"
set "MUSIC=%USERPROFILE%\Music"
set "VIDEO=%USERPROFILE%\Videos"
set "BACKUP=%USERPROFILE%\OpryxxBackups"
set "LOGFILE=%~dp0OPRYXX_LOG.txt"

if not exist "%BACKUP%" mkdir "%BACKUP%"

:: === DEFINE DATE ===
for /f "tokens=2 delims==." %%I in ('"wmic os get LocalDateTime /value"') do set datetime=%%I
set "YYYY=!datetime:~0,4!"
set "MM=!datetime:~4,2!"
set "DD=!datetime:~6,2!"
set "TODAY=!YYYY!!MM!!DD!"

:: === START LOG ===
echo ============================== >> "%LOGFILE%"
echo OPRYXX REPAIR RUN - !TODAY! >> "%LOGFILE%"
echo ============================== >> "%LOGFILE%"

:: === PROCESS FILES ===
echo Scanning libraries recursively...
for %%F in (%DOCUMENTS% %DOWNLOADS% %MUSIC% %VIDEO%) do (
    if exist "%%F" (
        for /R "%%F" %%G in (*.*) do (
            set "FILE=%%G"
            if exist "!FILE!" (
                set "EXT=%%~xG"
                set "NAME=%%~nxG"

                :: Determine target folder
                set "TARGET="
                if /I "!EXT!"==".doc" set TARGET=%DOCUMENTS%
                if /I "!EXT!"==".docx" set TARGET=%DOCUMENTS%
                if /I "!EXT!"==".pdf" set TARGET=%DOCUMENTS%
                if /I "!EXT!"==".txt" set TARGET=%DOCUMENTS%
                if /I "!EXT!"==".zip" set TARGET=%DOCUMENTS%
                if /I "!EXT!"==".mp3" set TARGET=%MUSIC%
                if /I "!EXT!"==".wav" set TARGET=%MUSIC%
                if /I "!EXT!"==".flac" set TARGET=%MUSIC%
                if /I "!EXT!"==".mp4" set TARGET=%VIDEO%
                if /I "!EXT!"==".mkv" set TARGET=%VIDEO%
                if /I "!EXT!"==".avi" set TARGET=%VIDEO%
                if /I "!EXT!"==".mov" set TARGET=%VIDEO%

                if defined TARGET (
                    echo Found: !FILE!
                    set /p DESC="Enter description for !NAME!: "
                    set "NEWNAME=!TODAY! !DESC!!EXT!"

                    :: Backup original
                    copy /Y "!FILE!" "%BACKUP%\!NAME!" >> "%LOGFILE%" 2>&1

                    :: Move and rename
                    move "!FILE!" "!TARGET!\!NEWNAME!" >> "%LOGFILE%" 2>&1
                    echo Moved to: !TARGET!\!NEWNAME!
                    echo !FILE! -> !TARGET!\!NEWNAME! >> "%LOGFILE%"
                )
            )
        )
    )
)

echo Sorting complete. Log saved to %LOGFILE%.
pause
