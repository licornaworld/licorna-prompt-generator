# config.py
from pathlib import Path

APP_TITLE = "Prompts Generator"
APP_GEOMETRY = "900x600"

# JSON stocké dans un .txt comme demandé
DATA_DIR = Path(__file__).parent
SETTINGS_FILE = DATA_DIR / "prompt_bases.txt"

# Identifiants internes (utilisés comme clés JSON)
PROMPT_KEYS = [
    "story_content",
    "characters_descr",
    "landing_img",
    "characters_img",
]

# Libellés UI (boutons écran principal)
BUTTON_LABELS = {
    "story_content": "Story Content",
    "characters_descr": "Characters Descr",
    "landing_img": "Landing Img",
    "characters_img": "Characters Img",
}

# Champs (label) par page
# mapping demandé :
# 'Story Content' : Story Highlights : Text
# 'Characters Descr' : Story Content : Text
# 'Landing Img' : Story Content : Text
# 'Characters Img' : Characters Descr : Text
PAGE_INPUT_LABEL = {
    "story_content": "Story Highlights",
    "characters_descr": "Story Content",
    "landing_img": "Story Content",
    "characters_img": "Characters Descr",
}

DEFAULT_PROMPT_BASES = {
    "story_content": "",
    "characters_descr": "",
    "landing_img": "",
    "characters_img": "",
}
