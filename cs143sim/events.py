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

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Flow` starts
    :param flow: :class:`~cs143sim.actors.Flow` that starts
    """
    def __init__(self, env, delay, flow):
        super(FlowStart, self).__init__(env, delay, value=flow)


class LinkAvailable(Timeout):
    """Router finishes sending a packet on Link

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Router` finishes
    :param router: :class:`~cs143sim.actors.Router` that finishes
    :param link: :class:`~cs143sim.actors.Link` on which a
        :class:`~cs143sim.actors.Packet` was sent
    """
    def __init__(self, env, delay, router, link):
        super(LinkAvailable, self).__init__(env, delay, value=(router, link))


class PacketReceipt(Timeout):
    """Router receives Packet on Link
    
    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until Packet begins to arrive at Router
    :param router: :class:`~cs143sim.actors.Router` that receives
    :param link: :class:`~cs143sim.actors.Link` on which
        :class:`~cs143sim.actors.Packet` arrives
    :param packet: :class:`~cs143sim.actors.Packet` that arrives
    """
    def __init__(self, env, delay, router, link, packet):
        super(PacketReceipt, self).__init__(env, delay, value=(router, link,
                                                               packet))


class UpdateRoutingTable(Timeout):
    """Router updates its routing table

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Router` updates
    :param router: :class:`~cs143sim.actors.Router` that updates
    """
    def __init__(self, env, delay, router):
        super(UpdateRoutingTable, self).__init__(env, delay, value=router)
