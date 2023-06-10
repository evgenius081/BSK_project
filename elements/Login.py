import tkinter as tk
import pyperclip
from utils.Connection import *
import re


class Login:
    def __init__(self, connection):
        self.connection = connection
        self.port = connection.my_port
        self.ip = self.connection.my_IP
        self.status_label = None
        self.connect_button = None
        self.is_connecting = False
        self.address_input = None
        self.password_input = None

    def copy_address(self, event) -> None:
        pyperclip.copy(f"{self.ip}:{self.port}")
        event.widget.configure(text=f"Your IP: {self.ip}:{self.port}\nCopied")
        event.widget.after(2000, lambda: event.widget.configure(text=f"Your IP: {self.ip}:{self.port}"))

    def connect_handler(self, connection_string, password) -> None:
        if not self.is_connecting and not \
                re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}:[1-9]\d\d\d?$", connection_string):
            self.status_label.configure(text=f"Your IP: {self.ip}:{self.port}\nProvide valid IP")
            self.status_label.after(2000, lambda: self.status_label.configure(text=f"Your IP: {self.ip}:{self.port}"))
            return
        if password.strip() == "":
            self.status_label.configure(text=f"Your IP: {self.ip}:{self.port}\nProvide valid password")
            self.status_label.after(2000, lambda: self.status_label.configure(text=f"Your IP: {self.ip}:{self.port}"))
            return
        ip = connection_string.split(":")[0]
        port = connection_string.split(":")[1]
        self.connect_button.configure(text="Connecting...")
        self.connection.connect(ip, port, password)

    def render_login(self) -> None:
        window = Tk()
        window.title("Connect")
        window.geometry('300x330')
        window["bg"] = Colors.MAIN_BG.value
        window.resizable(False, False)
        window.call('wm', 'iconphoto', window._w, PhotoImage(file='img/fav.png'))

        pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, height=330, confine=True, highlightthickness=0)

        self.connection.login_window = window
        paperclip = PhotoImage(file='img/paperclip-white-min.png')
        dots = PhotoImage(file='img/dots-white-min.png')
        paper_plane = PhotoImage(file='img/paper-plane-white-min.png')
        file_black = PhotoImage(file='img/file_black_min.png')
        arrow_up = PhotoImage(file='img/arrow-up-from-bracket-min.png')
        lock = PhotoImage(file='img/lock-min.png')
        images = [dots, paperclip, paper_plane, file_black, arrow_up, lock]
        self.connection.images = images

        main = tkinter.Frame(window, bg=Colors.MAIN_BG.value)

        wrap_frame = tk.Frame(main, bg=Colors.MAIN_BG.value)
        wrap_frame.pack(side=TOP)

        input_frame = Frame(wrap_frame, bg=Colors.MAIN_BG.value)
        input_frame.grid(row=1, column=0, sticky="w")

        title_label = Label(wrap_frame, text="Messenger", font=("Arial Bold", 18),
                            background=Colors.MAIN_BG.value, justify="center",
                            foreground=Colors.LABEL_TEXT_COLOR.value)
        title_label.grid(row=0, column=0, pady=35)

        text_label = Label(input_frame, text="Enter IP and Port", font=("Arial Bold", 10),
                           background=Colors.MAIN_BG.value, justify="left",
                           foreground=Colors.LABEL_TEXT_COLOR.value, pady=5)
        text_label.grid(row=0, column=0, sticky="nw")

        self.address_input = Text(input_frame, font=("Arial Bold", 12), height=1, width=25)
        self.address_input.grid(row=1, column=0, sticky="we")

        password_label = Label(input_frame, text="Enter Password", font=("Arial Bold", 10),
                               background=Colors.MAIN_BG.value, justify="left",
                               foreground=Colors.LABEL_TEXT_COLOR.value, pady=5)
        password_label.grid(row=2, column=0, sticky="nw")

        self.password_input = Entry(input_frame, show="*", font=("Arial Bold", 12), width=25)
        self.password_input.grid(row=3, column=0, sticky="we")

        self.connect_button = Button(wrap_frame, bg=Colors.LOGIN_BUTTON_BG.value,
                                     foreground=Colors.LOGIN_BUTTON_FOREGROUND.value,
                                     text="Connect", width=2, height=1, font=("Arial Bold", 12), bd=0,
                                     highlightthickness=0,
                                     cursor='hand2')
        self.connect_button.grid(row=2, column=0, sticky="we", pady=20)
        self.connect_button.configure(command=lambda: self.connect_handler(self.address_input.get(1.0, "end-1c"),
                                                                           self.password_input.get()))

        self.status_label = Label(wrap_frame, text=f"Your IP: {self.ip}:{self.port}", font=("Arial Bold", 10),
                                  background=Colors.MAIN_BG.value, justify="center",
                                  foreground=Colors.LABEL_TEXT_COLOR.value,
                                  cursor="hand2")
        self.status_label.grid(row=3, column=0, pady=15)
        self.status_label.bind("<Button-1>", self.copy_address)

        pav.create_window(36, 0, anchor=NW, window=main)
        pav.pack(expand=True)
        window.mainloop()
