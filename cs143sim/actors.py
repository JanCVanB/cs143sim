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

    Buffers store data to be linked while :class:`.Link` is busy sending data.

    :param int capacity: maximum number of bits that can be stored
    :ivar int capacity: maximum number of bits that can be stored
    :ivar list packets: :class:`Packets <.Packet>` currently in storage
    """
    def __init__(self, capacity):
        self.capacity = capacity
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
            # TODO: Insert callback for simulation monitor (report that a packet was dropped)
            pass


class Flow:
    """Representation of a connection between access points

    Flows try to transmit data from :class:`.Host` to :class:`.Host`.

    :param source: source :class:`.Host`
    :param destination: destination :class:`.Host`
    :param float amount: amount of data to transmit
    :ivar source: source :class:`.Host`
    :ivar destination: destination :class:`.Host`
    :ivar float amount: amount of data to transmit
    """
    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount

    def __str__(self):
        return ('Flow from ' + self.source.address +
                ' to ' + self.destination.address)

    def make_packet(self, packet_num):
        """
        Make a packet based on the packet number
        """

    def send_packet(self):
        """
        When possible, TLA use this method to send a packet
        """

    def receive_packet(self):
        """
        When receive a packet, check if the packet is an ack packet. If so, run TLA
        """

    def time_out(self):
        """
        When time out happens, run TLA
        Time_out timers should be reset if a the ack arrive
        """

    def tla(self):
        """
        Transport Layer Algorithm main body
        Including transmission control, congestion control algorithm (window size adjust)
        Flow control might not be needed, as the receiving buffer size is unlimited.

        For example (stop and wait):
            TLA send a packet
            while(! all packet have been transmitted):
                yield(time_out|receive_ack)
                if(time_out) :
                    retransmit
                    reset timer
                if(receive_ack) :
                    transmit new packet
                    reset timer
        """

    def react_to_flow_start(self, event):
        # TODO: react by sending packets to Host
        pass


class Host:
    """Representation of an access point

    Hosts send :class:`Packets <.Packet>` through a :class:`.Link` to a
    :class:`.Router` or to another :class:`.Host`.

    :param str address: IP address
    :ivar str address: IP address
    :ivar list flows: :class:`Flows <.Flow>` on this :class:`.Host`
    :ivar link: :class:`Link` connected to this :class:`.Host`
    """
    def __init__(self, address):
        self.address = address
        self.flows = []
        self.link = None

    def __str__(self):
        return 'Host at ' + self.address

    def send(self, packet):
        self.link.add(packet)

    def receive(self, packet):
        # TODO: pass to flows[packet.destination]
        pass


class Link:
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
    def __init__(self, source, destination, delay, rate, buffer_capacity):
        self.source = source
        self.destination = destination
        self.delay = delay
        self.rate = rate
        self.buffer = Buffer(capacity=buffer_capacity)
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


class Packet:
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
    PACKET_SIZE = 8192  # bits

    def __init__(self, source, destination, number, acknowledgement):
        self.source = source
        self.destination = destination
        self.number = number
        self.acknowledgement = acknowledgement
        self.size = Packet.PACKET_SIZE
        self.timestamp = ''  # TODO: Insert timestamp

    def __str__(self):
        return ('Packet ' + str(self.number) +
                ' from ' + self.source.address +
                ' to ' + self.destination.address)


class JunlinPacket(Packet):
    """Packet used for sending flow data"""


class RouterPacket(Packet):
    """Packet used for updating routing tables"""


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
    def __init__(self, links, address, all_destination):
        self.address = address
        self.links = links
        self.table = {}
        if len(links):
            self.default_gateway = links[0].destination
        else:
            self.default_gateway = address
        
        for d in all_destination:
            val = float("inf"), default_gateway
            table[d] = val
    
    
    def add_router_table(self, destination, distance, next_hoop):
        """
            update & append new item
            """
        value = distance, next_hoop
        table[destination] = value
    
    def update_router_table(self, RouterPacket):
        """
            This function is more important to routers which are not directly connected to this router.
            Implement Bellman Ford algorithm here
            
            
            for item in RouterPacket.routertable:
            if item.val + yamei_packet.router.distance < table[item.key]:
            update table[item.key] = item.val + yamei_packet.router.distance
            """
        
        for destination, val in RouterPacket.routertable:
            if destination in self.table:
                if val[0] + 1 < self.table[destination]:
                    update_val = val[0] + 1, RouterPacket.source
                    self.table[destination] = update_val
            else:
                update_val = val[0] + 1, RouterPacket.source
                self.table[destination] = update_val
        
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
        if packet.typ == 1 or packet.typ == 2:
            map_route(packet)
        elif packet.typ == 3:
            update_router_table(packet)
        
        pass
    
    """
        def get_neighbor_router(self):
        
        #Get the delay, rate, hop and destination information from links
        #Actually router table can update their neighbor_router's information without sending a communication packet.
        #Update the neighbor part of the router table here (maybe)
        
        neighbor = self.links.destination
        pass
        """
    
    def send(self, link, packet):
        """
            send packet to certain link
            the packet could be normal packet to forward or communication packet to send to all links.
            """
        link.add(packet)

    def react_to_routing_table_outdated(self, event):
        # TODO: react by generating routing packets to neighbor routers
        pass

