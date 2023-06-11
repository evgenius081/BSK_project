import threading
import tkinter
from datetime import datetime
from tkinter import ttk
from tkinter import filedialog
from classes.CipherModes import *
from elements.FileMessage import FileMessage
from elements.TextMessage import *
from classes.DecryptedMessage import DecryptedTextMessage, DecryptedFileMessage


def focus_out(event) -> None:
    if event.widget.compare("end-1c", "==", "1.0"):
        event.widget.configure(font=("Verdana", 10), width=90, foreground="#eeeeee")
        event.widget.insert("1.0", "Write a message...")


def handle_a(default_value) -> None:
    pass


def change_format(bt, settings) -> None:
    try:
        bt.configure(state="disabled")
        x = bt.winfo_rootx() - 58
        y = bt.winfo_rooty() + 14
        settings.tk_popup(x, y, 0)
    finally:
        settings.grab_release()
        bt.configure(state="normal")
        bt.configure(bg=Colors.BUTTON_BG.value)


class Chat:
    def __init__(self, connection) -> None:
        self.connection = connection
        self.cipher = CipherMethods.CBC
        self.messages = []
        self.lock = threading.Lock()
        self.message_frame = None
        self.canvas = None
        self.default_value = None
        self.current_file = None
        self.file_attached = False
        self.send_button = None
        self.text = None
        self.disconnected = False

    def file_sent(self) -> None:
        self.file_attached = False
        self.current_file = None
        self.text.configure(state=NORMAL)
        self.text.delete("1.0", "end-1c")
        self.text.configure(font=("Verdana", 12), width=72, foreground="#ffffff")

    def focus_in(self, event) -> None:
        if not self.file_attached:
            event.widget.configure(font=("Verdana", 12), width=72, foreground="#ffffff")
            if event.widget.get("1.0", "end-1c") == "Write a message...":
                event.widget.delete("1.0", "end-1c")

    def attach_file(self) -> None:
        chosen_file = filedialog.askopenfilename()
        if chosen_file != "":
            self.current_file = chosen_file
            self.text.configure(font=("Verdana", 10), width=90, foreground="#eeeeee")
            self.text.delete("1.0", "end-1c")
            self.text.insert("1.0", f"file: {self.current_file}")
            self.text.configure(state=DISABLED)
            self.file_attached = True

    def set_disconnected(self):
        if not self.disconnected:
            disconnected_message = Frame(self.message_frame, bg=Colors.MAIN_BG.value, width=850)
            self.messages.append(disconnected_message)
            disconnected_message.grid(row=self.messages.index(disconnected_message), column=0, columnspan=2)

            disconnected_frame = Frame(disconnected_message, bg=Colors.MESSAGE_BG.value, width=850, height=2)
            disconnected_frame.grid(row=0, column=0)

            disconnected_label = Label(disconnected_message, bg=Colors.MAIN_BG.value, foreground=Colors.MESSAGE_BG.value,
                                       font=("Verdana", "12"),
                                       text=f"{self.connection.IP}:{self.connection.port} disconnected", justify=CENTER)
            disconnected_label.grid(row=0, column=0)
            self.send_button.config(state=DISABLED)
            self.text.unbind("<Return>")
            self.disconnected = True

    def send_message(self, txt) -> None:
        message_txt = txt.get('1.0', END).strip()
        txt.delete('1.0', END)
        if self.file_attached:
            self.connection.send_file(self.current_file, self.cipher)
            self.canvas.yview_moveto(1)
        elif len(message_txt) > 0:
            self.connection.send_message(message_txt, self.cipher)
            self.canvas.yview_moveto(1)

    def enter_handler(self, event) -> None:
        self.send_message(event.widget)

    def handle_setting(self, method) -> None:
        self.cipher = CipherMethods[method]
        self.default_value.set(method)

    def add_text_message(self, message, author) -> None:
        with self.lock:
            self.messages.append(message)
            text_message(self.message_frame, DecryptedTextMessage(author, message["data"], datetime.now(),
                                                                  message["mode"]), len(self.messages)-1)
            self.message_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.canvas.yview_moveto(1)

    def add_file_message(self, message, author, images) -> FileMessage:
        with self.lock:
            self.messages.append(message)
            file_message = FileMessage()
            file_message.file_message(self.message_frame, DecryptedFileMessage(author, message["filename"],
                                                                               datetime.now(), message["mode"]),
                                      len(self.messages)-1, images),
            self.message_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.canvas.yview_moveto(1)
            return file_message

    def render_chat(self, window, images) -> None:
        for widget in window.winfo_children():
            widget.destroy()
        window.title(f"Messenger")
        window.geometry('863x505')
        window["bg"] = Colors.MAIN_BG.value
        pav = Canvas(window, bd=0, bg=Colors.MAIN_BG.value, confine=True, height=505, width=863, highlightthickness=0)

        main = tkinter.Frame(window, bg=Colors.BUTTON_BG.value)

        fr = tkinter.Frame(main, width=850, height=468, bd=0, bg=Colors.MAIN_BG.value)
        fr.grid(row=0, column=0, columnspan=4)

        self.canvas = tkinter.Canvas(fr, width=850, height=448, bg=Colors.MAIN_BG.value, bd=0, highlightthickness=0)
        self.canvas.pack(side=tkinter.LEFT, pady=10)

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Vertical.TScrollbar", gripcount=0,
                        background=Colors.SCROLLBAR_HANDLE.value, darkcolor=Colors.MAIN_BG.value,
                        lightcolor=Colors.MAIN_BG.value,
                        troughcolor=Colors.MAIN_BG.value, bordercolor=Colors.MAIN_BG.value,
                        arrowcolor=Colors.SCROLLBAR_HANDLE.value)

        scrollbar = ttk.Scrollbar(fr, orient=tkinter.VERTICAL, command=self.canvas.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.config(yscrollcommand=scrollbar.set)

        self.message_frame = tkinter.Frame(self.canvas, bg=Colors.MAIN_BG.value)
        self.message_frame.grid_columnconfigure(0, weight=1)
        self.message_frame.grid_columnconfigure(1, weight=1)

        connected_message = Frame(self.message_frame, bg=Colors.MAIN_BG.value, width=850)
        connected_message.grid(row=0, column=0, columnspan=2)
        self.messages.append(connected_message)

        connected_frame = Frame(connected_message, bg=Colors.MESSAGE_BG.value, width=850, height=2)
        connected_frame.grid(row=0, column=0)

        connected_label = Label(connected_message, bg=Colors.MAIN_BG.value, foreground=Colors.MESSAGE_BG.value,
                                font=("Verdana", "12"),
                                text=f"Connected with {self.connection.IP}:{self.connection.port}", justify=CENTER)
        connected_label.grid(row=0, column=0)

        self.canvas.create_window((0, 5), window=self.message_frame, anchor='nw', width=850)

        def on_mousewheel(event) -> None:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.controls(main, images)

        self.message_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        pav.create_window(0, 0, anchor=NW, window=main)
        pav.pack()

    def controls(self, main, images) -> None:
        self.text = Text(main, width=90, height=1, font=("Verdana", 10), wrap=WORD, padx=10, pady=6, bd=0,
                         bg=Colors.BUTTON_BG.value, insertbackground="white", foreground="#eeeeee")
        self.text.grid(row=1, column=2, rowspan=1)
        self.text.insert(1.0, "Write a message...")
        self.text.bind("<FocusIn>", self.focus_in)
        self.text.bind("<FocusOut>", focus_out)
        self.text.bind("<Return>", self.enter_handler)

        self.default_value = StringVar(value="CBC")
        settings = Menu(main, font=("Verdana", 12), tearoff=0, background="white", activebackground=Colors.MAIN_BG.value,
                        foreground="#000000", postcommand=lambda: handle_a(self.default_value), borderwidth=0, bd=0,
                        cursor="hand2")
        settings.add_radiobutton(label="CBC", font=("Verdana", "12"), command=lambda: self.handle_setting("CBC"),
                                 variable=self.default_value, value="CBC")
        settings.add_radiobutton(label="ECB", font=("Verdana", "12"), command=lambda: self.handle_setting("ECB"),
                                 variable=self.default_value, value="ECB")

        [dots, paperclip, paper_plane, file_black, arrow_up, lock] = images

        more_button = Button(main, image=dots, height=32, width=35, compound="bottom", font=("Arial Bold", 16),
                             bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white",
                             activebackground=Colors.BUTTON_BG.value, activeforeground="white", relief=FLAT, cursor='hand2')
        attach_button = Button(main, image=paperclip, height=32, width=35, compound="bottom", font=("Arial Bold", 16),
                               bg=Colors.BUTTON_BG.value, fg="white", justify="left", disabledforeground="white",
                               activebackground=Colors.BUTTON_BG.value, activeforeground="white", relief=FLAT,
                               cursor='hand2')
        self.send_button = Button(main, image=paper_plane, height=32, width=35, compound="bottom",
                                  font=("Arial Bold", 16), bg=Colors.BUTTON_BG.value, fg="white", justify="left",
                                  disabledforeground="white", activebackground=Colors.BUTTON_BG.value,
                                  activeforeground="white", relief=FLAT, cursor='hand2')

        self.send_button.config(command=lambda: self.send_message(self.text))
        attach_button.config(command=lambda: self.attach_file())
        more_button.config(command=lambda: change_format(more_button, settings=settings))

        more_button.grid(row=1, column=0)
        attach_button.grid(row=1, column=1)
        self.send_button.grid(row=1, column=3)

