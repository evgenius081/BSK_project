from tkinter import *
from elements.Chat import chat
from Colors import Colors
from elements.Login import Login


def login() -> None:
    login = Login()
    window = Tk()
    window.title("Connect")
    window.geometry('300x330')
    window["bg"] = Colors.MAIN_BG.value
    window.resizable(False, False)
    window.call('wm', 'iconphoto', window._w, PhotoImage(file='img/fav.png'))

    pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, confine=True, highlightthickness=0)

    main = login.render_login(window)
    main_zone = pav.create_window(36, 20, anchor=NW, window=main)
    pav.pack(expand=True)
    window.mainloop()


def main() -> None:
    window = Tk()
    window.title("Messenger")
    window.geometry('863x505')
    window["bg"] = Colors.MAIN_BG.value
    window.resizable(False, False)
    window.call('wm', 'iconphoto', window._w, PhotoImage(file='img/fav.png'))

    paperclip = PhotoImage(file='img/paperclip-white-min.png')
    dots = PhotoImage(file='img/dots-white-min.png')
    paper_plane = PhotoImage(file='img/paper-plane-white-min.png')

    pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, confine=True, height=505, width=863, highlightthickness=0)

    main = chat(window, paperclip, dots, paper_plane)
    main_zone = pav.create_window(0, 0, anchor=NW, window=main)
    pav.pack()
    window.mainloop()


if __name__ == "__main__":
    login()

