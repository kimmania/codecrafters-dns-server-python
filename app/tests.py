# pylint: disable=broad-exception-caught
from io import BytesIO
from dnsmessage import DNSMessage
from dnsrecord import DNSRecord, RClass, RType


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
    print(f'Record: {response.answers[0].to_bytes()}')

# b'\x03\xac\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
# [stage-2] Querying `A` record for codecrafters.io.
# [your_program] response: b'\x03\xac\x01\x00\x00\x02\x00\x01\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x08\x08\x08\x08'
# [your_program] b'\x04\xd2\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
# [stage-2] dns: overflow unpacking uint16
# [stage-2] Test failed (try setting 'debug: true' in your codecrafters.yml to see more details)
# [your_program] response: b'\x04\xd2\x01\x00\x00\x02\x00\x01\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x0ccodecrafters\x02io\x00\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x08\x08\x08\x08'

def testRecord():
    answer = DNSRecord().set_values('codecrafters.io', RType.A, RClass.IN, 60, "8.8.8.8")
    answer_bytes = answer.to_bytes()
    print(f'bytes: {answer_bytes}')
    try:
        reader = BytesIO(answer_bytes)
        test = DNSRecord().from_bytes(reader)
        print(f'ttl: {test.ttl}')
        print(f'after: {test.to_bytes()}')
        print(f'data: {test.rdata}')
    except Exception as e:
        print(f"Error handling: {e}")


def main():
    #testHeader()
    #sample()
    testRecord()

main()