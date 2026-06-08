# 🏆 BOT PENCA MUNDIAL 2026 — 100% GRATIS

## SERVICIOS USADOS (todos gratis)
| Servicio | Para qué | Costo |
|----------|----------|-------|
| Telegram Bot API | El bot | ✅ Gratis |
| Groq API | LLM (IA) | ✅ Gratis |
| DuckDuckGo | Búsqueda web | ✅ Gratis |

---

## PASO 1 — Obtené el Token de Telegram

1. Abrí Telegram → buscá **@BotFather**
2. Escribí `/newbot`
3. Seguí los pasos, te dará un token como:
   `1234567890:ABCdefGHIjklMNO...`

> ⚠️ Nunca compartas este token públicamente

---

## PASO 2 — Obtené la Groq API Key (gratis)

1. Entrá a **console.groq.com**
2. Creá una cuenta (Google login disponible)
3. Menú izquierdo → **API Keys** → **Create API Key**
4. Copiá la key (empieza con `gsk_...`)

---

## PASO 3 — Instalación

```bash
pip install -r requirements.txt
```

---

## PASO 4 — Configurar y correr

```bash
# Windows
set TELEGRAM_TOKEN=tu_token_aqui
set GROQ_API_KEY=gsk_tu_key_aqui
python bot.py

# Linux / Mac
export TELEGRAM_TOKEN="tu_token_aqui"
export GROQ_API_KEY="gsk_tu_key_aqui"
python bot.py
```

---

## USO DEL BOT

| Escribís | Resultado |
|----------|-----------|
| `prediccion` | Análisis del próximo partido |
| `/proximo` | Cuándo es el siguiente partido |
| `/hoy` | Partidos de hoy |
| `/ayuda` | Cómo funciona |
| Automático | 3 horas antes de cada partido |

---

## CORRER 24/7 EN WINDOWS (sin cerrar la PC)

Creá un archivo `arrancar_bot.bat`:
```bat
@echo off
set TELEGRAM_TOKEN=tu_token
set GROQ_API_KEY=gsk_tu_key
python bot.py
pause
```
Doble click para arrancar. Minimizalo y listo.

## CORRER EN LINUX / VPS

```bash
nohup python bot.py > bot.log 2>&1 &
```
