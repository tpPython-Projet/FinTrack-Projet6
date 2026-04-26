"""
couleurs.py
Projet : FinTrack Moniteur de Budget Personnel
Description : Constantes de couleurs et icones ASCII pour l'interface.
Auteurs : HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date : 25/04/2026
"""

from colorama import Fore, Back, Style, init

#Initialisation de colorama (autoreset=True) remet la couleur par défaut après chaque print automatiquement 

init(autoreset=True)

# Couleurs principales
VERT  = Fore.GREEN
ROUGE = Fore.RED
JAUNE   = Fore.YELLOW
BLEU    = Fore.CYAN
BLANC   = Fore.WHITE
GRAS    = Style.BRIGHT
RESET   = Style.RESET_ALL


#Couleurs par catégorie

COULEURS_CATEGORIES = {
    "Alimentation" : Fore.GREEN,
    "Transport"    : Fore.YELLOW,
    "Logement"     : Fore.BLUE,
    "Santé"        : Fore.RED,
    "Loisirs"      : Fore.MAGENTA,
    "Éducation"    : Fore.CYAN,
    "Revenu"       : Fore.GREEN,
    "Autre"        : Fore.WHITE,
}


# Icones ASCII par catégorie

ICONES_CATEGORIES = {
    "Alimentation" : "🍚",
    "Transport"    : "🚗",
    "Logement"     : "🏠",
    "Santé"        : "💊",
    "Loisirs"      : "🎮",
    "Éducation"    : "📚",
    "Revenu"       : "💰",
    "Autre"        : "📌",
}

# Symboles visuels 

OK      = VERT  + "✓"  + RESET
ERREUR  = ROUGE + "✗"  + RESET
ALERTE  = JAUNE + "⚠"  + RESET
INFO    = BLEU  + "ℹ"  + RESET

# Séparateurs ASCII visuels
 
SEP_EPAIS  = BLEU + "═" * 55 + RESET
SEP_FIN    = BLEU + "─" * 55 + RESET
SEP_TITRE  = BLEU + "╔" + "═" * 53 + "╗" + RESET
SEP_BAS    = BLEU + "╚" + "═" * 53 + "╝" + RESET