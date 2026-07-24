@echo off
setlocal
title Greys Label Studio - Upload to GitHub

REM ================================================================
REM  This folder is the boss: whatever is in it REPLACES what's on
REM  GitHub, every time. Any stuck git state gets wiped first.
REM
REM  EDIT THIS LINE if your GitHub repo has a different address:
set REPO_URL=https://github.com/brad695/jam-labels.git
REM ================================================================

cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
    echo.
    echo  Git is not installed on this computer.
    echo  Download it from:  https://git-scm.com/download/win
    echo  Install with default settings, then run this file again.
    echo.
    pause
    exit /b 1
)

echo Cleaning up old upload state...
if exist ".git" rmdir /s /q ".git"

git init -b main >nul
git remote add origin %REPO_URL%

echo.
echo Uploading this folder to %REPO_URL%
echo.

git add -A
git commit -m "Label studio update" >nul

git push --force origin main

if errorlevel 1 (
    echo.
    echo  Upload didn't finish.
    echo  - If a GitHub sign-in window popped up: sign in, run this again.
    echo  - Double-check the repo exists at:
    echo      %REPO_URL%
) else (
    echo.
    echo  Done. GitHub now matches this folder exactly.
)
echo.
pause
