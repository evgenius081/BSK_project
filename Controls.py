from tkinter import *
from tkinter import ttk
from enum import Enum
from datetime import *
from Colors import Colors

class CipherMethods(Enum):
    CBC = "CBC"
    ECB = "ECB"

cipher = CipherMethods.CBC


def SendMessage(txt):
    message_txt = txt.get('1.0', "end-1c")
    if message_txt[-2:] == '\n':
        message_txt = message_txt[:-2]
    txt.delete('1.0', "end-1c")
    print(message_txt)
    print("'" + txt.get('1.0', "end-1c") + "'")
    
def enterHandler(event):
    SendMessage(event.widget)

def focusIn(event):
    event.widget.configure(font=("Verdana", 12), width=72, foreground="#ffffff")
    if event.widget.get("1.0", "end-1c") == "Write a message...":
        event.widget.delete("1.0", "end-1c")

def focusOut(event):
    if event.widget.compare("end-1c", "==", "1.0"):
        event.widget.configure(font=("Verdana", 10), width=90, foreground="#eeeeee")
        event.widget.insert("1.0", "Write a message...")

def handleSetting(method):
    global cipher
    cipher = CipherMethods[method]

def handleA(defaultValue):
    pass


def ChangeFormat(bt, settings):
    try:         
        bt.configure(state = "disabled")
        x = bt.winfo_rootx()-58
        y = bt.winfo_rooty()+14
        settings.tk_popup(x, y, 0)
    finally:
        settings.grab_release()
        bt.configure(state = "normal")
        bt.configure(bg = Colors.BUTTON_BG)

def Controls(Main, dots, paperclip, paperPlane): 
    text = Text(Main, width=90, height=1, font=("Verdana", 10), wrap=WORD, padx=10, pady=6, bd=0, bg=Colors.BUTTON_BG.value, insertbackground="white", foreground="#eeeeee")
    text.grid(row = 1, column = 2,  rowspan = 1)
    text.insert(INSERT, "Write a message...")
    text.bind("<FocusIn>", focusIn)
    text.bind("<FocusOut>", focusOut)
    text.bind("<Return>", enterHandler)

    defaultValue = StringVar(value=cipher.value)
    settings = Menu(Main, font=("Verdana", 12), tearoff=0, background="white", activebackground=Colors.MAIN_BG.value, foreground="#000000", postcommand= lambda: handleA(defaultValue), borderwidth=0, bd=0, cursor="hand2")
    for option in [i.value for i in list(CipherMethods)]:
        settings.add_radiobutton(label=option, font=("Verdana", "12"), command= lambda: handleSetting(option), variable=defaultValue, value=option)


    more_button = Button(Main, image = dots, height = 32, width = 35, compound="bottom", font=("Arial Bold", 16), bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white", activebackground = Colors.BUTTON_BG.value, activeforeground="white", relief = FLAT, cursor='hand2')
    attach_button = Button(Main, image = paperclip, height = 32, width = 35, compound="bottom", font=("Arial Bold", 16), bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white", activebackground = Colors.BUTTON_BG.value, activeforeground="white", relief = FLAT, cursor='hand2')
    send_button = Button(Main, image = paperPlane, height = 32, width = 35, compound="bottom", font=("Arial Bold", 16), bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white", activebackground = Colors.BUTTON_BG.value, activeforeground="white", relief = FLAT, cursor='hand2')
 
    send_button.config(command = lambda: SendMessage(text))
    more_button.config(command = lambda: ChangeFormat(more_button, settings=settings))

    more_button.grid(row = 1, column = 0)
    attach_button.grid(row = 1, column = 1)
    send_button.grid(row = 1, column = 3)