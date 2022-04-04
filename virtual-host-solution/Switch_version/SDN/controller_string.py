from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp
from ryu.lib.packet import tcp
from ryu.lib.packet import icmp
from mininet.log import info, setLogLevel
import shlex,time
from subprocess import check_output
from ryu.lib import hub


class ExampleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ExampleSwitch13, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}
        self.mode = "STRING"
        self.monitor_thread = hub.spawn(self.change)

    def change(self):
        print("Controller starting up\n")
        time.sleep(10)

        check_output(shlex.split('sudo ovs-ofctl mod-port s1 3 down'),universal_newlines=True)  #down porte estreme collegate agli hub
        check_output(shlex.split('sudo ovs-ofctl mod-port s4 3 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s1 4 down'),universal_newlines=True)
        check_output(shlex.split('sudo ovs-ofctl mod-port s3 4 down'),universal_newlines=True)
        
        time.sleep(5)
        switches = ['s1','s2','s3','s4']    #cancello eventuali match sbagliati dovuti al collegamento iniziale con gli hub
        for switch in switches:
            check_output(shlex.split('sudo ovs-ofctl del-flows {} udp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} tcp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} icmp'.format(switch)),universal_newlines=True)
        self.mac_to_port = {}
        print("TOPOLOGIA A STRINGA S1-S2-S3-S4")
        print("fra 80 sec la topologia cambierà")
        print("------------")
        print(check_output(shlex.split('sudo ovs-ofctl dump-flows s1'),universal_newlines=True))    #dump table pre cancellazione
        print("-------------")

        time.sleep(20)
        print("inizio a mutare la topologia in stringa")
        check_output(shlex.split('sudo ovs-ofctl mod-port s1 3 up'),universal_newlines=True)    #collegamento hub1
        check_output(shlex.split('sudo ovs-ofctl mod-port s4 3 up'),universal_newlines=True)
        check_output(shlex.split('sudo ovs-ofctl mod-port s1 4 up'),universal_newlines=True)    #collegamento hub2
        check_output(shlex.split('sudo ovs-ofctl mod-port s3 4 up'),universal_newlines=True)
        check_output(shlex.split('sudo ovs-ofctl mod-port s1 2 down'),universal_newlines=True)  #collegamento s2
        check_output(shlex.split('sudo ovs-ofctl mod-port s3 2 down'),universal_newlines=True)
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 1 down'),universal_newlines=True) #stacco i collegamenti di s2 just in case
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 2 down'),universal_newlines=True)
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 3 down'),universal_newlines=True)


        
        time.sleep(5)

        switches = ['s1','s2','s3','s4']    #cancello eventuali match sbagliati dovuti al collegamento iniziale con gli hub
        for switch in switches:
            check_output(shlex.split('sudo ovs-ofctl del-flows {} udp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} tcp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} icmp'.format(switch)),universal_newlines=True)
        
        print("------------")
        print(check_output(shlex.split('sudo ovs-ofctl dump-flows s1'),universal_newlines=True))    #dump table post cancellazione
        print("-------------")
        
        self.mode = "RING"
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 1},
            2: {"00:00:00:00:00:02": 1},
            3: {"00:00:00:00:00:03": 1},
            4: {"00:00:00:00:00:04": 1},
        }
        print("TOPOLOGIA A ANELLO S1-S3-S4")

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)



    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        #self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        results=0
        # learn a mac address to avoid FLOOD next time.
        

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if self.mode == "STRING":
            self.mac_to_port[dpid][src] = in_port
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = ofproto.OFPP_FLOOD
        elif self.mode == "RING":
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                if(dpid==1):
                    out_port=4
                elif(dpid==3):
                    out_port=3
                elif(dpid==4):
                    out_port=3
                elif(dpid==2):
                    out_port=1
                else:
                    #self.logger.info("nessuna delle opzioni")
                    out_port = ofproto.OFPP_FLOOD

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if (out_port != ofproto.OFPP_FLOOD):
            #if ((self.mode == "RING" and results==1) or self.mode == "STRING"):
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)

#SWITCH1 
#  cookie=0x0, duration=39.476s, table=0, n_packets=18, n_bytes=1764, priority=1,in_port="s1-eth1",dl_dst=00:00:00:00:00:03 actions=output:"s1-eth2"
#  cookie=0x0, duration=37.106s, table=0, n_packets=1, n_bytes=98, priority=1,in_port="s1-eth1",dl_dst=00:00:00:00:00:02 actions=output:"s1-eth2"
#  cookie=0x0, duration=34.015s, table=0, n_packets=0, n_bytes=0, priority=1,in_port="s1-eth1",dl_dst=00:00:00:00:00:04 actions=output:"s1-eth2"
#  cookie=0x0, duration=16.867s, table=0, n_packets=2, n_bytes=140, priority=1,in_port="s1-eth4",dl_dst=33:33:00:00:00:02 actions=output:"s1-eth4"
#  cookie=0x0, duration=16.867s, table=0, n_packets=0, n_bytes=0, priority=1,in_port="s1-eth4",dl_dst=33:33:00:00:00:16 actions=output:"s1-eth4"
#  cookie=0x0, duration=16.857s, table=0, n_packets=1197390, n_bytes=83817300, priority=1,in_port="s1-eth3",dl_dst=33:33:00:00:00:02 actions=output:"s1-eth4"
#  cookie=0x0, duration=16.857s, table=0, n_packets=194565, n_bytes=16732590, priority=1,in_port="s1-eth3",dl_dst=33:33:ff:37:1d:b0 actions=output:"s1-eth4"
#  cookie=0x0, duration=16.829s, table=0, n_packets=1883645, n_bytes=177007030, priority=1,in_port="s1-eth3",dl_dst=33:33:00:00:00:16 actions=output:"s1-eth4"
#  cookie=0x0, duration=16.829s, table=0, n_packets=194486, n_bytes=16725796, priority=1,in_port="s1-eth3",dl_dst=33:33:ff:f7:13:22 actions=output:"s1-eth4"
#  cookie=0x0, duration=54.401s, table=0, n_packets=14204, n_bytes=1234696, priority=0 actions=CONTROLLER:65535