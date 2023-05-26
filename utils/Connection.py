import pickle
import socket
import time
from threading import *

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from elements.Chat import *
from utils.Encryption import Encryption
from classes.CipherModes import CipherMethods

BUFFER_SIZE = 8192


class Connection:
    def __init__(self, port):
        self.my_IP = "127.0.0.1"
        self.my_port = port
        self.IP = None
        self.port = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.my_IP, self.my_port))
        self.socket.listen(1)
        self.listen_thread = Thread(target=self._listen).start()
        self.login_window = None
        self.login = None
        self.images = None
        self.chat = None
        self.encryption = Encryption()

    def receive(self, connection) -> None:
        data = connection.recv(BUFFER_SIZE)
        message = pickle.loads(data)
        print(message)
        key = None

        if "public_key" in message:
            self.encryption.generate_session_key()
            another_user_key = RSA.import_key(message["public_key"])
            key = self.encryption.encrypt_key(another_user_key, self.encryption.session_key)

        if message["type"] == "greetings":
            key_change = {"type": "key", "session_key": key}
            self.port = int(message["port"])
            if self.login.is_connecting:
                self.chat = Chat(self.login.connection)
                self.chat.render_chat(self.login_window, self.images)
                connection.sendall(pickle.dumps(key_change))
            else:
                self.login.is_connecting = True
                self.login.status_label.configure(text=f"127.0.0.1:{self.port} wants to connect\nProvide password")
                self.login.address_input.delete("1.0", END)
                self.login.address_input.insert("1.0", f"127.0.0.1:{self.port}")
                self.login.address_input.configure(state=DISABLED)
            # add cypher of session key by public key
        elif message["type"] == "text":
            text = self.decrypt_data(message["data"], message["mode"])
            message["data"] = text
            self.chat.add_text_message(message, "partner")

    def _listen(self) -> None:
        while True:
            try:
                connection, address = self.socket.accept()
                self.IP = address[0]
                Thread(target=self.receive, args=(connection,)).start()
            except OSError:
                pass

    def _connect(self, ip, port, password) -> None:
        print(f"connecting to: {ip}:{port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, int(port)))
            self.encryption.create_private_key(self.encryption.hash(password))
            # send public key
            # if not self.login.is_connecting:
            greetings = {"type": "greetings", "port": self.my_port, "public_key": self.encryption.public_key.exportKey()}
            sock.sendall(pickle.dumps(greetings))
            self.login.is_connecting = True
            result = sock.recv(BUFFER_SIZE)
            message = pickle.loads(result)
            self.encryption.session_key = self.encryption.decrypt_key(self.encryption.private_key,
                                                                      message["session_key"])



        self.IP = ip
        self.port = int(port)
        self.found_partner = True
        self.login.password_input.configure(state=DISABLED)
        self.login.address_input.configure(state=DISABLED)
        self.chat = Chat(self.login.connection)
        self.chat.render_chat(self.login_window, self.images)

    def connect(self, ip, port, password) -> None:
        Thread(target=self._connect, args=(ip, port, password, )).start()

    def decrypt_data(self, data, mode) -> bytes:
        if mode == CipherMethods.ECB:
            return self.encryption.decrypt_mode(data)
        elif mode == CipherMethods.CBC:
            return self.encryption.decrypt_mode(data, AES.MODE_CBC)

    def encrypt_data(self, data, mode) -> bytes:
        if mode == CipherMethods.ECB:
            return self.encryption.encrypt_mode(data)
        elif mode == CipherMethods.CBC:
            return self.encryption.encrypt_mode(data, AES.MODE_CBC)

    def send_message(self, text, mode) -> None:
        # add mode
        enc = self.encrypt_data(text, mode)
        message = {"type": "text", "data": enc, "mode": mode}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print((self.IP, self.port))
            sock.connect((self.IP, self.port))
            sock.sendall(pickle.dumps(message))
        message["data"] = text
        self.chat.add_text_message(message, "me")
        self.chat.add_file_message({"type": "file", "filename": "paperclip-white-min.png", "mode": mode}, "me", self.images)
        self.chat.add_file_message({"type": "file", "filename": "paperclip-white-min.png", "mode": mode}, "partner", self.images)

