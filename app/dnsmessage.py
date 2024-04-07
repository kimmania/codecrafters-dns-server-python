# pylint: disable=broad-exception-caught
"""Module for the DNS Message"""
import struct
from io import BytesIO
from .dnsheader import DNSHeader, RCode
from .dnsquestion import DNSQuestion
from .dnsrecord import DNSRecord

class DNSMessage():
    """DNS Message"""
    header: DNSHeader
    questions: list[DNSQuestion] = []
    answers: list[DNSRecord] = []
    authorities: list[DNSRecord] = []
    additionals: list[DNSRecord] = []

    def __init__(self) -> None:
        self.header = DNSHeader()
        self.questions = []
        self.answers = []
        self.authorities = []
        self.additionals = []

    def add_question(self,  question: DNSQuestion) -> None:
        """Add a question to the message"""
        self.questions.append(question)
        self.header.increment_question()

    def add_answer(self, answer: DNSRecord) -> None:
        """Add an answer to the message"""
        self.answers.append(answer)
        self.header.increment_answer()

    def add_authority(self, authority:DNSRecord) -> None:
        """Add an authority to the message"""
        self.authorities.append(authority)
        self.header.increment_authority()

    def add_additional(self, additional: DNSRecord) -> None:
        """Add an additional to the message"""
        self.additionals.append(additional)
        self.header.increment_ar()

    def to_bytes(self) -> bytes:
        """turn into transmitable message"""
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

    def from_bytes(self, reader:BytesIO) -> "DNSMessage":
        """from the bytes of an existing message, parse into a DNS Message"""
        try:
            self.header = DNSHeader().from_bytes(reader.read(12))
        except Exception:
            self.header.update_rcode(RCode.FORMAT_ERROR)
