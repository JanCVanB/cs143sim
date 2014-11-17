from cs143sim.simulation import Controller


def run_case(case_number, until):
    controller_ = Controller(case='../cs143sim/cases/case' + str(case_number) + '.txt')
    controller_.run(until=until)
    
    print 'Done'

def test_case_0():
    run_case(case_number=0, until=100000)


def test_case_1():
    run_case(case_number=1, until=100000)

test_case_0()