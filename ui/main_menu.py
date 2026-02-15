# ui/main_menu.py
import tkinter as tk
from tkinter import ttk
from config import BUTTON_LABELS


class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=16)
        self.controller = controller

        # Header
        header = ttk.Frame(self)
        header.pack(fill="x")

        title = ttk.Label(header, text="Prompts Generator", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

        settings_btn = ttk.Button(header, text="Settings", command=self.controller.show_settings)
        settings_btn.pack(side="right")

        ttk.Separator(self).pack(fill="x", pady=12)

        # Body buttons
        body = ttk.Frame(self)
        body.pack(expand=True, fill="both")

        # grid 2x2
        buttons = [
            ("story_content", BUTTON_LABELS["story_content"]),
            ("characters_descr", BUTTON_LABELS["characters_descr"]),
            ("landing_img", BUTTON_LABELS["landing_img"]),
            ("characters_img", BUTTON_LABELS["characters_img"]),
        ]

        for idx, (key, label) in enumerate(buttons):
            r, c = divmod(idx, 2)
            btn = ttk.Button(
                body,
                text=label,
                command=lambda k=key: self.controller.open_prompt_page(k),
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=10, pady=10, ipadx=10, ipady=30)

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)
