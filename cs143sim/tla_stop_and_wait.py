"""
This module includes simple transport layer algorithm: stop and wait
"""
from cs143sim.events import PacketTimeOut



packet_size=1024*8
class StopAndWait:
    """
    :ivar W: window size
    :ivar packet_number: number of packets to be sent
    :ivar last_acked_packet_number
    :ivar last_sent_packet_number=
    """
    global env
    def __init__(self, env, flow):
        self.flow=flow
        self.env=env
        
        self.W=1
        
        self.packet_number=self.flow.amount/packet_size
        if self.packet_number*packet_size<self.flow.amount:
            self.packet_number+=1
        
        self.last_acked_packet_number=-1 
        
    def __str__(self):
        return self.flow.__str__()
    
    def react_to_flow_start(self, event):
       
        print "    Packet Amount: "+str(self.packet_number)             
        n=0
        packet=self.flow.make_packet(packet_number=n)
        self.flow.send_packet(packet)
        PacketTimeOut(env=self.env, delay=10, actor=self, packet_number=n)
    
    def react_to_ack(self, ack_packet):
        self.last_acked_packet_number+=1
        n=self.last_acked_packet_number+1

        if n<self.packet_number:
            packet=self.flow.make_packet(packet_number=n)
            self.flow.send_packet(packet)
            PacketTimeOut(env=self.env, delay=10, actor=self, packet_number=n)

    def react_to_time_out(self, event):

        n=self.last_acked_packet_number
        time_out_packet_number=event.value
        
        print "    Time Out "+str(time_out_packet_number)+" "+str(n)
        if time_out_packet_number>n:
            n=0
            packet=self.flow.make_packet(packet_number=n)
            self.flow.send_packet(packet)
            PacketTimeOut(env=self.env, delay=10, actor=self, packet_number=n)
        pass
    
    pass

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
    pass