from simpy.core import Environment

from cs143sim.events import FlowStart
from cs143sim.events import LinkAvailable
from cs143sim.events import PacketReceipt
from cs143sim.events import UpdateRoutingTable
from test_actors import basic_flow
from test_actors import basic_link
from test_actors import basic_packet
from test_actors import basic_router


def basic_environment():
    return Environment()


def basic_flow_start():
    FlowStart(env=basic_environment(), delay=1.0, flow=basic_flow())


def basic_link_available():
    LinkAvailable(env=basic_environment(), delay=1.0, router=basic_router(),
                  link=basic_link())


def basic_packet_receipt():
    PacketReceipt(env=basic_environment(), delay=1.0, router=basic_router(),
                  link=basic_link(), packet=basic_packet())


def basic_update_routing_table():
    UpdateRoutingTable(env=basic_environment(), delay=1.0,
                       router=basic_router())


def test_flow_start():
    basic_flow_start()


def test_link_available():
    basic_link_available()


def test_packet_receipt():
    basic_packet_receipt()


def test_update_routing_table():
    basic_update_routing_table()
