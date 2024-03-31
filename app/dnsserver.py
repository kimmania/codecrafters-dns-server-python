import socket
from .dnsmessage import DNSMessage
from .dnsanswer import RClass, RType
from .dnsquestion import QClass, QType

class DNSServer:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.udp_socket = None

    def run(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.ip, self.port))

        while True:
            try:
                buf, source = udp_socket.recvfrom(512)

                #print(buf)
                # Creating a DNS message and setting header
                response = DNSMessage()
                # for now the header is initialized with the values we want
                #Add question
                response.addQuestion("codecrafters.io", QType.A, QClass.IN)
                #Add answer
                response.addAnswer("codecrafters.io", RType.A, RClass.IN, 60, "8.8.8.8")
                
                # Sending response
                response_data = response.to_bytes()
                print(f'response: {response_data}')
                udp_socket.sendto(response_data, source)  
                
            except Exception as e:
                print(f"Error handling DNS message: {e}")
                break
