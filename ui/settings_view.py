# ui/settings_view.py
import tkinter as tk
from tkinter import ttk, messagebox

from config import BUTTON_LABELS, PROMPT_KEYS


class SettingsView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=16)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x")

        title = ttk.Label(header, text="Settings", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

        back_btn = ttk.Button(header, text="Back", command=self.controller.show_main_menu)
        back_btn.pack(side="right")

        ttk.Separator(self).pack(fill="x", pady=12)

        # Champs texte : un prompt base par bouton
        self.text_widgets = {}

        form = ttk.Frame(self)
        form.pack(fill="both", expand=True)

        for i, key in enumerate(PROMPT_KEYS):
            label = ttk.Label(form, text=f"Prompt Base — {BUTTON_LABELS[key]}", font=("Segoe UI", 11, "bold"))
            label.pack(anchor="w", pady=(10 if i else 0, 6))

            txt = tk.Text(form, height=5, wrap="word")
            txt.pack(fill="x", expand=False)

            self.text_widgets[key] = txt

        footer = ttk.Frame(self)
        footer.pack(fill="x", pady=14)

        save_btn = ttk.Button(footer, text="Save", command=self._save)
        save_btn.pack(side="right")

        reload_btn = ttk.Button(footer, text="Reload", command=self.refresh_from_controller)
        reload_btn.pack(side="right", padx=(0, 8))

    def refresh_from_controller(self):
        """
        Recharge l'état depuis controller.prompt_bases
        """
        bases = self.controller.prompt_bases
        for key, txt in self.text_widgets.items():
            txt.delete("1.0", "end")
            txt.insert("1.0", bases.get(key, ""))

    def _save(self):
        bases = {}
        for key, txt in self.text_widgets.items():
            bases[key] = txt.get("1.0", "end").rstrip("\n")

        self.controller.save_bases(bases)
        messagebox.showinfo("Saved", "Prompt bases saved successfully.")
