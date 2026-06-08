"""
Motor de predicciones 100% GRATIS.
Groq (LLM gratis) + DuckDuckGo (búsqueda web gratis, sin API key)
"""

import logging
import json
import re
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from urllib.error import URLError
import ssl

logger = logging.getLogger(__name__)

# ─── BÚSQUEDA WEB GRATIS (DuckDuckGo HTML, sin API) ─────────────────────────

def buscar_web(query: str, max_resultados: int = 5) -> str:
    """Busca en DuckDuckGo y retorna resumen de resultados. Sin API key."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Extraer snippets de resultados
        snippets = re.findall(
            r'class="result__snippet"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
        titles = re.findall(
            r'class="result__a"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )

        # Limpiar HTML tags
        def clean(s):
            s = re.sub(r'<[^>]+>', '', s)
            s = re.sub(r'\s+', ' ', s).strip()
            return s

        resultados = []
        for i, (t, s) in enumerate(zip(titles, snippets)):
            if i >= max_resultados:
                break
            t_clean = clean(t)
            s_clean = clean(s)
            if t_clean and s_clean:
                resultados.append(f"• {t_clean}: {s_clean}")

        if not resultados:
            return "Sin resultados encontrados."

        return "\n".join(resultados)

    except Exception as e:
        logger.warning(f"Error buscando '{query}': {e}")
        return f"No se pudo buscar: {e}"


def recopilar_contexto(local: str, visitante: str, fase: str) -> str:
    """Hace 3 búsquedas rápidas y consolida el contexto para el LLM."""
    logger.info(f"🔍 Buscando info: {local} vs {visitante}")

    queries = [
        f"{local} {visitante} Mundial 2026 prediccion apuestas",
        f"{local} seleccion forma reciente lesiones 2026",
        f"{visitante} seleccion forma reciente lesiones 2026",
    ]

    resultados = {}
    for q in queries:
        resultados[q] = buscar_web(q, max_resultados=4)

    contexto = f"""BÚSQUEDAS WEB REALIZADAS:

[{local} vs {visitante} - Predicciones]:
{resultados[queries[0]]}

[Noticias {local}]:
{resultados[queries[1]]}

[Noticias {visitante}]:
{resultados[queries[2]]}
"""
    return contexto


# ─── GROQ LLM (100% GRATIS) ──────────────────────────────────────────────────

import os

try:
    from groq import Groq
    GROQ_DISPONIBLE = True
except ImportError:
    GROQ_DISPONIBLE = False
    logger.error("groq no instalado. Ejecutá: pip install groq")


SYSTEM_PROMPT = """Eres un experto analista de apuestas deportivas del Mundial de Fútbol 2026.
Tu especialidad es predecir MARCADORES EXACTOS para pencas con amigos.

REGLAS DE LA PENCA:
- Solo se puede poner UN resultado exacto (ej: 2-1, 0-0, 1-3)
- Puntuación: resultado exacto = máximos puntos | acertar ganador/empate = puntos parciales
- Por eso tu estrategia debe ser: no solo predecir quién gana, sino el MARCADOR MÁS PROBABLE

FORMATO DE RESPUESTA — siempre usá este formato exacto en Markdown para Telegram:

⚽ *[LOCAL] vs [VISITANTE]*
📅 [FECHA/HORA] | 🏟️ [ESTADIO] | [FASE]

━━━━━━━━━━━━━━━━━━━━━━
🔍 *ANÁLISIS*
━━━━━━━━━━━━━━━━━━━━━━

📊 *Forma reciente:*
[LOCAL]: W W D L W (últimos 5)
[VISITANTE]: W L W W D (últimos 5)

⚡ *Factores clave:*
• [factor 1]
• [factor 2]
• [factor 3]

📰 *Contexto actual:*
• [noticia/dato relevante 1]
• [noticia/dato relevante 2]

━━━━━━━━━━━━━━━━━━━━━━
📈 *PROBABILIDADES*
━━━━━━━━━━━━━━━━━━━━━━

🏆 Gana [LOCAL]: XX%
🤝 Empate: XX%
🏆 Gana [VISITANTE]: XX%

━━━━━━━━━━━━━━━━━━━━━━
🎯 *MI PREDICCIÓN PARA LA PENCA*
━━━━━━━━━━━━━━━━━━━━━━

✅ *Ponelo: [LOCAL] X — Y [VISITANTE]*

💡 *Por qué este marcador:*
[2-3 líneas explicando por qué ese marcador exacto es el más probable]

🔄 *Alternativos:*
• [LOCAL] A-B [VISITANTE] (XX%)
• [LOCAL] C-D [VISITANTE] (XX%)

⚠️ *Ojo con:* [factor que podría cambiar todo]

_Análisis generado el [TIMESTAMP]_"""


class WorldCupPredictor:
    def __init__(self, api_key: str = None):
        groq_key = api_key or os.getenv("GROQ_API_KEY", "")
        if GROQ_DISPONIBLE and groq_key:
            self.client = Groq(api_key=groq_key)
            logger.info("✅ Groq inicializado correctamente")
        else:
            self.client = None
            logger.warning("⚠️ Groq no disponible — sin cliente LLM")

    async def analizar_partido(self, partido: dict) -> str:
        local     = partido["local"]
        visitante = partido["visitante"]
        fase      = partido.get("fase", "Mundial 2026")
        estadio   = partido.get("estadio", "Por confirmar")
        fecha_dt  = partido["datetime"]
        hora_str  = fecha_dt.strftime("%d/%m/%Y %H:%M") + " (UY)"
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        # 1. Búsqueda web gratis
        contexto_web = recopilar_contexto(local, visitante, fase)

        # 2. Prompt para el LLM
        prompt = f"""Analizá este partido del Mundial 2026 para una penca:

PARTIDO: {local} vs {visitante}
FECHA: {hora_str}
ESTADIO: {estadio}
FASE: {fase}

INFORMACIÓN RECOPILADA DE INTERNET:
{contexto_web}

Con base en esta información y tu conocimiento sobre ambas selecciones, generá el análisis completo siguiendo el formato indicado.
Timestamp: {timestamp}"""

        if not self.client:
            return (
                f"⚽ *{local} vs {visitante}*\n\n"
                f"❌ Bot no configurado. Revisá la GROQ\\_API\\_KEY.\n"
                f"Obtené tu key gratis en: console.groq.com"
            )

        try:
            logger.info(f"🤖 Generando predicción con Groq: {local} vs {visitante}")
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",   # modelo gratis, muy capaz
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            texto = response.choices[0].message.content
            logger.info(f"✅ Predicción generada para {local} vs {visitante}")
            return texto

        except Exception as e:
            logger.error(f"Error Groq: {e}")
            return (
                f"⚽ *{local} vs {visitante}*\n\n"
                f"❌ Error al generar predicción: `{e}`\n\n"
                f"Verificá tu GROQ\\_API\\_KEY en console.groq.com"
            )
