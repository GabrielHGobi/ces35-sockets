from argparse import ArgumentParser
from socket import *
from HTTPReq import *
from HTTPResp import *
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
        m_netloc = re.search("([a-zA-Z0-9\.-]+)(?::([1-9][0-9]*))?", netloc)
        if m_netloc is None:
            print("Invalid address: %s" % netloc)
            sys.exit(1)
        else:
            url_parsed['scheme'] = m_url.group(1)
            url_parsed['hostname'] = m_netloc.group(1)
            if m_netloc.group(2) != None:
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

        # construct HTTP request
        request = HTTPReq()
        request.set_method('GET')
        request.set_URL('/'+ url_parsed['path'])

        # headers
        request.add_header_field('Host', serverHostname)
        request.add_header_field('Connection', 'keep-alive')
        request.add_header_field('Accept', 'text/html')
        request.add_header_field('Accept-Encoding', 'gzip, deflate')
        request.add_header_field('Accept-Language', 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')

        # send the request over the TCP connection
        # No need to specify server name, port
        clientSocket.send(request.encode())

        # read a sequence of bytes from socket sent by the server
        resp_byte_stream = clientSocket.recv(1024)

        # parsing the bytes on a HTTP request
        server_response = HTTPResp()
        server_response.parse(resp_byte_stream)
        status_code = server_response.get_status_code()
        status_phrase = server_response.get_status_phrase()
        if status_code != 200:
            print("%s: Error %d: %s" % (URL, status_code, status_phrase))
        else:
            
            rcved_file = open(url_parsed['path'], 'w')
            rcved_file.write(server_response._body)
            rcved_file.close()

        # close the TCP connection
        try: 
            clientSocket.close()
        except error as e: 
            print ("Error closing socket: %s" % e) 
            sys.exit(1)

if __name__ == '__main__':
    client()