from simpy import *
from cs143sim.actors import *
from cs143sim.events import *
from cs143sim.tla import *
from cs143sim.constants import *





def case1():
    env=Environment()
    
    H1=Host(env=env, address="0")
    H2=Host(env=env, address="1")

    R1=Router(env=env, address="R1")
    R2=Router(env=env, address="R2")
    R3=Router(env=env, address="R3")
    R4=Router(env=env, address="R4")
    
    L0=Link(env=env, source=H1, destination=R1, delay=10, rate=12.5, buffer_capacity=64*PACKET_SIZE)
    L1=Link(env=env, source=R1, destination=R2, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L2=Link(env=env, source=R1, destination=R3, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L3=Link(env=env, source=R2, destination=R4, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L4=Link(env=env, source=R3, destination=R4, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L5=Link(env=env, source=R4, destination=H2, delay=10, rate=12.5, buffer_capacity=64*PACKET_SIZE)

    L00=Link(env=env, source=R1, destination=H1, delay=10, rate=12.5, buffer_capacity=64*PACKET_SIZE)
    L10=Link(env=env, source=R2, destination=R1, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L20=Link(env=env, source=R3, destination=R1, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L30=Link(env=env, source=R4, destination=R2, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L40=Link(env=env, source=R4, destination=R3, delay=10, rate=10, buffer_capacity=64*PACKET_SIZE)
    L50=Link(env=env, source=H2, destination=R4, delay=10, rate=12.5, buffer_capacity=64*PACKET_SIZE)

    
    all_host_ip_address = ["0","1"]

    H1.link=L0
    H2.link=L50

    R1.links.append(L1)
    R1.links.append(L2)
    R1.links.append(L00)
    R1.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)

    R4.links.append(L5)
    R4.links.append(L30)
    R4.links.append(L40)
    R4.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)

    R2.links.append(L3)
    R2.links.append(L10)
    R2.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)
    R3.links.append(L4)
    R3.links.append(L20)
    R3.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)    
    
    RoutingTableOutdated(env=env, delay=0, router=R1)
    RoutingTableOutdated(env=env, delay=0, router=R2)
    RoutingTableOutdated(env=env, delay=0, router=R3)
    RoutingTableOutdated(env=env, delay=0, router=R4)
   
    if DEBUG==True:
        env.run(1200)    
    else:
        env.run(50000)
           
    return env.now


def test_router_update():
    n=case1()
    return n

n=test_router_update()
print n
print "DONE"