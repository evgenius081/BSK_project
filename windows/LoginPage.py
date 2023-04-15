from tkinter import *
from Colors import Colors
from elements.Login import Login


def login_page(connection) -> None:
    window = Tk()
    window.title("Connect")
    window.geometry('300x330')
    window["bg"] = Colors.MAIN_BG.value
    window.resizable(False, False)
    window.call('wm', 'iconphoto', window._w, PhotoImage(file='img/fav.png'))

    pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, confine=True, highlightthickness=0)

    login = Login(connection)
    main = login.render_login(window)
    connection.login_window = window
    paperclip = PhotoImage(file='img/paperclip-white-min.png')
    dots = PhotoImage(file='img/dots-white-min.png')
    paper_plane = PhotoImage(file='img/paper-plane-white-min.png')
    images = [dots, paperclip, paper_plane]
    connection.images = images
    main_zone = pav.create_window(36, 20, anchor=NW, window=main)
    pav.pack(expand=True)
    window.mainloop()

