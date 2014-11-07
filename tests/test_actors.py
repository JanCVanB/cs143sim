from cs143sim.actors import Buffer
from cs143sim.actors import Flow
from cs143sim.actors import Host
from cs143sim.actors import Link
from cs143sim.actors import DataPacket
from cs143sim.actors import Router
from cs143sim.simulation import Controller
from cs143sim.simulation import ControlledEnvironment


def basic_buffer():
    return Buffer(env=ControlledEnvironment(controller=Controller()),
                  capacity=1, link=basic_link())


def basic_flow():
    return Flow(env=ControlledEnvironment(controller=Controller()),
                source=basic_host(), destination=basic_host(),
                amount=1.0)


def basic_host():
    return Host(env=ControlledEnvironment(controller=Controller()), address='')


def basic_link():
    return Link(env=ControlledEnvironment(controller=Controller()),
                source=basic_host(), destination=basic_host(),
                delay=1.0, rate=1.0, buffer_capacity=1)


def basic_packet():
    #return Packet(source=basic_host(), destination=basic_host(), number=1,
    #              acknowledgement=object())
    return DataPacket(env=ControlledEnvironment(controller=Controller()),
                      source=basic_host(), destination=basic_host(),
                      number=1, acknowledgement=object(), timestamp=0)

def basic_router_packet():
    #return Packet(source=basic_host(), destination=basic_host(), number=1,
    #              acknowledgement=object())
    return RouterPacket(env=ControlledEnvironment(controller=Controller()),
                      source=basic_host(), destination=basic_host(),
                      number=1, acknowledgement=object(), timestamp=0)

def basic_router():
    return Router(env=ControlledEnvironment(controller=Controller()),
                  address='')


def buffer_overflow():
    buffer_capacity = 2
    number_of_packets = 3
    buffer_ = basic_buffer()
    buffer_.env.controller.packet_loss[buffer_.link] = []
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


def router_initialize():
    router_ip_address = '1'
    router = basic_router()
    router.address = router_ip_address
    #router.default_gateway = '5'
    links = []
    number_of_links = 2
    
    link1_ = basic_link()
    link1_.destination = router
    link2_ = basic_link()
    link2_.source = router
    links.append(link1_)
    links.append(link2_)

    router.links = links
    assert link2_ in router.links
    assert link1_ == router.links[0]

    all_host_ip_addresses = ['11','12','13','14']
    router.initialize_routing_table(all_host_ip_addresses)
    



def router_forward():
    pass


def router_receive_update_packet():
    # packet_ = basic_packet()
    # link_1 = basic_link()
    # link_2 = basic_link()
    # router_ = basic_router()
    # router_.links.extend([link_1, link_2])
    # router_.do_things()

    pass

def router_send_update_packet():
    pass


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
    router_initialize()
    # router_forward()
    # router_receive_update_packet()
    # router_send_update_packet()
