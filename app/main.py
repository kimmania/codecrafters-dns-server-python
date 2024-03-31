import socket
from .dnsmessage import DNSMessage

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
    
            
            print(buf)
            # Creating a DNS message and setting header
            response = DNSMessage()
            # for now the header is initialized with the values we want

            # Sending response
            udp_socket.sendto(response.to_bytes(), source)  
            
        except Exception as e:
            print(f"Error handling DNS message: {e}")
            break


if __name__ == "__main__":
    main()
