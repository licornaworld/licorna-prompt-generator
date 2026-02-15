# ui/prompt_page.py
import tkinter as tk
from tkinter import ttk, messagebox

from config import BUTTON_LABELS, PAGE_INPUT_LABEL


class PromptPage(ttk.Frame):
    """
    Page générique pour un des 4 écrans.
    - Mode standard : un champ texte utilisateur + Generate (stub)
    - Mode Story Content :
      * Target Words
      * Story Highlight
      * Generate qui remplace {TARGET_WORDS} / {STORY_HIGHLIGHT} dans le prompt base
      * zone résultat éditable + bouton Copy
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

        # ---------- Zone d'entrée (standard) ----------
        self.standard_input = ttk.Frame(self)

        self.input_label = ttk.Label(self.standard_input, text="", font=("Segoe UI", 11, "bold"))
        self.input_label.pack(anchor="w", pady=(0, 6))

        self.text = tk.Text(self.standard_input, height=14, wrap="word")
        self.text.pack(fill="both", expand=True)

        self.standard_input.pack(fill="both", expand=True)

        # ---------- Zone d'entrée (Story Content) ----------
        self.story_input = ttk.Frame(self)

        target_row = ttk.Frame(self.story_input)
        target_row.pack(fill="x", pady=(0, 8))

        ttk.Label(target_row, text="Target Words", font=("Segoe UI", 11, "bold")).pack(side="left")
        self.target_words_var = tk.StringVar()
        self.target_words_entry = ttk.Entry(target_row, textvariable=self.target_words_var)
        self.target_words_entry.pack(side="left", fill="x", expand=True, padx=(12, 0))

        ttk.Label(self.story_input, text="Story Highlight", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        self.story_highlight_text = tk.Text(self.story_input, height=8, wrap="word")
        self.story_highlight_text.pack(fill="both", expand=True)

        ttk.Label(self.story_input, text="Generated Prompt", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(12, 6))
        self.generated_prompt_text = tk.Text(self.story_input, height=10, wrap="word")
        self.generated_prompt_text.pack(fill="both", expand=True)

        copy_row = ttk.Frame(self.story_input)
        copy_row.pack(fill="x", pady=(8, 0))
        self.copy_btn = ttk.Button(copy_row, text="Copy", command=self._copy_generated_prompt)
        self.copy_btn.pack(side="right")

        self.story_input.pack_forget()

        footer = ttk.Frame(self)
        footer.pack(fill="x", pady=14)

        self.generate_btn = ttk.Button(footer, text="Generate", command=self._on_generate)
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
        self.target_words_var.set("")
        self.story_highlight_text.delete("1.0", "end")
        self.generated_prompt_text.delete("1.0", "end")

        is_story_content = key == "story_content"
        self.preview_btn.pack_forget() if is_story_content else self.preview_btn.pack(side="right", padx=(0, 8))

        if is_story_content:
            self.standard_input.pack_forget()
            self.story_input.pack(fill="both", expand=True)
        else:
            self.story_input.pack_forget()
            self.standard_input.pack(fill="both", expand=True)

    def _on_generate(self):
        if self.current_key == "story_content":
            self._generate_story_content_prompt()
            return

        self._generate_stub()

    def _generate_stub(self):
        messagebox.showinfo("Generate", "Generate clicked (no action yet).")

    def _generate_story_content_prompt(self):
        base = self.controller.prompt_bases.get("story_content", "")
        target_words = self.target_words_var.get().strip()
        story_highlight = self.story_highlight_text.get("1.0", "end").rstrip("\n")

        generated_prompt = (
            base
            .replace("{TARGET_WORDS}", target_words)
            .replace("{STORY_HIGHLIGHT}", story_highlight)
        )

        self.generated_prompt_text.delete("1.0", "end")
        self.generated_prompt_text.insert("1.0", generated_prompt)

    def _copy_generated_prompt(self):
        content = self.generated_prompt_text.get("1.0", "end").rstrip("\n")
        if not content:
            messagebox.showwarning("Copy", "Nothing to copy.")
            return

        self.clipboard_clear()
        self.clipboard_append(content)
        self.update_idletasks()
        messagebox.showinfo("Copy", "Prompt copied to clipboard.")

    def _preview_stub(self):
        """
        Petit stub pratique : montre comment assembler prompt_base + input.
        Tu peux l'enlever si tu veux “ne rien faire du tout”.
        """
        base = self.controller.prompt_bases.get(self.current_key, "")
        user_text = self.text.get("1.0", "end").rstrip("\n")

        combined = (base.strip() + "\n\n" + user_text.strip()).strip()
        messagebox.showinfo("Preview (stub)", combined if combined else "(empty)")
