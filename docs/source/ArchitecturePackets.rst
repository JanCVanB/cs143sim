Packets
=======

Basic Structure
------
As the header structure varies as using different version of TCP, we shall let it be some Bytes and let the protocol itself to decode.

TCP Header
------
All TCP packets obey these rules
- Source Port
- Destination Port
- Sequence Number
- Acknowledgment
- ...(page 89)

Layer 3
------
When TCP packet going down to layer 3 (IP layer), some extra information will be added before TCP header.
( http://en.wikipedia.org/wiki/IPv4 )->Header

Layer 2 and Layer 1
------
We don't need to worry about them.