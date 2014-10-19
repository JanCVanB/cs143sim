"""
This module contains all event definitions

.. autosummary::

    FlowStart
    LinkAvailable
    PacketReceipt
    UpdateRoutingTable

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""

from simpy.events import Timeout


class FlowStart(Timeout):
    """Flow begins generating packets

    :param simpy.core.Environment environment: SimPy simulation environment
    :param float delay: time until flow starts
    :param actors.Flow flow: Flow that starts
    """
    def __init__(self, environment, delay, flow):
        super(FlowStart, self).__init__(environment, delay, value=flow)


class LinkAvailable(Timeout):
    """Router finishes sending a packet on Link

    :param simpy.core.Environment environment: SimPy simulation environment
    :param float delay: time until Router finishes
    :param actors.Router router: Router that finishes
    :param actors.Link link: Link on which a packet was sent
    """
    def __init__(self, environment, delay, router, link):
        super(LinkAvailable, self).__init__(environment, delay, value=(router, link))


class PacketReceipt(Timeout):
    """Router receives Packet on Link
    
    :param simpy.core.Environment environment: SimPy simulation environment
    :param float delay: time until Packet begins to arrive at Router
    :param actors.Router router: Router that receives
    :param actors.Link link: Link on which Packet arrives
    :param actors.Packet packet: Packet that arrives
    """
    def __init__(self, environment, delay, router, link, packet):
        super(PacketReceipt, self).__init__(environment, delay, value=(router, link, packet))


class UpdateRoutingTable(Timeout):
    """Router updates its routing table

    :param simpy.core.Environment environment: SimPy simulation environment
    :param float delay: time until Router updates
    :param actors.Router router: Router that updates
    """
    def __init__(self, environment, delay, router):
        super(UpdateRoutingTable, self).__init__(environment, delay, value=router)
