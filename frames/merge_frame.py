import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from PyPDF4 import PdfFileReader, PdfFileWriter
from helpers.file_helper import browse_pdf_files, save_as_pdf, decrypt

MESSAGE_TITLE = "Merge PDF"

class Merge(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        add_icon_image = Image.open("./assets/circle-add.png").resize((24, 24))
        add_icon = ImageTk.PhotoImage(add_icon_image)

        remove_icon_image = Image.open("./assets/circle-delete-trash.png").resize((24, 24))
        remove_icon = ImageTk.PhotoImage(remove_icon_image)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=0, sticky="EW", columnspan=2)
        add_button = ttk.Button(
            button_frame,
            image=add_icon,
            text="Add",
            cursor="hand2",
            compound=tk.LEFT,
            command=self.add_file
        )
        add_button.image = add_icon
        add_button.grid(row=0, column=0, padx=(5, 5), pady=(5, 10), sticky="NW")

        remove_button = ttk.Button(
            button_frame,
            image=remove_icon,
            text="Remove",
            cursor="hand2",
            compound=tk.LEFT,
            command=self.remove_files
        )
        remove_button.image = remove_icon
        remove_button.grid(row=0, column=1, padx=(5, 5), pady=(5, 10), sticky="NW")

        self.tree = ttk.Treeview(self, selectmode="browse", show="headings")
        self.tree["columns"] = ("filename", "filepath", "pages")
        self.tree.heading("filename", text="File Name", anchor="w")
        self.tree.heading("filepath", text="File Path", anchor="w")
        self.tree.heading("pages", text="Page Count", anchor="w")
        self.tree.grid(row=1, column=0, sticky="NSEW", padx=(5, 5), pady=(0, 5))

        move_control_frame = tk.Frame(self)
        move_control_frame.grid(row=1, column=1, sticky="NS")
        up_icon_image = Image.open("./assets/arrow-up.png").resize((20, 20))
        up_icon = ImageTk.PhotoImage(up_icon_image)
        up_button = ttk.Button(
            move_control_frame,
            image=up_icon,
            cursor="hand2",
            command=self.move_up
        )
        up_button.image = up_icon
        up_button.grid(row=0, column=0, pady=(0, 5), padx=(0, 5), sticky="N")

        down_icon_image = Image.open("./assets/arrow-down.png").resize((20, 20))
        down_icon = ImageTk.PhotoImage(down_icon_image)
        down_button = ttk.Button(
            move_control_frame,
            image=down_icon,
            cursor="hand2",
            command=self.move_down
        )
        down_button.image = down_icon
        down_button.grid(row=1, column=0, padx=(0, 5), sticky="N")

        footer_bar = ttk.Frame(self)
        footer_bar.columnconfigure(0, weight=1)
        footer_bar.grid(row=2, column=0, sticky="EW")
        merge_button = ttk.Button(
            footer_bar,
            text="Merge",
            cursor="hand2",
            style="PrimaryButton.TButton",
            command=self.merge
        )
        merge_button.grid(row=0, column=0, padx=(0, 5), pady=(5, 10), sticky="E")

    def add_file(self):
        path = browse_pdf_files()
        if not path:
            return

        file_path = Path(path)
        file_name = file_path.name

        pdf_reader = PdfFileReader(path)
        if pdf_reader.isEncrypted and not decrypt(pdf_reader, MESSAGE_TITLE):
            pages = "-"
        else:
            pages = pdf_reader.getNumPages()

        self.tree.insert("", "end", values=[file_name, path, pages])

    def remove_files(self):
        item = self.tree.selection()
        if item:
            self.tree.delete(item)

    def move_up(self):
        item = self.tree.selection()
        index = self.tree.index(item)
        parent = self.tree.parent(item)
        new_index = index - 1

        self.tree.move(item, parent, new_index)

    def move_down(self):
        item = self.tree.selection()
        index = self.tree.index(item)
        parent = self.tree.parent(item)
        new_index = index + 1

        self.tree.move(item, parent, new_index)

    def merge(self):
        save_path = save_as_pdf()
        if not save_path:
            messagebox.showerror(MESSAGE_TITLE, "You must specify a file save path.")
            return

        if save_path[-4:].lower() != ".pdf":
            save_path += ".pdf"

        pdf_writer = PdfFileWriter()

        for item in self.tree.get_children():
            item_values = self.tree.item(item, option="values")
            path = item_values[1]
            pdf_reader = PdfFileReader(path)
            if pdf_reader.isEncrypted and not decrypt(pdf_reader, MESSAGE_TITLE):
                messagebox.showwarning(MESSAGE_TITLE, f"{item_values[0]} could not be decrypted. It will not be "
                                                      f"included in the merge.")
                continue

            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))

        with Path(save_path).open(mode="wb") as save_file:
            pdf_writer.write(save_file)

        messagebox.showinfo(MESSAGE_TITLE, "PDF Merged")

