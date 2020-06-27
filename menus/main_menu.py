import tkinter as tk
from pubsub import pub


class MainMenu(tk.Menu):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Merge PDF", command=self.navigate_merge_pdf)
        file_menu.add_command(label="Split PDF", command=self.navigate_split_pdf)
        file_menu.add_command(label="Protect PDF", command=self.navigate_protect_pdf)
        # file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=self.quit)

    def navigate_merge_pdf(self):
        pub.sendMessage("show_frame", key="merge")

    def navigate_split_pdf(self):
        pub.sendMessage("show_frame", key="split")

    def navigate_protect_pdf(self):
        pub.sendMessage("show_frame", key="protect")

    def quit(self):
        pub.sendMessage("quit")
