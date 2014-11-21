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


def case2():
    env=Environment()
    
    S1=Host(env=env, address="S1")
    S2=Host(env=env, address="S2")
    S3=Host(env=env, address="S3")
    T1=Host(env=env, address="T1")
    T2=Host(env=env, address="T2")
    T3=Host(env=env, address="T3")

    R1=Router(env=env, address="R1")
    R2=Router(env=env, address="R2")
    R3=Router(env=env, address="R3")
    R4=Router(env=env, address="R4")
    
    
    L1=Link(env=env, source=R1, destination=R2, delay=10, rate=10, buffer_capacity=128*PACKET_SIZE)
    L2=Link(env=env, source=R2, destination=R3, delay=10, rate=10, buffer_capacity=128*PACKET_SIZE)
    L3=Link(env=env, source=R3, destination=R4, delay=10, rate=10, buffer_capacity=128*PACKET_SIZE)
    L_S1=Link(env=env, source=S1, destination=R1, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_S2=Link(env=env, source=S2, destination=R1, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_S3=Link(env=env, source=S3, destination=R3, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_T1=Link(env=env, source=T1, destination=R4, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_T2=Link(env=env, source=T2, destination=R2, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_T3=Link(env=env, source=T3, destination=R4, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)

    L10=Link(env=env, source=R2, destination=R1, delay=10, rate=10, buffer_capacity=128*PACKET_SIZE)
    L20=Link(env=env, source=R3, destination=R2, delay=10, rate=10, buffer_capacity=128*PACKET_SIZE)
    L30=Link(env=env, source=R4, destination=R3, delay=10, rate=10, buffer_capacity=128*PACKET_SIZE)
    L_S10=Link(env=env, source=R1, destination=S1, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_S20=Link(env=env, source=R1, destination=S2, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_S30=Link(env=env, source=R3, destination=S3, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_T10=Link(env=env, source=R4, destination=T1, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_T20=Link(env=env, source=R2, destination=T2, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)
    L_T30=Link(env=env, source=R4, destination=T3, delay=10, rate=12.5, buffer_capacity=128*PACKET_SIZE)

    
    all_host_ip_address = ["S1","S2","S3","T1","T2","T3"]

    S1.link=L_S1
    S2.link=L_S2
    S3.link=L_S3
    T1.link=L_T1
    T2.link=L_T2
    T3.link=L_T3

    R1.links.append(L1)
    R1.links.append(L_S10)
    R1.links.append(L_S20)
    R1.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)

    R4.links.append(L_T10)
    R4.links.append(L30)
    R4.links.append(L_T30)
    R4.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)

    R2.links.append(L2)
    R2.links.append(L10)
    R2.links.append(L_T20)
    R2.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)
    
    R3.links.append(L3)
    R3.links.append(L20)
    R3.links.append(L_S30)
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
    n=case2()
    return n

n=test_router_update()
print n
print "DONE"