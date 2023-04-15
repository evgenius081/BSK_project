import tkinter
from tkinter import ttk
from tkinter.ttk import *
from classes.Messages import *
from classes.DecryptedMessage import *
from elements.Controls import controls
from datetime import *
from Colors import Colors


def chat(window, images) -> tkinter.Frame:

    main = tkinter.Frame(window, bg=Colors.BUTTON_BG.value)

    fr = tkinter.Frame(main, width=850, height=468, bd=0, bg=Colors.MAIN_BG.value)
    fr.grid(row=0, column=0, columnspan=4)

    canvas = tkinter.Canvas(fr, width=850, height=448, bg=Colors.MAIN_BG.value, bd=0, highlightthickness=0)
    canvas.pack(side=tkinter.LEFT, pady=10)

    style = Style()
    style.theme_use('clam')
    
    style.configure("Vertical.TScrollbar", gripcount=0,
                    background=Colors.SCROLLBAR_HANDLE.value, darkcolor=Colors.MAIN_BG.value,
                    lightcolor=Colors.MAIN_BG.value,
                    troughcolor=Colors.MAIN_BG.value, bordercolor=Colors.MAIN_BG.value,
                    arrowcolor=Colors.SCROLLBAR_HANDLE.value)

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

    controls(main, images)

    # messages_list = [DecryptedTextMessage("a", "lorem ipsum", datetime.now(), Status.Read), DecryptedTextMessage("b",
    #                                                                                                             "lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
    #                                                                                                             datetime.now(),
    #                                                                                                             Status.Sent)]
    # for i in range(0, 60, 3):
    #     for message in messages_list:
    #         messages(frame, message, i+messages_list.index(message))

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    return main

