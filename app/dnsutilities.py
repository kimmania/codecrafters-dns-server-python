'''Collection of utilities to facilitiate processing'''
from io import BytesIO

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
        '''decode dns name'''
        parts = []
        while (length := reader.read(1)[0]) != 0:
            parts.append(reader.read(length))
        return b".".join(parts)