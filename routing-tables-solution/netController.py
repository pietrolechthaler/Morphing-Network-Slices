#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import comnetsemu.tool as tool
from comnetsemu.net import Containernet
from mininet.net import Mininet
from comnetsemu.node import DockerHost
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import RemoteController, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

from topoController import *

def addHost(net,name,index):
    return net.addHost(
        name,
        ip="10.0.0." + str(index) + "/24",
    )

def addRouter(net,name,index):
    return net.addHost(
        name,
        ip="10.0." + str(index) + ".254/24"
    )

def addHostR(net,name,index):
    return net.addHost(
        name,
        ip="10.0." + str(index) + ".1/24",
        mac="00:00:00:00:00:0"+str(index),
        defaultRoute='via 10.0.'+str(index)+'.254'
    )


class NetController():
    def __init__(self, count):
        info("[NC] init\n")
        
        self.count = count
        #info("A\n")
        self.net = Mininet(link=TCLink, switch=OVSKernelSwitch, topo=EmptyTopo(), build=False)
        #info("B\n")
        c0 = RemoteController("c0", ip="127.0.0.1", port=6633)
        #info("C\n")
        self.net.addController(c0)
        #info("D\n")

        self.topo = TopoController()
        self.slic = SlicController()
        
        for i in range(0, count):
            host = addHostR(self.net, "h" + str(i+1), i+1)
            id = "r" + str(i+1)
            router = addRouter(self.net, id,i+1)
        
    
    def start(self):
        info("[NC] start\n")

        # Physically morping the network
        # - string
        # - start
        # - ring
        self.topo.morph(self.net, "string", self.count)

        # Building the network
        self.net.build()

        # Starting the network
        self.net.start()

        # Morping the virtual
        self.slic.morph(self.net, "string", "ring", self.count)
        #self.slic.collapseRouter(self.net, 2)
        #self.slic.morph(self.net, "ring", "ring", self.count)
        #self.test()
        #info("\n\n\n")
        #self.slic.morph2(self.net, "string", "string", self.count)

    def stop(self):
        info("[NC] stop\n")
        self.net.stop()
    
    def print(self):
        info("[NC] \tControllers: " + str(self.net.controllers) + "\n")
        info("[NC] \tHosts: " + str(self.net.hosts) + "\n")
        info("[NC] \tLinks: " + str(self.net.links) + "\n")
        info("[NC] \tSwitches: " + str(self.net.switches) + "\n")

    def test(self):
        self.net.pingAll()

    def CLI(self):
        CLI(self.net)