from tkinter import *
from Chat import Chat
from time import sleep
from tkinter import messagebox
from Colors import Colors


Window = Tk()
Window.title("Messenger")
Window.geometry('863x505') 
Window["bg"] = Colors.MAIN_BG.value
Window.resizable = False
Window.call('wm', 'iconphoto', Window._w, PhotoImage(file='img/fav.png'))

Main = Frame(Window)

paperclip = PhotoImage(file='img/paperclip-white-min.png')
dots = PhotoImage(file='img/dots-white-min.png')
paperPlane = PhotoImage(file='img/paper-plane-white-min.png')

pav = Canvas(Window, bd=0, bg = Colors.MAIN_BG.value, confine = True, height = 505, width = 863, highlightthickness=0)

Main = Chat(Window, paperclip, dots, paperPlane)
MainZone = pav.create_window(0, 0, anchor=NW, window=Main)

pav.pack()

Window.mainloop()