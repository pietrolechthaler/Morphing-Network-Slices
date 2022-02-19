#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

class EmptyTopo(Topo):
    def build(self):
        pass
        
class TopoController():
    def __init__(self):
        info("[TC] instance init\n")
    
    def morph(self, net, topology):
        info("[TC] morphing to " + str(topology) + "\n")

        links = net.links
        for i in range(len(net.links)-1, -1, -1):
            net.delLink(net.links[i])

        if topology == "star":
            for i in range(0, len(net.hosts)):
                net.addLink(net.hosts[i], net.switches[0])
            
        elif topology == "string":
            for i in range(0, len(net.hosts)):
                net.addLink(net.hosts[i], net.switches[i])
            for i in range(0, len(net.hosts)-1):
                net.addLink(net.switches[i], net.switches[i+1])

        elif topology == "ring":
            for i in range(0, len(net.hosts)):
                net.addLink(net.hosts[i], net.switches[i])
                net.addLink(net.switches[i], net.switches[(i+1)%len(net.hosts)])

    def morph_routes(self, net, router, routeOld, routeNew):
        pass