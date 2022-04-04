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
        #print("------------")
        # print(check_output(shlex.split('sudo ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:01,actions=output:1'),universal_newlines=True))    #dump table pre cancellazione
        # print(check_output(shlex.split('sudo ovs-ofctl dump-flows s2'),universal_newlines=True))    #dump table pre cancellazione
        # print(check_output(shlex.split('sudo ovs-ofctl dump-flows s3'),universal_newlines=True))    #dump table pre cancellazione
        # print(check_output(shlex.split('sudo ovs-ofctl dump-flows s4'),universal_newlines=True))    #dump table pre cancellazione
        # print("-------------")
       
       # self.monitor_thread = hub.spawn(self.change)

    #def change(self):
       
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
        self.mac_to_port[dpid][src] = in_port
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
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