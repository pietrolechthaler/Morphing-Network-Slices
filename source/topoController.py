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
                net.addLink(net.switches[i], net.switches[i+1])

    def morph_routes(self, net, router, routeOld, routeNew):
        pass




######### VERSIONE ROUTERS

class TopoControllerRouters():
    def __init__(self):
        info("[TC] instance init\n")
    
    def morph(self, net, topology,index):
        info("[TC] morphing to " + str(topology) + "\n")

        links = net.links
        for i in range(len(net.links)-1, -1, -1):
            net.delLink(net.links[i])

        if topology == "star":  ##TODO
            for i in range(0, len(net.hosts)):
                net.addLink(net.hosts[i], net.switches[0])
 
        elif topology == "string":
            for i in range(0, index):
                id="r"+str(i+1)
                router=net.get(id)
                router.cmd('sysctl net.ipv4.ip_forward=1')
                net.addLink(net.get("h"+str(i+1)), router,
                intfName2=id+"-eth0",
                params2={'ip':'10.0.'+str(index)+'.254/24'}
                )
            for i in range(1, index):
                net.addLink(net.get("r"+str(i)), net.get("r"+str(i+1)))

            #net.build()
            #self.define_interfaces(net,index)

        elif topology == "ring":  ##TODO
            for i in range(0, len(net.hosts)):
                net.addLink(net.hosts[i], net.switches[i])
                net.addLink(net.switches[i], net.switches[i+1])

    def define_interfaces(self, net,index):
        for i in range(0, index):
            id="r"+str(i+1)
            router=net.get(id)
            router.cmd("ifconfig "+id+"-eth0 0")
            router.cmd("ifconfig "+id+"-eth0 hw ether 00:00:00:00:0"+str(index+1)+":01")
            router.cmd("ip addr add 10.0."+str(i+1)+".254/24 brd + dev "+id+"-eth0")



    def morph_routes(self, net, router, routeOld, routeNew):
        pass
        
        
        