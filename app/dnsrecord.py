# pylint: disable=broad-exception-caught
'''Generic Resource Record Module'''
from enum import Enum
from io import BytesIO
import socket
import struct
from .dnsutilities import DNSUtilities

class RType(Enum):
    """Enum of resource types"""
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
    """Enum of resource class"""
    IN = 1      # the Internet
    CS = 2      # the CSNET class (Obsolete - used only for examples in some obsolete RFCs)
    CH = 3      # the CHAOS class
    HS = 4      # Hesiod [Dyer 87]

class DNSRecord():
    '''Generic Message Section class used for Answers, Authority, and Additional sections'''
    rname: str
    rtype: RType
    rclass: RClass
    ttl: int = 0
    rdata: str

    def __init__(self) -> None:
        pass

    def set_values(self, rname, rtype: RType, rclass: RClass, ttl: int, rdata: str) -> "DNSRecord":
        '''Set the values for the record'''
        self.rname = rname
        self.rtype = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.rdata = rdata
        return self

    def to_bytes(self) -> bytes:
        '''turn into transmittable content'''
        encoded = DNSUtilities.encode_dns_name(self.rname)

        data_bytes = (self.rdata if isinstance(self.rdata, bytes) else socket.inet_aton(self.rdata))
        # todo: this is only structured relative to A record type, should handle other record types
        encoded +=  struct.pack("!HHIH",
                                self.rtype.value,
                                self.rclass.value,
                                self.ttl,
                                len(data_bytes)) + data_bytes

        return encoded

    def from_bytes(self, reader: BytesIO) -> "DNSRecord":
        '''parses the value into the a question'''
        self.rname = DNSUtilities.decode_name(reader).decode("ascii")
        data = reader.read(10)
        type_, class_, ttl, length = struct.unpack("!HHIH", data)
        self.rtype = RType(type_)
        self.rclass = RClass(class_)
        self.ttl = ttl

        # need to parse the length of data and then the data
        ip = reader.read(length)
        # todo: this is only structured relative to A record type, should handle other record types
        self.rdata = socket.inet_ntoa(ip)

        return self
