import random
from tkinter import *
from utils.Connection import Connection
from windows.LoginPage import login_page

if __name__ == "__main__":
    port = random.randint(100, 9999)
    connection = Connection(port)
    login_page(connection)

