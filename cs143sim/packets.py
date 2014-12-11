"""This module contains all packet definitions.

.. autosummary::

    Packet
    DataPacket
    RouterPacket

.. moduleauthor:: Lan Hongjian <lanhongjianlr@gmail.com>
.. moduleauthor:: Yamei Ou <oym111@gmail.com>
.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <neicullyn@gmail.com>
"""
from cs143sim.constants import PACKET_SIZE


class Packet(object):
    """Representation of a quantum of information

    Packets carry information along the network, between :class:`Hosts <.Host>`
    or :class:`Routers <.Router>`.

    :param destination: destination :class:`.Host` or :class:`.Router`
    :param source: source :class:`.Host` or :class:`.Router`
    :param str timestamp: time at which the packet was created
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar float timestamp: time at which the packet was created
    :ivar int size: size of the packet
    """
    def __init__(self, destination, source, timestamp):
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.size = PACKET_SIZE


class DataPacket(Packet):
    """A packet used for transferring data
    
    DataPackets transmit data along the network, between :class:`Hosts <.Host>`
    or :class:`Routers <.Router>`.

    :param destination: destination :class:`.Host` or :class:`.Router`
    :param source: source :class:`.Host` or :class:`.Router`
    :param float timestamp: time at which the packet was created
    :param bool acknowledgement: indicate whether the packet is an AckPacket
    :param int number: the number of the packet in a flow
    :ivar int number: the number of the packet in a flow
    :ivar bool acknowledgement: indicate whether the packet is an AckPacket
    """
    def __init__(self, destination, source, timestamp, acknowledgement, number):
        super(DataPacket, self).__init__(timestamp=timestamp, source=source,
                                         destination=destination)
        self.number = number
        self.acknowledgement = acknowledgement


class RouterPacket(Packet):
    """A packet used to update routing tables
    
    RouterPackets carry information of routing tables along the network, between :class:`Routers <.Router>`.

    :param source: source :class:`.Host` or :class:`.Router`
    :param float timestamp: time at which the packet was created
    :param dict router_table: the routing table
    :param bool acknowledgement: indicate whether the packet is an AckPacket
    :ivar dict router_table: the routing table of the RouterPacket
    :ivar int number: the number of the RouterPacket, which is always 0
    :ivar bool acknowledgement: indicate whether the packet is an AckPacket
    """
    def __init__(self, source, timestamp, router_table, acknowledgement):
        # TODO: define router_table in docstring
        super(RouterPacket, self).__init__(timestamp=timestamp, source=source,
                                           destination=0)
        self.router_table = router_table
        self.number = 0
        self.acknowledgement = acknowledgement
