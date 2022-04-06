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
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 1},
            2: {"00:00:00:00:00:02": 1},
            3: {"00:00:00:00:00:03": 1},
            4: {"00:00:00:00:00:04": 1},
        }

        print("Controller starting up\n")
        time.sleep(10)
        
        #we shut down the ports of s2 and also the links that connect s1 and s3 to it
        #therefore "cutting off" S2 from the logical view of the network.

        check_output(shlex.split('sudo ovs-ofctl mod-port s2 3 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 2 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 1 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s3 2 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s1 2 down'),universal_newlines=True)  
        
        time.sleep(5)
        
        #we clear eventual flows learned in the meantime and also mac to port pairings, then we proceed with the standard ring controller procedure
        switches = ['s1','s2','s3','s4']
        for switch in switches:
            check_output(shlex.split('sudo ovs-ofctl del-flows {} udp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} tcp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} icmp'.format(switch)),universal_newlines=True)
        
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 1},
            2: {"00:00:00:00:00:02": 1},
            3: {"00:00:00:00:00:03": 1},
            4: {"00:00:00:00:00:04": 1},
        }

        print("STAR TOPOLOGY S1-S2-S3-S4")


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

        #if destination mac address is in mac address table --> results = 1
        results=0
    
        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            results=1
        else:
            if(dpid==1):
                out_port=4 #to s6
            elif(dpid==2):
                out_port=1 #just to avoid random things from happening
            elif(dpid==3):
                out_port=3 #to s4
            elif(dpid==4):
                 out_port=3 #to s5
            elif(dpid==5):
                 out_port=1 #to s1
            elif(dpid==6):
                 out_port=2 #to s3
            else:
                return

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if (out_port != ofproto.OFPP_FLOOD and results==1):
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.logger.info("aggiunta flow %s %s", in_port, dst)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)