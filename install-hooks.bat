@echo off
if not exist ".git" (
    echo Not in a git repository
    exit /b 1
)

FOR %%A IN (pre-commit post-checkout post-merge) DO mklink /d "%cd%\.git\hooks\%A" "%~dp0delegate.py"

if %errorlevel%==0 (
	echo Installed Unity hooks.
) else (
	echo Unable to install Unity hooks
)
