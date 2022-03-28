from threading import Thread
from client import client_init
from server import server_init

# def func1():
#     val = ""
#     while(val != "exit"):
#         val = input("enter a value: ")
#         print("value entered: " + val)

# def func2():
#     print("Working")

# if __name__ == '__main__':
#     Thread(target = func1).start()
#     Thread(target = func2).start()

if __name__ == '__main__':
    Thread(target = server_init).start()
    Thread(target = client_init).start()
    