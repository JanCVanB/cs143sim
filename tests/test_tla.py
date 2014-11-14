from simpy import *
from cs143sim.actors import *
from cs143sim.events import *
from cs143sim.tla import *
from cs143sim.constants import *





def test_tla_tcp_tahoe():
    env=Environment()
    
    H1=Host(env=env, address="0")
    H2=Host(env=env, address="1")
    
    F1=Flow(env=env, source=H1, destination=H2, amount=20*1024*PACKET_SIZE-10)
    F1.tla=TCPTahoe(env=env, flow=F1, recorder="L1_record.txt")
    
    F2=Flow(env=env, source=H2, destination=H1, amount=20*1024*PACKET_SIZE-10)
    F2.tla=TCPTahoe(env=env, flow=F2, recorder="L2_record.txt")
    
    H1.flows.append(F1)
    H2.flows.append(F1)
    H1.flows.append(F2)
    H2.flows.append(F2)
    
    L1=Link(env=env, source=H1, destination=H2, delay=10, rate=0, buffer_capacity=64*PACKET_SIZE)
    L2=Link(env=env, source=H2, destination=H1, delay=10, rate=0, buffer_capacity=64*PACKET_SIZE)

    H1.link=L1
    H2.link=L2
    
    FlowStart(env=env, delay=0, flow=F1)
    FlowStart(env=env, delay=1000, flow=F2)
    
    if DEBUG==True:
        env.run(1200)    
    else:
        env.run(50000)
           
    return env.now

#test_tla_stop_and_wait_basic()
#test_tla_go_back_n_basic()
#test_tla_fast_retransmit_basic()
n=test_tla_tcp_tahoe()
print n
print "DONE"