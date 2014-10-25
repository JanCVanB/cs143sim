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


DEBUG = True


def print_event(event):
    print 'At', event.env.now, event.__class__.__name__, 'for',
    print full_string(event._value)


def full_string(thing):
    if type(thing) == dict:
        return ', '.join(full_string(key) + ' : ' + full_string(thing[key])
                         for key in thing)
    if type(thing) == list:
        return '[' + ', '.join(full_string(item) for item in thing) + ']'
    if type(thing) == tuple:
        return '(' + ', '.join(full_string(item) for item in thing) + ')'
    else:
        return str(thing)


class FlowStart(Timeout):
    """A :class:`~cs143sim.actors.Flow` begins generating packets

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Flow` starts
    :param flow: :class:`~cs143sim.actors.Flow` that starts
    """
    def __init__(self, env, delay, flow):
        super(FlowStart, self).__init__(env, delay, value=flow)
        if DEBUG:
            self.callbacks.append(print_event)


class LinkAvailable(Timeout):
    """A :class:`~cs143sim.actors.Router` finishes sending a
    :class:`~cs143sim.actors.Packet` on :class:`~cs143sim.actors.Link`

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Router` finishes
    :param router: :class:`~cs143sim.actors.Router` that finishes
    :param link: :class:`~cs143sim.actors.Link` on which a
        :class:`~cs143sim.actors.Packet` was sent
    """
    def __init__(self, env, delay, router, link):
        super(LinkAvailable, self).__init__(env, delay, value=(router, link))
        if DEBUG:
            self.callbacks.append(print_event)


class PacketReceipt(Timeout):
    """A :class:`~cs143sim.actors.Host` or a :class:`~cs143sim.actors.Router`
    receives a :class:`~cs143sim.actors.Packet` on a
    :class:`~cs143sim.actors.Link`
    
    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until Packet begins to arrive at Router
    :param receiver: :class:`~cs143sim.actors.Host` or
        :class:`~cs143sim.actors.Router` that receives `packet`
    :param link: :class:`~cs143sim.actors.Link` on which `packet` arrives
    :param packet: :class:`~cs143sim.actors.Packet` that arrives
    """
    def __init__(self, env, delay, receiver, link, packet):
        super(PacketReceipt, self).__init__(env, delay, value=(receiver, link,
                                                               packet))
        if DEBUG:
            self.callbacks.append(print_event)


class UpdateRoutingTable(Timeout):
    """A :class:`~cs143sim.actors.Router` updates its routing table

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param float delay: time until :class:`~cs143sim.actors.Router` updates
    :param router: :class:`~cs143sim.actors.Router` that updates
    """
    def __init__(self, env, delay, router):
        super(UpdateRoutingTable, self).__init__(env, delay, value=router)
        if DEBUG:
            self.callbacks.append(print_event)
