# pylint: disable=broad-exception-caught
"""Module for DNSHeader"""
import random
import struct
from enum import Enum
from io import BytesIO

class RCode(Enum):
    """Enum representing the different Response Codes"""
    NO_ERROR = 0
    FORMAT_ERROR = 1
    SEVER_FAILURE = 2
    NAME_ERROR = 3
    NOT_IMPLEMENTED = 4
    REFUSED = 5

class HeaderFlags:
    """Values that combined into a single 16 bit block"""
    qr: int = 0                     # 1 bit
    opcode: int = 0                 # 4 bits
    aa: int = 0                     # 1 bit
    tc: int = 0                     # 1 bit
    rd: int = 0                     # 1 bit
    ra: int = 0                     # 1 bit
    z: int = 0                      # 3 bits
    rcode: RCode = RCode.NO_ERROR   # 4 bits, refer to RCode enum for valid values

    def __init__(self, is_response: bool = True) -> None:
        if is_response:
            self.qr = 1

    def to_byte(self) -> int:
        """format into bytes for transmission"""
        return (self.qr << 15) | (self.opcode << 11) | (self.aa << 10) | (self.tc << 9) | (self.rd << 8) | (self.ra << 7) | (self.z << 4) | self.rcode.value

    # update RCode
    def update_rcode(self, rcode: RCode) -> None:
        """Update the Response Code"""
        self.rcode = rcode

    def from_bytes(self, value_bytes:bytes) -> "HeaderFlags":
        """separate the combined values into their individual values"""
        value = int.from_bytes(value_bytes)
        self.qr = (value >> 15) & 0x01
        self.opcode = (value >> 11) & 0x0F
        self.aa = (value >> 10) & 0x01
        self.tc = (value >> 9) & 0x01
        self.rd = (value >> 8) & 0x01
        self.ra = (value >> 7) & 0x01
        self.z = (value >> 4) & 0x07
        rcode_value = value & 0x0F
        self.rcode = RCode(rcode_value)
        return self

class DNSHeader():
    """Class representing a DNS message header section"""
    packid: bytes = 0   # 16 bits
    flags: HeaderFlags  # Combined 16 bits
    qdcount: int = 0    # 16 bits
    ancount: int = 0    # 16 bits
    nscount: int = 0    # 16 bits
    arcount: int = 0    # 16 bits

    def __init__(self, is_response: bool = True) -> None:
        self.flags = HeaderFlags(is_response)

    # pull the important values from a request header and use in a new response header
    def create_response(self, other):
        """Copy values header values from another header as a response"""
        if not isinstance(other, DNSHeader):
            raise ValueError("Can only copy from another DNSHeader instance")
      
        self.packid = other.packid
        self.flags.qr = 1
        self.flags.opcode = other.flags.opcode
        self.flags.rd = other.flags.rd

        if self.flags.opcode != 0:
            self.flags.update_rcode(RCode.NOT_IMPLEMENTED) # set to not implemented

    def create_question(self, other):
        '''Set the flags we need to pass along'''
        if not isinstance(other, DNSHeader):
            raise ValueError("Can only copy from another DNSHeader instance")
        
        self.flags.qr = 0
        self.flags.opcode = other.flags.opcode
        self.flags.rd = other.flags.rd

    # create an instance from bytes
    def from_bytes(self, reader: BytesIO) -> "DNSHeader":
        """from a bytes, populate the header values"""
        try:
            header = reader.read(12)
            #assume that input will be the full 12 bytes and only the 12 bytes
            self.packid = header[:2]
            self.flags.from_bytes(header[2:4])
            self.qdcount = int.from_bytes(header[4:6])
            self.ancount = int.from_bytes(header[6:8])
            self.nscount = int.from_bytes(header[8:10])
            self.arcount = int.from_bytes(header[10:12])
        except Exception as e:
            print(f"Error parsing DNS header: {e}")

        return self

    # increment methods
    def increment_question(self) -> None:
        """Increment question count"""
        self.qdcount += 1

    def increment_answer(self) -> None:
        """Increment answer count"""
        self.ancount += 1

    def increment_authority(self) -> None:
        """Increment authority count"""
        self.nscount += 1

    def increment_ar(self) -> None:
        """Increment AR Count"""
        self.arcount += 1

    # update RCode
    def update_rcode(self, rcode: RCode) -> None:
        """Update the Response Code"""
        self.flags.update_rcode(rcode)

    # formatting for network communication
    def to_bytes(self) -> bytes:
        """format into bytes for transmission"""
        if self.packid == 0:
            self.packid = struct.pack("!H", random.randint(1, 65535))

        header = self.packid + struct.pack(
            "!HHHHH",
            self.flags.to_byte(),
            self.qdcount,
            self.ancount,
            self.nscount,
            self.arcount,
        )
        return header
