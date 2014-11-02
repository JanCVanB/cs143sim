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

<<<<<<< Updated upstream
from tla_stop_and_wait import StopAndWait
=======
from cs143sim.constants import PACKET_SIZE
>>>>>>> Stashed changes

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
        """
        Adds packet to `packets` if `capacity` will not be exceeded,
        drops packet if buffer if full.

        :param packet: :class:`.Packet` added to buffer.
        """
        current_level = sum(packet.size for packet in self.packets)
        if current_level + packet.size <= self.capacity:
            self.packets.append(packet)
        else:
            # The packet cannot be stored, so the packet is dropped
            # TODO: Insert callback for simulation monitor (report that a packet was dropped)
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
        
        self.W=1
        self.tla=StopAndWait(self)
        

    def __str__(self):
        return ('Flow from ' + self.source.address +
                ' to ' + self.destination.address)

    def make_packet(self, packet_num):
        """
        Make a packet based on the packet number
        """

        
    def make_ack_packet(self, packet):
        """
        Make a ack packet
        """

    def send_packet(self, packet):
        """
        When possible, TLA use this method to send a packet
        """

    def receive_packet(self):
        """
        If the packet is a data packet, generate an ack packet
        """
        
        """
        If the packet is a ack packet, call tla.rcv_ack()
        """
        

    def time_out(self):
        """
        When time out happens, run TLA
        Time_out timers should be reset if a the ack arrive
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
    :param ack: acknowledgement... something
    :cvar int PACKET_SIZE: size of every :class:`.Packet`, in bits
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar int number: sequence number
    :ivar ack: acknowledgement... something
    :ivar int size: size, in bits
    :ivar str timestamp: time at which the packet was created
    """
    def __init__(self, timestamp, source, destination):
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.size = PACKET_SIZE

class DataPacket(Packet):
    def __init__(self, number, ack, timestamp, source, destination):
        Packet.__init__(self, timestamp, source, destination)
        self.number = number
        self.ack = ack

class RouterPacket(Packet):
    def __init__(self, timestamp, routertable, source):
        Packet.__init__(self, timestamp, source, destination = 0)
        self.routertable = routertable

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
