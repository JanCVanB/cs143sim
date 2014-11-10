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
    def __init__(self, env, flow):
        self.flow=flow
        self.env=env
        
        self.W=1
        
        self.packet_number=self.flow.amount/packet_size
        if self.packet_number*packet_size<self.flow.amount:
            self.packet_number+=1
        
        self.last_acked_packet_number=-1 
        
        self.TimeOut=13
        
    def __str__(self):
        return self.flow.__str__()
    
    def react_to_flow_start(self, event):
       
        print "    Packet Amount: "+str(self.packet_number)             
        n=0
        packet=self.flow.make_packet(packet_number=n)
        self.flow.send_packet(packet)
        PacketTimeOut(env=self.env, delay=self.TimeOut, actor=self, packet_number=n)
    
    def react_to_ack(self, ack_packet):
        if ack_packet.number==self.last_acked_packet_number+2:
            self.last_acked_packet_number+=1
            n=self.last_acked_packet_number+1
    
            if n<self.packet_number:
                packet=self.flow.make_packet(packet_number=n)
                self.flow.send_packet(packet)
                PacketTimeOut(env=self.env, delay=self.TimeOut, actor=self, packet_number=n)

    def react_to_time_out(self, event):

        n=self.last_acked_packet_number
        time_out_packet_number=event.value
        
        print "    Time Out "+str(time_out_packet_number)+" "+str(n)
        if time_out_packet_number>n:
            n=time_out_packet_number;
            packet=self.flow.make_packet(packet_number=n)
            self.flow.send_packet(packet)
            PacketTimeOut(env=self.env, delay=self.TimeOut, actor=self, packet_number=n)
        pass
    


class GoBackN:
    """
    :ivar W: window size
    :ivar packet_number: number of packets to be sent

    """

    """
    :ivar snd_not_sent: packet that has not been sent
    :ivar snd_sending: list of packet that are being sent
    """
    def __init__(self, env, flow):
        self.flow=flow
        self.env=env
        
        self.W=3
        self.TimeOut=13
        
        self.packet_number=self.flow.amount/packet_size
        if self.packet_number*packet_size<self.flow.amount:
            self.packet_number+=1
        
        
        self.snd_not_sent=0
        self.snd_sending=list()
        
    def __str__(self):
        return self.flow.__str__()
    
    def react_to_flow_start(self, event):
        print "    Packet Amount: "+str(self.packet_number)             
        self.send_new_packets()
    
    def react_to_ack(self, ack_packet):
        n=ack_packet.number
        
        for x in self.snd_sending:
            if x<n:
                self.snd_sending.remove(x)
                
        self.send_new_packets()

    def react_to_time_out(self, event):
        n=event.value
        if n in self.snd_sending:
            packet=self.flow.make_packet(packet_number=n)
            self.flow.send_packet(packet)
            PacketTimeOut(env=self.env, delay=self.TimeOut, actor=self, packet_number=n)
        pass
    
    def send_new_packets(self):
        while self.snd_not_sent<self.packet_number and len(self.snd_sending)<self.W:
            n=self.snd_not_sent
            packet=self.flow.make_packet(packet_number=n)
            self.flow.send_packet(packet)
            PacketTimeOut(env=self.env, delay=self.TimeOut, actor=self, packet_number=n)
            
            self.snd_sending.append(n)
            self.snd_not_sent+=1            
    pass
