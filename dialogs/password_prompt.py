import tkinter as tk
from tkinter.simpledialog import _QueryString


class PasswordDialog(_QueryString):
    def __init__(self, *args, **kwargs):
        super().__init__(show="*", *args, **kwargs)


def askpassword(title, prompt, **kwargs):
    '''get a password from the user

    :param title:
    :param prompt:
    :param kwargs:
    :return: result string
    '''
    d = PasswordDialog(title, prompt, **kwargs)
    return d.result