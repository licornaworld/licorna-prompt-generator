# app.py
import tkinter as tk
from tkinter import ttk

from config import APP_TITLE, APP_GEOMETRY
from storage import load_prompt_bases, save_prompt_bases

from ui.main_menu import MainMenu
from ui.settings_view import SettingsView
from ui.prompt_page import PromptPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(900, 700)

        # Style (simple)
        style = ttk.Style(self)
        # Utilise le thème par défaut dispo sur la machine
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # State
        self.prompt_bases = load_prompt_bases()

        # Container pour les frames
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        self.frames["main_menu"] = MainMenu(container, controller=self)
        self.frames["settings"] = SettingsView(container, controller=self)
        self.frames["prompt_page"] = PromptPage(container, controller=self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.show_main_menu()

    # Navigation
    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()

    def show_main_menu(self):
        self.show_frame("main_menu")

    def show_settings(self):
        settings_view = self.frames["settings"]
        settings_view.refresh_from_controller()
        self.show_frame("settings")

    def open_prompt_page(self, key: str):
        prompt_page = self.frames["prompt_page"]
        prompt_page.set_mode(key)
        self.show_frame("prompt_page")

    # Persistence
    def save_bases(self, new_bases: dict):
        self.prompt_bases = dict(new_bases)
        save_prompt_bases(self.prompt_bases)


if __name__ == "__main__":
    app = App()
    app.mainloop()
