import struct
from enum import Enum

class RCode(Enum):
    NO_ERROR = 0
    FORMAT_ERROR = 1
    SEVER_FAILURE = 2
    NAME_ERROR = 3
    NOT_IMPLEMENTED = 4
    REFUSED = 5

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



class DNSMessage():
    header: DNSHeader
    questions: list[bytes] = []
    answers: list[bytes] = []
    authorities: list[bytes] = []
    additionals: list[bytes] = []

    def __init__(self) -> None:
        self.header = DNSHeader(1234, True)
        pass

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
