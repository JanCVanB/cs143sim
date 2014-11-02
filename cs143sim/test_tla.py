from actors import *
from simpy import *
from events import *

import global_vars


H1=Host(env=global_vars.env, address="0")
H2=Host(env=global_vars.env, address="1")

F1=Flow(env=global_vars.env, source=H1, destination=H2, amount=5*1024*8)
H1.flows.append(F1)
H2.flows.append(F1)



FlowStart(env=global_vars.env, delay=1, flow=F1)
global_vars.env.run()

