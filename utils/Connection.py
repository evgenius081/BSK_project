import os
import pickle
import socket
import sys
import time
from timeit import default_timer as timer
from threading import *

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from elements.Chat import *
from utils.Encryption import Encryption
from classes.CipherModes import CipherMethods

BUFFER_SIZE = 8192
ENCRYPT_FOLDER = "enc"
DOWNLOAD_FOLDER = "downloads"


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
        self.BUFFER_SIZE_FILE = 64000

    def receive(self, connection) -> None:
        data = connection.recv(BUFFER_SIZE)
        message = pickle.loads(data)
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
                Thread(target=self.connection_check).start()
            else:
                self.login.is_connecting = True
                self.login.status_label.configure(text=f"127.0.0.1:{self.port} wants to connect\nProvide password")
                self.login.address_input.delete("1.0", END)
                self.login.address_input.insert("1.0", f"127.0.0.1:{self.port}")
                self.login.address_input.configure(state=DISABLED)
        elif message["type"] == "text":
            text = self.decrypt_data(message["data"], message["mode"])
            message["data"] = text
            self.chat.add_text_message(message, "partner")
        elif message["type"] == "file":
            Thread(target=self.receive_file, args=(connection, message,)).start()


    def _listen(self) -> None:
        while True:
            try:
                connection, address = self.socket.accept()
                self.IP = address[0]
                Thread(target=self.receive, args=(connection,)).start()
            except OSError:
                pass

    def connection_check(self):
        while True:
            time.sleep(1)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.connect((self.IP, self.port))
                    message = {"type": "check"}
                    sock.sendall(pickle.dumps(message))
                except Exception:
                    self.chat.set_disconnected()
                    break

        sys.exit()

    def _connect(self, ip, port, password) -> None:
        print(f"connecting to: {ip}:{port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, int(port)))
            self.encryption.create_private_key(self.encryption.hash(password))
            greetings = {"type": "greetings", "port": self.my_port,
                         "public_key": self.encryption.public_key.exportKey()}
            sock.sendall(pickle.dumps(greetings))
            self.login.is_connecting = True
            try:
                result = sock.recv(BUFFER_SIZE)
                message = pickle.loads(result)
                self.encryption.session_key = self.encryption.decrypt_key(self.encryption.private_key,
                                                                          message["session_key"])
            except EOFError:
                pass

        self.IP = ip
        self.port = int(port)
        self.found_partner = True
        self.chat = Chat(self.login.connection)
        self.chat.render_chat(self.login_window, self.images)
        Thread(target=self.connection_check).start()

        sys.exit()

    def connect(self, ip, port, password) -> None:
        Thread(target=self._connect, args=(ip, port, password,)).start()

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

    def _send_message(self, text, mode) -> None:
        enc = self.encrypt_data(text, mode)
        message = {"type": "text", "data": enc, "mode": mode}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print((self.IP, self.port))
            sock.connect((self.IP, self.port))
            sock.sendall(pickle.dumps(message))
        message["data"] = text
        self.chat.add_text_message(message, "me")

    def _send_file(self, path, mode) -> None:
        if not os.path.exists(ENCRYPT_FOLDER):
            os.makedirs(ENCRYPT_FOLDER)

        filename = os.path.split(path)[1]
        filesize = os.path.getsize(path)
        path_to_encrypted_file = os.path.join(ENCRYPT_FOLDER, filename + ".enc")
        message = {"type": "file", "filename": filename + ".enc", "size": filesize, "mode": mode}
        if mode == CipherMethods.ECB:
            mode = AES.MODE_ECB
        elif mode == CipherMethods.CBC:
            mode = AES.MODE_CBC

        sent_data_size = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.IP, self.port))
            sock.sendall(pickle.dumps(message))
            self.in_progress = True
            message["filename"] = message["filename"][:len(message["filename"]) - 4]
            file_message = self.chat.add_file_message(message, "me", self.images)
            start_timer = timer()
            self.encryption.encrypt_file(path, path_to_encrypted_file, mode)
            end_timer = timer()
            print("Encryption time:", end_timer - start_timer)
            file_message.start_sending()
            start_timer = timer()
            with open(path_to_encrypted_file, "rb") as file:
                data = file.read(self.BUFFER_SIZE_FILE)
                while data:
                    sent_data_size += self.BUFFER_SIZE_FILE
                    file_message.update_file_sending_procent(int(sent_data_size / filesize * 100))
                    sock.sendall(data)
                    data = file.read(self.BUFFER_SIZE_FILE)
                file_message.update_file_sending_procent(100)
                self.chat.file_sent()
                end_timer = timer()
        print("Sending time:", end_timer - start_timer)

        os.remove(path_to_encrypted_file)
        self.in_progress = False


    def receive_file(self, conn, message) -> None:
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)
        filename = message["filename"]
        message["filename"] = message["filename"][:len(message["filename"]) - 4]
        size = message["size"]
        mode = message["mode"]
        if mode == CipherMethods.ECB:
            mode = AES.MODE_ECB
        elif mode == CipherMethods.CBC:
            mode = AES.MODE_CBC

        path = os.path.join(DOWNLOAD_FOLDER, filename)

        real_filename = filename

        if os.path.exists(os.getcwd()+"\\"+path[:len(path) - 4]):
            path_temp = path[:len(path) - 4]
            count = 1
            while True:
                new_path = path_temp[:path_temp.rfind(".")]+f" ({count})"+path_temp[path_temp.rfind("."):]
                if not os.path.exists(os.getcwd()+"\\"+new_path):
                    path = new_path+".enc"
                    real_filename = (path_temp[:path_temp.rfind(".")]+f" ({count})" +
                                     path_temp[path_temp.rfind("."):])
                    break
                count += 1

        with open(path, "wb") as file:
            data = conn.recv(self.BUFFER_SIZE_FILE)
            while data:
                file.write(data)
                data = conn.recv(self.BUFFER_SIZE_FILE)

        file_message = self.chat.add_file_message(message, "partner", self.images)
        self.encryption.decrypt_file(path, size, mode=mode)
        file_message.update_decrypted(real_filename)
        os.remove(path)

    def send_file(self, path, mod) -> None:
        Thread(target=self._send_file, args=(path, mod,)).start()

    def send_message(self, text, mode) -> None:
        Thread(target=self._send_message, args=(text, mode,)).start()
