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

    Buffers store data to be linked while :class:`.Link` is busy sending data.

    :param int capacity: maximum number of bits that can be stored
    :ivar int capacity: maximum number of bits that can be stored
    :ivar list packets: :class:`Packets <.Packet>` currently in storage
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.packets = []

    def add(self, packet):
        current_level = sum(packet.size for packet in self.packets)
        if current_level + packet.size <= self.capacity:
            self.packets.append(packet)
        else:
            # The packet cannot be stored, so the packet is dropped
            pass


class Flow:
    """Representation of a connection between access points

    Flows try to transmit data from :class:`.Host` to :class:`.Host`.

    :param source: source :class:`.Host`
    :param destination: destination :class:`.Host`
    :param float amount: amount of data to transmit
    :ivar source: source :class:`.Host`
    :ivar destination: destination :class:`.Host`
    :ivar float amount: amount of data to transmit
    """
    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount

    def __str__(self):
        return ('Flow from ' + self.source.address +
                ' to ' + self.destination.address)

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

    def react_to_flow_start(self, event):
        # TODO: react by sending packets to Host
        pass


class Host:
    """Representation of an access point

    Hosts send :class:`Packets <.Packet>` through a :class:`.Link` to a
    :class:`.Router` or to another :class:`.Host`.

    :param str address: IP address
    :ivar str address: IP address
    :ivar list flows: :class:`Flows <.Flow>` on this :class:`.Host`
    :ivar link: :class:`Link` connected to this :class:`.Host`
    """
    def __init__(self, address):
        self.address = address
        self.flows = []
        self.link = None

    def __str__(self):
        return 'Host at ' + self.address

    def send(self, packet):
        self.link.add(packet)

    def receive(self, packet):
        # TODO: pass to flows[packet.destination]
        pass


class Link:
    """Representation of a physical link between access points or routers

    Links carry packets from one end to the other.

    :param source: source :class:`.Host` or :class:`.Router`
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param float delay: amount of time required to transmit a :class:`.Packet`
    :param float rate: speed of removing data from source
    :param int buffer_capacity: :class:`.Buffer` capacity in bits
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar float delay: amount of time required to transmit a :class:`.Packet`
    :ivar list buffer: :class:`Packets <.Packet>` currently in transmission
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

    def __str__(self):
        return ('Link from ' + self.source.address +
                ' to ' + self.destination.address)

    def add(self, packet):
        if self.busy:
            self.buffer.add(packet)
        else:
            self.send(packet)

    def react_to_link_available(self, event):
        # TODO: implement the pseudo-code below
        # self.busy = False
        # if packets in buffer:
        #     self.busy = True
        #     self.send(self.buffer.get_first_packet())
        pass

    def send(self, packet):
        # TODO: implement sending by scheduling LinkAvailable and PacketReceipt
        pass


class Packet:
    """Representation of a quantum of information

    Packets carry information along the network, between :class:`Hosts <.Host>`
    or :class:`Routers <.Router>`.

    :param source: source :class:`.Host` or :class:`.Router`
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param int number: sequence number
    :param acknowledgement: acknowledgement... something
    :cvar int PACKET_SIZE: size of every :class:`.Packet`, in bits
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar int number: sequence number
    :ivar acknowledgement: acknowledgement... something
    :ivar int size: size, in bits
    """
    PACKET_SIZE = 8192  # bits

    def __init__(self, source, destination, number, acknowledgement):
        self.source = source
        self.destination = destination
        self.number = number
        self.acknowledgement = acknowledgement
        self.size = Packet.PACKET_SIZE

    def __str__(self):
        return ('Packet ' + str(self.number) +
                ' from ' + self.source.address +
                ' to ' + self.destination.address)


class JunlinPacket(Packet):
    """Packet used for sending flow data"""


class YameiPacket(Packet):
    """Packet used for updating routing tables"""


class Router:
    """Representation of a data router

    Routers route :class:`Packets <.Packet>` through the network to their
    respective destination :class:`Hosts <.Host>`.

    :param str address: IP address
    :ivar str address: IP address
    :ivar list links: all connected :class:`Links <.Link>`
    :ivar dict table: routing table
    :ivar default_gateway: default :class:`.Link`
    """
    def __init__(self, address):
        self.address = address
        self.links = []
        self.table = {}
        self.default_gateway = None


    def __str__(self):
        return 'Router at ' + self.address

    def react_to_routing_table_outdated(self, event):
        self.update_router_table()

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
