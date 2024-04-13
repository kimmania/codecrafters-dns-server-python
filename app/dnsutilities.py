'''Collection of utilities to facilitiate processing'''
from io import BytesIO
import struct

class DNSUtilities:
    '''Collection of static methods'''
    @staticmethod
    def encode_dns_name(domain_name) -> bytes:
        '''Encode the domain name'''
        encoded = b""
        for part in domain_name.encode("ascii").split(b"."):
            encoded += bytes([len(part)]) + part
        return encoded + b"\x00"

    @staticmethod
    def decode_dns_name_simple(reader: BytesIO):
        '''decode dns name, does not account for compression'''
        parts = []
        while (length := reader.read(1)[0]) != 0:
            parts.append(reader.read(length))
        return b".".join(parts)

    # RFC covering the compression algorithm: https://www.rfc-editor.org/rfc/rfc1035#section-4.1.4
    # Code guiding me through reading the compression: 
    # https://implement-dns.wizardzines.com/book/part_2#implement-dns-compression
    @staticmethod
    def decode_name(reader):
        '''Decode the name accounting for compression'''
        parts = []
        while (length := reader.read(1)[0]) != 0:
            if length & 0b1100_0000:
                parts.append(DNSUtilities.decode_compressed_name(length, reader))
                break

            parts.append(reader.read(length))
        return b".".join(parts)

    @staticmethod
    def decode_compressed_name(length, reader):
        '''Decode with compression in mind, requires moving within the reader'''
        pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
        pointer = struct.unpack("!H", pointer_bytes)[0]
        current_pos = reader.tell()
        reader.seek(pointer)
        result = DNSUtilities.decode_name(reader)
        reader.seek(current_pos)
        return result