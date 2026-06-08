@echo off
title Detener Bot Mundial 2026
color 0C

echo.
echo  Deteniendo Bot Mundial 2026...
echo.

taskkill /F /IM python.exe /FI "WINDOWTITLE eq *bot*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq python.exe" >nul 2>&1

echo  Bot detenido.
echo.
echo  Para volver a arrancarlo: ejecuta C:\BotMundial\arrancar_oculto.vbs
echo.
pause
