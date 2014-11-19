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
    :ivar str timestamp: time at which the packet was created
    """
    def __init__(self, destination, source, timestamp):
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.size = PACKET_SIZE


class DataPacket(Packet):
    """A packet used for transferring data

    :param destination: destination :class:`.Host` or :class:`.Router`
    :param source: source :class:`.Host` or :class:`.Router`
    :param str timestamp: time at which the packet was created
    """
    def __init__(self, destination, source, timestamp, acknowledgement, number):
        # TODO: define number and acknowledgement in docstring
        super(DataPacket, self).__init__(timestamp=timestamp, source=source,
                                         destination=destination)
        self.number = number
        self.acknowledgement = acknowledgement


class RouterPacket(Packet):
    """A packet used to update routing tables

    :param source: source :class:`.Host` or :class:`.Router`
    :param str timestamp: time at which the packet was created
    """
    def __init__(self, source, timestamp, router_table):
        # TODO: define router_table in docstring
        super(RouterPacket, self).__init__(timestamp=timestamp, source=source,
                                           destination=0)
        self.router_table = router_table
