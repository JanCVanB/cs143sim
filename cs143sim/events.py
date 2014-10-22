"""
This module contains all event definitions.

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

    :param simpy.core.Environment env: SimPy simulation environment
    :param float delay: time until flow starts
    :param cs143sim.actors.Flow flow: Flow that starts
    """
    def __init__(self, env, delay, flow):
        super(FlowStart, self).__init__(env, delay, value=flow)


class LinkAvailable(Timeout):
    """Router finishes sending a packet on Link

    :param simpy.core.Environment env: SimPy simulation environment
    :param float delay: time until Router finishes
    :param cs143sim.actors.Router router: Router that finishes
    :param cs143sim.actors.Link link: Link on which a packet was sent
    """
    def __init__(self, env, delay, router, link):
        super(LinkAvailable, self).__init__(env, delay, value=(router, link))


class PacketReceipt(Timeout):
    """Router receives Packet on Link
    
    :param simpy.core.Environment env: SimPy simulation environment
    :param float delay: time until Packet begins to arrive at Router
    :param cs143sim.actors.Router router: Router that receives
    :param cs143sim.actors.Link link: Link on which Packet arrives
    :param cs143sim.actors.Packet packet: Packet that arrives
    """
    def __init__(self, env, delay, router, link, packet):
        super(PacketReceipt, self).__init__(env, delay, value=(router, link,
                                                               packet))


class UpdateRoutingTable(Timeout):
    """Router updates its routing table

    :param simpy.core.Environment env: SimPy simulation environment
    :param float delay: time until Router updates
    :param cs143sim.actors.Router router: Router that updates
    """
    def __init__(self, env, delay, router):
        super(UpdateRoutingTable, self).__init__(env, delay, value=router)
