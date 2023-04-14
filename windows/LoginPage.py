from tkinter import *
from Colors import Colors
from elements.Login import Login


def login_page() -> None:
    window = Tk()
    window.title("Connect")
    window.geometry('300x330')
    window["bg"] = Colors.MAIN_BG.value
    window.resizable(False, False)
    window.call('wm', 'iconphoto', window._w, PhotoImage(file='img/fav.png'))

    pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, confine=True, highlightthickness=0)

    login = Login()
    main = login.render_login(window)
    main_zone = pav.create_window(36, 20, anchor=NW, window=main)
    pav.pack(expand=True)
    window.mainloop()
