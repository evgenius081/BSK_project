import pickle
import socket
from threading import *
from windows.ChatPage import main_page

BUFFER_SIZE = 8192


class Connection:
    def __init__(self, port):
        self.my_IP = "127.0.0.1" #socket.gethostbyname(socket.gethostname())
        self.my_port = port
        self.found_partner = False
        self.IP = None
        self.port = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.my_IP, self.my_port))
        self.socket.listen(1)
        self.listen_thread = Thread(target=self._listen).start()
        self.login_window = None
        self.images = None

    def connection_recieve(self, connection, ip):
        data = connection.recv(BUFFER_SIZE)
        info = pickle.loads(data)
        print(info)
        if info["type"] == "greetings":
            self.IP = ip
            self.port = int(info["port"])
            connection.sendall(bytes("greetings", "utf-8"))
            self.found_partner = True
            main_page(self.login_window, self.images)

    def _listen(self):
        print("Started listening")
        while not self.found_partner:
            try:
                connection, ip = self.socket.accept()
                print("found smth")
                Thread(target=self.connection_recieve, args=(connection, ip,)).start()
            except OSError:
                pass

    def _connect(self, ip, port) -> None:
        print(f"connecting to: {ip}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))
        greetings = {"type": "greetings", "port": self.my_port}
        sock.sendall(pickle.dumps(greetings))
        result = sock.recv(BUFFER_SIZE).decode("utf-8")

        print(result)
        sock.close()
        self.found_partner = True
        main_page(self.login_window, self.images)

    def connect(self, ip, port) -> None:
        Thread(target=self._connect, args=(ip, port,)).start()

