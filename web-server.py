import argparse

server_parser = argparse.ArgumentParser(description='List the address of the web server \
    with host and port and the directory where the files will be served')

server_parser.add_argument('Host', metavar='host',type=str,
                            help='the hostname of the web server')
server_parser.add_argument('Port', metavar='port', type=str,
                            help='the port of the webs erver')
server_parser.add_argument('Dir', metavar='dir', type=str,
                            help='the directory where the files will be served')

args = server_parser.parse_args()
print(args.Host, args.Port, args.Dir)
