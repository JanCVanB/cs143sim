from actors import *
from simpy import *
from events import *

import global_vars


H1=Host("0")
H2=Host("1")

F1=Flow(H1,H2,1*1024*8)
H1.flows.append(F1)
H2.flows.append(F1)



FlowStart(env=global_vars.env, delay=1, flow=F1)
global_vars.env.run()

