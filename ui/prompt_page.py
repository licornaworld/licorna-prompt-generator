# ui/prompt_page.py
import tkinter as tk
from tkinter import ttk, messagebox

from config import BUTTON_LABELS, PAGE_INPUT_LABEL


class PromptPage(ttk.Frame):
    """
    Page générique pour un des 4 écrans.
    - Mode standard : un champ texte utilisateur + Generate (stub)
    - Mode template :
      * Target Words
      * Story Highlight
      * Generate qui remplace les placeholders selon la section dans le prompt base
      * zone résultat éditable + bouton Copy
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=16)
        self.controller = controller
        self.current_key = None
        self.template_modes = {
            "story_content": {
                "field_one_label": "Target Words",
                "field_two_label": "Story Highlight",
                "placeholder_one": "{TARGET_WORDS}",
                "placeholder_two": "{STORY_HIGHLIGHT}",
            },
            "characters_descr": {
                "field_one_label": "Existing Characters",
                "field_two_label": "Story Content",
                "placeholder_one": "{EXISTING_CHARACTERS}",
                "placeholder_two": "{STORY_CONTENT}",
            },
        }

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

        # ---------- Zone d'entrée (template) ----------
        self.template_input = ttk.Frame(self)

        target_row = ttk.Frame(self.template_input)
        target_row.pack(fill="x", pady=(0, 8))

        self.field_one_label = ttk.Label(target_row, text="", font=("Segoe UI", 11, "bold"))
        self.field_one_label.pack(side="left")
        self.field_one_var = tk.StringVar()
        self.field_one_entry = ttk.Entry(target_row, textvariable=self.field_one_var)
        self.field_one_entry.pack(side="left", fill="x", expand=True, padx=(12, 0))

        self.field_two_label = ttk.Label(self.template_input, text="", font=("Segoe UI", 11, "bold"))
        self.field_two_label.pack(anchor="w", pady=(0, 6))
        self.field_two_text = tk.Text(self.template_input, height=8, wrap="word")
        self.field_two_text.pack(fill="both", expand=True)

        ttk.Label(self.template_input, text="Generated Prompt", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(12, 6))
        self.generated_prompt_text = tk.Text(self.template_input, height=10, wrap="word")
        self.generated_prompt_text.pack(fill="both", expand=True)

        copy_row = ttk.Frame(self.template_input)
        copy_row.pack(fill="x", pady=(8, 0))
        self.copy_btn = ttk.Button(copy_row, text="Copy", command=self._copy_generated_prompt)
        self.copy_btn.pack(side="right")

        self.template_input.pack_forget()

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
        self.field_one_var.set("")
        self.field_two_text.delete("1.0", "end")
        self.generated_prompt_text.delete("1.0", "end")

        is_template_mode = key in self.template_modes
        self.preview_btn.pack_forget() if is_template_mode else self.preview_btn.pack(side="right", padx=(0, 8))

        if is_template_mode:
            mode = self.template_modes[key]
            self.field_one_label.config(text=mode["field_one_label"])
            self.field_two_label.config(text=mode["field_two_label"])

            self.standard_input.pack_forget()
            self.template_input.pack(fill="both", expand=True)
        else:
            self.template_input.pack_forget()
            self.standard_input.pack(fill="both", expand=True)

    def _on_generate(self):
        if self.current_key in self.template_modes:
            self._generate_template_prompt()
            return

        self._generate_stub()

    def _generate_stub(self):
        messagebox.showinfo("Generate", "Generate clicked (no action yet).")

    def _generate_template_prompt(self):
        mode = self.template_modes.get(self.current_key)
        if not mode:
            return

        base = self.controller.prompt_bases.get(self.current_key, "")
        field_one = self.field_one_var.get().strip()
        field_two = self.field_two_text.get("1.0", "end").rstrip("\n")

        generated_prompt = (
            base
            .replace(mode["placeholder_one"], field_one)
            .replace(mode["placeholder_two"], field_two)
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
