# pylint: disable=broad-exception-caught
'''Module for DNS Question section'''
from enum import Enum
import struct

class QType(Enum):
    """Enum of question types"""
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
    AXFR = 252      # A request for a transfer of an entire zone
    MAILB = 253     # A request for mailbox-related records (MB, MG or MR)
    MAILA = 254     # A request for mail agent RRs (Obsolete - see MX)
    ALL = 255       # A request for all records

class QClass(Enum):
    """Enum of question classes"""
    IN = 1      # the Internet
    CS = 2      # the CSNET class (Obsolete - used only for examples in some obsolete RFCs)
    CH = 3      # the CHAOS class
    HS = 4      # Hesiod [Dyer 87]
    ALL = 255   # any class

class DNSQuestion():
    """Class for DNS Message Question section"""
    qname: str
    qtype: QType
    qclass: QClass

    def __init__(self, name: str, qtype: QType, qclass: QClass) -> None:
        self.qname = name
        self.qtype = qtype
        self.qclass = qclass

    def set_values(self, name: str, qtype: QType, qclass: QClass) -> "DNSQuestion":
        '''set values'''
        self.qname = name
        self.qtype = qtype
        self.qclass = qclass
        return self

    def from_bytes(self, value:bytes) -> "DNSQuestion":
        """parses the value into the a question"""
        #todo
        return self

    def to_bytes(self) -> bytes:
        """turns the question into bytes"""
        encoded = b""
        for part in self.qname.encode("ascii").split(b"."):
            encoded += bytes([len(part)]) + part
        return encoded + b"\x00" + struct.pack("!H", self.qtype.value) + struct.pack("!H", self.qclass.value)
