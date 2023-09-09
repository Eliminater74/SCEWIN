@echo off
:: Request administrator privilieges
fltmc >nul 2>&1 || (
    PowerShell Start -Verb RunAs '%0' 2> nul || (
        echo error: right-click on the script and select "Run as administrator"
        pause
    )
    exit /b 1
)

pushd %~dp0
SCEWIN_64.exe /I /S BIOSSettings.txt
pause
