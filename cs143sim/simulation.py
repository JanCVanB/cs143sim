"""
This module contains the simulation setup and execution.

.. autosummary:

    Controller

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""


from csv import reader

from simpy.core import Environment

from cs143sim.actors import Flow
from cs143sim.actors import Host
from cs143sim.actors import Link
from cs143sim.actors import Router
from cs143sim.constants import DEBUG
from cs143sim.events import FlowStart


class Controller:
    """Controller that prepares, starts, and cleans up a run of the simulation

    :param str case: path to simulation input file
    :ivar env: SimPy simulation :class:`~simpy.core.Environment`
    :ivar dict flows: all :class:`Flows <.Flow>` in the simulation
    :ivar dict hosts: all :class:`Hosts <.Host>` in the simulation
    :ivar dict links: all :class:`Links <.Link>` in the simulation
    :ivar dict routers: all :class:`Routers <.Router>` in the simulation
    """

    def __init__(self, case='cs143sim/cases/case0.csv'):
        self.env = Environment()
        self.flows = {}
        self.hosts = {}
        self.links = {}
        self.routers = {}
        self.read_case(case)

    def make_flow(self, name, source, destination, amount, start_time):
        """Make a new :class:`.Flow` and add it to `self.flows`

        :param str name: new :class:`.Flow` name
        :param source: source :class:`.Host`
        :param destination: destination :class:`.Host`
        :param int amount: amount of data to transfer, in bits
        :param float start_time: time the new :class:`.Flow` starts
        """
        new_flow = Flow(source=source, destination=destination, amount=amount)
        source.flows.append(new_flow)
        destination.flows.append(new_flow)
        self.flows[name] = new_flow
        FlowStart(env=self.env, delay=start_time, flow=new_flow)

    def make_host(self, name):
        """Make a new :class:`.Host` and add it to `self.hosts`

        :param str name: new :class:`.Host` name
        """
        address = name + ' address'  # TODO: implement IP addresses
        new_host = Host(address=address)
        self.hosts[name] = new_host

    def make_link(self, name, source, destination, rate, delay, buffer_capacity):
        """Make a new :class:`.Host` and add it to `self.hosts`

        :param str name: new :class:`.Link` name
        :param source: source :class:`.Host` or :class:`.Router`
        :param destination: destination :class:`.Host` or :class:`.Router`
        :param float rate: rate of data transfer, in Mbps
        :param float delay: delay for data transfer, in ms
        :param int buffer_capacity: size of receiver :class:`.Buffer`, in KB
        """
        new_link = Link(source=source, destination=destination, delay=delay,
                        rate=rate, buffer_capacity=buffer_capacity)
        for actor in (source, destination):
            if isinstance(actor, Host):
                actor.link = new_link
            elif isinstance(actor, Router):
                actor.links.append(new_link)
        self.links[name] = new_link

    def make_router(self, name):
        """Make a new :class:`.Router` and add it to `self.routers`

        :param str name: new :class:`.Router` name
        """
        address = name + ' address'  # TODO: implement IP addresses
        new_router = Router(address=address)
        self.routers[name] = new_router

    def read_case(self, case):
        """Read input file at path `case` and create actors and events

        :param str case: path to simulation input file
        """
        with open(case, 'rb') as case_file:
            case_reader = reader(case_file)
            for case_line in case_reader:
                if not case_line:
                    continue
                actor_name = case_line[0]
                if 'F' in actor_name:
                    source_name, destination_name = case_line[1:3]
                    amount = int(case_line[3])
                    start_time = float(case_line[4])
                    for host_name in (source_name, destination_name):
                        if host_name not in self.hosts:
                            if DEBUG:
                                print 'Creating', host_name
                            self.make_host(name=host_name)
                    source = self.hosts[source_name]
                    destination = self.hosts[destination_name]
                    if DEBUG:
                        print 'Creating', actor_name
                    self.make_flow(name=actor_name, source=source,
                                   destination=destination, amount=amount,
                                   start_time=start_time)
                elif 'L' in actor_name:
                    source_name, destination_name = case_line[1:3]
                    rate = float(case_line[3])
                    delay = float(case_line[4])
                    buffer_capacity = int(case_line[5])
                    for host_or_router_name in (source_name, destination_name):
                        if (host_or_router_name not in self.hosts and
                                host_or_router_name not in self.routers):
                            if DEBUG:
                                print 'Creating', host_or_router_name
                            if 'H' in host_or_router_name:
                                self.make_host(name=host_or_router_name)
                            elif 'R' in host_or_router_name:
                                self.make_router(name=host_or_router_name)
                    source = self.hosts[source_name]
                    destination = self.hosts[destination_name]
                    if DEBUG:
                        print 'Creating', actor_name
                    self.make_link(name=actor_name, source=source,
                                   destination=destination, rate=rate,
                                   delay=delay, buffer_capacity=buffer_capacity)

    def run(self, until=None):
        """Run the simulation for a specified duration

        :param float until: simulation duration
        """
        self.env.run(until=until)
