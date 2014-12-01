"""This module includes simple transport layer algorithm: stop and wait

.. autosummary::

    GoBackN
    FastRetransmit
    StopAndWait
    TCPTahoe

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <neicullyn@gmail.com>
"""
from cs143sim.constants import DEBUG
from cs143sim.constants import PACKET_SIZE
from cs143sim.events import PacketTimeOut
from cs143sim.events import VegasTimeOut
from cs143sim.utilities import full_string
from math import floor


class TCPTahoe:
    """
    Constants:
    :ivar enable_fast_retransmit
    :ivar enable_fast_recovery
    :ivar ka: k of additive
    :ivar ks: k of slow start
    :ivar rtt_alpha: change rate of rtt_avg
    :ivar rtt_beta: change rate of rtt_div    
    
    :ivar W: window size
    :ivar packet_number: number of packets to be sent
    :ivar time_out: timer's waiting time

    Transmitter:
    :ivar transmitter_not_sent: packets that have not been sent
    :ivar transmitter_sending: list of packets that are being sent
    :ivar transmitter_acked: packets  that have been acked
    
    Ack management:
    :ivar duplicate_ack_number: record last acked packet number
    :ivar duplicate_ack_times: record how many times the packet has been continuous acked
    
    Timeout Management:
    :ivar last_reset: last effective timeout time
    :ivar time_out_event: current time out event
    
    Slow Start:
    :ivar slow_start_treshold: treshold of slow start
    
    RTT caculator:
    :ivar rtt_avg
    :ivar rtt_div
    
    Flags:    
    :ivar slow_start_flag
    :ivar fast_recovery_flag
    """
    # TODO: define class in docstring and fix triplicate docstring
    def __init__(self, env, flow):
        self.enable_fast_retransmit=False
        self.enable_fast_recovery=True
        self.ka=1
        self.ks=1
        self.rtt_alpha=0.125
        self.rtt_beta=0.25
        
        self.flow=flow
        self.env=env
        
        self.packet_number=self.flow.amount/PACKET_SIZE
        if self.packet_number*PACKET_SIZE<self.flow.amount:
            self.packet_number+=1
      
        self.time_out=1000
        self.first_ack_flag=True
        #self.rtt_avg
        #self.rtt_div
        
        self.transmitter_not_sent=0
        self.transmitter_sending=list()
        self.transmitter_acked=-1
        
        self.duplicate_ack_number=-1
        self.duplicate_ack_times=0
        
        
        self.slow_start_treshold=100
        
      
        
        self.change_W(W=1)
        
        self.last_reset=0
        self.time_out_event=None
        
        self.slow_start_flag=True
        self.fast_recovery_flag=False


        

    def __str__(self):
        return self.flow.__str__()
    
    def react_to_flow_start(self, event):
        print "    Packet Amount: "+str(self.packet_number)             
        self.send_new_packets()
    
    def react_to_ack(self, ack_packet):
        """
        Updating Time out (according to 7.4.4 Timers)
        """
        #RFC 6298

        
        if self.first_ack_flag:
            t=self.env.now-ack_packet.timestamp
            self.rtt_avg=t
            self.rtt_div=t
            self.first_ack_flag=False

        else:
            t=self.env.now-ack_packet.timestamp
            
            self.rtt_div=(1-self.rtt_beta)*self.rtt_div+self.rtt_beta*abs(t-self.rtt_avg)
            self.rtt_avg=(1-self.rtt_alpha)*self.rtt_avg+self.rtt_alpha*t
            
            self.time_out=int(1+(self.rtt_avg+4*self.rtt_div))
            if self.time_out<1000:
                self.time_out=1000
        
        RTT_DEBUG=True
        if DEBUG and RTT_DEBUG:
            print "      rtt_avg "+str(self.rtt_avg)
            print "      rtt_div "+str(self.rtt_div)
            
        """
        Process Duplicate Ack
         
        """
        n=ack_packet.number
        if n>self.transmitter_acked:
            if n==self.duplicate_ack_number:
                self.duplicate_ack_times+=1
            else:
                self.duplicate_ack_number=n
                self.duplicate_ack_times=0
                
                
            if self.enable_fast_retransmit and self.duplicate_ack_times==4 and self.env.now-self.last_reset>self.time_out:
                if DEBUG:
                    print "    Duplicate Ack "+str(n)
                    print "    Fast retransmit"
                self.react_to_time_out_base()
            elif self.enable_fast_recovery and self.duplicate_ack_times==4:
                if DEBUG:
                    print "    Duplicate Ack "+str(n)+" Times "+str(self.duplicate_ack_times)
                    print "    Enter Fast recovery"
                    
                self.fast_recovery_flag=True
                self.slow_start_treshold=self.W/2    
                #self.change_W(self.W/2+3)
                """
                Actually, W is not windows size at that means. 
                W is number of packets between the first and the last unacked packets
                """
                while len(self.transmitter_sending)>=self.W:
                    self.transmitter_sending.pop()
                         
                n=self.duplicate_ack_number
                packet=self.flow.make_packet(packet_number=n)  
                self.flow.send_packet(packet)
                
                
            elif self.enable_fast_recovery and self.duplicate_ack_times>4:
                if DEBUG:
                    print "    Duplicate Ack "+str(n)+" Times "+str(self.duplicate_ack_times)
                    print "    More Fast recovery" 
                self.change_W(self.W+1)
                self.send_new_packets()
            else:
#             else:
                """
                Process Ack
                """
                if self.enable_fast_recovery and self.fast_recovery_flag==True:
                    """
                    Just leave fast recovery
                    """
                    if self.env.now-self.last_reset>self.rtt_avg:
                        self.change_W(floor(self.slow_start_treshold))
                        self.last_reset=self.env.now
                    self.fast_recovery_flag=False
                    self.slow_start_flag=False
                    
                    """
                    Note: you can not start sending a lot of packets now. 
                    See send_new_packets: limit the packets send for each ack
                    (Data Burst: RFC3782)
                    """
                 
               
#                if DEBUG:
#                    print "            Old "+str(self.snd_sending)   
                
                del_list=list()
                         
                for x in self.transmitter_sending:            
                    if x<n:
                        del_list.append(x)
                        
                if self.transmitter_sending[0] in del_list:
                    self.reset_timer()
                    
                for x in del_list:            
                    self.transmitter_sending.remove(x)
                        
#                if DEBUG:
#                    print "            New "+str(self.snd_sending) 
                
                n=ack_packet.number
                self.transmitter_acked=max([self.transmitter_acked,n-1])
                
                """
                Process sending
                """
                    
                """
                    Note: you can not start sending a lot of packets now. 
                    See send_new_packets: limit the packets send for each ack
                    (Data Burst: RFC3782)
                """ 
                if self.W-len(self.transmitter_sending)<2:        
                    if self.slow_start_flag:
                        self.change_W(self.W+self.ks*1.0)
                        if self.W>self.slow_start_treshold:
                            self.slow_start_flag=False
                    else:
                        self.change_W(self.W+self.ka*1.0/max(self.W,1))      
                self.send_new_packets()


    def react_to_time_out(self, event):
        if event==self.time_out_event:
            if DEBUG:
                print "    "+full_string(self.flow)+" Timeout"
            self.react_to_time_out_base()

            
    
    def react_to_time_out_base(self):
        if len(self.transmitter_sending)>0:

            
            self.time_out=2*self.time_out
            self.reset_timer()
    
            self.slow_start_treshold=self.W/2
            self.slow_start_flag=True
            
            self.change_W(W=1)
            self.transmitter_sending=[]
            self.send_new_packets()
            
            self.last_reset=self.env.now
    
    def send_new_packets(self):

        send_flag=False
        Cnt=2
        while len(self.transmitter_sending)<self.W and Cnt>0:
            Cnt-=1
            send_flag=True
            
            l=len(self.transmitter_sending)
            if l==0:
                n=self.transmitter_acked+1
            else:
                n=self.transmitter_sending[l-1]+1
            
            if n>self.packet_number:
                break
            
            packet=self.flow.make_packet(packet_number=n)            
            self.flow.send_packet(packet)            
            self.transmitter_sending.append(n)
        
        if send_flag==True and self.time_out_event==None:
            self.reset_timer()
            
#         if DEBUG:
#             print "        Sending "+str(self.snd_sending) 
            
    def change_W(self, W):
        self.W=W
        self.env.controller.record_window_size(flow=self.flow, window_size=self.W)
        
        if DEBUG:
                print "        W="+str(self.W) 
     
    pass

    def reset_timer(self):
        self.time_out_event=PacketTimeOut(env=self.env, delay=self.time_out, actor=self, expected_time=self.env.now+self.time_out)
class TCPVegas:
    """
    Constants:
    :ivar vegas_alpha
    :ivar vegas_beta
    :ivar ka: k of additive
    :ivar ks: k of slow start
    :ivar rtt_alpha: change rate of rtt_avg
    :ivar rtt_beta: change rate of rtt_div    
    
    :ivar W: window size
    :ivar packet_number: number of packets to be sent
    :ivar time_out: timer's waiting time

    Transmitter:
    :ivar transmitter_not_sent: packets that have not been sent
    :ivar transmitter_sending: list of packets that are being sent
    :ivar transmitter_acked: packets  that have been acked
    
    Ack management:
    :ivar duplicate_ack_number: record last acked packet number
    :ivar duplicate_ack_times: record how many times the packet has been continuous acked
    
    Timeout Management:
    :ivar last_reset: last effective timeout time
    :ivar time_out_event: current time out event
    
    Slow Start:
    :ivar slow_start_treshold: treshold of slow start
    
    RTT caculator:
    :ivar rtt_avg
    :ivar rtt_div
    
    Flags:    
    :ivar slow_start_flag
    :ivar fast_recovery_flag
    
    Vegas:
    :ivar vegas_rtt
    :ivar vegas_rtt_base
    :ivar vegas_time_out_event
    """
    # TODO: define class in docstring and fix triplicate docstring
    def __init__(self, env, flow):
        self.vegas_alpha=4
        self.vegas_beta=8
        self.vegas_gamma=6
        self.fast_alpha=4
        self.vegas_virtual_rtt=0
        
        self.enable_fast=False
        
        self.ka=1
        self.ks=1
        self.rtt_alpha=0.125
        self.rtt_beta=0.25
        
        self.flow=flow
        self.env=env
        
        self.packet_number=self.flow.amount/PACKET_SIZE
        if self.packet_number*PACKET_SIZE<self.flow.amount:
            self.packet_number+=1
      
        self.time_out=1000
        self.first_ack_flag=True
        #self.rtt_avg
        #self.rtt_div
        
        self.transmitter_not_sent=0
        self.transmitter_sending=list()
        self.transmitter_acked=-1
        
        self.duplicate_ack_number=-1
        self.duplicate_ack_times=0
        
        
        self.slow_start_treshold=240
        
      
        
        self.change_W(W=1)
        
        self.last_reset=0
        self.last_half=0
        self.time_out_event=None
        
        self.slow_start_flag=True
        self.vegas_time_out_event=None



        

    def __str__(self):
        return self.flow.__str__()
    
    def react_to_flow_start(self, event):
        print "    Packet Amount: "+str(self.packet_number)             
        self.send_new_packets()
    
    def react_to_ack(self, ack_packet):
        """
        Updating Time out (according to 7.4.4 Timers)
        Updating vegas_rtt
        """
        #RFC 6298
        
        if self.first_ack_flag:
            t=self.env.now-ack_packet.timestamp
            self.rtt_avg=t
            self.rtt_div=t
            self.first_ack_flag=False
            
            self.vegas_rtt=t
            self.vegas_rtt_base=t

        else:
            t=self.env.now-ack_packet.timestamp
            
            self.rtt_div=(1-self.rtt_beta)*self.rtt_div+self.rtt_beta*abs(t-self.rtt_avg)
            self.rtt_avg=(1-self.rtt_alpha)*self.rtt_avg+self.rtt_alpha*t
            
            self.time_out=int(1+(self.rtt_avg+4*self.rtt_div))
            if self.time_out<1000:
                self.time_out=1000
            
            self.vegas_rtt=t
            if self.vegas_rtt_base>t:
                self.vegas_rtt_base=t
                
        RTT_DEBUG=True
        if DEBUG and RTT_DEBUG:
            print "      rtt_avg "+str(self.rtt_avg)
            print "      rtt_div "+str(self.rtt_div)
            

        """
        Process Duplicate Ack         
        """
        n=ack_packet.number
        if n>self.transmitter_acked:
            if n==self.duplicate_ack_number:
                self.duplicate_ack_times+=1
            else:
                self.duplicate_ack_number=n
                self.duplicate_ack_times=0
                
            if self.duplicate_ack_times==4:
                if DEBUG:
                    print "    Duplicate Ack "+str(n)
                    print "    Fast retransmit"
                self.react_to_time_out_base()
            elif ack_packet.timestamp>=self.last_reset:
                """
                Process Ack
                """
 
                del_list=list()
                         
                for x in self.transmitter_sending:            
                    if x<n:
                        del_list.append(x)
                        
                if self.transmitter_sending[0] in del_list:
                    self.reset_timer()
                    
                for x in del_list:            
                    self.transmitter_sending.remove(x)
                
                n=ack_packet.number
                self.transmitter_acked=max([self.transmitter_acked,n-1])
                
                """
                Process sending
                """
                    
                """
                    Note: you can not start sending a lot of packets now. 
                    See send_new_packets: limit the packets send for each ack
                    (Data Burst: RFC3782)
                """      
                if self.slow_start_flag:
                    self.change_W(self.W+self.ks*1.0)
                    if self.W/self.vegas_rtt_base - self.W/self.vegas_rtt > self.vegas_gamma/self.vegas_rtt_base:
                        self.slow_start_flag=False
                    self.send_new_packets(4)
                else:
                    if self.vegas_time_out_event==None:
                        self.vegas_time_out_event=VegasTimeOut(env=self.env, delay= self.vegas_rtt, actor=self)
                    self.send_new_packets(2)

    def react_to_vegas_time_out(self, event):
        if self.vegas_virtual_rtt==0:
            vrtt=self.vegas_rtt_base
        else:
            vrtt=self.vegas_virtual_rtt
            
        if not self.enable_fast:
            if self.W/self.vegas_rtt_base-self.W/self.vegas_rtt < self.vegas_alpha/vrtt:
                self.change_W(W=self.W+1)
            if self.W/self.vegas_rtt_base-self.W/self.vegas_rtt > self.vegas_beta/vrtt:
                self.change_W(W=self.W-1)
        else:
            self.change_W(W=self.W*self.vegas_rtt_base/self.vegas_rtt+self.fast_alpha)
        self.vegas_time_out_event=VegasTimeOut(env=self.env, delay= self.vegas_rtt, actor=self)
                

    def react_to_time_out(self, event):
        if event==self.time_out_event:
            if DEBUG:
                print "    "+full_string(self.flow)+" Timeout"
            print "    "+full_string(self.flow)+" Timeout"
            self.react_to_time_out_base()

            
    
    def react_to_time_out_base(self):
        if len(self.transmitter_sending)>0:
            
            self.time_out=2*self.time_out
            self.reset_timer()
    
            self.change_W(W=1)
            self.transmitter_sending=[]
            self.send_new_packets()
            
            self.last_reset=self.env.now
    
    def send_new_packets(self, cnt=1):

        send_flag=False
        while len(self.transmitter_sending)<self.W and cnt>0:
            cnt-=1
            send_flag=True
            
            l=len(self.transmitter_sending)
            if l==0:
                n=self.transmitter_acked+1
            else:
                n=self.transmitter_sending[l-1]+1
            
            if n>self.packet_number:
                break
            
            packet=self.flow.make_packet(packet_number=n)            
            self.flow.send_packet(packet)            
            self.transmitter_sending.append(n)
        
        if send_flag==True and self.time_out_event==None:
            self.reset_timer()
        return cnt

            
    def change_W(self, W):
        self.W=W
        self.env.controller.record_window_size(flow=self.flow, window_size=self.W)
        if DEBUG:
                print "        W="+str(self.W) 
     
    pass

    def reset_timer(self):
        self.time_out_event=PacketTimeOut(env=self.env, delay=self.time_out, actor=self, expected_time=self.env.now+self.time_out)
