import tkinter
from tkinter import *
from enum import Enum
from Colors import Colors


class CipherMethods(Enum):
    CBC = "CBC"
    ECB = "ECB"


cipher = CipherMethods.CBC


def send_message(txt) -> None:
    message_txt = txt.get('1.0', "end-1c")
    if message_txt[-2:] == '\n':
        message_txt = message_txt[:-2]
    txt.delete('1.0', "end-1c")


def enter_handler(event) -> None:
    send_message(event.widget)


def focus_in(event) -> None:
    event.widget.configure(font=("Verdana", 12), width=72, foreground="#ffffff")
    if event.widget.get("1.0", "end-1c") == "Write a message...":
        event.widget.delete("1.0", "end-1c")


def focus_out(event) -> None:
    if event.widget.compare("end-1c", "==", "1.0"):
        event.widget.configure(font=("Verdana", 10), width=90, foreground="#eeeeee")
        event.widget.insert("1.0", "Write a message...")


def handle_setting(method) -> None:
    global cipher
    cipher = CipherMethods[method]


def handle_a(default_value) -> None:
    pass


def change_format(bt, settings) -> None:
    try:         
        bt.configure(state="disabled")
        x = bt.winfo_rootx()-58
        y = bt.winfo_rooty()+14
        settings.tk_popup(x, y, 0)
    finally:
        settings.grab_release()
        bt.configure(state="normal")
        bt.configure(bg=Colors.BUTTON_BG.value)


def controls(main, images) -> None:
    text = Text(main, width=90, height=1, font=("Verdana", 10), wrap=WORD, padx=10, pady=6, bd=0,
                bg=Colors.BUTTON_BG.value, insertbackground="white", foreground="#eeeeee")
    text.grid(row=1, column=2,  rowspan=1)
    text.insert(INSERT, "Write a message...")
    text.bind("<FocusIn>", focus_in)
    text.bind("<FocusOut>", focus_out)
    text.bind("<Return>", enter_handler)

    default_value = StringVar(value=cipher.value)
    settings = Menu(main, font=("Verdana", 12), tearoff=0, background="white", activebackground=Colors.MAIN_BG.value,
                    foreground="#000000", postcommand=lambda: handle_a(default_value), borderwidth=0, bd=0,
                    cursor="hand2")
    for option in [i.value for i in list(CipherMethods)]:
        settings.add_radiobutton(label=option, font=("Verdana", "12"), command=lambda: handle_setting(option),
                                 variable=default_value, value=option)

    [dots, paperclip, paper_plane] = images

    more_button = Button(main, image=dots, height=32, width=35, compound="bottom", font=("Arial Bold", 16),
                         bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white",
                         activebackground=Colors.BUTTON_BG.value, activeforeground="white", relief=FLAT, cursor='hand2')
    attach_button = Button(main, image=paperclip, height=32, width=35, compound="bottom", font=("Arial Bold", 16),
                           bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white",
                           activebackground=Colors.BUTTON_BG.value, activeforeground="white", relief=FLAT,
                           cursor='hand2')
    send_button = Button(main, image=paper_plane, height=32, width=35, compound="bottom", font=("Arial Bold", 16),
                         bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white",
                         activebackground=Colors.BUTTON_BG.value, activeforeground="white", relief=FLAT, cursor='hand2')
 
    send_button.config(command=lambda: send_message(text))
    more_button.config(command=lambda: change_format(more_button, settings=settings))

    more_button.grid(row=1, column=0)
    attach_button.grid(row=1, column=1)
    send_button.grid(row=1, column=3)

