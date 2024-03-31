from .dnsheader import DNSHeader
from .dnsquestion import DNSQuestion, QClass, QType
from .dnsanswer import DNSAnswer, RClass, RType
class DNSMessage():
    header: DNSHeader
    questions: list[DNSQuestion] = []
    answers: list[DNSAnswer] = []
    authorities: list[bytes] = []
    additionals: list[bytes] = []

    def __init__(self) -> None:
        self.header = DNSHeader(1234, True)
        self.questions = []
        self.answers = []

    def addQuestion(self,  name: str, qtype: QType, qclass: QClass) -> None:
        question = DNSQuestion(name, qtype, qclass)
        self.questions.append(question)
        self.header.addQuestion()

    def addAnswer(self, name: str, rtype: RType, rclass: RClass, ttl: int, data) -> None:
        answer = DNSAnswer(name, rtype, rclass, ttl, data)
        self.answers.append(answer)
        self.header.addAnswer()

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
