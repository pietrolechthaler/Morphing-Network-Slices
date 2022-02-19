#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

#ROBE, brought to you by Matteino Gattino
''' if(index==4):            #set default gateaway nei router
        reteAnello="41"
    else:
        reteAnello=str(index)+str(index+1)
    defaultRoute='via 10.0.'+(reteAnello)+'.2'
'''

from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

class SlicControllerRouter():
    def __init__(self):
        pass
    
    def morph(self, net, physicalTopo, virtualTopo, count):
        if physicalTopo == "string" and virtualTopo == "string":
            for i in range(1, count+1):
                name = "r" + str(i)
                net[name].cmd("device clear ip route")

            for i in range(1, count+1):
                router = net.get("r" + str(i))
                for j in range(1, i):
                    remote = "10.0." + str(j) + ".0/24"
                    nexthop = "10.0." + str(i-1) + str(i) + ".1"
                    intf = "r" + str(i) + "-eth2"
                    router.cmd("ip route add " + remote + " via " + nexthop + " dev " + intf)
                    #######
                    remote = "10.0." + str(j)+str(j+1) + ".0/24"
                    router.cmd("ip route add " + remote + " via " + nexthop + " dev " + intf)
                for j in range(i+1, count+1):
                    remote = "10.0." + str(j) + ".0/24"
                    nexthop = "10.0." + str(i) + str(i+1) + ".2"
                    intf = "r" + str(i) + "-eth1"
                    router.cmd("ip route add " + remote + " via " + nexthop + " dev " + intf)
                    #######
                    remote = "10.0." + str(j-1)+str(j) + ".0/24"
                    router.cmd("ip route add " + remote + " via " + nexthop + " dev " + intf)



        elif physicalTopo == "string" and virtualTopo == "ring":
            #morph, eventuale collapse di un router
            pass
        elif physicalTopo == "ring" and virtualTopo == "ring":
            #impostare route "verso destra"
            pass
        elif physicalTopo == "ring" and virtualTopo == "string":
            #morphing di qualche tipo
            pass
            
        

