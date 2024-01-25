@echo off
:: Request administrator privileges
fltmc >nul 2>&1 || (
    PowerShell Start -Verb RunAs '%0' 2> nul || (
        echo error: right-click on the script and select "Run as administrator"
        pause
    )
    exit /b 1
)

:: Change to the directory where the batch file is located
pushd %~dp0

:: Confirmation for checking the necessary files
echo This script will check for necessary driver files and the NVRAM script file.
choice /M "Are you sure you want to continue"
if errorlevel 2 exit /b

:: Loop to check for the existence of each driver file and NVRAM script file
for %%a in ("amifldrv64.sys", "amigendrv64.sys", "nvram.txt") do (
    if not exist "%%~a" (
        echo error: %%~a not found in the current directory

        if "%%~a" == "nvram.txt" (
            echo Please rename your NVRAM script file to "nvram.txt" or run "Export.bat" to create it
        )

        pause
        exit /b 1    
    )    
)

:: Confirmation before running SCEWIN_64.exe
echo This script will run SCEWIN_64.exe to import NVRAM settings from nvram.txt.
choice /M "Are you sure you want to import NVRAM settings"
if errorlevel 2 exit /b

:: Execute SCEWIN_64.exe with arguments
SCEWIN_64.exe /I /S nvram.txt 2> log-file.txt
if errorlevel 1 (
    echo There was an error running SCEWIN_64.exe. Check log-file.txt for details.
)

:: Pause to view the SCEWIN_64.exe output
pause

:: End of the script
exit /b 0
