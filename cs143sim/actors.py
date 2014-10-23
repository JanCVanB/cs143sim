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

    :param cs143sim.actors.Host source: source Host
    :param cs143sim.actors.Host destination: destination Host
    :param float amount: amount of data to transmit
    :ivar cs143sim.actors.Host source: source Host
    :ivar cs143sim.actors.Host destination: destination Host
    :ivar float amount: amount of data to transmit
    """
    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount


class Host:
    """Representation of an access point

    Hosts send Packets through Links to Routers or other Hosts.

    :param str address: IP address
    :param int buffer: Sending buffer
    :param list flows: Flows on this host
    :param link link: Link connected to this host
    :ivar str address: IP address
    :ivar int buffer: Sending buffer
    :ivar list link: Link connected to this host
    :ivar list flows: Flows on this host
    """
    def __init__(self, address, flows, link, buffer):
        self.address = address
        self.flows = flows
        self.link = link
        self.buffer = buffer

    def detect_buffer(self)
        return self.link.buffer

    def send(self, packet)
        if self.detect_buffer() >= packet.PACKET_SIZE:
           pass to the link

    def receive(self, packet)
        pass to flows[packet.destination]

class Link:
    """Representation of a physical link between access points or routers

    Links carry packets from one end to the other.

    :param source: source Host or Router
    :param destination: destination Host or Router
    :param float delay: amount of time required to transmit a packet
    :param float rate: speed of removing data from source
    :param int buffer_capacity: Buffer capacity in bits
    :ivar source: source Host
    :ivar destination: destination Host
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

    :param source: source port
    :param destination: destination port
    :param int number: sequence number
    :param acknowledgement: acknowledgement... something
    :cvar int PACKET_SIZE: size of every packet, in bits
    :ivar source: source port
    :ivar destination: destination port
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
    :ivar list links: all connected Links
    :ivar dict table: routing table
    """
    def __init__(self, links):
        self.links = links
        self.table = {}
