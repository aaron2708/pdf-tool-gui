import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from PyPDF4 import PdfFileReader, PdfFileWriter
from helpers.file_helper import save_as_pdf
from components.file_selector import SelectFile
from styles import ENTRY_FONT, ENTRY_WIDTH

MESSAGE_TITLE = "PDF Encrypt"


class Protect(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure((0, 1), weight=1)

        self.file_selector = SelectFile(self, callback=self.on_file_selected)
        self.file_selector.grid(row=0, column=0, sticky="EW", padx=5, pady=5, columnspan=2)

        password_label = ttk.Label(
            self,
            text="Password:"
        )
        password_label.grid(row=1, column=0, sticky="W", padx=(10, 5), pady=10)

        self.password = tk.StringVar()
        password_field = tk.Entry(
            self,
            textvariable=self.password,
            show="*",
            font=ENTRY_FONT,
            width=ENTRY_WIDTH
        )
        password_field.grid(row=1, column=1, sticky="W", pady=10)

        encrypt_button = ttk.Button(
            self,
            text="Encrypt",
            cursor="hand2",
            command=self.encrypt_file
        )
        encrypt_button.grid(row=2, column=0, sticky="E", padx=(0, 10), pady=10, columnspan=2)

    def on_file_selected(self):
        pass

    def encrypt_file(self):
        path = self.file_selector.getpath()
        if not path:
            messagebox.showerror(MESSAGE_TITLE, "You must select a PDF file.")
            return

        if not self.password.get():
            messagebox.showerror(MESSAGE_TITLE, "You must enter a password.")
            return

        pdf_reader = PdfFileReader(path)
        if pdf_reader.isEncrypted:
            messagebox.showwarning(MESSAGE_TITLE, "File is already encrypted.")
            return

        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.encrypt(self.password.get())

        save_path = save_as_pdf(parent=self)
        if not save_path:
            messagebox.showerror(MESSAGE_TITLE, "You must specify a file save path")

        if save_path[-4:].lower() != ".pdf":
            save_path += ".pdf"

        with Path(save_path).open(mode="wb") as save_file:
            pdf_writer.write(save_file)

        messagebox.showinfo(MESSAGE_TITLE, "PDF encrypted.")

