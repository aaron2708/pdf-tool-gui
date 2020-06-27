import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from PyPDF4 import PdfFileReader, PdfFileWriter
from helpers.file_helper import save_as_pdf, decrypt
from components.file_selector import SelectFile
from dialogs.password_prompt import askpassword
from styles import ENTRY_FONT, ENTRY_WIDTH

MESSAGE_TITLE = "PDF Extract"


class Split(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure((0, 1), weight=1)

        self.file_selector = SelectFile(self, callback=self.on_file_selected)
        self.file_selector.grid(row=0, column=0, sticky="EW", padx=5, pady=5, columnspan=2)

        self.extract_pages = tk.StringVar()
        extract_field = tk.Entry(
            self,
            textvariable=self.extract_pages,
            font=ENTRY_FONT,
            width=ENTRY_WIDTH
        )
        extract_field.grid(row=1, column=0, sticky="W", padx=(10, 5), pady=10)
        extract_field_explanation = tk.Label(
            self,
            text="Enter page numbers and/or page ranges.\nFor example: 1, 3 or 4-10"
        )
        extract_field_explanation.grid(row=1, column=1, sticky="W", padx=(10, 5), pady=10)

        footer_bar = ttk.Frame(self)
        footer_bar.columnconfigure(2, weight=1)
        footer_bar.grid(row=2, column=0, sticky="EW", columnspan=2)

        page_count_label = tk.Label(footer_bar, text="No. of Pages:")
        page_count_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="NW")

        self.page_count_text = tk.StringVar()
        page_count = tk.Label(footer_bar, textvariable=self.page_count_text)
        page_count.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="NW")

        extract_button = ttk.Button(
            footer_bar,
            text="Extract",
            cursor="hand2",
            command=self.extract_pdf
        )
        extract_button.grid(row=0, column=2, padx=(0, 5), pady=(5, 10), sticky="E")

    def on_file_selected(self):
        if self.file_selector.getpath():
            pdf_reader = PdfFileReader(self.file_selector.getpath())
            if pdf_reader.isEncrypted and not decrypt(pdf_reader, MESSAGE_TITLE):
                self.page_count_text.set("")
                self.file_selector.clear()
            else:
                self.page_count_text.set(pdf_reader.getNumPages())

    def extract_pdf(self):

        path = self.file_selector.getpath()
        if not path:
            messagebox.showerror(MESSAGE_TITLE, "You must select a PDF file.")
            return

        if not self.extract_pages.get():
            messagebox.showerror(MESSAGE_TITLE, "You must specify the page(s) to extract.")
            return

        if "-" in self.extract_pages.get():
            start, stop = self.extract_pages.get().split("-")
            pages = range(int(start)-1, int(stop))
        elif "," in self.extract_pages.get():
            pages = [int(n)-1 for n in self.extract_pages.get().split(",")]
        else:
            pages = [int(self.extract_pages.get())-1]

        if pages:
            pdf_reader = PdfFileReader(path)

            # check for encryption and prompt user for password
            if pdf_reader.isEncrypted:
                if not decrypt(pdf_reader, MESSAGE_TITLE):
                    return

            pdf_writer = PdfFileWriter()
            for page in pages:
                pdf_page = pdf_reader.getPage(page)
                if pdf_page:
                    pdf_writer.addPage(pdf_page)

            save_path = save_as_pdf(parent=self)
            if not save_path:
                messagebox.showerror(MESSAGE_TITLE, "You must specify a file save path.")
                return

            if save_path[-4:].lower() != ".pdf":
                save_path += ".pdf"

            with Path(save_path).open(mode="wb") as save_file:
                pdf_writer.write(save_file)

            messagebox.showinfo(MESSAGE_TITLE, f"Page(s) {self.extract_pages.get()} have been extracted.")
        else:
            messagebox.showwarning(MESSAGE_TITLE, "No pages to extract.")
