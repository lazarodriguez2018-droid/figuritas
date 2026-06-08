"""
🏆 BOT PENCA MUNDIAL 2026
Experto en apuestas deportivas - Predicciones con IA
"""

import logging
import os
import sys
from datetime import datetime
import pytz

from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from predictor import WorldCupPredictor
from partidos import PARTIDOS_MUNDIAL_2026

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────

TELEGRAM_TOKEN    = os.getenv("TELEGRAM_TOKEN", "TU_NUEVO_TOKEN_AQUI")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
CHAT_IDS          = os.getenv("CHAT_IDS", "6447149607").split(",")

TIMEZONE    = pytz.timezone("America/Montevideo")
HORAS_ANTES = 3

# ─── LOGGING: archivo + consola ──────────────────────────────────────────────

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

# ─── PREDICTOR ────────────────────────────────────────────────────────────────

api_key = GROQ_API_KEY or ANTHROPIC_API_KEY
predictor = WorldCupPredictor(api_key=api_key)

# ─── UTILS ───────────────────────────────────────────────────────────────────

def get_proximo_partido():
    ahora = datetime.now(TIMEZONE)
    futuros = [p for p in PARTIDOS_MUNDIAL_2026 if p["datetime"] > ahora]
    return futuros[0] if futuros else None

# ─── HANDLERS ────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"🏆 *BOT PENCA MUNDIAL 2026* 🏆\n\n"
        f"¡Hola! Soy tu experto en apuestas del Mundial.\n\n"
        f"📋 *Cómo usarme:*\n"
        f"• Escribí *prediccion* → análisis del próximo partido\n"
        f"• /proximo → ver cuándo es el siguiente\n"
        f"• /hoy → partidos de hoy\n"
        f"• /ayuda → cómo funciona\n\n"
        f"_Las predicciones también se envían automáticamente 3 horas antes de cada partido._\n\n"
        f"📨 Tu Chat ID: `{chat_id}`",
        parse_mode="Markdown"
    )

async def cmd_proximo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ahora   = datetime.now(TIMEZONE)
    partido = get_proximo_partido()
    if not partido:
        await update.message.reply_text("✅ Ya terminaron todos los partidos del Mundial.")
        return
    delta   = partido["datetime"] - ahora
    horas   = int(delta.total_seconds() // 3600)
    minutos = int((delta.total_seconds() % 3600) // 60)
    await update.message.reply_text(
        f"⚽ *PRÓXIMO PARTIDO*\n\n"
        f"🆚 {partido['local']} vs {partido['visitante']}\n"
        f"📅 {partido['datetime'].strftime('%d/%m/%Y %H:%M')} (UY)\n"
        f"🏟️ {partido['estadio']}\n"
        f"🔢 Fase: {partido['fase']}\n\n"
        f"⏳ Faltan *{horas}h {minutos}m*\n\n"
        f"_Escribí *prediccion* para el análisis completo_",
        parse_mode="Markdown"
    )

async def cmd_hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ahora      = datetime.now(TIMEZONE)
    hoy_inicio = ahora.replace(hour=0,  minute=0,  second=0,  microsecond=0)
    hoy_fin    = ahora.replace(hour=23, minute=59, second=59, microsecond=0)
    partidos_hoy = [p for p in PARTIDOS_MUNDIAL_2026 if hoy_inicio <= p["datetime"] <= hoy_fin]
    if not partidos_hoy:
        await update.message.reply_text("📅 No hay partidos del Mundial hoy.")
        return
    texto = f"📅 *PARTIDOS HOY — {ahora.strftime('%d/%m/%Y')}*\n\n"
    for p in partidos_hoy:
        emoji = "✅" if p["datetime"] < ahora else "⏰"
        texto += f"{emoji} *{p['local']} vs {p['visitante']}* — {p['datetime'].strftime('%H:%M')}\n_{p['fase']}_\n\n"
    await update.message.reply_text(texto, parse_mode="Markdown")

async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *CÓMO FUNCIONA EL BOT*\n\n"
        "1️⃣ Escribí *prediccion* → análisis completo del próximo partido\n\n"
        "2️⃣ Automáticamente manda predicciones *3 horas antes* de cada partido\n\n"
        "3️⃣ Cada predicción incluye:\n"
        "   • 🎯 Marcador exacto recomendado\n"
        "   • 📊 Probabilidades (gana A / empate / gana B)\n"
        "   • 🔍 Forma reciente de cada equipo\n"
        "   • 📰 Noticias del momento\n"
        "   • 💡 Estrategia para la penca\n\n"
        "⚠️ _Las predicciones son análisis probabilísticos, no garantías._",
        parse_mode="Markdown"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (update.message.text or "").lower().strip()
    palabras_clave = ["prediccion", "predicción", "predic", "pred"]
    if not any(texto.startswith(p) for p in palabras_clave):
        return

    partido = get_proximo_partido()
    if not partido:
        await update.message.reply_text("✅ No quedan más partidos en el fixture del Mundial 2026.")
        return

    ahora = datetime.now(TIMEZONE)
    delta = partido["datetime"] - ahora
    horas = int(delta.total_seconds() // 3600)
    mins  = int((delta.total_seconds() % 3600) // 60)

    msg = await update.message.reply_text(
        f"🔍 *Analizando el próximo partido...*\n\n"
        f"⚽ {partido['local']} vs {partido['visitante']}\n"
        f"⏳ En {horas}h {mins}m\n\n"
        f"_Buscando noticias, estadísticas y predicciones... (30-60 seg)_",
        parse_mode="Markdown"
    )

    try:
        prediccion = await predictor.analizar_partido(partido)
        await msg.edit_text(prediccion, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        await msg.edit_text(f"❌ Error al generar la predicción: {e}")

async def verificar_y_enviar_predicciones(bot: Bot):
    ahora = datetime.now(TIMEZONE)
    for partido in PARTIDOS_MUNDIAL_2026:
        delta_min = (partido["datetime"] - ahora).total_seconds() / 60
        if 178 <= delta_min <= 183:
            logger.info(f"⚡ Auto-predicción: {partido['local']} vs {partido['visitante']}")
            try:
                prediccion = await predictor.analizar_partido(partido)
                for chat_id in CHAT_IDS:
                    await bot.send_message(
                        chat_id=chat_id.strip(),
                        text=f"🤖 *PREDICCIÓN AUTOMÁTICA — 3 HORAS ANTES*\n\n{prediccion}",
                        parse_mode="Markdown"
                    )
                logger.info("✅ Enviada")
            except Exception as e:
                logger.error(f"❌ Error: {e}")

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    logger.info("🚀 Iniciando Bot Penca Mundial 2026...")
    logger.info(f"📁 Log guardado en: {LOG_FILE}")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("proximo", cmd_proximo))
    app.add_handler(CommandHandler("hoy",     cmd_hoy))
    app.add_handler(CommandHandler("ayuda",   cmd_ayuda))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        verificar_y_enviar_predicciones,
        "interval",
        minutes=5,
        args=[app.bot],
        id="check_partidos"
    )
    scheduler.start()

    logger.info("✅ Bot corriendo. Esperando mensajes...")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
