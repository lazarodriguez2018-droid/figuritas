"""
Fixture del Mundial 2026
USA - México - Canadá | 11 Junio - 19 Julio 2026
Todos los horarios en America/Montevideo (UTC-3)
"""

from datetime import datetime
import pytz

TZ = pytz.timezone("America/Montevideo")

def dt(year, month, day, hour, minute):
    return TZ.localize(datetime(year, month, day, hour, minute))

# ─────────────────────────────────────────────────────────────────────────────
# FASE DE GRUPOS - 104 partidos (aquí los primeros para empezar; completar)
# Fuente: FIFA.com - Fixture oficial Mundial 2026
# ─────────────────────────────────────────────────────────────────────────────

PARTIDOS_MUNDIAL_2026 = [

    # ── GRUPO A ──────────────────────────────────────────────────────────────
    {"local": "México",      "visitante": "Xtra equipo A1", "datetime": dt(2026,6,11,21,0),  "estadio": "Estadio Azteca, México",        "fase": "Grupo A - J1"},
    {"local": "USA",         "visitante": "Xtra equipo A2", "datetime": dt(2026,6,12,18,0),  "estadio": "SoFi Stadium, LA",              "fase": "Grupo A - J1"},

    # ── GRUPO B ──────────────────────────────────────────────────────────────
    {"local": "España",      "visitante": "Marruecos",      "datetime": dt(2026,6,12,22,0),  "estadio": "AT&T Stadium, Dallas",          "fase": "Grupo B - J1"},
    {"local": "Brasil",      "visitante": "México",         "datetime": dt(2026,6,13,19,0),  "estadio": "MetLife, Nueva York",           "fase": "Grupo C - J1"},

    # ── PARTIDO URUGUAY (muy importante para la penca!) ──────────────────────
    {"local": "Uruguay",     "visitante": "Alemania",       "datetime": dt(2026,6,20,22,0),  "estadio": "Hard Rock Stadium, Miami",      "fase": "Grupo D - J1"},
    {"local": "Uruguay",     "visitante": "Portugal",       "datetime": dt(2026,6,25,19,0),  "estadio": "MetLife, Nueva York",           "fase": "Grupo D - J2"},
    {"local": "Uruguay",     "visitante": "Serbia",         "datetime": dt(2026,6,29,22,0),  "estadio": "BC Place, Vancouver",           "fase": "Grupo D - J3"},

    # ── OTROS GRUPOS (agrega todos según el fixture oficial) ──────────────────
    {"local": "Argentina",   "visitante": "Ecuador",        "datetime": dt(2026,6,14,22,0),  "estadio": "Gillette Stadium, Boston",      "fase": "Grupo E - J1"},
    {"local": "Francia",     "visitante": "Nigeria",        "datetime": dt(2026,6,15,19,0),  "estadio": "Levi's Stadium, SF",            "fase": "Grupo F - J1"},
    {"local": "Inglaterra",  "visitante": "Senegal",        "datetime": dt(2026,6,16,22,0),  "estadio": "Rose Bowl, LA",                 "fase": "Grupo G - J1"},
    {"local": "Alemania",    "visitante": "Japón",          "datetime": dt(2026,6,17,19,0),  "estadio": "Arrowhead, Kansas City",        "fase": "Grupo H - J1"},
    {"local": "Portugal",    "visitante": "Ghana",          "datetime": dt(2026,6,17,22,0),  "estadio": "Estadio Akron, Guadalajara",    "fase": "Grupo D - J1"},
    {"local": "Colombia",    "visitante": "Costa Rica",     "datetime": dt(2026,6,18,19,0),  "estadio": "BC Place, Vancouver",           "fase": "Grupo I - J1"},
    {"local": "Países Bajos","visitante": "Arabia S.",      "datetime": dt(2026,6,18,22,0),  "estadio": "Lumen Field, Seattle",          "fase": "Grupo J - J1"},
    {"local": "Italia",      "visitante": "Ecuador",        "datetime": dt(2026,6,19,19,0),  "estadio": "Lincoln Financial, Filadelfia", "fase": "Grupo K - J1"},
    {"local": "Croacia",     "visitante": "Camerún",        "datetime": dt(2026,6,19,22,0),  "estadio": "NRG Stadium, Houston",          "fase": "Grupo L - J1"},

    # ── OCTAVOS DE FINAL (fechas aproximadas) ─────────────────────────────────
    {"local": "1ro Grupo A", "visitante": "2do Grupo B",   "datetime": dt(2026,7, 4,19,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF1"},
    {"local": "1ro Grupo C", "visitante": "2do Grupo D",   "datetime": dt(2026,7, 4,22,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF2"},
    {"local": "1ro Grupo E", "visitante": "2do Grupo F",   "datetime": dt(2026,7, 5,19,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF3"},
    {"local": "1ro Grupo G", "visitante": "2do Grupo H",   "datetime": dt(2026,7, 5,22,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF4"},
    {"local": "1ro Grupo B", "visitante": "2do Grupo A",   "datetime": dt(2026,7, 6,19,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF5"},
    {"local": "1ro Grupo D", "visitante": "2do Grupo C",   "datetime": dt(2026,7, 6,22,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF6"},
    {"local": "1ro Grupo F", "visitante": "2do Grupo E",   "datetime": dt(2026,7, 7,19,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF7"},
    {"local": "1ro Grupo H", "visitante": "2do Grupo G",   "datetime": dt(2026,7, 7,22,0),  "estadio": "Por confirmar",                 "fase": "Octavos - OF8"},

    # ── CUARTOS DE FINAL ───────────────────────────────────────────────────────
    {"local": "Gan. OF1",    "visitante": "Gan. OF2",      "datetime": dt(2026,7,11,22,0),  "estadio": "Por confirmar",                 "fase": "Cuartos - QF1"},
    {"local": "Gan. OF3",    "visitante": "Gan. OF4",      "datetime": dt(2026,7,12,22,0),  "estadio": "Por confirmar",                 "fase": "Cuartos - QF2"},
    {"local": "Gan. OF5",    "visitante": "Gan. OF6",      "datetime": dt(2026,7,13,22,0),  "estadio": "Por confirmar",                 "fase": "Cuartos - QF3"},
    {"local": "Gan. OF7",    "visitante": "Gan. OF8",      "datetime": dt(2026,7,14,22,0),  "estadio": "Por confirmar",                 "fase": "Cuartos - QF4"},

    # ── SEMIFINALES ────────────────────────────────────────────────────────────
    {"local": "Gan. QF1",    "visitante": "Gan. QF2",      "datetime": dt(2026,7,15,22,0),  "estadio": "MetLife, Nueva York",           "fase": "Semifinal - SF1"},
    {"local": "Gan. QF3",    "visitante": "Gan. QF4",      "datetime": dt(2026,7,16,22,0),  "estadio": "Rose Bowl, Los Ángeles",        "fase": "Semifinal - SF2"},

    # ── TERCER PUESTO ──────────────────────────────────────────────────────────
    {"local": "Perd. SF1",   "visitante": "Perd. SF2",     "datetime": dt(2026,7,18,19,0),  "estadio": "AT&T Stadium, Dallas",          "fase": "Tercer Puesto"},

    # ── FINAL ──────────────────────────────────────────────────────────────────
    {"local": "Gan. SF1",    "visitante": "Gan. SF2",      "datetime": dt(2026,7,19,18,0),  "estadio": "MetLife Stadium, Nueva York",   "fase": "🏆 FINAL"},
]

# Ordenar por fecha
PARTIDOS_MUNDIAL_2026.sort(key=lambda p: p["datetime"])
