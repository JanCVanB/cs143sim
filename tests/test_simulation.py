from cs143sim.simulation import Controller


def basic_controller():
    return Controller()


def controller_run_basic():
    controller_ = basic_controller()
    controller_.run()


def test_controller():
    controller_run_basic()
