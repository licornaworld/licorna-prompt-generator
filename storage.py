# storage.py
import json
from typing import Dict
from config import SETTINGS_FILE, DEFAULT_PROMPT_BASES, PROMPT_KEYS


def load_prompt_bases() -> Dict[str, str]:
    """
    Charge le JSON depuis prompt_bases.txt.
    Si le fichier n'existe pas / est invalide, retourne des defaults.
    """
    if not SETTINGS_FILE.exists():
        return DEFAULT_PROMPT_BASES.copy()

    try:
        raw = SETTINGS_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return DEFAULT_PROMPT_BASES.copy()

        data = json.loads(raw)

        # normaliser / sécuriser
        bases = DEFAULT_PROMPT_BASES.copy()
        for k in PROMPT_KEYS:
            v = data.get(k, "")
            bases[k] = v if isinstance(v, str) else ""
        return bases

    except (json.JSONDecodeError, OSError):
        return DEFAULT_PROMPT_BASES.copy()


def save_prompt_bases(bases: Dict[str, str]) -> None:
    """
    Sauvegarde les bases en JSON dans prompt_bases.txt.
    """
    safe = {}
    for k in PROMPT_KEYS:
        v = bases.get(k, "")
        safe[k] = v if isinstance(v, str) else ""

    SETTINGS_FILE.write_text(
        json.dumps(safe, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
