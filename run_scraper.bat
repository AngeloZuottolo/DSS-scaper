@echo off
title DSS SkyNet Scraper
color 0A

echo ================================================
echo    DSS SkyNet Fleet Scraper
echo ================================================
echo.

cd /d "%~dp0"

echo [*] Installing dependencies (if needed)...
pip install -r requirements.txt >nul 2>&1

echo.
echo [*] Running scraper...
python scraper.py

if errorlevel 1 (
    echo.
    echo [ERROR] Scraper failed. Press any key to exit...
    pause >nul
    exit /b 1
)

echo.
echo [*] Opening dashboard...
start "" "index.html"

echo.
echo [OK] Done! Dashboard opened in browser.
echo.
echo ================================================
echo Press any key to exit...
pause >nul
