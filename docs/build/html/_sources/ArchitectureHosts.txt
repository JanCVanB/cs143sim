Hosts
=====

This is a summary of variables and functions of host.

Abstract
--------

In the general cases, hosts are in charge of flow control. congestion control, and transmission protocols. But in our architecture, there is an individual flow class, so the main mission of hosts is to link flows(packets) to the outer world, which are links and routers. 

Variables
---------

- IP address
- Flows on this host
- Sending Buffer?
- Receiving Buffer?
- Links connected to this host

.. note:: Sending buffer? Ask Flows each time link available?

.. note:: Receiving buffer?

Functions
---------

- Detect the buffer of the links it connects
- Transmit packets: Take the order of the flow, transmit the packet if the link is robust.
- Receive packets: Receive packets from links. It should be able to distinguish acknowledge packets from normal packets.
- Send feedbacks to flows: When the host receives an acknowledgement, it should let the flow know that the packet has been sent successfully.
- Check the destination IP address of incoming packets

.. note:: Ignore bad destination IPs?
