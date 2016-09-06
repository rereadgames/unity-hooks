@echo off
if not exist ".git" (
    echo Not in a git repository
    exit /b 1
)

for %%A in (pre-commit post-checkout post-merge) do (
	mklink "%cd%\.git\hooks\%%A" "%~dp0hooks\delegate.py"
)

if %errorlevel%==0 (
	echo Installed Unity hooks.
) else (
	echo Unable to install Unity hooks
)
