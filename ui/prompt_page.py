# ui/prompt_page.py
import tkinter as tk
from tkinter import ttk, messagebox

from config import BUTTON_LABELS, PAGE_INPUT_LABEL


class PromptPage(ttk.Frame):
    """
    Page générique pour un des 4 écrans.
    Elle affiche :
      - un titre
      - un champ Text avec le label demandé
      - un bouton Generate (stub)
      - back
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=16)
        self.controller = controller
        self.current_key = None

        header = ttk.Frame(self)
        header.pack(fill="x")

        self.title_lbl = ttk.Label(header, text="", font=("Segoe UI", 16, "bold"))
        self.title_lbl.pack(side="left")

        back_btn = ttk.Button(header, text="Back", command=self.controller.show_main_menu)
        back_btn.pack(side="right")

        ttk.Separator(self).pack(fill="x", pady=12)

        self.input_label = ttk.Label(self, text="", font=("Segoe UI", 11, "bold"))
        self.input_label.pack(anchor="w", pady=(0, 6))

        self.text = tk.Text(self, height=14, wrap="word")
        self.text.pack(fill="both", expand=True)

        footer = ttk.Frame(self)
        footer.pack(fill="x", pady=14)

        self.generate_btn = ttk.Button(footer, text="Generate", command=self._generate_stub)
        self.generate_btn.pack(side="right")

        self.preview_btn = ttk.Button(footer, text="Preview Prompt (stub)", command=self._preview_stub)
        self.preview_btn.pack(side="right", padx=(0, 8))

    def set_mode(self, key: str):
        """
        Configure la page selon la section choisie.
        """
        self.current_key = key
        self.title_lbl.config(text=BUTTON_LABELS.get(key, ""))
        self.input_label.config(text=f"{PAGE_INPUT_LABEL.get(key, 'Input')} :")

        self.text.delete("1.0", "end")

    def _generate_stub(self):
        # Ne fait rien pour le moment (comme demandé)
        messagebox.showinfo("Generate", "Generate clicked (no action yet).")

    def _preview_stub(self):
        """
        Petit stub pratique : montre comment assembler prompt_base + input.
        Tu peux l'enlever si tu veux “ne rien faire du tout”.
        """
        base = self.controller.prompt_bases.get(self.current_key, "")
        user_text = self.text.get("1.0", "end").rstrip("\n")

        combined = (base.strip() + "\n\n" + user_text.strip()).strip()
        messagebox.showinfo("Preview (stub)", combined if combined else "(empty)")
