import threading
import time
from tkinter import *
from Colors import Colors
import tkinter.font as tkFont

MAX_MESSAGE_WIDTH = 420

class FileMessage:
    def __init__(self):
        self.file_sending_procent = None
        self.frame_width = 0
        self.status_label = None
        self.author = None

    def start_sending(self):
        self.status_label.grid_forget()
        self.file_sending_procent.grid(row=1, column=0, sticky="nw")

    def update_file_sending_procent(self, procent, message):
        if procent == 100:
            self.file_sending_procent.grid_forget()
            self.file_sending_procent.destroy()
            if self.author == "partner":
                self.status_label.grid(row=1, column=0, sticky="ne")
                self.status_label.config(text=f"{message.cipher_mode.value} ● {message.datetime.strftime('%H:%M')}")
            elif self.author == "me":
                self.status_label.grid(row=1, column=0, sticky="nw")
                self.status_label.config(bg=Colors.MY_MESSAGE_BG.value,
                                         text=f"{message.datetime.strftime('%H:%M')} ● {message.cipher_mode.value}")
        else:
            self.file_sending_procent.config(width=int(procent * self.frame_width / 100))

    def file_message(self, parent, message, message_id, images) -> None:
        [a, b, c, file_black] = images
        self.author = message.author_id
        frame = Frame(parent)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        text_frame = Frame(frame)
        file_label = Label(text_frame, image=file_black)
        file_label.grid(row=1, column=0, sticky="nw", pady=3, padx=5)
        text_frame.grid_propagate(False)
        text = Text(text_frame, font=("Verdana", 11), bd=0, wrap=WORD)
        text.insert(INSERT, message.filename)
        self.status_label = Label(frame, font=("Verdana", 7),
                                  foreground=Colors.MESSAGES_TIME_FOREGROUND.value)

        self.file_sending_procent = Frame(frame, bg="#000000")

        if message.author_id == "me":
            frame.config(bg=Colors.MY_MESSAGE_BG.value)
            text_frame.config(bg=Colors.MY_MESSAGE_BG.value)
            frame.grid(row=message_id, column=1, sticky="ne", padx=6, pady=3)
            text.config(background=Colors.MY_MESSAGE_BG.value, foreground=Colors.MY_MESSAGES_TEXT_FOREGROUND.value)
            text.grid(row=1, column=1, sticky="nw", padx=3, pady=15)
            file_label.config(bg=Colors.MY_MESSAGE_BG.value)
            self.status_label.config(text="Encrypting...", bg=Colors.MY_MESSAGE_BG.value,)
            self.status_label.grid(row=1, column=0, sticky="nw")
        elif message.author_id == "partner":
            frame.config(bg=Colors.MESSAGE_BG.value)
            text_frame.config(bg=Colors.MESSAGE_BG.value)
            frame.grid(row=message_id, column=0, sticky="nw", padx=6, pady=3)
            text.config(background=Colors.MESSAGE_BG.value, foreground=Colors.MESSAGES_TEXT_FOREGROUND.value)
            text.grid(row=1, column=1, sticky="ne", padx=3, pady=15)
            file_label.config(bg=Colors.MESSAGE_BG.value)

        parent.update_idletasks()

        width = tkFont.Font(family="Verdana", size=11).measure(message.filename) + 55
        height = 50
        if width > MAX_MESSAGE_WIDTH:
            width = MAX_MESSAGE_WIDTH
            height = 50 + (int(len(message.filename)/42) - 1) * 14
            text.config(width=42)

        text_frame.config(width=width, height=height+5)
        self.file_sending_procent.config(height=5)
        self.frame_width = width

        text.config(state="disabled")
        text_frame.grid(row=0, column=0, sticky="w")

        self.start_sending()
        self.update_file_sending_procent(50, message)
        self.update_file_sending_procent(100, message)

