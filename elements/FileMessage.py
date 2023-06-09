import datetime
import os
from tkinter import *
from Colors import Colors
import tkinter.font as tkFont
from showinfm import show_in_file_manager

MAX_MESSAGE_WIDTH = 420


class FileMessage:
    def __init__(self):
        self.file_sending_procent = None
        self.frame_width = 0
        self.status_label = None
        self.author = None
        self.message = None
        self.real_filename = None
        self.file_label = None
        self.file_black = None
        self.arrow_up = None
        self.lock = None

    def update_decrypted(self, real_filename) -> None:
        self.file_sending_procent.grid_forget()
        self.file_sending_procent.destroy()
        self.status_label.grid(row=1, column=0, sticky="nw")
        self.status_label.config(bg=Colors.MESSAGE_BG.value,
                                 text=f"{self.message.cipher_mode.value} ● "
                                      f"{datetime.datetime.now().strftime('%H:%M')}")
        self.real_filename = real_filename
        self.file_label.config(image=self.file_black)

    def set_message_info(self):
        if self.file_sending_procent.winfo_exists():
            self.file_sending_procent.grid_forget()
            self.file_sending_procent.destroy()
            self.status_label.grid(row=1, column=0, sticky="nw")
            self.status_label.config(bg=Colors.MY_MESSAGE_BG.value,
                                     text=f"{datetime.datetime.now().strftime('%H:%M')} ● "
                                          f"{self.message.cipher_mode.value}")

    def set_encrypting(self):
        self.file_label.config(image=self.lock)

    def set_sending(self):
        self.file_label.config(image=self.arrow_up)

    def set_sent(self):
        self.file_label.config(image=self.file_black)

    def update_procent(self, procent) -> None:
        self.file_sending_procent.config(width=int(procent * self.frame_width / 100))

    def open_in_folder(self, event) -> None:
        show_in_file_manager(os.getcwd()+"\\"+self.real_filename)

    def file_message(self, parent, message, message_id, images) -> None:
        [a, b, c, file_black, arrow_up, lock] = images
        self.file_black = file_black
        self.arrow_up = arrow_up
        self.lock = lock
        self.message = message
        self.author = message.author_id
        frame = Frame(parent)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        text_frame = Frame(frame)
        self.file_label = Label(text_frame, image=lock, cursor="hand2")
        self.file_label.grid(row=1, column=0, sticky="nw", pady=3, padx=5)
        text_frame.grid_propagate(False)
        text = Text(text_frame, font=("Verdana", 11), bd=0, wrap=WORD)
        text.insert(INSERT, message.filename)
        self.status_label = Label(frame, font=("Verdana", 7),
                                  foreground=Colors.MESSAGES_TIME_FOREGROUND.value)

        self.file_sending_procent = Frame(frame, bg="#000000")
        self.file_sending_procent.grid(row=1, column=0, sticky="nw")

        if message.author_id == "me":
            frame.config(bg=Colors.MY_MESSAGE_BG.value)
            text_frame.config(bg=Colors.MY_MESSAGE_BG.value)
            frame.grid(row=message_id, column=1, sticky="ne", padx=6, pady=3)
            text.config(background=Colors.MY_MESSAGE_BG.value, foreground=Colors.MY_MESSAGES_TEXT_FOREGROUND.value)
            text.grid(row=1, column=1, sticky="nw", padx=3, pady=15)
            self.file_label.config(bg=Colors.MY_MESSAGE_BG.value)
            # self.status_label.config(bg=Colors.MY_MESSAGE_BG.value,)
            # self.status_label.grid(row=1, column=0, sticky="nw")
        elif message.author_id == "partner":
            frame.config(bg=Colors.MESSAGE_BG.value)
            text_frame.config(bg=Colors.MESSAGE_BG.value)
            frame.grid(row=message_id, column=0, sticky="nw", padx=6, pady=3)
            text.config(background=Colors.MESSAGE_BG.value, foreground=Colors.MESSAGES_TEXT_FOREGROUND.value)
            text.grid(row=1, column=1, sticky="ne", padx=3, pady=15)
            self.file_label.config(bg=Colors.MESSAGE_BG.value)
            # self.status_label.config(bg=Colors.MESSAGE_BG.value,)
            # self.status_label.grid(row=1, column=0, sticky="ne")
            self.file_label.bind("<Button-1>", self.open_in_folder)

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
