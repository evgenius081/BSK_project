from tkinter import *
from Colors import Colors

MAX_MESSAGE_WIDTH = 42


def messages(parent, message, message_id):
    frame = Frame(parent, width=210, height=30)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    text = Text(frame, font=("Verdana", 11), bd=0, wrap=WORD)
    text.insert(INSERT, message.text)
    time = Label(frame, text=message.datetime.strftime("%H:%M"), font=("Verdana", 7),
                 foreground=Colors.MESSAGES_TIME_FOREGROUND.value)
    if message.author_id == "a":
        frame.config(bg=Colors.MY_MESSAGE_BG.value)
        frame.grid(row=message_id, column=1, sticky="ne", padx=6, pady=3)
        text.config(background=Colors.MY_MESSAGE_BG.value, foreground=Colors.MY_MESSAGES_TEXT_FOREGROUND.value, padx=6)
        time.config(bg=Colors.MY_MESSAGE_BG.value)
        time.grid(row=1, column=0, padx=6, sticky="nw")
    else:
        frame.config(bg=Colors.MESSAGE_BG.value)
        frame.grid(row=message_id, column=0, sticky="nw", padx=6, pady=3)
        text.config(background=Colors.MESSAGE_BG.value, foreground=Colors.MESSAGES_TEXT_FOREGROUND.value)
        time.config(bg=Colors.MESSAGE_BG.value)
        time.grid(row=1, column=0, padx=6, sticky="ne")

    parent.update_idletasks()

    symbols_number = len(text.get("1.0", "end-1c").replace("\n", ""))
    width = symbols_number - 1
    height = 1
    if symbols_number > MAX_MESSAGE_WIDTH:
        if not (text.get("1.0", "end-1c")[MAX_MESSAGE_WIDTH-1].isalpha()):
            width = MAX_MESSAGE_WIDTH - 1
        else:
            width = MAX_MESSAGE_WIDTH - 1
        height = int(symbols_number/width)
        
    text.config(width=width, height=height)

    text.config(state="disabled")
    text.grid(row=0, column=0, padx=6)

