# pylint: disable=broad-exception-caught
'''Main executer'''
import argparse
import sys
from .dnsserver import DNSServer

HOST = "localhost"
PORT = 2053

def main():
    '''Initializes and starts the DNS Server'''
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolver", default=None, required=False, type=str)
    args = parser.parse_args()
    dns = DNSServer(HOST, PORT, resolver=args.resolver)

    try:
        dns.start()
    finally:
        dns.stop()


if __name__ == "__main__":
    sys.exit(main())
