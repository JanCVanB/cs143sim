"""
This module includes simple transport layer algorithm: stop and wait
"""
packet_size=1024*8
class StopAndWait:
    """
    :ivar W: window size
    :ivar packet_number: number of packets to be sent
    :ivar last_acked_packet_number
    :ivar last_sent_packet_number=
    """
    def __init__(self,flow):
        self.flow=flow
        
        self.W=1
        
        self.packet_number=self.flow.amount/packet_size
        if self.packet_number*packet_size<self.flow.amount:
            self.packet_number+=1
        
        self.last_acked_packet_number=-1 
        
        
    def response_to_ack(self):
        self.last_acked_packet_number+=1
        n=self.last_acked_packet_number
        
        if n<self.packet_number:
            packet=self.flow.make_packet(n)
            self.flow.send_packet(packet)

    
    def response_to_time_out(self):
        n=self.last_acked_packet_number
        packet=self.flow.make_packet(n)
        self.flow.send_packet(packet)
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