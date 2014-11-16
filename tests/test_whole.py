from cs143sim.simulation import *
from cs143sim.events import full_string
def test_whole():
	controller=Controller("../cs143sim/cases/case1_newformat.txt")

	for x in controller.hosts.values():
		print x.flows

	controller.run(2000)
	
test_whole()