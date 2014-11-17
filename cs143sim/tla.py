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
from cs143sim.utilities import full_string


class TCPTahoe:
    """
    :ivar W: window size
    :ivar packet_number: number of packets to be sent
    :ivar TimeOut: timer's waiting time

    """

    """
    :ivar snd_not_sent: packet that has not been sent
    :ivar snd_sending: list of packet that are being sent
    """
    """
    :ivar enable_fast_retransmit
    """
    """
    :ivar slow_start_flag
    """
    # TODO: define class in docstring and fix triplicate docstring
    def __init__(self, env, flow, recorder=None):
        
        if recorder==None:
            self.recorder=open("W_record.txt","w")
        else:
            self.recorder=open(recorder,"w")
        
        self.flow=flow
        self.env=env
        
        self.packet_number=self.flow.amount/PACKET_SIZE
        if self.packet_number*PACKET_SIZE<self.flow.amount:
            self.packet_number+=1
          
        
        
        self.time_out=1000
        self.first_ack_flag=True
        #self.rtt_avg
        #self.rtt_div
        
        self.snd_not_sent=0
        self.snd_sending=list()
        self.snd_acked=-1
        
        self.duplicate_ack_number=-1
        self.duplicate_ack_times=0
        
        self.enable_fast_retransmit=False
        self.enable_fast_recovery=False
        
        self.slow_start_flag=True
        self.slow_start_treshold=64
        
        
        
        self.change_W(W=1)
        #slew rate of AIMD:AI
        self.ka=0.5
        self.ks=1
        
        self.last_reset=0
        self.time_out_event=None
        
        self.fast_recovery_flag=False
        
        print self.recorder
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
        alpha=0.125
        beta=0.25
        
        if self.first_ack_flag:
            t=self.env.now-ack_packet.timestamp
            self.rtt_avg=t
            self.rtt_div=t
            self.first_ack_flag=False

        else:
            t=self.env.now-ack_packet.timestamp
            
            self.rtt_div=(1-beta)*self.rtt_div+beta*abs(t-self.rtt_avg)
            self.rtt_avg=(1-alpha)*self.rtt_avg+alpha*t
            
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
        if n>self.snd_acked:
            if n==self.duplicate_ack_number:
                self.duplicate_ack_times+=1
            else:
                self.duplicate_ack_number=n
                self.duplicate_ack_times=0
                
                
            if self.enable_fast_retransmit and self.duplicate_ack_times==4:
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
                Acturally, W is not windows size at that means. 
                W is number of packets between the first and the last unacked packets
                """
                while len(self.snd_sending)>=self.W:
                    self.snd_sending.pop()
                         
                n=self.duplicate_ack_number
                packet=self.flow.make_packet(packet_number=n)  
                self.flow.send_packet(packet)
                
                
            elif self.enable_fast_recovery and self.duplicate_ack_times>4:
                if DEBUG:
                    print "    Duplicate Ack "+str(n)+" Times "+str(self.duplicate_ack_times)
                    print "    More Fast recovery" 
                self.change_W(self.W+1)
                self.send_new_packets()
#             elif ack_packet.timestamp>=self.last_reset:
            else:
                """
                Process Ack
                """
                if self.enable_fast_recovery and self.fast_recovery_flag==True:
                    """
                    Just leave fast recovery
                    """
                    self.change_W(self.slow_start_treshold-1)
                    self.fast_recovery_flag=False
                    self.slow_start_flag=False
                    
                    """
                    Note: you can not start sending a lot of packets now. 
                    See send_new_packets: limit the packets send for each ack
                    (Data Burst: RFC3782)
                    """
                    
                    
                if self.slow_start_flag:
                    self.change_W(self.W+self.ks*1.0)
                    if self.W>self.slow_start_treshold:
                        self.slow_start_flag=False
                else:
                    self.change_W(self.W+self.ka*1.0/self.W)
                    #self.change_W(self.W+1)
                    
               
                if DEBUG:
                    print "            Old "+str(self.snd_sending)   
                
                del_list=list()
                         
                for x in self.snd_sending:            
                    if x<n:
                        del_list.append(x)
                        
                if len(del_list)>0:
                    self.reset_timer()
                    
                for x in del_list:            
                    self.snd_sending.remove(x)
                        
                if DEBUG:
                    print "            New "+str(self.snd_sending) 
                
                n=ack_packet.number
                self.snd_acked=max([self.snd_acked,n-1])
                
                """
                Process sending
                """             
                self.send_new_packets()

    def react_to_time_out(self, event):
        if event==self.time_out_event:
            if DEBUG:
                print "    "+full_string(self.flow)+" Timeout"
            self.react_to_time_out_base()

            
    
    def react_to_time_out_base(self):
        if len(self.snd_sending)>0:

            
            self.time_out=2*self.time_out
            self.reset_timer()
    
            self.slow_start_treshold=self.W/2
            self.slow_start_flag=True
            
            self.change_W(W=1)
            self.snd_sending=[]
            self.send_new_packets()
            
            self.last_reset=self.env.now
    
    def send_new_packets(self):

        send_flag=False
        Cnt=10
        while len(self.snd_sending)<self.W and Cnt>0:
            Cnt-=1
            send_flag=True
            
            l=len(self.snd_sending)
            if l==0:
                n=self.snd_acked+1
            else:
                n=self.snd_sending[l-1]+1
            
            if n>self.packet_number:
                break
            
            packet=self.flow.make_packet(packet_number=n)            
            self.flow.send_packet(packet)            
            self.snd_sending.append(n)
        
        if send_flag==True and self.time_out_event==None:
            self.reset_timer()
            
#         if DEBUG:
#             print "        Sending "+str(self.snd_sending) 
            
    def change_W(self, W):
        self.W=W
        self.env.controller.record_window_size(flow=self.flow, window_size=self.W)
        
        if DEBUG:
                print "        W="+str(self.W) 
                
        self.recorder.write("{0},{1},{2},{3}\r\n".format(str(self.env.now),str(self.W),str(int(self.slow_start_flag)),str(self.slow_start_treshold)))
        
    pass

    def reset_timer(self):
        self.time_out_event=PacketTimeOut(env=self.env, delay=self.time_out, actor=self, expected_time=self.env.now+self.time_out)
