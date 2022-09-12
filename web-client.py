import argparse

server_parser = argparse.ArgumentParser(description='List URL\'s to files to be requested by the client')

server_parser.add_argument('URL', metavar='URL', type=str,  nargs='+',
                            help='file URL to be retrieved')

args = server_parser.parse_args()
print(args.URL)
