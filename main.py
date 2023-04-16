import random
from utils.Connection import Connection
from elements.Login import Login

if __name__ == "__main__":
    port = random.randint(100, 9999)
    connection = Connection(port)
    login = Login(connection)
    connection.login = login
    login.render_login()

