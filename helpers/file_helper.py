import os
from tkinter import filedialog, messagebox

from dialogs.password_prompt import askpassword

DOCUMENT_PATH = os.path.expanduser("~")
FILETYPE_ALL = ("All types", "*.*")
FILETYPE_PDF = ("PDF File", "*.pdf")
FILETYPE_CSV = ("CSV File", "*.csv")
DIALOG_TITLE = "Select {} file"
SAVE_DIALOG_TITLE = "Save as {} file"


def _browse_files(**kwargs):
    file_path = filedialog.askopenfilename(
        initialdir=DOCUMENT_PATH,
        **kwargs
    )
    return file_path


def browse_pdf_files(**kwargs):
    return _browse_files(
        title=DIALOG_TITLE.format("PDF"),
        filetypes=[FILETYPE_PDF],
        **kwargs
    )


def browse_csv_files(**kwargs):
    return _browse_files(
        title= DIALOG_TITLE.format("CSV"),
        filetypes=[FILETYPE_CSV],
        **kwargs
    )


def _save_as(**kwargs):
    file_path = filedialog.asksaveasfilename(
        initialdir=DOCUMENT_PATH,
    )
    return file_path


def save_as_pdf(**kwargs):
    return _save_as(
        title=SAVE_DIALOG_TITLE.format("PDF"),
        filetypes=[FILETYPE_PDF],
        defaultextension=".pdf",
        **kwargs
    )


def decrypt(pdf_reader, message_title="File"):
    try:
        password = askpassword(title=message_title, prompt="Enter a password")

        if not password:
            messagebox.showerror(message_title, "You must enter a password.")
            return False

        if not pdf_reader.decrypt(password):
            messagebox.showerror(message_title, "Incorrect password")
            return False

        return True
    except NotImplementedError:
        messagebox.showerror(message_title, "This PDF cannot be decrypted by this application")
        return False