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


class Buffer:
    """Representation of a data storage container

    Buffers store data to be linked while Link is busy sending data.

    :param int capacity: maximum number of bits that can be stored
    :ivar int capacity: maximum number of bits that can be stored
    :ivar list packets: packets currently in storage
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.packets = []

    def add(self, packet):
        current_level = sum(packet.size for packet in self.packets)
        if current_level + packet.size <= self.capacity:
            self.packets.append(packet)


class Flow:
    """Representation of a connection between access points

    Flows try to transmit data from Host to Host.

    :param cs143sim.actors.Host source: source Host
    :param cs143sim.actors.Host destination: destination Host
    :param float amount: amount of data to transmit
    :ivar cs143sim.actors.Host source: source Host
    :ivar cs143sim.actors.Host destination: destination Host
    :ivar float amount: amount of data to transmit
    """
    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount


class Host:
    """Representation of an access point

    Hosts send Packets through Links to Routers or other Hosts.

    :param str address: IP address
    :param list flows: Flows on this host
    :ivar str address: IP address
    :ivar list flows: Flows on this host
    """
    def __init__(self, address, flows):
        self.address = address
        self.flows = flows


class Link:
    """Representation of a physical link between access points or routers

    Links carry packets from one end to the other.

    :param source: source Host or Router
    :param destination: destination Host or Router
    :param float delay: amount of time required to transmit a packet
    :param float rate: speed of removing data from source
    :param int buffer_capacity: Buffer capacity in bits
    :ivar source: source Host
    :ivar destination: destination Host
    :ivar float delay: amount of time required to transmit a packet
    :ivar list buffer: packets currently in transmission
    :ivar bool busy: whether currently removing data from source
    :ivar float utilization: fraction of capacity in use
    """
    def __init__(self, source, destination, delay, rate, buffer_capacity):
        self.source = source
        self.destination = destination
        self.delay = delay
        self.rate = rate
        self.buffer = Buffer(capacity=buffer_capacity)
        self.busy = False
        self.utilization = 0

    def add(self, packet):
        if self.busy:
            self.buffer.add(packet)
        else:
            self.send(packet)

    def send(self, packet):
        # TODO: implement sending
        pass


class Packet:
    """Representation of a quantum of information

    Packets carry information along the network, between Hosts or Routers.

    :param source: source port
    :param destination: destination port
    :param int number: sequence number
    :param acknowledgement: acknowledgement... something
    :cvar int PACKET_SIZE: size of every packet, in bits
    :ivar source: source port
    :ivar destination: destination port
    :ivar int number: sequence number
    :ivar acknowledgement: acknowledgement... something
    :ivar int size: size of packet, in bits
    """
    PACKET_SIZE = 8192  # bits

    def __init__(self, source, destination, number, acknowledgement):
        self.source = source
        self.destination = destination
        self.number = number
        self.acknowledgement = acknowledgement
        self.size = Packet.PACKET_SIZE


class Router:
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
    def __init__(self, links, address):
        self.address = address
        self.links = links
        self.table = {}
        self.default_gateway = table[0]
     
    def add_router_table(self, destination, distance, next_hoop):
        value = [distance, next_hoop]
        table[destination]= value
    
    def update_router_table(self, RouterPacket):
        """
        This function is more important to routers which are not directly connected to this router.
        Implement Bellman Ford algorithm here
        
        
        for item in RouterPacket.routertable:
            if item.val + yamei_packet.router.distance < table[item.key]:
                update table[item.key] = item.val + yamei_packet.router.distance
        """ 
        
        for item in RouterPacket.routertable:
            if item.val + 1 < table[item.key]:
                update table[item.key] = item.val + 1
        pass
    
    def generate_communication_packet(self):
        """
        Design a sepcial packet that send the whole router table of this router to communicate with its neighbor
        """
        time_interval = 1
        for l in links:
            router_packet = RouterPackect(routertable = self.table, source = self.address, destination = l.destination)
            send(link = l, packet = router_packet)
        #return communication_packet
        pass
    
    def map_route(self,packet):
        if packet.destination in table:
            route_link = table[packet.destination]
            send(link = route_link, packet = packet)
        else:
            route_link = self.default_gateway
            send(link = route_link, packet = packet)
        pass
        
        
        
    def receive(packet):
        """
        Read packet head to tell whether is a normal packet or a update_RT_communication packet
        If it is normal packet, call map_route function
        If it is update_RT_communication packet, call update_router_table function
        """
        if packet.typ == 1 || packet.typ == 2:
            map_route(packet)
        elif packet.typ == 3:
            update_router_table(packet)
        
        pass
    
    """   
    def get_neighbor_router(self):
        """
        Get the delay, rate, hop and destination information from links
        Actually router table can update their neighbor_router's information without sending a communication packet.
        Update the neighbor part of the router table here (maybe)
        """
        neighbor = self.links.destination
        pass
    """
    
    def send(self, link, packet):
        """
        send packet to certain link
        the packet could be normal packet to forward or communication packet to send to all links.
        """
        link.add(packet)
        
