from threading import Thread
from client_manager import client_init
from server_manager import server_init
import sys
import config

if __name__ == '__main__':

    # Who are we connecting to
    if(len(sys.argv) > 1):
        config.ConnectionPort = int(sys.argv[1])
        config.ConnectionAddress = (config.sendIP, config.ConnectionPort)
    else:
        config.ConnectionPort = int(input("\nEnter server port you want to connect to: "))
        config.ConnectionAddress = (config.sendIP, config.ConnectionPort)

    # What port are we binding to
    if(len(sys.argv) > 2):
        config.BindPort = int(sys.argv[2])
        config.BindAddress = (config.localIP, config.BindPort)
    else:
        config.BindPort = int(input("\nEnter port we are binding our server to: "))
        config.BindAddress = (config.localIP, config.BindPort)
    
    Thread(target = server_init).start()
    Thread(target = client_init).start()