from tkinter import *
from Colors import Colors
import tkinter.font as tkFont

MAX_MESSAGE_WIDTH = 420


def text_message(parent, message, message_id) -> None:
    frame = Frame(parent)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    text_frame = Frame(frame)
    text_frame.grid_propagate(False)
    text = Text(text_frame, font=("Verdana", 11), bd=0, wrap=WORD)
    text.insert(INSERT, message.text)
    time = Label(frame, text=message.datetime.strftime("%H:%M"), font=("Verdana", 7),
                 foreground=Colors.MESSAGES_TIME_FOREGROUND.value)
    if message.author_id == "me":
        frame.config(bg=Colors.MY_MESSAGE_BG.value)
        text_frame.config(bg=Colors.MY_MESSAGE_BG.value)
        frame.grid(row=message_id, column=1, sticky="ne", padx=6, pady=3)
        text.config(background=Colors.MY_MESSAGE_BG.value, foreground=Colors.MY_MESSAGES_TEXT_FOREGROUND.value)
        time.config(bg=Colors.MY_MESSAGE_BG.value)
        time.grid(row=1, column=0, sticky="nw")
        text.grid(row=1, column=0, sticky="nw", padx=3)
    elif message.author_id == "partner":
        frame.config(bg=Colors.MESSAGE_BG.value)
        text_frame.config(bg=Colors.MESSAGE_BG.value)
        frame.grid(row=message_id, column=0, sticky="nw", padx=6, pady=3)
        text.config(background=Colors.MESSAGE_BG.value, foreground=Colors.MESSAGES_TEXT_FOREGROUND.value)
        time.config(bg=Colors.MESSAGE_BG.value)
        time.grid(row=1, column=0, sticky="ne")
        text.grid(row=1, column=0, sticky="ne", padx=3)

    parent.update_idletasks()

    width = tkFont.Font(family="Verdana", size=11).measure(message.text) + 6
    height = 25
    if width > MAX_MESSAGE_WIDTH:
        width = MAX_MESSAGE_WIDTH
        height = 25 + (int(len(message.text)/42) - 1) * 14
        text.config(width=42)
        
    text_frame.config(width=width, height=height)

    text.config(state="disabled")
    text_frame.grid(row=0, column=0)

