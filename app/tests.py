# pylint: disable=broad-exception-caught
from io import BytesIO
from dnsmessage import DNSMessage


def sample():
    buf =  b'\x04\xd2\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
    reader = BytesIO(buf)

    request = DNSMessage()
    request.from_bytes(reader)

    response = DNSMessage()
    response.create_response(request)

     # Sending response
    response_data = response.to_bytes()
    print(f'response: {response_data}')

# b'\x03\xac\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
# [stage-2] Querying `A` record for codecrafters.io.
# [your_program] response: b'\x03\xac\x01\x00\x00\x02\x00\x01\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x08\x08\x08\x08'
# [your_program] b'\x04\xd2\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
# [stage-2] dns: overflow unpacking uint16
# [stage-2] Test failed (try setting 'debug: true' in your codecrafters.yml to see more details)
# [your_program] response: b'\x04\xd2\x01\x00\x00\x02\x00\x01\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x08\x08\x08\x08'


def main():
    #testHeader()
    sample()

main()