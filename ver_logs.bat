@echo off
title Logs Bot Mundial 2026
color 0B

echo.
echo  ==========================================
echo   LOGS DEL BOT MUNDIAL 2026
echo  ==========================================
echo.

set LOG_FILE=C:\BotMundial\bot.log

if not exist "%LOG_FILE%" (
    echo  No hay logs todavia. El bot puede no haber arrancado aun.
    echo.
    echo  Intenta arrancar el bot con: C:\BotMundial\arrancar_oculto.vbs
    pause
    exit /b
)

echo  Ultimas 50 lineas del log:
echo.
powershell -command "Get-Content '%LOG_FILE%' -Tail 50"
echo.
pause
