# Summary
This DNS project ultimately will forward each question to DNS server, accummulate the answers into a response back to the caller. It will only handle processing of A record types and does not do anythng with Authority or Additional sections.

# Todo
1. x Parse a record object
2. x Create a more formal startup
3. Create a local cache for lookig up relative to cached ttl
4. Create a mechanism to call out DNS server for each question
5. Create a mechanism to process through each question and request get answer
6. Add answer to local cache



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

# Answer section structure
The answer section contains a list of RRs (Resource Records), which are answers to the questions asked in the question section.

Each RR has the following structure:
| Field	| Type	| Description |
| -------- | ------- | ------- |
| Name | Label Sequence | The domain name encoded as a sequence of labels. |
| Type | 2-byte Integer | 1 for an A record, 5 for a CNAME record etc., full list here |
| Class | 2-byte Integer | Usually set to 1 (full list here) |
| TTL (Time-To-Live) | 4-byte Integer | The duration in seconds a record can be cached before  |requerying.
| Length (RDLENGTH) | 2-byte Integer | Length of the RDATA field in bytes. |
| Data (RDATA) | Variable | Data specific to the record type. |

Section 3.2.1 of the RFC covers the answer section format in detail.

# DNS Documentation

* RFC 1035: https://datatracker.ietf.org/doc/html/rfc1035#section-4.1
* Wikipedia: https://en.wikipedia.org/wiki/Domain_Name_System#DNS_message_format
* DNS Guide: https://github.com/EmilHernvall/dnsguide/blob/b52da3b32b27c81e5c6729ac14fe01fef8b1b593/chapter1.md

# Binary Format

struck.pack can be used to transform the fields into a binary format suitable for network transmission. The !HHHHHH format string indicates that the data should be packed in network order (big-endian) and consists of six 16-bit unsigned integers. The bitwise operations combine the single-bit and multi-bit fields into the second 16-bit integer, as specified by the DNS protocol.

Here is an example showing how the 6 fields are pushed into a singular 16 bit value:
```
header = self.packid + struct.pack(
    "!HHHHH",
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

Example code to parse the flags into individual values (dnsheader.py, HeaderFlags.from_bytes):
```
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
```

To get the bytes for the DNSHeader (dnsheader.py, DNSHeader.from_bytes):
```
def from_bytes(self, header: bytes) -> "DNSHeader":
    """from a bytes, populate the header values"""
    #assume that input will be the full 12 bytes and only the 12 bytes
    self.packid = header[:2]
    self.flags.from_bytes(header[2:4])
    self.qdcount = int.from_bytes(header[4:6])
    self.ancount = int.from_bytes(header[6:8])
    self.nscount = int.from_bytes(header[8:10])
    self.arcount = int.from_bytes(header[10:12])
```