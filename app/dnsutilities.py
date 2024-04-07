'''Collection of utilities to facilitiate processing'''

class DNSUtilities:
    '''Collection of static methods'''
    @staticmethod
    def encode_dns_name(domain_name) -> bytes:
        '''Encode the domain name'''
        encoded = b""
        for part in domain_name.encode("ascii").split(b"."):
            encoded += bytes([len(part)]) + part
        return encoded + b"\x00"
