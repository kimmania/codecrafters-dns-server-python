# Messages

All communications in the DNS protocol are carried in a single format called a "message". Each message consists of 5 sections: 
* header
* question
* answer
* authority
* an additional space

# Header section structure

The header section of a DNS message contains the following fields: (we've also included the values that the tester expects in this stage)

| Field	| Size	| Description |
| -------- | ------- | ------- |
| Packet Identifier (ID) | 16 bits | A random ID assigned to query packets. Response packets must reply with the same ID. <br/>Expected value: 1234. |
| Query/Response Indicator (QR) | 1 bit | 1 for a reply packet, 0 for a question packet. <br/>Expected value: 1. |
| Operation Code (OPCODE) | 4 bits | Specifies the kind of query in a message. <br/>Expected value: 0. |
| Authoritative Answer (AA) | 1 bit | 1 if the responding server "owns" the domain queried, i.e., it's authoritative. <br/>Expected value: 0. |
| Truncation (TC) | 1 bit | 1 if the message is larger than 512 bytes. Always 0 in UDP responses. <br/>Expected value: 0. |
| Recursion Desired (RD) | 1 bit | Sender sets this to 1 if the server should recursively resolve this query, 0 otherwise. <br/>Expected value: 0. |
| Recursion Available (RA) | 1 bit | Server sets this to 1 to indicate that recursion is available. <br/>Expected value: 0. |
| Reserved (Z) | 3 bits | Used by DNSSEC queries. At inception, it was reserved for future use. <br/>Expected value: 0. |
| Response Code (RCODE) | 4 bits | Response code indicating the status of the response. <br/>Expected value: 0 (no error). |
| Question Count (QDCOUNT) | 16 bits | Number of questions in the Question section. <br/>Expected value: 0. |
| Answer Record Count (ANCOUNT) | 16 bits | Number of records in the Answer section. <br/>Expected value: 0. |
| Authority Record Count (NSCOUNT) | 16 bits | Number of records in the Authority section. <br/>Expected value: 0. |
| Additional Record Count (ARCOUNT) | 16 bits | Number of records in the Additional section. <br/>Expected value: 0. |


The header section is always **12 bytes** long. Integers are encoded in big-endian format.

# Question section structure

The question section contains a list of questions (usually just 1) that the sender wants to ask the receiver. This section is present in both query and reply packets.

Each question has the following structure:
* Name: A domain name, represented as a sequence of "labels" (more on this below)
* Type: 2-byte int; the type of record (1 for an A record, 5 for a CNAME record etc., full list here)
* Class: 2-byte int; usually set to 1 (full list here)

Section 4.1.2 of the RFC covers the question section format in detail. Section 3.2 has more details on Type and class.

## Domain name encoding
Domain names in DNS packets are encoded as a sequence of labels.

Labels are encoded as <length><content>, where <length> is a single byte that specifies the length of the label, and <content> is the actual content of the label. The sequence of labels is terminated by a null byte (\x00).

For example:

google.com is encoded as \x06google\x03com\x00 (in hex: 06 67 6f 6f 67 6c 65 03 63 6f 6d 00)
\x06google is the first label
\x06 is a single byte, which is the length of the label
google is the content of the label
\x03com is the second label
\x03 is a single byte, which is the length of the label
com is the content of the label
\x00 is the null byte that terminates the domain name

# DNS Documentation

* RFC 1035: https://datatracker.ietf.org/doc/html/rfc1035#section-4.1
* Wikipedia: https://en.wikipedia.org/wiki/Domain_Name_System#DNS_message_format
* DNS Guide: https://github.com/EmilHernvall/dnsguide/blob/b52da3b32b27c81e5c6729ac14fe01fef8b1b593/chapter1.md

# Binary Format

struck.pack can be used to transform the fields into a binary format suitable for network transmission. The !HHHHHH format string indicates that the data should be packed in network order (big-endian) and consists of six 16-bit unsigned integers. The bitwise operations combine the single-bit and multi-bit fields into the second 16-bit integer, as specified by the DNS protocol.

Here is an example showing how the 6 fields are pushed into a singular 16 bit value:
```
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
```



Future
```   
class DNSAnswer:
    def __init__(self, name, rtype, rclass, ttl, data):
        self.name = name
        self.type = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.data = data
    def to_bytes(self):
        name_bytes = b"".join(
            struct.pack("!B", len(label)) + label.encode()
            for label in self.name.split(".")
        )
        data_bytes = (
            self.data if isinstance(self.data, bytes) else socket.inet_aton(self.data)
        )
        return (
            name_bytes
            + struct.pack("!HHIH", self.type, self.rclass, self.ttl, len(data_bytes))
            + data_bytes
        )
```