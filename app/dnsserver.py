# pylint: disable=broad-exception-caught
'''Class for the DNS Server'''
import socket
from io import BytesIO
from .dnsmessage import DNSMessage
from .dnsrecord import DNSRecord, RClass, RType
from .dnsquestion import DNSQuestion, QClass, QType

class DNSServer:
    """Class representing the DNS Server"""
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.udp_socket = None

    def run(self):
        """Runner"""
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.ip, self.port))

        while True:
            try:
                buf, source = udp_socket.recvfrom(512)

                print(buf)
                reader = BytesIO(buf)
                # Read a DNS message
                request = DNSMessage()
                request.from_bytes(reader)

                # Prepare the response
                response = DNSMessage()
                response.create_response(request)

                # Sending response
                response_data = response.to_bytes()
                print(f'response: {response_data}')
                udp_socket.sendto(response_data, source)

            except Exception as e:
                print(f"Error handling DNS message: {e}")
                break
