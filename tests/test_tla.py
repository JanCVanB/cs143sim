from simpy import *
from cs143sim.actors import *
from cs143sim.events import *
from cs143sim.tla import *



def test_tla_stop_and_wait_basic():
    env=Environment()
    
    H1=Host(env=env, address="0")
    H2=Host(env=env, address="1")
    
    F1=Flow(env=env, source=H1, destination=H2, amount=10*1024*8)
    F1.tla=StopAndWait(env=env, flow=F1)
    H1.flows.append(F1)
    H2.flows.append(F1)
   
    FlowStart(env=env, delay=1, flow=F1)
    env.run()
    n=env.now
    assert n<150 and n>100
    
def test_tla_go_back_n_basic():
    env=Environment()
    
    H1=Host(env=env, address="0")
    H2=Host(env=env, address="1")
    
    F1=Flow(env=env, source=H1, destination=H2, amount=10*1024*8)
    F1.tla=GoBackN(env=env, flow=F1)
    H1.flows.append(F1)
    H2.flows.append(F1)
   
    FlowStart(env=env, delay=1, flow=F1)
    env.run()
    
    n=env.now

    assert n<75 and n>40

test_tla_stop_and_wait_basic()
test_tla_go_back_n_basic()
