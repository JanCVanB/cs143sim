from actors import *
from simpy import *
from events import *


def test_tla_basic():
    env=Environment()
    
    H1=Host(env=env, address="0")
    H2=Host(env=env, address="1")
    
    F1=Flow(env=env, source=H1, destination=H2, amount=10*1024*8)
    H1.flows.append(F1)
    H2.flows.append(F1)
   
    FlowStart(env=env, delay=1, flow=F1)
    env.run(200)

test_tla_basic()