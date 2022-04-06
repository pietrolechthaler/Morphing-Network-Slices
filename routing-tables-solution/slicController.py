#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

def addRoute(router, remote, nexthop, intf):
    router.cmd("ip route add " + remote + " via " + nexthop + " dev " + intf)

class SlicController():
    def __init__(self):
        info("[SC] init\n")
        pass
    
    def morph(self, net, physicalTopo, virtualTopo, count):
        info("[SC] morph\n")
        # Rimozione routing tables pre-esistenti
        for i in range(1, count+1):
            name = "r" + str(i)
            routes = net[name].cmd("ip route")
            lines = routes.split("\n")
            for l in lines:
                if l.find("via") > 0:
                    net[name].cmd("ip route del " + l)
        
        # Configurazione routing tables per morph da string OR ring TO string
        if (physicalTopo == "string" or physicalTopo == "ring") and virtualTopo == "string":
            for i in range(1, count+1):
                router = net.get("r" + str(i))
                addRoute(router, "10.0."+str(i)+".1/32", "10.0."+str(i)+".254", "r"+str(i)+"-eth0")
                for j in range(1, i):
                    remote = "10.0." + str(j) + ".0/24"
                    nexthop = "10.0." + str(i-1) + str(i) + ".1"
                    intf = "r" + str(i) + "-eth2"
                    addRoute(router, remote, nexthop, intf)
                    remote = "10.0." + str(j)+str(j+1) + ".0/24"
                    addRoute(router, remote, nexthop, intf)
                for j in range(i+1, count+1):
                    remote = "10.0." + str(j) + ".0/24"
                    nexthop = "10.0." + str(i) + str(i+1) + ".2"
                    intf = "r" + str(i) + "-eth1"
                    addRoute(router, remote, nexthop, intf)
                    remote = "10.0." + str(j-1)+str(j) + ".0/24"
                    addRoute(router, remote, nexthop, intf)

        # Configurazione routing tables per morph da string TO ring
        elif physicalTopo == "string" and virtualTopo == "ring":
            #morph, eventuale collapse di un router
            pass

        # Configurazione routing tables per morph da ring TO ring
        elif physicalTopo == "ring" and virtualTopo == "ring":
            for i in range(1, count+1):
                router = net.get("r" + str(i))
                addRoute(router, "10.0."+str(i)+".1/32", "10.0."+str(i)+".254", "r"+str(i)+"-eth0")
                remote = "10.0.0.0/16"
                nexthop = "10.0." + str(i) + str((i) % count + 1) + ".2"
                intf = "r" + str(i) + "-eth1"
                addRoute(router, remote, nexthop, intf)
    
    def collapseRouter(self, net, index):
        name = "r" + str(index)
        net[name].cmd("ip route del 10.0." + str(index) + ".0/24")
        net[name].cmd("ip route del 10.0." + str(index) + ".1")
