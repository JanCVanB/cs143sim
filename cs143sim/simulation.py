"""
This module contains the simulation setup and execution.

.. autosummary:

    Controller

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""


from simpy.core import Environment

from cs143sim.actors import Flow
from cs143sim.actors import Host
from cs143sim.actors import Link
from cs143sim.actors import Router
from cs143sim.constants import DEBUG
from cs143sim.events import FlowStart


class MissingAttribute(Exception):
    """
    MissingAttribute is an `Exception` designed to notify the user that the input file is missing information
    """
    def __init__(self, obj_type, obj_id, missing_attr):
        self.obj_type = obj_type
        self.obj_id = obj_id
        self.missing_attr = missing_attr

    def __str__(self):
        return 'I/O Error: Type ' + self.obj_type + ' (ID: ' + self.obj_id + ') is missing attribute ' + \
               self.missing_attr


class InputFileSyntaxError(Exception):
    """
    InputFileSyntaxError is an `Exception` thrown when an unrecognized syntax is used in
    the input file.
    """
    def __init__(self, line_number, message):
        self.line_number = line_number
        self.message = message

    def __str__(self):
        return 'Input File Syntax Error: (Line ' + str(self.line_number) + ') ' + self.message


class InputFileUnknownReference(Exception):
    """
    InputFileUnknownReference is an `Exception` thrown when a link or host makes reference
    to an unknown object (Host/Router/Link)
    """
    def __init__(self, line_number, message):
        self.line_number = line_number
        self.message = message

    def __str__(self):
        return 'InputFileUnknownReference (Line ' + str(self.line_number) + '): ' + self.message


class Controller:
    """Controller that prepares, starts, and cleans up a run of the simulation

    :param str case: path to simulation input file
    :ivar env: SimPy simulation :class:`~simpy.core.Environment`
    :ivar dict flows: all :class:`Flows <.Flow>` in the simulation
    :ivar dict hosts: all :class:`Hosts <.Host>` in the simulation
    :ivar dict links: all :class:`Links <.Link>` in the simulation
    :ivar dict routers: all :class:`Routers <.Router>` in the simulation
    """

    def __init__(self, case='cs143sim/cases/case0_newformat.txt'):
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

    def make_host(self, name, ip_address):
        """Make a new :class:`.Host` and add it to `self.hosts`

        :param str name: new :class:`.Host` name
        :param str ip_address: new :class:`.Host`'s IP address
        """
        new_host = Host(address=ip_address)
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
            else:
                raise Exception('Unknown Source/Destination: ' + actor)
        self.links[name] = new_link

    def make_router(self, name, ip_address):
        """Make a new :class:`.Router` and add it to `self.routers`

        :param str name: new :class:`.Router` name
        :param str ip_address: new :class:`.Router`'s IP Address
        """
        new_router = Router(address=ip_address)
        self.routers[name] = new_router

    def read_case(self, case):
        """Read input file at path `case` and create actors (and events?) accordingly

        :param str case: path to simulation input file
        """
        with open(case, 'rb') as case_file:
            # Open the file for line-by-line consumption
            obj_type = ''  # obj_type holds the current object type (LINK/HOST/Etc) to which attributes apply
            obj_id = ''    # obj_id is the current ID of the object
            # These are "simple" attributes that have only 1 argument.
            # Not included in this list is the CONNECTS attribute, which has 2 arguments,
            #   and ID, which requires special processing.
            attributes = ('RATE', 'DELAY', 'DATA', 'BUFFER', 'DST', 'SRC', 'START', 'IP')
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
                        # make sure we have all the attributes available, then create the link object
                        for attribute in ['BUFFER', 'DELAY', 'RATE', 'SRC', 'DST']:
                            if store_in[attribute] in ['', []]:
                                # Make sure all the attributes are not empty
                                raise MissingAttribute(obj_type, obj_id, attribute)
                        # If all the attributes are present, create the object
                        if DEBUG:
                            print 'Making Link: ' + obj_id
                        the_src = ''  # temporary variables that will point to the actual src/dst instances
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
                                raise InputFileUnknownReference(line_number, target + ' is not a valid Host/Router.')
                        self.make_link(obj_id, the_src, the_dst, float(store_in['RATE']),
                                       float(store_in['DELAY']), int(store_in['BUFFER']))
                    elif obj_type == 'HOST':
                        # check the attribute(s) (there's only one for HOSTS so far: IP)
                        for attribute in ['IP']:
                            if store_in[attribute] in ['', []]:
                                # Make sure all the attributes are not empty
                                raise MissingAttribute(obj_type, obj_id, attribute)
                        if DEBUG:
                            print 'Making host: ' + obj_id
                        self.make_host(obj_id, store_in['IP'])

                    elif obj_type == 'ROUTER':
                        # check the attribute(s) (only one so far: IP)
                        # TODO: Add router update-routing-tables value to attributes
                        for attribute in ['IP']:
                            if store_in[attribute] in ['', []]:
                                raise MissingAttribute(obj_type, obj_id, attribute)
                        if DEBUG:
                            print 'Making Router: ' + obj_id
                        self.make_router(obj_id, store_in['IP'])

                    elif obj_type == 'FLOW':
                        # TODO: Specify congestion control algorithm as attribute
                        for attribute in ['SRC', 'DST', 'START', 'DATA']:
                            if store_in[attribute] in ['', []]:
                                raise MissingAttribute(obj_type, obj_id, attribute)
                        # if all the attributes are there, lets go ahead and create the flow
                        # BUT FIRST, we need to make sure the SRC/DST hosts actually exist..
                        # if they don't, warn the user that "No, i'm sorry, you have to specify
                        # hosts that actually exist."
                        if DEBUG:
                            print 'Making Flow: ' + obj_id
                        try:
                            self.make_flow(obj_id, self.hosts[store_in['SRC']], self.hosts[store_in['DST']],
                                           int(store_in['DATA']), float(store_in['START']))
                        except KeyError as e:
                            raise InputFileUnknownReference(line_number,
                                                            'Input File Formatting Error: ' +
                                                            'Reference to unknown object: ' + repr(e))

                    else:
                        # Unexpected ID attribute (out of context of an object Type)
                        raise InputFileSyntaxError(line_number, 'Unexpected "ID" attribute.')
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
                        raise InputFileSyntaxError(line_number,
                                                   'Input File Formatting Error: CONNECTS attribute ' +
                                                   'formatted incorrectly.\nExpects: CONNECTS A B')
                else:
                    raise InputFileSyntaxError(line_number, 'Unrecognized keyword: ' + keyword)

    def run(self, until=None):
        """Run the simulation for a specified duration

        :param float until: simulation duration
        """
        self.env.run(until=until)
