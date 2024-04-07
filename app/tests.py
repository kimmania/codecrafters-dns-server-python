# pylint: disable=broad-exception-caught
from dnsheader import DNSHeader
#from dnsmessage import DNSMessage

def testHeader():
    header1 = DNSHeader(1234, True)
    header1_bytes = header1.to_bytes()

    header2 = DNSHeader().from_bytes(header1_bytes)
    header2_bytes = header2.to_bytes()

    assert header1_bytes == header2_bytes

def sample():
    buf =  b'\x04\xd2\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'

    header_bytes = b'\x04\xd2\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
    print(f'Before: {header_bytes}')
    header = DNSHeader()
    header.from_bytes(header_bytes)
    print(f'After: {header.to_bytes()}')

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