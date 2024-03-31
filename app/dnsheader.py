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

    def addQuestion(self) -> None:
        self.qdcount += 1 

    def addAnswer(self) -> None:
        self.ancount += 1

    def addAuthority(self) -> None:
        self.nscount += 1

    def addAdditionalRecord(self) -> None:
        self.arcount += 1

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
