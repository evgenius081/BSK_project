import pickle
import socket
from threading import *

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from elements.Chat import *
from utils.Encryption import Encryption
from classes.CipherModes import CipherMethods

BUFFER_SIZE = 8192


class Connection:
    def __init__(self, port):
        self.my_IP = "127.0.0.1" #socket.gethostbyname(socket.gethostname())
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
            self.chat = Chat(self.login.connection)
            self.chat.render_chat(self.login_window, self.images)
            connection.sendall(pickle.dumps(key_change))
            # add cypher of session key by public key
        elif message["type"] == "text":
            text = self.decrypt_data(message["data"], message["mode"])
            print(text)
            message["data"] = text
            self.chat.add_message(message, "partner")

    def _listen(self) -> None:
        while True:
            try:
                connection, address = self.socket.accept()
                self.IP = address[0]
                Thread(target=self.receive, args=(connection,)).start()
            except OSError:
                pass

    def _connect(self, ip, port) -> None:
        print(f"connecting to: {ip}:{port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, int(port)))
            # send public key
            greetings = {"type": "greetings", "port": self.my_port, "public_key": self.encryption.public_key.exportKey()}
            sock.sendall(pickle.dumps(greetings))
            result = sock.recv(BUFFER_SIZE)
            message = pickle.loads(result)
            self.encryption.session_key = self.encryption.decrypt_key(self.encryption.private_key,
                                                                      message["session_key"])

        print(result)
        self.IP = ip
        self.port = int(port)
        self.found_partner = True
        self.chat = Chat(self.login.connection)
        self.chat.render_chat(self.login_window, self.images)

    def connect(self, ip, port) -> None:
        Thread(target=self._connect, args=(ip, port,)).start()

    def decrypt_data(self, data, mode):
        if mode == CipherMethods.ECB:
            return self.encryption.decrypt_mode(data)
        elif mode == CipherMethods.CBC:
            return self.encryption.decrypt_mode(data, AES.MODE_CBC)

    def encrypt_data(self, data, mode):
        if mode == CipherMethods.ECB:
            return self.encryption.encrypt_mode(data)
        elif mode == CipherMethods.CBC:
            return self.encryption.encrypt_mode(data, AES.MODE_CBC)

    def send_message(self, text, mode):
        # add mode
        enc = self.encrypt_data(text, mode)
        message = {"type": "text", "data": enc, "mode": mode}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print((self.IP, self.port))
            sock.connect((self.IP, self.port))
            sock.sendall(pickle.dumps(message))
        message["data"] = text
        self.chat.add_message(message, "me")

