Flows
=====

This is a summary of the roles, attributes, and design of flows.

Abstract
------

In this case, flows are in charge of transport layer.
There are three main part of transport layer:
- Error Control
- Congestion Control
- Flow Control
They are all features of TCP protocol. Different versions of TCP protocol employ different strategies.

Error Control: How to retransmit
-----
Three basic strategies
- Stop-and-wait
- Go Back N
- Selective Acknowledgments

Congestion Control: What's window size; Avoid saturating routers
------
Basic strategies
- AIMD
	additive increase, multiple decrease
- Fast Retransmit and Fast Recovery
- Adjust Rate

Flow Control: Avoid saturating destination
------
- When sending ack packet, the destination inform how many buffers left.

What we need to do
------
- Realize all the features
- Combine different features so we have different versions of TCP