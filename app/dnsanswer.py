from enum import Enum
import socket
import struct

class RType(Enum):
    A = 1           # a host address
    NS = 2          # an authoritative name server
    MD = 3          # a mail destination (Obsolete - use MX)
    MF = 4          # a mail forwarder (Obsolete - use MX)
    CNAME = 5       # the canonical name for an alias
    SOA = 6         # marks the start of a zone of authority
    MB = 7          # a mailbox domain name (EXPERIMENTAL)
    MG = 8          # a mail group member (EXPERIMENTAL)
    MR = 9          # a mail rename domain name (EXPERIMENTAL)
    NULL = 10       # a null RR (EXPERIMENTAL)
    WKS = 11        # a well known service description
    PTR = 12        # a domain name pointer
    HINFO = 13      # host information
    MINFO = 14      # mailbox or mail list information
    MX = 15         # mail exchange
    TXT = 16        # text strings

class RClass(Enum):
    IN = 1      # the Internet
    CS = 2      # the CSNET class (Obsolete - used only for examples in some obsolete RFCs)
    CH = 3      # the CHAOS class
    HS = 4      # Hesiod [Dyer 87]

class DNSAnswer():
    name: str
    rtype: RType
    rclass: RClass
    ttl: int = 0

    def __init__(self, name: str, rtype: RType, rclass: RClass, ttl: int, data) -> None:
        self.aname = name
        self.rtype = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.data = data

    def to_bytes(self) -> bytes:
        encoded = b""
        for part in self.aname.encode("ascii").split(b"."):
            encoded += bytes([len(part)]) + part
        
        data_bytes = (self.data if isinstance(self.data, bytes) else socket.inet_aton(self.data))
        
        encoded +=  b"\x00" + struct.pack("!HHIH", self.rtype.value, self.rclass.value, self.ttl, len(data_bytes)) + data_bytes  
        
        return encoded
