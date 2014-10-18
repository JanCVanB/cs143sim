Links
=====

The links are in charge of connecting hosts/routers together and passing on the packets along through the network.

Link Components
---------------

- Source and Destination. The links will be the intermediary handler of packets between hosts/routers.
- Delay. Link will hold onto packets from given amount of time (delay) before handing it off to routers/hosts.
- Add packets to receiving host/router's buffer (64KB) and allow the host/router to pull from that buffer.
- Utilization. This metric will be calculated by the link object and reported/made available to the monitoring system.

.. note:: Receiving buffer?
