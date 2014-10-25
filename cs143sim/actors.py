"""
This module contains all actor definitions.

.. autosummary::

    Buffer
    Flow
    Host
    Link
    Packet
    Router

.. moduleauthor:: Lan Hongjian <lanhongjianlr@gmail.com>
.. moduleauthor:: Yamei Ou <oym111@gmail.com>
.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <neicullyn@gmail.com>
"""


class Buffer:
    """Representation of a data storage container

    Buffers store data to be linked while Link is busy sending data.

    :param int capacity: maximum number of bits that can be stored
    :ivar int capacity: maximum number of bits that can be stored
    :ivar list packets: packets currently in storage
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.packets = []

    def add(self, packet):
        current_level = sum(packet.size for packet in self.packets)
        if current_level + packet.size <= self.capacity:
            self.packets.append(packet)


class Flow:
    """Representation of a connection between access points

    Flows try to transmit data from Host to Host.

    :param .Host source: source Host
    :param .Host destination: destination Host
    :param float amount: amount of data to transmit
    :ivar .Host source: source Host
    :ivar .Host destination: destination Host
    :ivar float amount: amount of data to transmit
    """
    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount

    def make_packet(self, packet_num):
        """
        Make a packet based on the packet number
        """

    def send_packet(self):
        """
        When possible, TLA use this method to send a packet
        """

    def receive_packet(self):
        """
        When receive a packet, check if the packet is an ack packet. If so, run TLA
        """

    def time_out(self):
        """
        When time out happens, run TLA
        Time_out timers should be reset if a the ack arrive
        """

    def tla(self):
        """
        Transport Layer Algorithm main body
        Including transmission control, congestion control algorithm (window size adjust)
        Flow control might not be needed, as the receiving buffer size is unlimited.

        For example (stop and wait):
            TLA send a packet
            while(! all packet have been transmitted):
                yield(time_out|receive_ack)
                if(time_out) :
                    retransmit
                    reset timer
                if(receive_ack) :
                    transmit new packet
                    reset timer
        """


class Host:
    """Representation of an access point

    Hosts send Packets through Links to Routers or other Hosts.

    :param str address: IP address
    :param list flows: Flows on this host
    :param .Link link: Link connected to this host
    :ivar str address: IP address
    :ivar .Link link: Link connected to this host
    :ivar list flows: Flows on this host
    """
    def __init__(self, address, flows, link):
        self.address = address
        self.flows = flows
        self.link = link

    def send(self, packet):
        self.link.add(packet)

    def receive(self, packet):
        # TODO: pass to flows[packet.destination]
        pass


class Link:
    """Representation of a physical link between access points or routers

    Links carry packets from one end to the other.

    :param source: source :class:`.Host` or :class:`.Router`
    :param destination: destination Host or Router
    :param float delay: amount of time required to transmit a packet
    :param float rate: speed of removing data from source
    :param int buffer_capacity: Buffer capacity in bits
    :ivar source: source Host or Router
    :ivar destination: destination Host or Router
    :ivar float delay: amount of time required to transmit a packet
    :ivar list buffer: packets currently in transmission
    :ivar bool busy: whether currently removing data from source
    :ivar float utilization: fraction of capacity in use
    """
    def __init__(self, source, destination, delay, rate, buffer_capacity):
        self.source = source
        self.destination = destination
        self.delay = delay
        self.rate = rate
        self.buffer = Buffer(capacity=buffer_capacity)
        self.busy = False
        self.utilization = 0

    def add(self, packet):
        if self.busy:
            self.buffer.add(packet)
        else:
            self.send(packet)

    def send(self, packet):
        # TODO: implement sending
        pass


class Packet:
    """Representation of a quantum of information

    Packets carry information along the network, between Hosts or Routers.

    :param source: source Host or Router
    :param destination: destination Host or Router
    :param int number: sequence number
    :param acknowledgement: acknowledgement... something
    :cvar int PACKET_SIZE: size of every packet, in bits
    :ivar source: source Host or Router
    :ivar destination: destination Host or Router
    :ivar int number: sequence number
    :ivar acknowledgement: acknowledgement... something
    :ivar int size: size of packet, in bits
    """
    PACKET_SIZE = 8192  # bits

    def __init__(self, source, destination, number, acknowledgement):
        self.source = source
        self.destination = destination
        self.number = number
        self.acknowledgement = acknowledgement
        self.size = Packet.PACKET_SIZE


class Router:
    """Representation of a router...

    Routers route packets through the network to their destination Hosts.

    :param list links: all connected Links
    :param .Link default_gateway: default route
    :ivar list links: all connected Links
    :ivar dict table: routing table
    """
    def __init__(self, links, address, default_gateway):
        self.address = address
        self.links = links
        self.table = {}
        self.default_gateway = default_gateway

    def update_router_table(self):
        # TODO: update router table
        pass

    def map_route(self, packet):
        # TODO: get output_link
        return output_link

    def read_packet_head(packet):
        # TODO: get destination_address
        return destination_address

    def get_neighbor_router(self):
        # TODO: get neighbor_routers
        return neighbor_routers
