from argparse import ArgumentParser
from threading import Thread
from socket import *
from HTTPReq import *
from HTTPResp import *
import sys
import os
import signal
import datetime
import base64

class ClientThread(Thread):
    def __init__(self, clientAddr, clientConn, serverDir):
        Thread.__init__(self)
        self.cConn = clientConn
        self.sDir = serverDir
        print("New connection added: ", clientAddr)

        
    def run(self):
        # read a sequence of bytes from socket sent by the client
        req_byte_stream = self.cConn.recv(1048576)
        
        # parsing the bytes on a HTTP request
        client_request = HTTPReq()
        client_request.parse(req_byte_stream)
        # creating a HTTP response
        if client_request.is_BadRequest():
            response = HTTPRespBadRequest()
        else:
            method = client_request.get_method()
            if method == "POST" or method == "PUT" or method == "HEAD":
                raise NotImplementedError("This code just implements GET requests.")
            elif method != "GET":
                print("Invalid method.")
                sys.exit(1)
            else:
                fileURL = './' + self.sDir + client_request.get_URL()
                if not os.path.exists(fileURL):
                    response = HTTPRespNotFound()
                else:
                    response = HTTPRespOK()
                    # headers
                    currDate = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
                    response.add_header_field('Date', f'{currDate}')
                    response.add_header_field('Content-Language', 'en-US')
                    response.add_header_field('Connection', 'Keep-Alive')
                    # envio de png
                    m_png = re.findall("(\.png)", fileURL)
                    if m_png:
                        response.add_header_field('Content-Type', 'image/png')
                        response.add_header_field('Accept-Encoding', 'base64')
                        body_part_bytes = open(fileURL, "rb")
                        body_part = base64.b64encode(body_part_bytes.read()).decode()
                        response._body = body_part
                    else:    
                        body_part = open(fileURL, 'r')
                        body_part = body_part.read()
                        response._body = body_part
                    response.add_header_field('Content-Length', str({len(response.get_body().encode(encoding='UTF-8'))}))

        # send back HTTP respose over the TCP connection
        self.cConn.send(response.encode())

        # close the TCP connection
        self.cConn.close()    
                

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
    else:
        serverDir = args.Dir
    
    # server begins listening for incoming TCP requests
    serverSocket.listen(1)

    print("Server started")
    print("Waiting for client request...")

    # double-check interrupt 
    def int_handler(signum, frame):
        ans = input("\nSIGINT detected. Do you really want to exit? (y/n): ")
        if ans == 'y':
            try:
                serverSocket.close()
                sys.exit(1)
            except error as e: 
                print ("Error closing socket: %s" % e) 
                sys.exit(1)

    signal.signal(signal.SIGINT, int_handler)

    while True:
        # server waits for incoming requests; new socket created on return
        connectionSocket, addr = serverSocket.accept()
        new_thread = ClientThread(addr, connectionSocket, serverDir)
        new_thread.start()

if __name__ == '__main__':
    server()
