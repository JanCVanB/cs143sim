'''
This module contains all event definitions

.. autosummary::

    FlowStart
    LinkAvailable
    PacketReceipt
    UpdateRoutingTable

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
'''

from simpy.events import Timeout


class FlowStart(Timeout):
    '''Flow begins generating packets

    :param simpy.core.Environment Environment: SimPy simulation environment
    :param float Delay: time until flow starts
    :param actors.Flow Flow: flow that starts
    '''
    def __init__(self, Environment, Delay, Flow):
        super(UpdateRoutingTable, self).__init__(Environment, Delay, value=Flow)


class LinkAvailable(Timeout):
    '''Router finishes sending a packet on Link

    :param simpy.core.Environment Environment: SimPy simulation environment
    :param float Delay: time until Router finishes
    :param actors.Router Router: Router that finishes
    :param actors.Link Link: Link on which a packet was sent
    '''
    def __init__(self, Environment, Delay, Router, Link):
        super(PortAvailable, self).__init__(Environment, Delay, value=(Router, Link))


class PacketReceipt(Timeout):
    '''Router receives Packet on Link

    :param simpy.core.Environment Environment: SimPy simulation environment
    :param float Delay: time until Packet begins to arrive at Router
    :param actors.Router Router: Router that receives
    :param actors.Link Link: Link on which Packet arrives
    :param actors.Packet Packet: Packet that arrives
    '''
    def __init__(self, Environment, Delay, Router, Link, Packet):
        super(PacketReceived, self).__init__(Environment, Delay, value=(Router, Link))


class UpdateRoutingTable(Timeout):
    '''Router updates its routing table

    :param simpy.core.Environment Environment: SimPy simulation environment
    :param float Delay: time until Router updates
    :param actors.Router Router: Router that updates
    '''
    def __init__(self, Environment, Delay, Router):
        super(UpdateRoutingTable, self).__init__(Environment, Delay, value=Router)
