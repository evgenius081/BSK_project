from tkinter import *

from Colors import Colors
from elements.Chat import chat


def main_page(window, images) -> None:
    print("main page")
    for widget in window.winfo_children():
        widget.destroy()
    window.title("Messenger")
    window.geometry('863x505')
    window["bg"] = Colors.MAIN_BG.value
    window.resizable(False, False)
    pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, confine=True, height=505, width=863, highlightthickness=0)

    main = chat(window, images)
    main_zone = pav.create_window(0, 0, anchor=NW, window=main)
    pav.pack()

