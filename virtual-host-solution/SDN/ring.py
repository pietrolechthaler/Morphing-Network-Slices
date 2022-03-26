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
            3: {"00:00:00:00:00:03": 1},
            4: {"00:00:00:00:00:04": 1},
        }        
        self.monitor_thread = hub.spawn(self.change)

    def change(self):
        print("Controller starting up\n")
        time.sleep(10)

        check_output(shlex.split('sudo ovs-ofctl mod-port s2 3 down'),universal_newlines=True)  #down porte s2 e porte altri switch collegati a s2
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 2 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s2 1 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s3 2 down'),universal_newlines=True)  
        check_output(shlex.split('sudo ovs-ofctl mod-port s1 2 down'),universal_newlines=True)  

        
        time.sleep(5)
        switches = ['s1','s2','s3','s4']    #cancello eventuali match sbagliati dovuti al collegamento iniziale con gli hub
        for switch in switches:
            check_output(shlex.split('sudo ovs-ofctl del-flows {} udp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} tcp'.format(switch)),universal_newlines=True)
            check_output(shlex.split('sudo ovs-ofctl del-flows {} icmp'.format(switch)),universal_newlines=True)
        print("TOPOLOGIA AD ANELLO S1-S2-S3-S4")
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 1},
            3: {"00:00:00:00:00:03": 1},
            4: {"00:00:00:00:00:04": 1},
        }
        print("------------")
        print(check_output(shlex.split('sudo ovs-ofctl dump-flows s1'),universal_newlines=True))    #dump table pre cancellazione
        print(check_output(shlex.split('sudo ovs-ofctl dump-flows s2'),universal_newlines=True))    #dump table pre cancellazione
        print(check_output(shlex.split('sudo ovs-ofctl dump-flows s3'),universal_newlines=True))    #dump table pre cancellazione
        print(check_output(shlex.split('sudo ovs-ofctl dump-flows s4'),universal_newlines=True))    #dump table pre cancellazione        
        print("-------------")


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
        #self.mac_to_port[dpid][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if dst in self.mac_to_port[dpid]:
            self.logger.info("MAC: sono dentro %s %s %s %s", dpid, src, dst, in_port)
            out_port = self.mac_to_port[dpid][dst]
            results=1
        else:
            if(dpid==1):
                #self.logger.info("1. sono dentro %s %s %s %s", dpid, src, dst, in_port)
                out_port=4
            elif(dpid==3):
                #self.logger.info("3. sono dentro %s %s %s %s", dpid, src, dst, in_port)
                out_port=3
            elif(dpid==4):
                #self.logger.info("4. sono dentro %s %s %s %s", dpid, src, dst, in_port)
                out_port=3
            else:
                #self.logger.info("nessuna delle opzioni")
                #self.logger.info("NN. sono dentro %s %s %s %s", dpid, src, dst, in_port)
                out_port = ofproto.OFPP_FLOOD
                

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