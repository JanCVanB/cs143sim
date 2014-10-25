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
    return Host(address='', flows=[], link=None)


def basic_link():
    return Link(source=basic_host(), destination=basic_host(), delay=1.0,
                rate=1.0, buffer_capacity=1)


def basic_packet():
    return Packet(source=basic_host(), destination=basic_host(), number=1,
                  acknowledgement=object())


def basic_router():
    return Router(links=[basic_link()], address='',
                  default_gateway=basic_link())


def buffer_overflow():
    buffer_capacity = 2
    number_of_packets = 3
    buffer_ = basic_buffer()
    packets = []
    for _ in range(number_of_packets):
        packet_ = basic_packet()
        packet_.size = 1
        packets.append(packet_)
    buffer_.capacity = buffer_capacity
    for packet_ in packets:
        buffer_.add(packet_)
        print(buffer_.packets)
    for i in range(number_of_packets):
        if i < buffer_capacity:
            assert packets[i] in buffer_.packets
        else:
            assert packets[i] not in buffer_.packets


def link_busy():
    link_ = basic_link()
    assert link_.buffer.capacity == 1
    packet_ = basic_packet()
    packet_.size = 1
    link_.busy = True
    link_.add(packet_)
    assert packet_ in link_.buffer.packets


def test_buffer():
    basic_buffer()
    buffer_overflow()


def test_flow():
    basic_flow()


def test_host():
    basic_host()


def test_link():
    basic_link()
    link_busy()


def test_packet():
    basic_packet()


def test_router():
    basic_router()
