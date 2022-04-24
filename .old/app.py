from threading import Thread
from client import client_init
from server import server_init

if __name__ == '__main__':
    Thread(target = server_init).start()
    Thread(target = client_init).start()
    