from tkinter import *
from Colors import Colors


def login(window):
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
    button = Button(wrap_frame, bg=Colors.LOGIN_BUTTON_BG.value, foreground=Colors.LOGIN_BUTTON_FOREGROUND.value,
                    text="Connect", width=2, height=1, font=("Arial Bold", 12), bd=0, highlightthickness=0,
                    cursor='hand2')
    button.grid(row=2, column=0, sticky="we", pady=20)

    ip_label = Label(wrap_frame, text="Your IP: 127.127.127.127:182", font=("Arial Bold", 10),
                     background=Colors.MAIN_BG.value, justify="center", foreground=Colors.LABEL_TEXT_COLOR.value,
                     cursor="hand2")
    ip_label.grid(row=3, column=0, pady=15)

    return main

