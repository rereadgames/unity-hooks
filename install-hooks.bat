@echo off
if not exist ".git" (
    echo Not in a git repository
    exit /b 1
)

mklink /d "%cd%\.git\hooks" "%~dp0hooks"
if %errorlevel%==0 (
	echo Installed Unity hooks.
) else (
	echo Unable to install Unity hooks
)