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
echo This will check for necessary driver files.
choice /M "Are you sure you want to continue"
if errorlevel 2 exit /b

:: Loop to check for the existence of each driver file
for %%a in ("amifldrv64.sys", "amigendrv64.sys") do (
    if not exist "%%~a" (
        echo error: %%~a not found in the current directory
        pause
        exit /b 1    
    )    
)

:: Confirmation before running SCEWIN_64.exe
echo This will run SCEWIN_64.exe with output to nvram.txt and log errors to log-file.txt.
choice /M "Are you sure you want to proceed"
if errorlevel 2 exit /b

:: Execute SCEWIN_64.exe with arguments
SCEWIN_64.exe /O /S nvram.txt 2> log-file.txt
if errorlevel 1 (
    echo There was an error running SCEWIN_64.exe. Check log-file.txt for details.
)

:: Pause to view the SCEWIN_64.exe output
pause

:: End of the script
exit /b 0
