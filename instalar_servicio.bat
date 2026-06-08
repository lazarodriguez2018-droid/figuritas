@echo off
:: ============================================================
::  BOT PENCA MUNDIAL 2026 — Instalador de Servicio Windows
::  Ejecutar como ADMINISTRADOR
:: ============================================================

title Instalador Bot Mundial 2026
color 0A

echo.
echo  ==========================================
echo   BOT PENCA MUNDIAL 2026 - INSTALADOR
echo  ==========================================
echo.

:: Verificar que se ejecuta como admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [ERROR] Necesitas ejecutar como ADMINISTRADOR
    echo.
    echo  Click derecho en este archivo ^> "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

:: ─── CONFIGURACION ────────────────────────────────────────
set /p TELEGRAM_TOKEN="Pega tu TELEGRAM TOKEN y presiona Enter: "
set /p GROQ_API_KEY="Pega tu GROQ API KEY y presiona Enter: "

echo.
echo  [1/5] Verificando Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo  [ERROR] Python no encontrado.
    echo  Descargalo de: https://www.python.org/downloads/
    echo  IMPORTANTE: Marcar "Add Python to PATH" al instalar
    pause
    exit /b 1
)
python --version
echo  OK

:: ─── CREAR CARPETA ────────────────────────────────────────
echo.
echo  [2/5] Creando carpeta del bot...
set BOT_DIR=C:\BotMundial
if not exist "%BOT_DIR%" mkdir "%BOT_DIR%"

:: Copiar archivos del bot (asume que estan en la misma carpeta que este .bat)
copy /Y "%~dp0bot.py"          "%BOT_DIR%\bot.py"          >nul
copy /Y "%~dp0predictor.py"    "%BOT_DIR%\predictor.py"    >nul
copy /Y "%~dp0partidos.py"     "%BOT_DIR%\partidos.py"     >nul
copy /Y "%~dp0requirements.txt" "%BOT_DIR%\requirements.txt" >nul
echo  Archivos copiados a C:\BotMundial\
echo  OK

:: ─── INSTALAR DEPENDENCIAS ────────────────────────────────
echo.
echo  [3/5] Instalando dependencias Python...
pip install -r "%BOT_DIR%\requirements.txt" --quiet
if %errorLevel% neq 0 (
    echo  [ERROR] Fallo la instalacion de dependencias
    pause
    exit /b 1
)
echo  OK

:: ─── CREAR SCRIPT DE ARRANQUE CON VARIABLES ───────────────
echo.
echo  [4/5] Creando script de arranque...

(
echo @echo off
echo set TELEGRAM_TOKEN=%TELEGRAM_TOKEN%
echo set GROQ_API_KEY=%GROQ_API_KEY%
echo cd /d C:\BotMundial
echo python bot.py
) > "%BOT_DIR%\arrancar.bat"

:: Script VBS para arrancar SIN ventana visible
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run "cmd /c C:\BotMundial\arrancar.bat", 0, False
) > "%BOT_DIR%\arrancar_oculto.vbs"

echo  OK

:: ─── REGISTRAR EN INICIO DE WINDOWS ──────────────────────
echo.
echo  [5/5] Registrando en inicio de Windows...

:: Crear acceso directo en la carpeta Startup de Windows
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
copy /Y "%BOT_DIR%\arrancar_oculto.vbs" "%STARTUP%\BotMundial.vbs" >nul
echo  OK

:: ─── ARRANCAR AHORA ───────────────────────────────────────
echo.
echo  Arrancando el bot ahora...
start "" "%BOT_DIR%\arrancar_oculto.vbs"
timeout /t 3 >nul

echo.
echo  ==========================================
echo   INSTALACION COMPLETADA CON EXITO
echo  ==========================================
echo.
echo   El bot esta corriendo en segundo plano.
echo   Arrancara automaticamente con Windows.
echo   No aparece en ninguna ventana visible.
echo.
echo   Para verificar que funciona:
echo   Abre Telegram y escribe "prediccion" al bot.
echo.
echo   Para detenerlo: ejecuta detener_bot.bat
echo.
pause
