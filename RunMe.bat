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

:menu
cls
echo SCEWIN NVRAM Utility
echo ====================
echo.
echo 1. Export NVRAM settings
echo 2. Import NVRAM settings
echo 3. Exit
echo.
echo Please select an option:

choice /C 123 /N /M "Enter your choice:"
echo.

:: Option 1: Export
if "%errorlevel%" == "1" goto confirm_export

:: Option 2: Import
if "%errorlevel%" == "2" goto confirm_import

:: Option 3: Exit
if "%errorlevel%" == "3" goto end_script

:confirm_export
echo You have chosen to export NVRAM settings.
choice /M "Are you sure you want to proceed with export"
if errorlevel 2 goto menu
goto export_nvram

:confirm_import
echo You have chosen to import NVRAM settings.
choice /M "Are you sure you want to proceed with import"
if errorlevel 2 goto menu
goto import_nvram

:export_nvram
call :check_files "amifldrv64.sys" "amigendrv64.sys"
echo Running SCEWIN_64.exe to export NVRAM settings...
SCEWIN_64.exe /O /S nvram.txt 2> log-file.txt
goto operation_complete

:import_nvram
call :check_files "amifldrv64.sys" "amigendrv64.sys" "nvram.txt"
echo Running SCEWIN_64.exe to import NVRAM settings...
SCEWIN_64.exe /I /S nvram.txt 2> log-file.txt
goto operation_complete

:check_files
echo Checking necessary files...
for %%a in (%*) do (
    if not exist "%%~a" (
        echo error: %%~a not found in the current directory
        pause
        goto menu
    )
)
goto :eof

:operation_complete
if errorlevel 1 (
    echo There was an error running SCEWIN_64.exe. Check log-file.txt for details.
) else (
    echo Operation completed successfully.
)
pause
goto menu

:end_script
exit /b 0
