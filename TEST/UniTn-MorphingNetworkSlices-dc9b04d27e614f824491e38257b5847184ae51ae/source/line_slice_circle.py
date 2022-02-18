from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller.controller import Datapath
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp
from ryu.lib.packet import tcp
from ryu.lib.packet import icmp
import json


class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)



        # outport = self.mac_to_port[dpid][mac_address]
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 1,
                "00:00:00:00:00:02": 2,
                "00:00:00:00:00:03": 2,
                "00:00:00:00:00:04": 2
            },
            2: {"00:00:00:00:00:01": 3,
                "00:00:00:00:00:02": 2,
                "00:00:00:00:00:03": 3,
                "00:00:00:00:00:04": 3
            },
            3: {"00:00:00:00:00:01": 3,
                "00:00:00:00:00:02": 3,
                "00:00:00:00:00:03": 2,
                "00:00:00:00:00:04": 3
            },
            4: {"00:00:00:00:00:04": 2},
        }




    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
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

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        dst = eth.dst
        src = eth.src

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        
        dpid = datapath.id

        '''if(dpid==1):
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)
            else:
                out_port = 2
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                #self.add_flow(datapath, 1, match, actions)
                #self.mac_to_port[dpid][src] = in_port
                self._send_package(msg, datapath, in_port, actions) 
        elif(dpid==4):
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)
            else:
                out_port = 1
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                #self.add_flow(datapath, 1, match, actions)
                #self.mac_to_port[dpid][src] = in_port
                self._send_package(msg, datapath, in_port, actions)
        else:
            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)
            else:
                if(in_port==3):
                    out_port = 1
                    actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                    match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                    #self.add_flow(datapath, 1, match, actions)
                    self.mac_to_port[dpid][src] = in_port
                    self._send_package(msg, datapath, in_port, actions)
                else:
                    out_port = 3
                    actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                    match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                    #self.add_flow(datapath, 1, match, actions)
                    self.mac_to_port[dpid][src] = in_port
                    self._send_package(msg, datapath, in_port, actions)
        '''    

        '''
from ryu.ofproto import ether
from ryu.lib.packet import ethernet, arp, packet

e = ethernet.ethernet(dst='ff:ff:ff:ff:ff:ff',
                      src='08:60:6e:7f:74:e7',
                      ethertype=ether.ETH_TYPE_ARP)
a = arp.arp(hwtype=1, proto=0x0800, hlen=6, plen=4, opcode=2,
            src_mac='08:60:6e:7f:74:e7', src_ip='192.0.2.1',
            dst_mac='00:00:00:00:00:00', dst_ip='192.0.2.2')
p = packet.Packet()
p.add_protocol(e)
p.add_protocol(a)
p.serialize()
print repr(p.data)  # the on-wire packet
        '''

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
            #self.logger.info('utilizzato invio diretto')
        else:
            if dpid == 4:
                in_port=3
                if(dst=="00:00:00:00:00:01"):
                    out_port = 1
                else:
                    out_port = 2
                datapath.id = 1
                msg.buffer_id = 1
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                #match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
                #self.mac_to_port[dpid][src] = in_port
                self.logger.info("magia\n")
                self._send_package(msg, Datapath(3, "00:00:00:00:00:01"), in_port, actions)
            else:
                out_port = ofproto.OFPP_FLOOD
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                #match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
                #self.mac_to_port[dpid][src] = in_port
                #self.logger.info("FLOOD from "+str(dpid)+"\n")
                self._send_package(msg, datapath, in_port, actions)
        




        #  cookie=0x0, duration=233.092s, table=0, n_packets=11, n_bytes=798, priority=1,dl_dst=00:00:00:00:00:01 actions=output:"s2-eth3"
        #  cookie=0x0, duration=233.068s, table=0, n_packets=10, n_bytes=700, priority=1,dl_dst=00:00:00:00:00:02 actions=output:"s2-eth1"
        #  cookie=0x0, duration=232.969s, table=0, n_packets=5, n_bytes=378, priority=1,dl_dst=00:00:00:00:00:03 actions=output:"s2-eth3"
        #  cookie=0x0, duration=232.877s, table=0, n_packets=5, n_bytes=378, priority=1,dl_dst=00:00:00:00:00:04 actions=output:"s2-eth3"
        #  cookie=0x0, duration=242.898s, table=0, n_packets=46, n_bytes=3128, priority=0 actions=CONTROLLER:65535

        #  2 -- 2,3--2,3--2
        #  1     1    1    1

        #  se ad anello invece:

        #  3,2--1,3--1,3--1,3
        #  1     2    2    2