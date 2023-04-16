import pickle
import socket
from threading import *
from elements.Chat import *

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

    def receive(self, connection) -> None:
        data = connection.recv(BUFFER_SIZE)
        message = pickle.loads(data)
        print(message)
        if message["type"] == "greetings":
            connection.sendall(bytes("greetings", "utf-8"))
            self.port = int(message["port"])
            self.chat = Chat(self.login.connection)
            self.chat.render_chat(self.login_window, self.images)
        elif message["type"] == "text":
            print(message["data"])
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
            greetings = {"type": "greetings", "port": self.my_port}
            sock.sendall(pickle.dumps(greetings))
            result = sock.recv(BUFFER_SIZE).decode("utf-8")

        print(result)
        self.IP = ip
        self.port = int(port)
        self.found_partner = True
        self.chat = Chat(self.login.connection)
        self.chat.render_chat(self.login_window, self.images)

    def connect(self, ip, port) -> None:
        Thread(target=self._connect, args=(ip, port,)).start()

    def send_message(self, text):
        message = {"type": "text", "data": text}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print((self.IP, self.port))
            sock.connect((self.IP, self.port))
            sock.sendall(pickle.dumps(message))
        self.chat.add_message(message, "me")

