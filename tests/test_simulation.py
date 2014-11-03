from cs143sim.simulation import Controller
from test_actors import basic_flow
from test_actors import basic_link


def basic_controller():
    return Controller()


def controller_record_buffer_occupancy():
    controller_ = basic_controller()
    link = basic_link()
    controller_.buffer_occupancy[link] = []
    buffer_occupancies = list(range(5))
    for buffer_occupancy in buffer_occupancies:
        controller_.record_buffer_occupancy(link=link,
                                            buffer_occupancy=buffer_occupancy)
    recorded_buffer_occupancies = [record[1] for record in
                                   controller_.buffer_occupancy[link]]
    assert recorded_buffer_occupancies == buffer_occupancies


def controller_record_flow_rate():
    controller_ = basic_controller()
    flow = basic_flow()
    controller_.flow_rate[flow] = []
    flow_rates = list(range(5))
    for flow_rate in flow_rates:
        controller_.record_flow_rate(flow=flow, flow_rate=flow_rate)
    recorded_flow_rates = [record[1] for record in controller_.flow_rate[flow]]
    assert recorded_flow_rates == flow_rates


def controller_record_link_rate():
    controller_ = basic_controller()
    link = basic_link()
    controller_.link_rate[link] = []
    link_rates = list(range(5))
    for link_rate in link_rates:
        controller_.record_link_rate(link=link, link_rate=link_rate)
    recorded_link_rates = [record[1] for record in controller_.link_rate[link]]
    assert recorded_link_rates == link_rates


def controller_record_packet_delay():
    controller_ = basic_controller()
    flow = basic_flow()
    controller_.packet_delay[flow] = []
    packet_delays = list(range(5))
    for packet_delay in packet_delays:
        controller_.record_packet_delay(flow=flow, packet_delay=packet_delay)
    recorded_packet_delays = [record[1] for record in
                              controller_.packet_delay[flow]]
    assert recorded_packet_delays == packet_delays


def controller_record_packet_loss():
    # TODO: determine packet loss metric
    pass


def controller_record_window_size():
    controller_ = basic_controller()
    flow = basic_flow()
    controller_.window_size[flow] = []
    window_sizes = list(range(5))
    for window_size in window_sizes:
        controller_.record_window_size(flow=flow, window_size=window_size)
    recorded_window_sizes = [record[1] for record in
                             controller_.window_size[flow]]
    assert recorded_window_sizes == window_sizes


def controller_run_basic():
    controller_ = basic_controller()
    controller_.run()


def test_controller():
    controller_run_basic()
    controller_record_buffer_occupancy()
    controller_record_flow_rate()
    controller_record_link_rate()
    controller_record_packet_delay()
    controller_record_packet_loss()
    controller_record_window_size()
