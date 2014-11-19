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

    #L0A is an in link, while L0B is an out link
    L0A=Link(env=env, source=H1, destination=R1, delay=10, rate=12.5*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L1A=Link(env=env, source=R1, destination=R2, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L2A=Link(env=env, source=R1, destination=R3, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L3A=Link(env=env, source=R2, destination=R4, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L4A=Link(env=env, source=R3, destination=R4, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L5A=Link(env=env, source=R4, destination=H2, delay=10, rate=12.5*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)

    L0B=Link(env=env, source=R1, destination=H1, delay=10, rate=12.5*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L1B=Link(env=env, source=R2, destination=R1, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L2B=Link(env=env, source=R3, destination=R1, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L3B=Link(env=env, source=R4, destination=R2, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L4B=Link(env=env, source=R4, destination=R3, delay=10, rate=10*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)
    L5B=Link(env=env, source=H2, destination=R4, delay=10, rate=12.5*1024*1024/1000, buffer_capacity=64*PACKET_SIZE)

    
    all_host_ip_address = ["0","1"]

    H1.link=L0A
    H2.link=L5B

    R1.links.append(L1A)
    R1.links.append(L2A)
    R1.links.append(L0B)
    R1.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)

    R4.links.append(L5A)
    R4.links.append(L3B)
    R4.links.append(L4B)
    R4.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)

    R2.links.append(L3A)
    R2.links.append(L1B)
    R2.initialize_routing_table(all_host_ip_addresses = all_host_ip_address)
    R3.links.append(L4A)
    R3.links.append(L2B)


#    R1.initialize_routing_table(all_host_ip_addresses = all_host_ip_address) 
#    R2.initialize_routing_table(all_host_ip_addresses = all_host_ip_address) 
#    R3.initialize_routing_table(all_host_ip_addresses = all_host_ip_address) 
#    R4.initialize_routing_table(all_host_ip_addresses = all_host_ip_address) 

#    R1.table = {}
    R1.table[H1] = 1, H1
    R1.table[H2] = 3, R2
    R1.table[R2] = 1, R2
    R1.table[R3] = 1, R3
    R1.table[R4] = 2, R2

#    R2.table = {}
    R2.table[H1] = 2, R1
    R2.table[H2] = 2, R4
    R2.table[R1] = 1, R1
    R2.table[R3] = 2, R1
    R2.table[R4] = 1, R4

#    R3.table = {}
    R3.table[H1] = 2, R1
    R3.table[H2] = 2, R4
    R3.table[R1] = 1, R1
    R3.table[R2] = 2, R1
    R3.table[R4] = 1, R4

#    R4.table = {}
    R4.table[H1] = 3, R2
    R4.table[H2] = 1, H2
    R4.table[R1] = 2, R2
    R4.table[R2] = 1, R2
    R4.table[R3] = 1, R3

    F1=Flow(env=env, source=H1, destination=H2, amount=128*PACKET_SIZE-10)
    F1.tla=TCPTahoe(env=env, flow=F1, recorder="L_record.txt")

    H1.flows.append(F1)
    H2.flows.append(F1)

    rate=10.0*1024*1024/1000;
#   L1=Link(env=env, source=H1, destination=H2, delay=10, rate=rate, buffer_capacity=64*PACKET_SIZE)
#    L2=Link(env=env, source=H2, destination=H1, delay=10, rate=rate, buffer_capacity=64*PACKET_SIZE)

#    H1.link=L1
#    H2.link=L2
    
    FlowStart(env=env, delay=0, flow=F1)
#    TestPacket = DataPacket(env=env, number=0, acknowledgement=0, timestamp=0, source="0", destination="1")
#    H1.send(TestPacket)
    
    
#    RoutingTableOutdated(env=env, delay=0, router=R1)
#    RoutingTableOutdated(env=env, delay=0, router=R2)
#    RoutingTableOutdated(env=env, delay=0, router=R3)
#    RoutingTableOutdated(env=env, delay=0, router=R4)
   
    if DEBUG==True:
        env.run(400)    
    else:
        env.run(50000)
           
    return env.now


def test_router_update():
    n=case1()
    return n

n=test_router_update()
print n
print "DONE"
