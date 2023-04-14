import pickle
import socket
from threading import *
from windows.ChatPage import main

BUFFER_SIZE = 8192


class Connection:
    def __init__(self, port):
        self.my_IP = socket.gethostbyname(socket.gethostname())
        self.my_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.my_IP, self.my_port))
        self.found_partner = False
        self.IP = None
        self.port = None

        Thread(target=self._listen()).start()

    def connection_recieve(self, connection, ip):
        data = connection.recv(BUFFER_SIZE)
        info = pickle.loads(data)
        print(info)
        if info["type"] == "greetings":
            self.IP = ip
            self.port = int(info["port"])
            connection.sendall("greetings")
            self.found_partner = True

    def _listen(self):
        print("Started listening")
        while not self.found_partner:
            try:
                connection, ip = self.socket.accept()
                Thread(target=self.connection_recieve, args=(connection, ip,)).start()
            except OSError:
                pass

    def _connect(self, ip, port, login_window) -> None:
        print(f"connecting to: {ip}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        greetings = {"type": "greetings", "port": self.my_port}
        sock.sendall(pickle.dumps(greetings))
        result = sock.recv(BUFFER_SIZE).decode("utf-8")

        print(result)
        sock.close()
        login_window.destroy()
        main.main()

    def connect(self, ip, port, login_window) -> None:
        Thread(target=self._connect, args=(ip, port, login_window,)).start()

