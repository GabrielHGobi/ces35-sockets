from argparse import ArgumentParser
from threading import Thread
from socket import *
import sys
import os

class ClientThread(Thread):
    def __init__(self, clientAddr, clientConn):
        Thread.__init__(self)
        self.cConn = clientConn
        print("New connection added: ", clientAddr)

    def run(self):
        pass

def server():
    server_parser = ArgumentParser(description='List the address of the web server \
        with host and port and the directory where the files will be served')
    server_parser.add_argument('Host', metavar='host',type=str,
                                help='the hostname of the web server')
    server_parser.add_argument('Port', metavar='port', type=int,
                                help='the port of the webs erver')
    server_parser.add_argument('Dir', metavar='dir', type=str,
                                help='the directory where the files will be served')
    args = server_parser.parse_args()

    # create TCP welcoming socket
    try: 
        serverSocket = socket(AF_INET, SOCK_STREAM) 
    except error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1)

    # retrive the IP of the host
    try:
        IP_host = gethostbyname(args.Host)
    except gaierror:
        print("Invalid hostname: %s" % args.Host)
        sys.exit(1)

    # open a TCP connection
    try: 
        serverSocket.bind((IP_host, args.Port)) 
    except gaierror as e: 
        print("Address-related error binding to server: %s" % e) 
        sys.exit(1) 
    except error as e: 
        print("Binding error: %s" % e) 
        sys.exit(1)

    # check if the dir passed is valid
    if not os.path.isdir(args.Dir):
        print("Directory %s does not exist" % args.Dir)
        sys.exit(1)
    
    # server begins listening for incoming TCP requests
    serverSocket.listen(1)

    print("Server started")
    print("Waiting for client request...")
    while True:
        # server waits for incoming requests; new socket created on return
        connectionSocket, addr = serverSocket.accept()
        new_thread = ClientThread(addr, connectionSocket)
        new_thread.start()

    try: 
        serverSocket.close()
    except error as e: 
        print ("Error closing socket: %s" % e) 
        sys.exit(1)

if __name__ == '__main__':
    server()
