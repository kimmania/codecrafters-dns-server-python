import struct
from enum import Enum

class RCode(Enum):
    NO_ERROR = 0
    FORMAT_ERROR = 1
    SEVER_FAILURE = 2
    NAME_ERROR = 3
    NOT_IMPLEMENTED = 4
    REFUSED = 5

class QType(Enum):
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
    IN = 1      # the Internet
    CS = 2      # the CSNET class (Obsolete - used only for examples in some obsolete RFCs)
    CH = 3      # the CHAOS class
    HS = 4      # Hesiod [Dyer 87]
    ALL = 255   # any class

class DNSHeader():
    packid: int = 0     # 16 bits
    qr: int = 0         # 1 bit
    opcode: int = 0     # 4 bits
    aa: int = 0         # 1 bit
    tc: int = 0         # 1 bit
    rd: int = 0         # 1 bit
    ra: int = 0         # 1 bit
    z: int = 0          # 3 bits
    rcode: int = 0      # 4 bits
    qdcount: int = 0    # 16 bits
    ancount: int = 0    # 16 bits
    nscount: int = 0    # 16 bits
    arcount: int = 0    # 16 bits

    def __init__(self, id:int = 0, response: bool = True) -> None:
        self.packid = id
        if response:
            self.qr = 1

    def updateRCode(self, code: RCode) -> None:
        self.rcode = code.value

    def addQuestion(self) -> None:
        self.qdcount += 1 

    def to_bytes(self) -> bytes:
        header = struct.pack(
            "!HHHHHH",
            self.packid,
            (self.qr << 15)
            | (self.opcode << 11)
            | (self.aa << 10)
            | (self.tc << 9)
            | (self.rd << 8)
            | (self.ra << 7)
            | (self.z << 4)
            | self.rcode,
            self.qdcount,
            self.ancount,
            self.nscount,
            self.arcount,
        )
        return header

class DNSQuestion():
    qname: str
    qtype: QType
    qclass: QClass

    def __init__(self, name, qtype: QType, qclass: QClass) -> None:
        self.qname = name
        self.qtype = qtype
        self.qclass = qclass

    def to_bytes(self) -> bytes:
        encoded = b""
        for part in self.qname.encode("ascii").split(b"."):
            encoded += bytes([len(part)]) + part
        return encoded + b"\x00" + struct.pack("!H", self.qtype.value) + struct.pack("!H", self.qclass.value)

class DNSMessage():
    header: DNSHeader
    questions: list[DNSQuestion] = []
    answers: list[bytes] = []
    authorities: list[bytes] = []
    additionals: list[bytes] = []

    def __init__(self) -> None:
        self.header = DNSHeader(1234, True)
        self.questions = []

    def addQuestion(self,  name, qtype: QType, qclass: QClass)-> None:
        question = DNSQuestion(name, qtype, qclass)
        self.questions.append(question)
        self.header.addQuestion()

    def to_bytes(self) -> bytes:
        header_bytes = self.header.to_bytes()
        question_bytes = b"".join(q.to_bytes() for q in self.questions)
        answer_bytes = b"".join(a.to_bytes() for a in self.answers)
        authority_bytes = b"".join(a.to_bytes() for a in self.authorities)
        additional_bytes = b"".join(a.to_bytes() for a in self.additionals)

        return (
            header_bytes
            + question_bytes
            + answer_bytes
            + authority_bytes
            + additional_bytes
        )
