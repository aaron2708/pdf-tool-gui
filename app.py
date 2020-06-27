import tkinter as tk
from tkinter import ttk, messagebox
from pubsub import pub
from menus import MainMenu
from frames import Merge, Split, Protect


class PdfTool(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style(self)

        self.title("PDF Tool")
        self.frames = dict()

        menu = MainMenu(self)
        self.config(menu=menu)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid()

        merge_frame = Merge(container)
        merge_frame.grid(row=0, column=0, sticky="NSEW")
        self.frames["merge"] = merge_frame

        split_frame = Split(container)
        split_frame.grid(row=0, column=0, sticky="NSEW")
        self.frames["split"] = split_frame

        protect_frame = Protect(container)
        protect_frame.grid(row=0, column=0, sticky="NSEW")
        self.frames["protect"] = protect_frame

        pub.subscribe(self.show_frame, "show_frame")
        pub.subscribe(self.exit_app, "quit")

        self.show_frame("merge")

    def show_frame(self, key):
        frame = self.frames.get(key)
        frame.tkraise()

    def exit_app(self):
        result = messagebox.askokcancel("Confirm Quit", "Are you sure you want to quit?")
        print(result)
        if result:
            app.destroy()


app = PdfTool()
app.mainloop()