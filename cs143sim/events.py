"""This module contains all event definitions.

.. autosummary::

    FlowStart
    LinkAvailable
    PacketReceipt
    PacketTimeOut
    RoutingTableOutdated
    VegasTimeOut

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <jancvanbruggen@gmail.com>
"""
from simpy.events import Timeout


class FlowStart(Timeout):
    """A :class:`~cs143sim.actors.Flow` begins generating packets

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Flow` starts
    :param flow: :class:`~cs143sim.actors.Flow` that starts
    """
    def __init__(self, env, delay, flow):

        super(FlowStart, self).__init__(env=env, delay=delay)
        self.callbacks.append(flow.react_to_flow_start)


class LinkAvailable(Timeout):
    """A :class:`~cs143sim.actors.Router` finishes sending a
    :class:`~cs143sim.actors.Packet` on :class:`~cs143sim.actors.Link`

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Router` finishes
    :param router: :class:`~cs143sim.actors.Router` that finishes
    :param link: :class:`~cs143sim.actors.Link` on which a
        :class:`~cs143sim.actors.Packet` was sent
    """
    def __init__(self, env, delay, link):
        super(LinkAvailable, self).__init__(env=env, delay=delay)
        self.callbacks.append(link.react_to_link_available)


class PacketReceipt(Timeout):
    """A :class:`~cs143sim.actors.Host` or a :class:`~cs143sim.actors.Router`
    receives a :class:`~cs143sim.actors.Packet` on a
    :class:`~cs143sim.actors.Link`
    
    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until Packet begins to arrive at Router (in ms)
    :param receiver: :class:`~cs143sim.actors.Host` or
        :class:`~cs143sim.actors.Router` that receives `packet`
    :param link: :class:`~cs143sim.actors.Link` on which `packet` arrives
    :param packet: :class:`~cs143sim.actors.Packet` that arrives
    """
    def __init__(self, env, delay, receiver, packet):

        super(PacketReceipt, self).__init__(env=env, delay=delay, value=packet)
        self.callbacks.append(receiver.react_to_packet_receipt)


class PacketTimeOut(Timeout):
    """
    Time out event for tla
    """
    def __init__(self, env, delay, actor, expected_time):
        super(PacketTimeOut, self).__init__(env, delay, value=expected_time)
        self.callbacks.append(actor.react_to_time_out)    


class RoutingTableOutdated(Timeout):
    """A :class:`~cs143sim.actors.Router` updates its routing table

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Router` updates
    :param router: :class:`~cs143sim.actors.Router` that updates
    """
    def __init__(self, env, delay, router):
        super(RoutingTableOutdated, self).__init__(env=env, delay=delay)
        self.callbacks.append(router.react_to_routing_table_outdated)


class VegasTimeOut(Timeout):
    """
    Time out event for tla
    """
    def __init__(self, env, delay, actor):
        super(VegasTimeOut, self).__init__(env, delay)
        self.callbacks.append(actor.react_to_vegas_time_out)
