"""This module contains the simulation setup and execution.

.. autosummary:

    ControlledEnvironment
    Controller

.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
from simpy.core import Environment

from cs143sim.actors import Flow
from cs143sim.actors import Host
from cs143sim.actors import Link
from cs143sim.actors import Router
from cs143sim.constants import OUTPUT_BUFFER_OCCUPANCY_SCALE_FACTOR
from cs143sim.constants import OUTPUT_FLOW_RATE_SCALE_FACTOR
from cs143sim.constants import OUTPUT_LINK_RATE_SCALE_FACTOR
from cs143sim.constants import INPUT_FILE_RATE_SCALE_FACTOR
from cs143sim.constants import INPUT_FILE_BUFFER_SCALE_FACTOR
from cs143sim.constants import INPUT_FILE_DATA_SCALE_FACTOR
from cs143sim.constants import INPUT_FILE_TIME_SCALE_FACTOR
from cs143sim.constants import INPUT_FILE_DELAY_SCALE_FACTOR
from cs143sim.constants import INPUT_FILE_UPDATE_SCALE_FACTOR
from cs143sim.constants import GENERATE_ROUTER_PACKET_DEFAULT_INTERVAL
from cs143sim.errors import InputFileSyntaxError
from cs143sim.errors import InputFileUnknownReference
from cs143sim.errors import MissingAttribute
from cs143sim.events import FlowStart, RoutingTableOutdated


class ControlledEnvironment(Environment):
    """SimPy :class:`~simpy.core.Environment` with a reference to its
    :class:`.Controller`

    :param controller: :class:`.Controller` that created the
        :class:`~simpy.core.Environment`
    """
    def __init__(self, controller):
        super(ControlledEnvironment, self).__init__()
        self.controller = controller


class Controller:
    """Controller that prepares, starts, and cleans up a run of the simulation

    :param str case: path to simulation input file
    :ivar env: SimPy simulation :class:`~simpy.core.Environment`
    :ivar dict flows: all :class:`Flows <.Flow>` in the simulation
    :ivar dict hosts: all :class:`Hosts <.Host>` in the simulation
    :ivar dict links: all :class:`Links <.Link>` in the simulation
    :ivar dict routers: all :class:`Routers <.Router>` in the simulation
    :ivar dict buffer_occupancy: buffer occupancy records for each link;
        :class:`Links <.Link>` key to lists of (time, value) tuples
    :ivar dict flow_rate: flow rate records for each flow;
        :class:`Flows <.Flow>` key to lists of (time, value) tuples
    :ivar dict link_rate: link rate records for each link;
        :class:`Links <.Link>` key to lists of (time, value) tuples
    :ivar dict packet_delay: packet delay records for each flow;
        :class:`Flows <.Flow>` key to lists of (time, value) tuples
    :ivar dict packet_loss: packet loss records for each link;
        :class:`Links <.Link>` key to lists of (time, value) tuples
    :ivar dict window_size: window size records for each flow;
        :class:`Flows <.Flow>` key to lists of (time, value) tuples
    """
    def __init__(self, case='cs143sim/cases/case0.txt'):
        self.env = ControlledEnvironment(controller=self)
        self.flows = {}
        self.hosts = {}
        self.links = {}
        self.routers = {}
        self.buffer_occupancy = {}
        self.flow_rate = {}
        self.link_rate = {}
        self.packet_delay = {}
        self.packet_loss = {}
        self.window_size = {}
        self.algorithm = 0  # default algorithm is specified by
        self.read_case(case)

    def make_flow(self, name, source, destination, amount, start_time, algorithm):
        """Make a new :class:`.Flow` and add it to `self.flows`

        :param str name: new :class:`.Flow` name
        :param source: source :class:`.Host`
        :param destination: destination :class:`.Host`
        :param int amount: amount of data to transfer, in bits
        :param float start_time: time the new :class:`.Flow` starts
        """
        new_flow = Flow(env=self.env, source=source, destination=destination,
                        amount=amount, algorithm=algorithm)
        source.flows.append(new_flow)
        destination.flows.append(new_flow)
        self.flows[name] = new_flow
        self.algorithm = algorithm
        FlowStart(env=self.env, delay=start_time, flow=new_flow)

    def make_host(self, name, ip_address):
        """Make a new :class:`.Host` and add it to `self.hosts`

        :param str name: new :class:`.Host` name
        :param str ip_address: new :class:`.Host`'s IP address
        """
        new_host = Host(env=self.env, address=ip_address)
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
        new_link = Link(env=self.env, source=source, destination=destination,
                        delay=delay, rate=rate, buffer_capacity=buffer_capacity)
        # NOTE: Each link is split into two links (one for each direction) in the read_case function
        #       and appended with 'a' or 'b' on its ID. (e.g. 'L1' becomes 'L1a' and 'L1b')
        actor = source
        if isinstance(actor, Host):
            actor.link = new_link
        elif isinstance(actor, Router):
            actor.links.append(new_link)
        else:
            raise Exception('Unknown Source/Destination: ' + actor)
        self.links[name] = new_link

    def make_router(self, name, ip_address, update_time):
        """Make a new :class:`.Router` and add it to `self.routers`

        :param str name: new :class:`.Router` name
        :param str ip_address: new :class:`.Router`'s IP Address
        """
        new_router = Router(env=self.env, address=ip_address, update_time=int(update_time))
        self.routers[name] = new_router
        RoutingTableOutdated(env=self.env, delay=0, router=new_router)

    def read_case(self, case):
        """Read input file at path `case` and create actors accordingly

        :param str case: path to simulation input file
        """
        with open(case, 'rb') as case_file:
            # Open the file for line-by-line consumption
            obj_type = ''  # obj_type holds the current object type (LINK/HOST/Etc)
                           # to which attributes apply
            obj_id = ''    # obj_id is the current ID of the object
            # These are "simple" attributes that have only 1 argument.
            # Not included in this list is the CONNECTS attribute, which has 2 arguments,
            #   and ID, which requires special processing.
            attributes = ('RATE', 'DELAY', 'DATA', 'BUFFER', 'DST', 'SRC', 'START', 'IP', 'ALGORITHM', 'UPDATE')
            # Input File Attributes:
            # RATE - belongs to a :class:`.Link`, specifies link rate in Mbps (float)
            # DELAY - belongs to a :class:`.Link`, specifies link delay in ms (int)
            # DATA - belongs to a :class:`.Flow`, specifies amount of data to be transmitted in MegaBytes (int)
            # BUFFER - belongs to a :class:`.Link`, specifies buffer size in KiloBytes (int)
            # DST - belongs to a :class:`.Link` or :class:`.Flow`, specifies a destination (ID of destination)
            # SRC - belongs to a :class:`.Link` or :class:`.Flow`, specifies a source (ID of source)
            # START - belongs to a :class:`.Flow`, specifies starting time for that flow in seconds (float)
            # IP - belongs to a :class:`.Router` or :class:`.Host`, specifies the IP address of the HOST or ROUTER (str)
            # ALGORITHM - belongs to a :class:`.Flow`, specifies the congestion control algorithm for that flow (int)
            # UPDATE - belongs to a :class:`.Router`, specifies the time between router table updates in ms (int)
            # CONNECTS - belongs to a :class:`.Link`, specifies two Hosts/Routers that are connected by that link (ID ID)
            # Note: most of the units above will be converted internally and apply only to the input file.
            store_in = {attribute: '' for attribute in attributes}  # initialize all attributes to ''
            line_number = 0
            for case_line in case_file:
                line_number += 1
                line_comp = case_line.split()
                if line_comp == [] and obj_id == '':
                    obj_id = ''  # clear obj_ID and type on empty line
                    obj_type = ''
                    continue
                try:
                    # if the line is empty, just set keyword to ''
                    keyword = line_comp[0].upper()
                except AttributeError:
                    keyword = ''
                except IndexError:
                    keyword = ''
                if keyword == '//':
                    continue  # ignore the comment line in the file
                elif keyword in ['HOST', 'ROUTER', 'LINK', 'FLOW']:
                    # if we have a valid obj type, listen for new object attributes
                    obj_type = keyword
                    obj_id = ''
                elif keyword in attributes:
                    # store simple attributes in their place in the store_in dictionary
                    store_in[keyword] = line_comp[1]

                elif keyword == 'ID' or (keyword == '' and obj_id != ''):
                    # if we get a new ID attr (and already were working with another ID attr)
                    # OR if we read an empty line and there was an ID we were working with
                    # THEN
                    # create the object in the simulation, and start a new ID
                    if obj_id == '':
                        obj_id = line_comp[1].upper()
                    elif obj_type == 'LINK':
                        # if we're getting an additional ID attribute on a LINK
                        # make sure we have all the attributes available,
                        # then create the link object
                        for attribute in ['BUFFER', 'DELAY', 'RATE', 'SRC', 'DST']:
                            if store_in[attribute] in ['', []]:
                                # Make sure all the attributes are not empty
                                raise MissingAttribute(obj_type=obj_type, obj_id=obj_id,
                                                       missing_attr=attribute)
                        # If all the attributes are present, create the object
                        the_src = ''  # temp variables that will point to src/dst instances
                        the_dst = ''
                        # Enforce referential integrity (aka check that the specified
                        # hosts/routers actually exist in the simulation)
                        for target in [store_in['SRC'], store_in['DST']]:
                            print 'Checking: ' + target
                            if target in self.hosts:
                                if the_src == '':
                                    the_src = self.hosts[target]
                                else:
                                    the_dst = self.hosts[target]
                            elif target in self.routers:
                                if the_src == '':
                                    the_src = self.routers[target]
                                else:
                                    the_dst = self.routers[target]
                            else:
                                raise InputFileUnknownReference(line_number, target +
                                                                ' is not a valid Host/Router.')
                        self.make_link(name=obj_id + 'a', source=the_src, destination=the_dst,
                                       rate=float(store_in['RATE']) * INPUT_FILE_RATE_SCALE_FACTOR,
                                       delay=float(store_in['DELAY']) * INPUT_FILE_DELAY_SCALE_FACTOR,
                                       buffer_capacity=int(store_in['BUFFER']) * INPUT_FILE_BUFFER_SCALE_FACTOR)

                        # Links are split into two, one for each direction (so that they are full-duplex).
                        self.make_link(name=obj_id + 'b', source=the_dst, destination=the_src,
                                       rate=float(store_in['RATE']) * INPUT_FILE_RATE_SCALE_FACTOR,
                                       delay=float(store_in['DELAY']) * INPUT_FILE_DELAY_SCALE_FACTOR,
                                       buffer_capacity=int(store_in['BUFFER']) * INPUT_FILE_BUFFER_SCALE_FACTOR)
                                       # convert into bits
                    elif obj_type == 'HOST':
                        # check the attribute(s) (there's only one for HOSTS so far: IP)
                        for attribute in ['IP']:
                            if store_in[attribute] in ['', []]:
                                # Make sure all the attributes are not empty
                                raise MissingAttribute(obj_type=obj_type, obj_id=obj_id,
                                                       missing_attr=attribute)
                        self.make_host(name=obj_id, ip_address=store_in['IP'])

                    elif obj_type == 'ROUTER':
                        # check the attribute(s) (only one so far: IP), UPDATE is not mandatory.
                        for attribute in ['IP', 'UPDATE']:
                            if store_in[attribute] in ['', []]:
                                if attribute == 'UPDATE':
                                    # Just set update to a default value
                                    store_in[attribute] = GENERATE_ROUTER_PACKET_DEFAULT_INTERVAL
                                else:
                                    raise MissingAttribute(obj_type=obj_type, obj_id=obj_id,
                                                           missing_attr=attribute)
                        self.make_router(name=obj_id, ip_address=store_in['IP'],
                                         update_time=store_in['UPDATE'] * INPUT_FILE_UPDATE_SCALE_FACTOR)

                    elif obj_type == 'FLOW':
                        for attribute in ['SRC', 'DST', 'START', 'DATA', 'ALGORITHM']:
                            if store_in[attribute] in ['', []]:
                                if attribute == 'ALGORITHM':
                                    store_in[attribute] = 0
                                else:
                                    raise MissingAttribute(obj_type=obj_type, obj_id=obj_id,
                                                           missing_attr=attribute)
                        # if all the attributes are there, lets go ahead and create the flow
                        # BUT FIRST, we need to make sure the SRC/DST hosts actually exist..
                        # if they don't, warn the user that "No, i'm sorry, you have to specify
                        # hosts that actually exist."
                        try:
                            self.make_flow(name=obj_id, source=self.hosts[store_in['SRC']],
                                           destination=self.hosts[store_in['DST']],
                                           amount=int(store_in['DATA']) * INPUT_FILE_DATA_SCALE_FACTOR,
                                           start_time=float(store_in['START']) * INPUT_FILE_TIME_SCALE_FACTOR,
                                           algorithm=int(store_in['ALGORITHM']))

                        except KeyError as e:
                            raise InputFileUnknownReference(line_number=line_number,
                                                            message='Input File Formatting Error: ' +
                                                            'Reference to unknown object: ' + repr(e))
                    else:
                        # Unexpected ID attribute (out of context of an object Type)
                        raise InputFileSyntaxError(line_number=line_number,
                                                   message='Unexpected "ID" attribute.')
                    if keyword == 'ID':
                        obj_id = line_comp[1].upper()
                    else:
                        obj_id = ''
                        obj_type = ''
                elif keyword == 'CONNECTS':
                    if obj_type == 'LINK':
                        store_in['SRC'] = line_comp[1].upper()
                        store_in['DST'] = line_comp[2].upper()
                    else:
                        raise InputFileSyntaxError(line_number=line_number,
                                                   message='Input File Formatting Error: ' +
                                                           'CONNECTS attribute formatted incorrectly.\n' +
                                                           'Expects: CONNECTS A B')
                else:
                    raise InputFileSyntaxError(line_number=line_number,
                                               message='Unrecognized keyword: ' + keyword)
        all_host_ip_addresses = [host.address for host in self.hosts.values()]
        assert len(all_host_ip_addresses) > 0
        for router in self.routers.values():
            router.initialize_routing_table(all_host_ip_addresses=all_host_ip_addresses)

    def record(self, recorder, actor, value):
        """Record the time and `value` in the recorder keyed by the `actor`

        :param dict recorder: recorder to record the change
        :param actor: :class:`.Actor` that experienced the change
        :param value: new value of changed quantity
        """
        entry = (self.env.now, value)
        try:
            recorder[actor].append(entry)
        except KeyError:
            recorder[actor] = [entry]

    def record_buffer_occupancy(self, link, buffer_occupancy):
        """Record the occupancy of a link buffer

        :param link: :class:`.Link` changing its buffer occupancy
        :param float buffer_occupancy: new buffer occupancy (bytes)
        """
        self.record(recorder=self.buffer_occupancy, actor=link,
                    value=buffer_occupancy * OUTPUT_BUFFER_OCCUPANCY_SCALE_FACTOR)

    def record_flow_rate(self, flow, packet_size):
        """Record the size of a delivered packet

        :param flow: :class:`.Flow` to which the delivered packet belongs
        :param float packet_size: size of the delivered packet (bits)
        """
        self.record(recorder=self.flow_rate, actor=flow,
                    value=packet_size * OUTPUT_FLOW_RATE_SCALE_FACTOR)

    def record_link_rate(self, link, send_duration):
        """Record the duration a link sends a packet

        :param link: :class:`.Link` sending the packet
        :param float send_duration: duration required to send the packet (ms)
        """
        self.record(recorder=self.link_rate, actor=link,
                    value=send_duration * OUTPUT_LINK_RATE_SCALE_FACTOR)

    def record_packet_delay(self, flow, packet_delay):
        """Record the delay of a delivered packet

        :param flow: :class:`.Flow` to which the delivered packet belongs
        :param int packet_delay: time since the delivered packet was sent (ms)
        """
        self.record(recorder=self.packet_delay, actor=flow, value=packet_delay)

    def record_packet_loss(self, link):
        """Record a packet loss

        :param link: :class:`.Link` that dropped the packet
        """
        self.record(recorder=self.packet_loss, actor=link, value=None)

    def record_window_size(self, flow, window_size):
        """Record the flow's window size

        :param flow: :class:`.Flow` changing its window size
        :param int window_size: new window size
        """
        self.record(recorder=self.window_size, actor=flow, value=window_size)

    def run(self, until=None):
        """Run the simulation for a specified duration

        :param float until: simulation duration
        """
        self.env.run(until=until)
