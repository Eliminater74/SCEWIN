@echo off
:: Request administrator privilieges
fltmc >nul 2>&1 || (
    echo info: administrator privileges are required.
    PowerShell Start -Verb RunAs '%0' 2> nul || (
        echo info: right-click on the script and select "Run as administrator".
        pause & exit /b 1
    )
    exit /b
)

pushd %~dp0
SCEWIN_64.exe /O /S BIOSSettings.txt
pause
