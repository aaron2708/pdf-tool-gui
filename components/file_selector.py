import tkinter as tk
from tkinter import ttk
from helpers.file_helper import browse_pdf_files
from styles import ENTRY_FONT, ENTRY_WIDTH


class SelectFile(tk.Frame):
    def __init__(self, container, callback, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.callback = callback

        self.file_path = tk.StringVar()
        file_entry = tk.Entry(
            self,
            state="disabled",
            textvariable=self.file_path,
            width=ENTRY_WIDTH,
            font=ENTRY_FONT
        )
        file_entry.grid(row=0, column=0, sticky="EW", padx=(5,5), pady=(5, 5))
        browse_button = ttk.Button(
            self,
            text="Select PDF",
            cursor="hand2",
            command=self._select_file
        )
        browse_button.grid(row=0, column=1, padx=(0, 5))

    def _select_file(self):
        path = browse_pdf_files(parent=self)
        if path:
            self.file_path.set(path)

        if self.callback:
            self.callback()

    def getpath(self):
        return self.file_path.get()

    def clear(self):
        self.file_path.set("")
