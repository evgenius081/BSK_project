from tkinter import *
import tkinter
from tkinter import ttk
from tkinter.ttk import *
from Messages import *
from DecryptedMessage import *
from Controls import Controls
from datetime import *
from Colors import Colors

def Chat(Window, paperclip, dots, paperPlane):

    Main = tkinter.Frame(Window, bg=Colors.BUTTON_BG.value)

    messages = [DecryptedTextMessage("a", "lorem ipsum", datetime.now(), Status.Read), DecryptedTextMessage("b", "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet", datetime.now(), Status.Sent)]

    fr = tkinter.Frame(Main, width=850, height=468, bd=0, bg=Colors.MAIN_BG.value)
    fr.grid(row=0, column=0, columnspan=4)

    canvas = tkinter.Canvas(fr, width=850, height=448, bg=Colors.MAIN_BG.value, bd=0, highlightthickness=0)
    canvas.pack(side=tkinter.LEFT, pady=10)

    style = Style()
    style.theme_use('clam')
    
    style.configure("Vertical.TScrollbar", gripcount=0,
                background=Colors.SCROLLBAR_HANDLE.value, darkcolor=Colors.MAIN_BG.value, lightcolor=Colors.MAIN_BG.value,
                troughcolor=Colors.MAIN_BG.value, bordercolor=Colors.MAIN_BG.value, arrowcolor=Colors.SCROLLBAR_HANDLE.value)

    scrollbar = ttk.Scrollbar(fr, orient=tkinter.VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    canvas.config(yscrollcommand=scrollbar.set)

    frame = tkinter.Frame(canvas, bg=Colors.MAIN_BG.value)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    canvas.create_window((0, 5), window=frame, anchor='nw', width=850)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    Controls(Main, dots, paperclip, paperPlane)

    for i in range(0, 60, 3):
        for message in messages:
            Messages(frame, message, i+messages.index(message))

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    return Main