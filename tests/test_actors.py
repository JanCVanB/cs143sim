from cs143sim.actors import Buffer
from cs143sim.actors import Flow
from cs143sim.actors import Host
from cs143sim.actors import Link
from cs143sim.actors import Packet
from cs143sim.actors import Router


def basic_buffer():
    return Buffer(capacity=1)


def basic_flow():
    return Flow(source=basic_host(), destination=basic_host(), amount=1.0)


def basic_host():
    return Host(address='', flows=[])


def basic_link():
    return Link(source=basic_host(), destination=basic_host(), delay=1.0)


def basic_packet():
    return Packet(source=basic_host(), destination=basic_host(), number=1,
                  acknowledgement=object())


def basic_router():
    return Router(links=[basic_link()])


def test_buffer():
    basic_buffer()


def test_flow():
    basic_flow()


def test_host():
    basic_host()


def test_link():
    basic_link()


def test_packet():
    basic_packet()


def test_router():
    basic_router()
