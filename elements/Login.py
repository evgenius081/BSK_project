import random
import tkinter
from tkinter import *
from Colors import Colors
import pyperclip
from utils.Connection import *


class Login:
    def __init__(self):
        self.port = random.randint(100, 9999)
        self.communication = Connection(self.port)
        self.ip = self.communication.my_IP
        self.status_label = None
        self.connect_button = None

    def copy_address(self, event) -> None:
        pyperclip.copy(f"{self.ip}:{self.port}")
        event.widget.configure(text=f"Your IP: {self.ip}:{self.port}\nCopied")
        event.widget.after(2000, lambda: event.widget.configure(text=f"Your IP: {self.ip}:{self.port}"))

    def connect_handler(self, connection_string, window) -> None:
        ip = connection_string.split(":")[0]
        port = connection_string.split(":")[1]
        self.connect_button.configure(text="Connecting...")
        self.communication.connect(ip, port, window)

    def render_login(self, window) -> tkinter.Frame:
        main = Frame(window, bg=Colors.MAIN_BG.value)

        wrap_frame = Frame(main, bg=Colors.MAIN_BG.value)
        wrap_frame.pack(side=TOP)

        input_frame = Frame(wrap_frame, bg=Colors.MAIN_BG.value)
        input_frame.grid(row=1, column=0, sticky="w")

        title_label = Label(wrap_frame, text="Messenger", font=("Arial Bold", 18),
                            background=Colors.MAIN_BG.value, justify="center", foreground=Colors.LABEL_TEXT_COLOR.value)
        title_label.grid(row=0, column=0, pady=35)

        text_label = Label(input_frame, text="Enter IP and Port", font=("Arial Bold", 10),
                           background=Colors.MAIN_BG.value, justify="left", foreground=Colors.LABEL_TEXT_COLOR.value, pady=5)
        text_label.grid(row=0, column=0, sticky="nw")

        text = Text(input_frame, font=("Arial Bold", 12), height=1, width=25)
        text.grid(row=1, column=0, sticky="we")
        self.connect_button = Button(wrap_frame, bg=Colors.LOGIN_BUTTON_BG.value, foreground=Colors.LOGIN_BUTTON_FOREGROUND.value,
                        text="Connect", width=2, height=1, font=("Arial Bold", 12), bd=0, highlightthickness=0,
                        cursor='hand2')
        self.connect_button.grid(row=2, column=0, sticky="we", pady=20)
        self.connect_button.configure(command=lambda: self.connect_handler(text.get(1.0, "end-1c"), window))

        self.status_label = Label(wrap_frame, text=f"Your IP: {self.ip}:{self.port}", font=("Arial Bold", 10),
                         background=Colors.MAIN_BG.value, justify="center", foreground=Colors.LABEL_TEXT_COLOR.value,
                         cursor="hand2")
        self.status_label.grid(row=3, column=0, pady=15)
        self.status_label.bind("<Button-1>", self.copy_address)

        return main

