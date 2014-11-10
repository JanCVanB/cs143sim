"""
This module contains all actor definitions.

.. autosummary::

    Buffer
    Flow
    Host
    Link
    Packet
    Router

.. moduleauthor:: Lan Hongjian <lanhongjianlr@gmail.com>
.. moduleauthor:: Yamei Ou <oym111@gmail.com>
.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <neicullyn@gmail.com>
"""

from tla import *
from cs143sim.constants import PACKET_SIZE,GENERATE_ROUTERPACKET_TIME_INTEVAL
from cs143sim.events import PacketReceipt
from cs143sim.constants import *
from random import randint
from test.test_socketserver import receive




class Actor(object):
    """Representation of an actor

    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :ivar env: SimPy simulation :class:`~simpy.core.Environment`
    """
    def __init__(self, env):
        self.env = env


class Buffer(Actor):
    """Representation of a data storage container

    Buffers store data to be linked while :class:`.Link` is busy sending data.

    :param int capacity: maximum number of bits that can be stored
    :param link: :class:`.Link` containing this buffer
    :ivar int capacity: maximum number of bits that can be stored
    :ivar link: :class:`.Link` containing this buffer
    :ivar list packets: :class:`Packets <.Packet>` currently in storage
    """
    def __init__(self, env, capacity, link):
        super(Buffer, self).__init__(env=env)
        self.capacity = capacity
        self.link = link
        self.packets = []

    def add(self, packet):
        """
        Adds packet to `packets` if `capacity` will not be exceeded,
        drops packet if buffer if full.

        :param packet: :class:`.Packet` added to buffer.
        """
        current_level = sum(packet.size for packet in self.packets)
        if current_level + packet.size <= self.capacity:
            self.packets.append(packet)
        else:
            # The packet cannot be stored, so the packet is dropped
            self.env.controller.record_packet_loss(link=self.link)


class Flow(Actor):
    """Representation of a connection between access points

    Flows try to transmit data from :class:`.Host` to :class:`.Host`.

    :param source: source :class:`.Host`
    :param destination: destination :class:`.Host`
    :param float amount: amount of data to transmit
    :ivar source: source :class:`.Host`
    :ivar destination: destination :class:`.Host`
    :ivar float amount: amount of data to transmit
    
    
    Receiver
    :ivar rcv_expect_to_receive: next packet expect to receive
    :ivar rcv_received_packets:  list of packets that have been received, but not what we need now.
    """
    def __init__(self, env, source, destination, amount):
        super(Flow, self).__init__(env=env)
        self.source = source
        self.destination = destination
        self.amount = amount
        

        self.tla=GoBackN(env=self.env, flow=self)
        
        self.rcv_expect_to_receive=0;
        self.rcv_received_packets=list();

    def __str__(self):
        return ('Flow from ' + self.source.address +
                ' to ' + self.destination.address)

    def make_packet(self, packet_number):
        """
        Make a packet based on the packet number
        """

        packet=DataPacket(env=self.env, number=packet_number, 
                          acknowledgement=False, timestamp=self.env.now, 
                          source=self.source, destination=self.destination)

        return packet
        
    def make_ack_packet(self, packet):
        """
        Make a ack packet
        """
        """
        Go Back N version, compatible with stop and wait
        """
        n=packet.number
        if n< self.rcv_expect_to_receive:
            """
            This packet has been received before
            """
            pass
        elif n==self.rcv_expect_to_receive:
            """
            This packet is what we expect to receive
            """
            """
            Find out next packet expect to receive
            """
            self.rcv_expect_to_receive=self.rcv_expect_to_receive+1
            flag=True
            while flag:
                for x in self.rcv_received_packets:
                    if x==self.rcv_expect_to_receive:
                        self.rcv_expect_to_receive+=1
                        continue
                flag=False
        else:
            """
            This packet is not what we expect to receive
            """
            """
            Store it
            """
            self.rcv_received_packets.append(n)
        """
        using the timestamp of packet to be acked as the timestamp of ack packet
        to calculate RTT
        """
        ack_packet=DataPacket(env=self.env, number=self.rcv_expect_to_receive,
                              acknowledgement=True, timestamp=packet.timestamp, 
                              source=packet.destination, destination=packet.source)
        return ack_packet

    def send_packet(self, packet):
        """
        When possible, TLA use this method to send a packet
        """
        #self.source.send(packet)
        
        #to test ack and time out, there is a probability of 0.5 for the packet to be sent.
        r=randint(0,3)
#         if packet.acknowledgement==True:
#             r=0
#         r=0    
        if r!=0:
            r=randint(0,3)
            PacketReceipt(env=self.env, delay=5+r, receiver=self.destination, packet=packet)
        else:
            if DEBUG:
                if packet.acknowledgement==False:
                    print "    send packet "+str(packet.number)+' (fail)'
                else:
                    print "    send ack "+str(packet.number)+' (fail)'
            pass
        
        
    def react_to_packet_receipt(self, event):
        packet=event.value
        """
        If the packet is a data packet, generate an ack packet
        """        
        if packet.acknowledgement==False:
            print "    Data "+str(packet.number)+" Received"
            ack_packet=self.make_ack_packet(packet)
            self.send_packet(ack_packet)
        """
        If the packet is a ack packet, call tla.rcv_ack()
        """
        if packet.acknowledgement==True:
            print "    Ack "+str(packet.number)+" Received"
            self.tla.react_to_ack(packet)

    def time_out(self, timeout_packet_number):
        """
        When time out happens, run TLA
        Time_out timers should be reset if a the ack arrive
        """
        self.tla.react_to_time_out(timeout_packet_number)

    def react_to_flow_start(self, event):
        self.tla.react_to_flow_start(event=event)
    


class Host(Actor):
    """Representation of an access point

    Hosts send :class:`Packets <.Packet>` through a :class:`.Link` to a
    :class:`.Router` or to another :class:`.Host`.

    :param str address: IP address
    :ivar str address: IP address
    :ivar list flows: :class:`Flows <.Flow>` on this :class:`.Host`
    :ivar link: :class:`Link` connected to this :class:`.Host`
    """
    def __init__(self, env, address):
        super(Host, self).__init__(env=env)
        self.address = address
        self.flows = []
        self.link = None

    def __str__(self):
        return 'Host at ' + self.address

    def send(self, packet):
        link.add(packet)

    def react_to_packet_receipt(self, event):
        packet=event.value
        if isinstance(packet, DataPacket):
            for f in self.flows:
                if (packet.source==f.source)and(packet.destination==f.destination):
                    f.react_to_packet_receipt(event=event)
                if (packet.acknowledgement==True):
                    if (packet.source==f.destination)and(packet.destination==f.source):
                        f.react_to_packet_receipt(event=event)


class Link(Actor):
    """Representation of a physical link between access points or routers

    Links carry packets from one end to the other.

    :param source: source :class:`.Host` or :class:`.Router`
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param float delay: amount of time required to transmit a :class:`.Packet`
    :param float rate: speed of removing data from source
    :param int buffer_capacity: :class:`.Buffer` capacity in bits
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar float delay: amount of time required to transmit a :class:`.Packet`
    :ivar list buffer: :class:`Packets <.Packet>` currently in transmission
    :ivar bool busy: whether currently removing data from source
    :ivar float utilization: fraction of capacity in use
    """
    def __init__(self, env, source, destination, delay, rate, buffer_capacity):
        super(Link, self).__init__(env=env)
        self.source = source
        self.destination = destination
        self.delay = delay
        self.rate = rate
        self.buffer = Buffer(env=env, capacity=buffer_capacity, link=self)
        self.busy = False
        self.utilization = 0

    def __str__(self):
        return ('Link from ' + self.source.address +
                ' to ' + self.destination.address)

    def add(self, packet):
        if self.busy:
            self.buffer.add(packet)
        else:
            self.send(packet)

    def react_to_link_available(self, event):
        # TODO: implement the pseudo-code below
        # self.busy = False
        # if packets in buffer:
        #     self.busy = True
        #     self.send(self.buffer.get_first_packet())
        pass

    def send(self, packet):
        # TODO: implement sending by scheduling LinkAvailable and PacketReceipt
        
        pass


class Packet(Actor):
    """Representation of a quantum of information

    Packets carry information along the network, between :class:`Hosts <.Host>`
    or :class:`Routers <.Router>`.

    :param source: source :class:`.Host` or :class:`.Router`
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param int number: sequence number
    :param acknowledgement: acknowledgement... something
    :cvar int PACKET_SIZE: size of every :class:`.Packet`, in bits
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar int number: sequence number
    :ivar acknowledgement: acknowledgement... something
    :ivar int size: size, in bits
    :ivar str timestamp: time at which the packet was created
    """
    def __init__(self, env, timestamp, source, destination):
        super(Packet, self).__init__(env=env)
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.size = PACKET_SIZE


class DataPacket(Packet):
    def __init__(self, env, number, acknowledgement, timestamp, source,
                 destination):
        super(DataPacket, self).__init__(env, timestamp, source, destination)
        self.number = number

        self.acknowledgement = acknowledgement


class RouterPacket(Packet):
    def __init__(self, env, timestamp, routertable, source):
        super(RouterPacket, self).__init__(env, timestamp, source, destination=0)
        self.routertable = routertable


class Router(Actor):
    """Representation of a router...

    Routers route packets through the network to their destination Hosts.

    :param address:IP address for router
    :param list links: all connected Links
    :param Link default_gateway: default route
    :param default_gateway: default out port if can not decide route
    :ivar list links: all connected Links
    :ivar dict table: routing table
    :ivar default_gateway: default out port if can not decide route
    """
    def __init__(self, env, address):
        super(Router, self).__init__(env=env)
        self.address = address
        self.links = []
        self.table = {}
        self.defaul_gateway = None
  
    def initialize_routing_table(self, all_host_ip_addresses):
        """
        the key of table is destination (IP_address of hosts)
        the first element in value of table is the distance between current router to final host
        the second element in value of table is where to go for next hop
        """
        self.default_gateway = self.links[0].destination.address
        for host_ip_address in all_host_ip_addresses:
            val = float("inf"), self.default_gateway
            self.table[host_ip_address] = val
    
    def update_router_table(self, RouterPacket):
        """
            This function is to check every item in router table if any update.
            Implement Bellman Ford algorithm here.
            mesurement is hop.
            
        """
        
        for destination, val in RouterPacket.routertable:
            if destination in self.table:
                if val[0] + 1 < self.table[destination]:
                    update_val = val[0] + 1, RouterPacket.source
                    self.table[destination] = update_val
            else:
                update_val = val[0] + 1, RouterPacket.source
                self.table[destination] = update_val
        
        
    
    def generate_router_packet(self):
        """
            Design a sepcial packet that send the whole router table of this router to communicate with its neighbor
        """
        for l in links:
            router_packet = RouterPackect(routertable = self.table, source = self.address)
            send(link = l, packet = router_packet)
      
    
    def map_route(self, packet):
        if packet.destination in table:
            next_hop = table[packet.destination][1]
            for link in links:
                if (next_hop == link.destination.address):
                    route_link = link
                    break
            send(link = route_link, packet = packet)
        else:
            next_hop = self.default_gateway # can be delete
            send(link = links[0], packet = packet)
      
    
    
    def react_to_packet_receipt(self, event):
        """
            Read packet head to tell whether is a normal packet or a update_RT_communication packet
            If it is normal packet, call map_route function
            If it is update_RT_communication packet, call update_router_table function
            """
        packet = event.value
        if isinstance(packet, DataPacket):
            map_route(packet = packet)
        elif isinstance(packet, RouterPacket):
            update_router_table(packet = packet)
        
       
      
    
    def send(self, link, packet):
        """
            send packet to certain link
            the packet could be normal packet to forward or communication packet to send to all links.
        """
        link.add(packet = packet)

    def react_to_routing_table_outdated(self, event):
        self.generate_router_packet()
        RoutingTableOutdated(env=self.env, delay=GENERATE_ROUTERPACKET_TIME_INTEVAL, router=self)
