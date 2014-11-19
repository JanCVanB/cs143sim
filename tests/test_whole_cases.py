from cs143sim.simulation import Controller
from cs143sim.constants import DEBUG

def run_case(case_number, until):
    controller_ = Controller(case='../cs143sim/cases/case' + str(case_number) + '.txt')
    controller_.run(until=until)
    
    print 'Done'

def test_case_0():
    if DEBUG==False:
        run_case(case_number=0, until=100000)
    else:
        run_case(case_number=0, until=8000)


def test_case_1():
    if DEBUG==False:
        run_case(case_number=1, until=100000)
    else:
        run_case(case_number=1, until=2000)

test_case_1()