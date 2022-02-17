#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

from slicController import *

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

        if topology == "star": 
            id="r1"
            router=net.get(id)
            router.cmd('sysctl net.ipv4.ip_forward=1')
            for i in range(0, index):
                net.addLink(net.get("h"+str(i+1)), router,
                    intfName2=id+"-eth"+str(i),
                    params2={'ip':'10.0.'+str(i+1)+'.254/24'}
                )
                
 
        elif topology == "string":
            for i in range(0, index):
                id="r"+str(i+1)
                router=net.get(id)
                router.cmd('sysctl net.ipv4.ip_forward=1')
                net.addLink(net.get("h"+str(i+1)), router,
                    intfName2=id+"-eth0",
                    params2={'ip':'10.0.'+str(i)+'.254/24'}
                )
            for i in range(0, index-1):
                idrete = str(i+1)+str(i+2)
                id1="r"+str(i+1)
                id2="r"+str(i+2)
                net.addLink(net.get(id1), net.get(id2),
                    intfName1=id1+"-eth1",
                    params1={'ip':'10.0.'+idrete+'.1/24'},
                    intfName2=id2+"-eth2",
                    params2={'ip':'10.0.'+idrete+'.2/24'}
                )

        elif topology == "ring":  
            for i in range(0, index):
                id="r"+str(i+1)
                router=net.get(id)
                router.cmd('sysctl net.ipv4.ip_forward=1')
                net.addLink(net.get("h"+str(i+1)), router,
                    intfName2=id+"-eth0",
                    params2={'ip':'10.0.'+str(i)+'.254/24'}
                )
            for i in range(0, index-1):
                idrete = str(i+1)+str(i+2)
                id1="r"+str(i+1)
                id2="r"+str(i+2)
                net.addLink(net.get(id1), net.get(id2),
                    intfName1=id1+"-eth1",
                    params1={'ip':'10.0.'+idrete+'.1/24'},
                    intfName2=id2+"-eth2",
                    params2={'ip':'10.0.'+idrete+'.2/24'}
                )

            idrete = str(index)+str(1)
            id1="r"+str(index)
            id2="r"+str(1)
            net.addLink(net.get(id1), net.get(id2),
                intfName1=id1+"-eth1",
                params1={'ip':'10.0.'+idrete+'.1/24'},
                intfName2=id2+"-eth2",
                params2={'ip':'10.0.'+idrete+'.2/24'}
            )
        
        
        