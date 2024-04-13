# pylint: disable=broad-exception-caught
'''Class for the DNS Server'''
import socket
import threading
from io import BytesIO
from .dnsmessage import DNSMessage
from .dnsresolver import DNSResolver

class DNSServer:
    """Class representing the DNS Server"""
    def __init__(self, ip, port, resolver):
        self.port = port
        self.ip = ip
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        self.thread_pool = []
        if resolver is None:
            self.resolver = None
        else:
            self.resolver = DNSResolver(resolver)    # address of the form <ip>:<port>

    def start(self):
        '''Start the Server'''
        print("Starting server...")
        self.running = True
        self.udp_socket.bind((self.ip, self.port))
        while self.running:
            message, client_address = self.udp_socket.recvfrom(512)
            t = threading.Thread(target=self._process_request, args=(client_address, message))
            self.thread_pool.append(t)
            t.start()

        self.udp_socket.close()

    def stop(self):
        '''Stop the Server'''
        print("Shutting down server...")
        self.running = False
        self.udp_socket.shutdown()
        for t in self.thread_pool:
            t.join()

    def _process_request(self, client_address, message: bytes):  #: (str, int)
        '''Runner'''
        try:
            print(message)
            reader = BytesIO(message)
            # Read a DNS message
            request = DNSMessage()
            request.from_bytes(reader)

            # Prepare the response
            response = DNSMessage()
            response.prepare_response(request)

            if self.resolver is not None:
                # loop through the questions
                for question in request.questions:
                    # append question to the response
                    response.add_question(question)
                    # need to prepare a new message
                    res_question = DNSMessage().create_question(request.header, question)
                    # send to resolver
                    res_data, _ = self.resolver.send_request(res_question)
                    # parse the response
                    res_message = DNSMessage().from_bytes(BytesIO(res_data))
                    # append to the answer(s) to the response
                    for answer in res_message.answers:
                        response.add_answer(answer)

            # Sending response
            response_data = response.to_bytes()
            print(f'response: {response_data}')
            self.udp_socket.sendto(response_data, client_address)

        except Exception as e:
            print(f"Error handling DNS message: {e}")
            raise e
