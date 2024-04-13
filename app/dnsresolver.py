# pylint: disable=broad-exception-caught
'''Resolver of queries'''

import socket

class DNSResolver():
    '''Resolver'''
    def __init__(self, resolver: str) -> None:
        '''initialize the resolver'''
        self.client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        [self.ip, port] = resolver.split(":")
        self.port = int(port)

    def send(self, buf: bytes):
        '''send the message'''
        self.client_udp_socket.sendto(buf, (self.ip, self.port))

    def send_request(self, buf: bytes):
        '''send the message and return the response'''
        self.send(buf)
        return self.client_udp_socket.recvfrom(512)
