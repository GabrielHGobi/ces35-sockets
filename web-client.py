import argparse

server_parser = argparse.ArgumentParser(description='List URL\'s to files to be requested by the client')

def client():
    server_parser = ArgumentParser(description='List URL\'s to files to be requested by the client')
    server_parser.add_argument('URL_list', metavar='URL', type=str,  nargs='+',
                            help='file URL to be retrieved')
    args = server_parser.parse_args()

    for URL in args.URL_list:

        # server machine's name 
        serverHostname = url_parsed['hostname']

        # server port number
        serverPort = url_parsed['port']

        # create TCP socket on client to use for connecting to remote
        # server.  Indicate the server's remote listening port
        try: 
            clientSocket = socket(AF_INET, SOCK_STREAM) 
        except error as e: 
            print ("Error creating socket: %s" % e) 
            sys.exit(1)

        # retrive the IP of the server
        try:
            IP_server = gethostbyname(serverHostname)
        except gaierror:
            print("Invalid hostname in URL: %s: %s" % (URL, serverHostname))
            sys.exit(1)

        # open the TCP connection
        try: 
            clientSocket.connect((IP_server, serverPort))
        except gaierror as e: 
            print("Address-related error connecting to server: %s" % e) 
            sys.exit(1) 
        except error as e: 
            print("Connection error: %s" % e) 
            sys.exit(1)

        # construct and send HTTP request

        # close the TCP connection
        try: 
            clientSocket.close()
        except error as e: 
            print ("Error closing socket: %s" % e) 
            sys.exit(1)

if __name__ == '__main__':
    client()