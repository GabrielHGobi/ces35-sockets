from argparse import ArgumentParser
from socket import *
import re
import sys

def urlparse(URL):
    url_parsed = {}
    m_url = re.search("(http|https)://(.*)/(.*)", URL)
    if m_url is None:
        print("Invalid URL: %s" % URL)
        sys.exit(1)
    else:
        netloc = m_url.group(2)
        m_netloc = re.search("([a-zA-Z0-9]+)(?::([1-9][0-9]*))?", netloc)
        if m_netloc is None:
            print("Invalid address: %s" % netloc)
            sys.exit(1)
        else:
            url_parsed['scheme'] = m_url.group(1)
            url_parsed['hostname'] = m_netloc.group(1)
            if m_netloc.group(2) != '':
                url_parsed['port'] = int(m_netloc.group(2))
            else:
                url_parsed['port'] = 8080 #default HTTP port
            if m_url.group(3) != '':
                url_parsed['path'] = m_url.group(3)
            else:
                url_parsed['path'] = 'index.html'
            
            return url_parsed



def client():
    server_parser = ArgumentParser(description='List URL\'s to files to be requested by the client')
    server_parser.add_argument('URL_list', metavar='URL', type=str,  nargs='+',
                                help='file URL to be retrieved')
    args = server_parser.parse_args()

    for URL in args.URL_list:
        url_parsed = urlparse(URL)

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