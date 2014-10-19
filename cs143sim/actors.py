"""
This module contains all actor definitions.

.. autosummary::

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


class Flow:
    """Representation of a connection between access points

    Flows try to transmit data from Host to Host.

    :param actors.Host source: source Host
    :param actors.Host destination: destination Host
    :param float amount: amount of data to transmit
    :ivar actors.Host source: source Host
    :ivar actors.Host destination: destination Host
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
    :param list flows: Flows on this host
    :ivar str address: IP address
    :ivar list flows: Flows on this host
    """
    def __init__(self, address, flows):
        self.address = address
        self.flows = flows


class Link:
    """Representation of a physical link between access points or routers

    Links carry packets from one end to the other.

    :param source: source Host or Router
    :param destination: destination Host or Router
    :param float delay: amount of time required to transmit a packet
    :ivar source: source Host
    :ivar destination: destination Host
    :ivar float delay: amount of time required to transmit a packet
    :ivar list buffer: packets currently in transmission
    :ivar float utilization: fraction of capacity in use
    """
    def __init__(self, source, destination, delay):
        self.source = source
        self.destination = destination
        self.delay = delay
        self.buffer = []
        self.utilization = 0


class Packet:
    """Representation of a quantum of information

    Packets carry information along the network, between Hosts or Routers.

    :param source: source port
    :param destination: destination port
    :param int number: sequence number
    :param acknowledgement: acknowledgement... something
    :ivar source: source port
    :ivar destination: destination port
    :ivar int number: sequence number
    :ivar acknowledgement: acknowledgement... something
    """
    def __init__(self, source, destination, number, acknowledgement):
        self.source = source
        self.destination = destination
        self.number = number
        self.acknowledgement = acknowledgement


class Router:
    """Representation of a... router

    Routers route packets through the network to their destination Hosts.

    :param list links: all connected Links
    :ivar list links: all connected Links
    :ivar dict table: routing table
    """
    def __init__(self, links):
        self.links = links
        self.table = {}
